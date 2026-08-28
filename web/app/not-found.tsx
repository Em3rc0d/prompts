import Link from "next/link";

export default function NotFound(){return <main><section className="pageHero"><div className="wrap"><div className="eyebrow">404</div><h1>This path is outside the quarry.</h1><p className="lead">Return to the commercial surface or start with the Free Developer Starter Pack.</p><div className="actions"><Link className="btn btnPrimary" href="/">Back to Prompt Quarry</Link><Link className="btn btnSecondary" href="/free/developer-starter-pack">Get Free Pack</Link></div></div></section></main>}
