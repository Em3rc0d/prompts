import type { Metadata } from "next";
import Link from "next/link";
import { FunnelTracker } from "@/components/funnel-tracker";
import "./globals.css";

export const metadata: Metadata = {
  title: "Prompt Machine — Reusable AI Workflows for Real Tasks",
  description: "Discover reusable AI workflows by what you need to get done. Start free, inspect the evidence, and upgrade to curated workflow collections.",
  applicationName: "Prompt Machine",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>
    <FunnelTracker />
    <header className="nav"><div className="wrap navInner">
      <Link className="brand" href="/" aria-label="Prompt Machine home"><span className="brandGlyph" aria-hidden="true"><i /><i /><i /></span><span className="brandWord">Prompt <b>Machine</b></span><span className="brandVersion">/ 01</span></Link>
      <nav className="navLinks" aria-label="Primary"><Link href="/#workflows">Workflows</Link><Link href="/collections">Collections</Link><Link href="/#how-it-works">How it works</Link><Link href="/#evidence">Evidence</Link><span className="navDivider" aria-hidden="true" /><Link className="navCta" href="/free/developer-starter-pack">Start Free <span>↗</span></Link></nav>
    </div></header>
    {children}
    <footer className="footer"><div className="wrap footerGrid"><div className="footerBrand"><span className="brandWord">Prompt <b>Machine</b></span><p>Reusable AI workflows organized around what you need to get done.</p></div><div className="footerMeta"><span>FREE LIBRARY / USEFUL STANDALONE WORKFLOWS</span><span>COLLECTIONS / PAID WHEN THE UPGRADE EARNS IT</span><span>FACTORY / PROMPT QUARRY · EVIDENCE BEFORE CLAIMS</span></div><div className="footerLinks"><Link href="/free/developer-starter-pack">Free Workflows</Link><Link href="/collections">Collections</Link><Link href="/developer-pack">Developer Collection</Link><Link href="/license">License</Link></div></div></footer>
  </body></html>;
}
