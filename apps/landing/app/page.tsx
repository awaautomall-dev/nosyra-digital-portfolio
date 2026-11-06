import Image from "next/image";
import Link from "next/link";
import { ArrowRight, ArrowUpRight, Boxes, Workflow, UsersRound } from "lucide-react";

const workspaces = [
  {
    number: "01",
    title: "Nosyra CRM",
    category: "Customer relationships",
    description: "Keep every customer conversation, lead, and next step moving together.",
    href: "/crm",
    icon: UsersRound,
    tone: "navy",
  },
  {
    number: "02",
    title: "Nosyra Inventory",
    category: "Products and stock",
    description: "Stay ahead of stock, purchasing, suppliers, and warehouse activity.",
    href: "/inventory",
    icon: Boxes,
    tone: "teal",
  },
  {
    number: "03",
    title: "Nosyra ProjectFlow",
    category: "Projects and teams",
    description: "Bring projects, tasks, milestones, and people into one clear view.",
    href: "/projectflow",
    icon: Workflow,
    tone: "mist",
  },
];

export default function Home() {
  return (
    <main className="site-shell">
      <header className="topbar">
        <Link className="brand" href="/" aria-label="Nosyra Digital home">
          <Image src="/nosyra-logo.png" alt="Nosyra Digital" width={178} height={56} priority />
        </Link>
        <a className="company-link" href="https://www.nosyradigital.com.ng/" target="_blank" rel="noreferrer">
          <span>Visit Nosyra Digital</span>
          <ArrowUpRight size={16} aria-hidden="true" />
        </a>
      </header>

      <section className="hero" aria-labelledby="hero-title">
        <div className="hero-copy">
          <div className="eyebrow"><span className="eyebrow-dot" /> NOSYRA DIGITAL SOFTWARE SUITE</div>
          <h1 id="hero-title">Your next move,<br /><em>all in one place.</em></h1>
          <p className="hero-description">
            Choose a focused workspace for the work that keeps your business moving—from customer relationships to stock and projects.
          </p>
          <a className="hero-cta" href="#workspaces">
            Explore the workspaces <ArrowRight size={17} aria-hidden="true" />
          </a>
        </div>

        <div className="hero-art" aria-hidden="true">
          <div className="orbit orbit-one" />
          <div className="orbit orbit-two" />
          <div className="orbit orbit-three" />
          <div className="art-center">
            <Image src="/nosyra-logo.png" alt="" width={162} height={51} />
            <span>Business, in better view.</span>
          </div>
          <div className="orbit-node node-crm"><UsersRound size={19} /></div>
          <div className="orbit-node node-inventory"><Boxes size={19} /></div>
          <div className="orbit-node node-projectflow"><Workflow size={19} /></div>
        </div>
      </section>

      <section className="workspace-section" id="workspaces" aria-labelledby="workspace-title">
        <div className="section-heading">
          <div>
            <p className="section-kicker">YOUR WORKSPACES</p>
            <h2 id="workspace-title">Where would you like to start?</h2>
          </div>
          <span className="section-count">03 <span>/</span> 03</span>
        </div>

        <div className="workspace-grid">
          {workspaces.map(({ number, title, category, description, href, icon: Icon, tone }) => (
            <Link className={`workspace-card ${tone}`} href={href} key={href}>
              <div className="card-topline">
                <span className="card-icon"><Icon size={21} aria-hidden="true" /></span>
                <span className="card-number">{number}</span>
              </div>
              <p className="card-category">{category}</p>
              <h3>{title}</h3>
              <p className="card-description">{description}</p>
              <span className="card-link">Open workspace <ArrowRight size={16} aria-hidden="true" /></span>
            </Link>
          ))}
        </div>
      </section>

      <footer className="footer">
        <p>Built for clearer work and better next steps.</p>
        <a href="https://www.nosyradigital.com.ng/" target="_blank" rel="noreferrer">
          Websites that actually convert <ArrowUpRight size={14} aria-hidden="true" />
        </a>
        <span>© {new Date().getFullYear()} Nosyra Digital</span>
      </footer>
    </main>
  );
}
