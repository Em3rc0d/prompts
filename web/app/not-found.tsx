import Link from "next/link";

export default function NotFound(){return <main><section className="pageHero"><div className="wrap"><div className="eyebrow">404 / VERLUNE</div><h1>This workflow path does not exist.</h1><p className="lead">Return to Verlune or start with the useful Free Library.</p><div className="actions"><Link className="btn btnPrimary" href="/">Back to Verlune</Link><Link className="btn btnSecondary" href="/free/developer-starter-pack">Use the Free Library</Link></div></div></section></main>}
