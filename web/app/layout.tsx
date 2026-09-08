import type { Metadata } from "next";
import Link from "next/link";
import { FunnelTracker } from "@/components/funnel-tracker";
import "./globals.css";

export const metadata: Metadata = {
  title: "Verlune — Reusable AI Workflows You Can Inspect",
  description: "Verlune turns recurring work into reusable AI workflows with visible evidence, explicit boundaries, and practical verification.",
  applicationName: "Verlune",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>
    <FunnelTracker />
    <header className="nav"><div className="wrap navInner">
      <Link className="brand" href="/" aria-label="Verlune home"><span className="brandGlyph" aria-hidden="true"><i /><i /><i /></span><span className="brandWord"><b>VERLUNE</b></span><span className="brandVersion">/ 01</span></Link>
      <nav className="navLinks" aria-label="Primary"><Link href="/#workflows">Workflows</Link><Link href="/collections">Collections</Link><Link href="/learn">Learn</Link><Link href="/#how-it-works">How it works</Link><Link href="/#evidence">Evidence</Link><span className="navDivider" aria-hidden="true" /><Link className="navCta" href="/free/developer-starter-pack">Start Free <span>↗</span></Link></nav>
    </div></header>
    {children}
    <footer className="footer"><div className="wrap footerGrid"><div className="footerBrand"><span className="brandWord"><b>VERLUNE</b></span><p>Reusable AI workflows with visible evidence and explicit boundaries.</p></div><div className="footerMeta"><span>FREE LIBRARY / USEFUL STANDALONE WORKFLOWS</span><span>CODE REVIEW / USD 9 PRICE HYPOTHESIS · CHECKOUT OFF</span><span>FULL / USD 19 FUTURE HYPOTHESIS · CHECKOUT OFF</span><span>RULE / MARKETING CLAIM ≤ OBSERVED EVIDENCE</span></div><div className="footerLinks"><Link href="/free/developer-starter-pack">Free Workflows</Link><Link href="/starter-collection">Code Review $9</Link><Link href="/developer-pack">Full $19</Link><Link href="/collections">Collections</Link><Link href="/learn">Learn</Link><Link href="/license">License</Link></div></div></footer>
  </body></html>;
}
