import type { Metadata } from "next";
import Link from "next/link";
import { FunnelTracker } from "@/components/funnel-tracker";
import { CODE_REVIEW, codeReviewPrice } from "@/lib/public-products";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "Verlune — Reusable AI workflows", template: "%s | Verlune" },
  description: "Reusable AI workflows with clear inputs, structured results, and practical verification. Explore Verlune Code Review or try three free developer workflows.",
  applicationName: "Verlune",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>
    <a className="skipLink" href="#main-content">Skip to content</a>
    <FunnelTracker />
    <header className="nav"><div className="wrap navInner">
      <Link className="brand" href="/" aria-label="Verlune home"><span className="brandMark" aria-hidden="true">V</span><span>VERLUNE</span></Link>
      <nav className="navLinks" aria-label="Primary"><Link href="/code-review">Code Review</Link><Link href="/free">Free</Link><Link href="/learn">Learn</Link><Link href="/license">License</Link></nav>
      <Link className="navCta" href="/code-review">Explore Code Review <span aria-hidden="true">↗</span></Link>
    </div></header>
    <div id="main-content" tabIndex={-1}>{children}</div>
    <footer className="footer"><div className="wrap footerGrid">
      <div><Link className="brand" href="/">VERLUNE</Link><p>Clear inputs. Structured results.<br />Work worth verifying.</p></div>
      <div className="footerProduct"><strong>{CODE_REVIEW.name}</strong><span>{codeReviewPrice} {CODE_REVIEW.billingModel} · v{CODE_REVIEW.version}</span><span>A downloadable workflow for developers.</span></div>
      <nav className="footerLinks" aria-label="Footer"><Link href="/code-review">Code Review</Link><Link href="/free">Free workflows</Link><Link href="/learn">Learn</Link><Link href="/license">License</Link></nav>
    </div><div className="wrap footerBottom">AI assists the review. You decide what ships.</div></footer>
  </body></html>;
}
