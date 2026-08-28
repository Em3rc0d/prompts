from __future__ import annotations
import argparse, hashlib, json, re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from mk0_harvester_router import apply_route, load_policy
from mk0_semantic_artifact_gate import classify_artifact
SOURCE_RECORDS=Path("mk0/normalized/harvester/source-records.jsonl"); CANDIDATE_SCHEMA=Path("mk0/harvester/CANDIDATE_RECORD.schema.json"); QUEUE_ROOT=Path("mk0/golden-dataset/candidate-queue"); REFERENCE_ROOT=Path("mk0/reference-corpus")
DOMAIN_RULES={"software":["code","software","api","github","debug","test","developer","programming","cli","python","javascript","typescript"],"research":["research","paper","evidence","study","literature","benchmark","empirical"],"content":["content","write","writing","copy","blog","article","social","marketing"],"data":["data","sql","database","analytics","dataset","spreadsheet"],"agentic":["agent","skill","tool","workflow","capability","instructions"]}
INTENT_RULES={"review":["review","audit","critique","check","inspect"],"generate":["generate","create","write","draft","build","implement"],"research":["research","investigate","evidence","study","compare","benchmark"],"transform":["rewrite","refactor","convert","improve","optimize","edit"],"operate":["run","execute","deploy","publish","workflow","automate"]}
TECHNIQUE_RULES={"role-framing":["you are","act as","role:"],"explicit-constraints":["must","must not","never","required","constraints"],"structured-output":["json","yaml","markdown","format","schema","output"],"step-decomposition":["steps","step-by-step","workflow","procedure","process"],"examples":["example","examples","few-shot"],"verification":["verify","validate","test","check","evidence","citation"],"tool-use":["tool","command","api","browser","search"],"context-boundary":["context","source","provided","do not assume","unknown"]}
ARCH_RULES={"role-task-constraints-output":["you are","must","output"],"procedure-driven":["steps","workflow","procedure"],"evidence-grounded":["evidence","citation","source","verify"],"tool-augmented":["tool","api","browser","command"],"example-conditioned":["example","few-shot"]}
def utc_now(): return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def load_jsonl(path): return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
def read_body(r):
 ref=r.get("provenance",{}).get("raw_record_ref"); p=Path(ref) if ref else None; return p.read_text(encoding="utf-8",errors="replace") if p and p.exists() else ""
def normalized_text(t): return re.sub(r"\s+"," ",re.sub(r"https?://\S+"," URL ",t.casefold())).strip()
def fingerprint(t): return "sha256:"+hashlib.sha256(normalized_text(t).encode()).hexdigest()
def score_rules(text,rules):
 f=text.casefold(); s={k:sum(1 for x in v if x in f) for k,v in rules.items()}; o=sorted(s.items(),key=lambda x:(-x[1],x[0])); return o[0][0],o[0][1],o[1][1]
def detected(text,rules):
 f=text.casefold(); return sorted(k for k,v in rules.items() if any(x in f for x in v))
def conf(best,second,base=.79,ceiling=.98): return .72 if best<=0 else min(ceiling,base+min(best,6)*.025+max(best-second,0)*.015)
def characterize(r,body,seen,policy):
 text=f"{r.get('title') or ''}\n{body}"; semantic=classify_artifact(r.get('title') or '',body,r["source_type"]); domain,db,ds=score_rules(text,DOMAIN_RULES); intent,ib,is_=score_rules(text,INTENT_RULES); techniques=detected(text,TECHNIQUE_RULES); architecture=detected(text,ARCH_RULES); fp=fingerprint(body or r["canonical_url"]); duplicate=seen.get(fp)
 cc=min(conf(db,ds),conf(ib,is_)); tc=min(.98,.84+min(len(techniques),7)*.02) if techniques else .78; ac=min(.98,.84+min(len(architecture),5)*.025) if architecture else .76; dc=.99 if body else .82
 length=len(body); structural=min(.98,.55+min(length,12000)/30000+min(len(techniques),6)*.035); novelty=.20 if duplicate else min(.95,.58+min(len(techniques),6)*.045+min(len(architecture),4)*.03); coverage=min(.95,.55+(.12 if domain!="agentic" else .08)+min(len(techniques),5)*.04); gv=round(structural*.4+novelty*.3+coverage*.3,4)
 flags=[]
 if r.get("license_status")=="UNKNOWN": flags.append("license_unknown_for_redistribution")
 if r.get("body_observation_status")!="OBSERVED": flags.append("content_observation_ambiguity")
 if db==ds and db>0: flags.append("conflicting_classifiers")
 if novelty>=.90 and ac<.90: flags.append("high_novelty_ambiguous_mapping")
 cid="cand-"+hashlib.sha256((r["source_id"]+fp).encode()).hexdigest()[:20]
 c={"schema":"prompt-quarry-candidate-record-v1","candidate_id":cid,"source_id":r["source_id"],"candidate_fingerprint":fp,"artifact_type":r["source_type"] if r["source_type"] in {"prompt","skill","agent","instruction-markdown","capability","workflow"} else "other","semantic_gate":semantic,"stage":"SCORED","classification":{"domain":domain,"intent":intent,"family":f"{domain}_{intent}","language":r.get("language")},"techniques":techniques,"architecture":architecture,"confidence":{"classification":round(cc,4),"technique_extraction":round(tc,4),"architecture_mapping":round(ac,4),"deduplication":dc,"aggregate":0.0},"quality":{"structural_quality":round(structural,4),"novelty":round(novelty,4),"coverage_value":round(coverage,4),"golden_value":gv},"duplicate_of":duplicate,"critical_flags":sorted(set(flags)),"route":"HOLD","route_reasons":[],"eligibility":{"golden_research_eligibility":{"eligible":False,"reasons":["pending"]},"distribution_eligibility":{"eligible":False,"reasons":["pending"]}},"policy_version":policy["policy_version"],"source_record_ref":"mk0/normalized/harvester/source-records.jsonl","characterization_ref":"mk0/analysis/harvester/characterization-batch-001-receipt.json","created_at":utc_now()}
 out=apply_route(c,policy)
 if not duplicate: seen[fp]=cid
 return out
