import { FREE_ASSETS } from "./verlune-free-catalog";
import { PREMIUM_ASSETS } from "./verlune-premium-catalog";

export type LibraryTier = "free" | "premium";
export type LibraryDiscoveryType = "Prompt" | "Workflow" | "Builder" | "Toolkit";

export type LibraryDiscoveryAsset = {
  id: string;
  name: string;
  type: LibraryDiscoveryType;
  tier: LibraryTier;
  category: string;
  categoryLabel: string;
  summary: string | null;
  publicNameOnly?: boolean;
  href: string;
  cta: string;
};

export type LibraryCollection = {
  id: string;
  name: string;
  description: string;
  assetIds: readonly string[];
};

export const LIBRARY_COLLECTIONS: readonly LibraryCollection[] = [
  {
    id: "start-here",
    name: "Start here",
    description: "Eight complete Free entry points — one useful task in every public category.",
    assetIds: [
      "VF-P-DEV-001","VF-P-STUDY-001","VF-P-RES-001","VF-P-BIZ-001",
      "VF-P-WRITE-001","VF-P-CONTENT-001","VF-P-PLAN-001","VF-P-CAREER-001"
    ]
  },
  {
    id: "premium-essentials",
    name: "Premium essentials",
    description: "The original eight deeper Premium entry points plus the two Builders.",
    assetIds: [
      "VP-P-DEV-001","VP-P-STUDY-001","VP-P-RES-002","VP-P-BIZ-001",
      "VP-P-WRITE-001","VP-P-CONTENT-001","VP-P-PLAN-001","VP-P-CAREER-001",
      "VP-BUILDER-001","VP-BUILDER-002"
    ]
  },
  {
    id: "ship-software",
    name: "Ship software",
    description: "Understand, diagnose, specify, plan and review software work without collapsing evidence into assumptions.",
    assetIds: [
      "VF-P-DEV-001","VF-P-DEV-002","VF-WF-003",
      "VP-P-DEV-001","VP-P-DEV-002","VP-P-DEV-003","VP-P-DEV-004","VP-WF-001"
    ]
  },
  {
    id: "research-decide",
    name: "Research & decide",
    description: "Move from sources and uncertainty to a bounded comparison or decision input.",
    assetIds: [
      "VF-P-RES-001","VF-P-RES-002","VF-WF-001",
      "VP-P-RES-002","VP-P-RES-003","VP-P-RES-004","VP-P-RES-005","VP-WF-003","VP-WF-004"
    ]
  },
  {
    id: "learn-prepare",
    name: "Learn & prepare",
    description: "Build understanding, test recall, find gaps and prepare for exams or interviews.",
    assetIds: [
      "VF-P-STUDY-001","VF-P-STUDY-002","VF-WF-002","VF-P-CAREER-001",
      "VP-P-STUDY-001","VP-P-STUDY-002","VP-P-STUDY-003","VP-P-STUDY-004",
      "VP-WF-006","VP-P-CAREER-002"
    ]
  },
  {
    id: "operate-plan",
    name: "Operate & plan",
    description: "Turn work into processes and plans with dependencies, risks, decisions and recovery paths.",
    assetIds: [
      "VF-P-BIZ-001","VF-P-BIZ-002","VF-P-PLAN-001","VF-P-PLAN-002",
      "VP-P-BIZ-001","VP-P-BIZ-002","VP-P-BIZ-003","VP-P-BIZ-004",
      "VP-P-PLAN-001","VP-P-PLAN-002","VP-P-PLAN-003","VP-P-PLAN-004","VP-WF-004"
    ]
  },
  {
    id: "write-communicate",
    name: "Write & communicate",
    description: "Preserve factual meaning while adapting clarity, audience, format and decision usefulness.",
    assetIds: [
      "VF-P-WRITE-001","VF-P-WRITE-002",
      "VP-P-WRITE-001","VP-P-WRITE-002","VP-P-WRITE-003","VP-P-WRITE-004"
    ]
  },
  {
    id: "content-audience",
    name: "Content & audience",
    description: "Move from real audience signals and source material to distinct, bounded content work.",
    assetIds: [
      "VF-P-CONTENT-001","VF-P-CONTENT-002",
      "VP-P-CONTENT-001","VP-P-CONTENT-002","VP-P-CONTENT-003","VP-P-CONTENT-004","VP-WF-007"
    ]
  }
] as const;

function freeAssets(): LibraryDiscoveryAsset[] {
  return FREE_ASSETS.map((asset) => ({
    id: asset.id,
    name: asset.name,
    type: asset.type,
    tier: "free",
    category: asset.category,
    categoryLabel: asset.categoryLabel,
    summary: asset.summary,
    href: `/free/asset/${encodeURIComponent(asset.id)}`,
    cta: asset.type === "Workflow" ? "Open free workflow" : "Open free prompt"
  }));
}

function premiumAssets(destination: "public" | "private"): LibraryDiscoveryAsset[] {
  return PREMIUM_ASSETS.map((asset) => ({
    id: asset.id,
    name: asset.name,
    type: asset.type,
    tier: "premium",
    category: asset.category,
    categoryLabel: asset.categoryLabel,
    summary: destination === "private" ? asset.summary : null,
    publicNameOnly: destination === "public",
    href: destination === "private"
      ? `/app/asset/${encodeURIComponent(asset.id)}`
      : "/premium",
    cta: destination === "private" ? `Open ${asset.type.toLowerCase()}` : "Explore Premium"
  }));
}

export function getPublicLibraryAssets(): LibraryDiscoveryAsset[] {
  return [...freeAssets(), ...premiumAssets("public")];
}

export function getFreeLibraryDiscoveryAssets(): LibraryDiscoveryAsset[] {
  return freeAssets();
}

export function getPremiumLibraryDiscoveryAssets(): LibraryDiscoveryAsset[] {
  return premiumAssets("private");
}
