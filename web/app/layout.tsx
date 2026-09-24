import type { Metadata } from "next";
import Link from "next/link";
import { FunnelTracker } from "@/components/funnel-tracker";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "Verlune — Structured AI work", template: "%s | Verlune" },
  description: "Reusable prompts, workflows and builders for structured AI work. Use Verlune assets in your own compatible AI assistant, verify the result, and reuse the process.",
  applicationName: "Verlune",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>
    <a className="skipLink" href="#main-content">Skip to content</a>
    <FunnelTracker />
    <header className="nav vNav"><div className="wrap navInner">
      <Link className="brand" href="/" aria-label="Verlune home"><span className="brandMark" aria-hidden="true">V</span><span>VERLUNE</span></Link>
      <nav className="navLinks" aria-label="Primary">
        <Link href="/library">Library</Link>
        <Link href="/free">Free</Link>
        <Link href="/premium">Premium</Link>
        <Link href="/learn">Learn</Link>
        <Link href="/code-review">Code Review</Link>
      </nav>
      <Link className="navCta vNavCta" href="/unlock">Unlock access <span aria-hidden="true">→</span></Link>
      <details className="mobileNav">
        <summary aria-label="Open navigation"><span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span></summary>
        <nav aria-label="Mobile">
          <Link href="/library">Library</Link>
          <Link href="/free">Free</Link>
          <Link href="/premium">Premium</Link>
          <Link href="/learn">Learn</Link>
          <Link href="/code-review">Code Review</Link>
          <Link href="/unlock">Unlock access</Link>
        </nav>
      </details>
    </div></header>
    <div id="main-content" tabIndex={-1}>{children}</div>
    <footer className="footer vFooter"><div className="wrap footerGrid">
      <div>
        <Link className="brand" href="/"><span className="brandMark" aria-hidden="true">V</span><span>VERLUNE</span></Link>
        <p>Clear inputs. Structured results.<br />Work worth verifying.</p>
      </div>
      <div className="footerProduct">
        <strong>Use ours. Build yours.</strong>
        <span>Reusable prompts, workflows, Builders and verification tools.</span>
        <span>AI execution happens in your compatible assistant.</span>
      </div>
      <nav className="footerLinks" aria-label="Footer">
        <Link href="/library">Library</Link>
        <Link href="/free">Free</Link>
        <Link href="/premium">Premium</Link>
        <Link href="/learn">Learn</Link>
        <Link href="/license">License</Link>
      </nav>
    </div><div className="wrap footerBottom">Verlune supplies the structure and methodology. You decide how the result is used.</div></footer>
  </body></html>;
}