def validate(records):
 schema=json.loads(CANDIDATE_SCHEMA.read_text()); v=Draft202012Validator(schema,format_checker=FormatChecker()); errors=[f"record[{i}] {e.json_path}: {e.message}" for i,r in enumerate(records) for e in v.iter_errors(r)]
 if errors: raise ValueError("candidate validation failed:\n"+"\n".join(errors))
def persist(records,output,receipt,reference_output,policy):
 output.parent.mkdir(parents=True,exist_ok=True); output.write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in records),encoding="utf-8")
 refs=[r for r in records if r["semantic_gate"]["disposition"]=="REFERENCE_CORPUS"]; reference_output.parent.mkdir(parents=True,exist_ok=True); reference_output.write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in refs),encoding="utf-8")
 routes=Counter(r["route"] for r in records); semantics=Counter(r["semantic_gate"]["artifact_class"] for r in records); dispositions=Counter(r["semantic_gate"]["disposition"] for r in records); domains=Counter(r["classification"]["domain"] for r in records); fam=Counter(r["classification"]["family"] for r in records); tech=Counter(t for r in records for t in r["techniques"]); ag=[r["confidence"]["aggregate"] for r in records]; research=sum(r["eligibility"]["golden_research_eligibility"]["eligible"] for r in records); distribution=sum(r["eligibility"]["distribution_eligibility"]["eligible"] for r in records); bands={">=0.95":sum(x>=.95 for x in ag),"0.90-<0.95":sum(.90<=x<.95 for x in ag),"<0.90":sum(x<.90 for x in ag)}
 payload={"schema":"prompt-quarry-characterization-receipt-v1","batch_id":"mk0-characterization-001","policy_version":policy["policy_version"],"status":"PASS","created_at":utc_now(),"records":len(records),"routes":dict(routes),"semantic_artifact_classes":dict(semantics),"semantic_dispositions":dict(dispositions),"reference_corpus_records":len(refs),"confidence_bands":bands,"eligibility":{"golden_research_eligible":research,"distribution_eligible":distribution},"domains":dict(domains),"top_families":dict(fam.most_common(12)),"top_techniques":dict(tech.most_common(12)),"aggregate_confidence":{"min":min(ag),"max":max(ag),"mean":round(sum(ag)/len(ag),4)},"duplicates":sum(1 for r in records if r.get("duplicate_of")),"claim_boundary":"Semantic artifact identity is gated before Golden routing. REFERENCE_CORPUS is non-canonical reference material, not truth and not Golden evidence. UNKNOWN license remains UNKNOWN and blocks distribution. Human approval does not establish behavioral certification."}; receipt.parent.mkdir(parents=True,exist_ok=True); receipt.write_text(json.dumps(payload,indent=2)+"\n")
def main():
 p=argparse.ArgumentParser(); p.add_argument("--input",type=Path,default=SOURCE_RECORDS); p.add_argument("--output",type=Path,default=QUEUE_ROOT/"batch-001.jsonl"); p.add_argument("--reference-output",type=Path,default=REFERENCE_ROOT/"batch-001.jsonl"); p.add_argument("--receipt",type=Path,default=Path("mk0/analysis/harvester/characterization-batch-001-receipt.json")); a=p.parse_args(); policy=load_policy(); seen={}; records=[characterize(r,read_body(r),seen,policy) for r in load_jsonl(a.input)]; validate(records); persist(records,a.output,a.receipt,a.reference_output,policy); print(json.dumps({"records":len(records),"policy_version":policy["policy_version"],"output":str(a.output),"reference_output":str(a.reference_output),"receipt":str(a.receipt)},indent=2))
if __name__=="__main__": main()
