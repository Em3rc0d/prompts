import Link from "next/link";
import "./globals.css";

export const metadata = {
  title: "Prompt Quarry — Structured Prompts for Developers",
  description: "Structured developer prompts with explicit context, constraints, output contracts, and evidence boundaries.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <header className="nav">
          <div className="wrap navInner">
            <Link className="brand" href="/"><span className="mark">PQ</span><span>Prompt <b>Quarry</b></span></Link>
            <nav>
              <Link href="/free/developer-starter-pack">Free Pack</Link>
              <Link href="/developer-pack">Developer Pack</Link>
              <Link href="/license">License</Link>
            </nav>
          </div>
        </header>
        {children}
        <footer><div className="wrap footer"><span>Prompt Quarry</span><span>not observed == unknown</span></div></footer>
      </body>
    </html>
  );
}
