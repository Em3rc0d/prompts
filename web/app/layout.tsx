import type { Metadata } from "next";
import Link from "next/link";
import { FunnelTracker } from "@/components/funnel-tracker";
import "./globals.css";

export const metadata: Metadata = {
  title: "Prompt Quarry — Structured Prompts for Developers",
  description: "A prompt engineering system for developers: governed workflows, explicit evidence boundaries, and versioned delivery.",
  applicationName: "Prompt Quarry",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>
    <FunnelTracker />
    <header className="nav"><div className="wrap navInner">
      <Link className="brand" href="/" aria-label="Prompt Quarry home"><span className="brandGlyph" aria-hidden="true"><i /><i /><i /></span><span className="brandWord">Prompt <b>Quarry</b></span><span className="brandVersion">/ 01</span></Link>
      <nav className="navLinks" aria-label="Primary"><Link href="/free/developer-starter-pack">Free Pack</Link><Link href="/developer-pack">Developer Pack</Link><Link href="/#method">Method</Link><span className="navDivider" aria-hidden="true" /><Link className="navCta" href="/free/developer-starter-pack">Get Free Pack <span>↗</span></Link></nav>
    </div></header>
    {children}
    <footer className="footer"><div className="wrap footerGrid"><div className="footerBrand"><span className="brandWord">Prompt <b>Quarry</b></span><p>A governed prompt factory for structured developer AI workflows.</p></div><div className="footerMeta"><span>FREE / v1.1.0 · DELIVERY VERIFIED</span><span>PAID / v1.1 · DRAFT · NOT FOR SALE</span><span>EVIDENCE / NOT OBSERVED == UNKNOWN</span></div><div className="footerLinks"><Link href="/free/developer-starter-pack">Free Pack</Link><Link href="/developer-pack">Developer Pack</Link><Link href="/license">License</Link></div></div></footer>
  </body></html>;
}
