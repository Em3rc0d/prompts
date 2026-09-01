import "./globals.css";

export const metadata={title:"Prompt Quarry — Structured AI Workflows for Developers",description:"Governed developer prompt workflows with explicit evidence, constraints, output contracts, and release boundaries."};

export default function RootLayout({children}){return <html lang="en"><body><header className="nav"><div className="wrap navInner"><a className="brand" href="/"><span className="mark"><span>PQ</span></span><span>Prompt <b>Quarry</b></span></a><nav><a href="/free/developer-starter-pack">Free Pack</a><a href="/developer-pack">Developer Pack</a><a href="/license">License</a></nav></div></header>{children}<footer><div className="wrap footer"><span>Prompt Quarry</span><span>not observed == unknown</span></div></footer></body></html>}
