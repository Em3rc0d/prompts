import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Prompt Quarry — Structured Prompts for Developers",
  description: "Structured developer prompts with explicit context, constraints, output contracts, and evidence boundaries.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <header className="nav">
          <div className="wrap navInner">
            <Link className="brand" href="/">Prompt <span>Quarry</span></Link>
            <nav className="navLinks" aria-label="Primary">
              <Link href="/free/developer-starter-pack">Free Pack</Link>
              <Link href="/developer-pack">Developer Pack</Link>
              <Link href="/#method">Method</Link>
              <Link className="btn btnPrimary" href="/free/developer-starter-pack">Get Free Pack</Link>
            </nav>
          </div>
        </header>
        {children}
        <footer className="footer"><div className="wrap">Prompt Quarry · Use and adapt. Do not resell or redistribute.</div></footer>
      </body>
    </html>
  );
}
