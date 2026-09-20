import { useState } from 'react';
import { ArrowUpRight, Check, ChevronRight, CircleUserRound, KeyRound, Menu, ShieldCheck, X } from 'lucide-react';

const projects = [
  {
    id: 'aiops',
    name: 'DataSnare-AIOps',
    category: 'Operations platform',
    description: 'Monitor systems, investigate incidents, and orchestrate approved remediation.',
    path: '/aiops',
    license: 'Active',
    accent: 'mint',
  },
  {
    id: 'ailogscope',
    name: 'DataSnare-AILogScope',
    category: 'Log intelligence',
    description: 'Normalize event logs and application evidence into explainable findings.',
    path: '/ailogscope',
    license: 'Active',
    accent: 'amber',
  },
  {
    id: 'aiperf',
    name: 'DataSnare-AIPerf',
    category: 'Performance analysis',
    description: 'Review Performance Monitor captures and identify resource pressure.',
    path: '/aiperf',
    license: 'Active',
    accent: 'blue',
  },
  {
    id: 'aiprocmon',
    name: 'DataSnare-AIProcMon',
    category: 'Process investigation',
    description: 'Trace process activity, failures, and slow operations from ProcMon exports.',
    path: '/aiprocmon',
    license: 'Active',
    accent: 'coral',
  },
  {
    id: 'airca',
    name: 'DataSnare-AIRootCause',
    category: 'Root cause analysis',
    description: 'Combine normalized evidence into an incident narrative and next actions.',
    path: '/airca',
    license: 'Active',
    accent: 'violet',
  },
  {
    id: 'ainetscope',
    name: 'DataSnare-AINetScope',
    category: 'Network analysis',
    description: 'Inspect large packet captures, streams, and protocol-level behavior.',
    path: '/ainetscope',
    license: 'Active',
    accent: 'teal',
  },
  {
    id: 'core',
    name: 'DataSnare-Core',
    category: 'Suite control plane',
    description: 'Manage suite identity, access, licensing, and project launch points.',
    path: '/',
    license: 'Included',
    accent: 'ink',
  },
];

function ProjectCard({ project, onOpen }) {
  return (
    <article className={`project-card project-card--${project.accent}`}>
      <div className="project-card__topline">
        <span className="project-card__mark">{project.name.replace('DataSnare-', '').slice(0, 2)}</span>
        <span className="license-pill"><Check size={13} /> {project.license}</span>
      </div>
      <p className="eyebrow">{project.category}</p>
      <h3>{project.name}</h3>
      <p className="project-card__description">{project.description}</p>
      <button className="project-card__link" type="button" onClick={() => onOpen(project)}>
        Open project <ArrowUpRight size={16} />
      </button>
    </article>
  );
}

export default function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [sessionOpen, setSessionOpen] = useState(false);

  const openProject = (project) => {
    if (project.id === 'core') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }
    window.location.assign(project.path);
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="DataSnare home">
          <span className="brand__glyph">DS</span>
          <span>DataSnare</span>
        </a>
        <button className="menu-toggle" type="button" onClick={() => setMenuOpen(!menuOpen)} aria-label="Toggle navigation">
          {menuOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
        <nav className={`topbar__nav ${menuOpen ? 'topbar__nav--open' : ''}`}>
          <a href="#projects" onClick={() => setMenuOpen(false)}>Projects</a>
          <a href="#access" onClick={() => setMenuOpen(false)}>Access</a>
          <a href="#billing" onClick={() => setMenuOpen(false)}>Licensing</a>
          <button className="session-button" type="button" onClick={() => setSessionOpen(true)}>
            <CircleUserRound size={17} /> Sign in
          </button>
        </nav>
      </header>

      <main id="top">
        <section className="hero">
          <div className="hero__copy">
            <p className="eyebrow">The DataSnare control plane</p>
            <h1>One workspace for the moments when systems get complicated.</h1>
            <p className="hero__lede">Launch every DataSnare investigation from one account, with each tool licensed and operated on its own terms.</p>
            <div className="hero__actions">
              <a className="primary-button" href="#projects">Explore projects <ChevronRight size={17} /></a>
              <button className="quiet-button" type="button" onClick={() => setSessionOpen(true)}><KeyRound size={17} /> Connect account</button>
            </div>
          </div>
          <div className="hero__signal" aria-label="Suite status">
            <div className="signal-orbit signal-orbit--one" />
            <div className="signal-orbit signal-orbit--two" />
            <div className="signal-core"><ShieldCheck size={32} /><span>Suite ready</span></div>
            <span className="signal-label signal-label--one">Observe</span>
            <span className="signal-label signal-label--two">Explain</span>
            <span className="signal-label signal-label--three">Act</span>
          </div>
        </section>

        <section className="section-heading" id="projects">
          <div><p className="eyebrow">Project registry</p><h2>Seven instruments, one point of entry.</h2></div>
          <p>Each project keeps its own release cycle and license while the suite keeps your context close.</p>
        </section>
        <section className="project-grid" aria-label="DataSnare projects">
          {projects.map((project) => <ProjectCard key={project.id} project={project} onOpen={openProject} />)}
        </section>

        <section className="access-band" id="access">
          <div><p className="eyebrow">Shared access</p><h2>Sign in once. Move with the investigation.</h2></div>
          <div className="access-band__detail"><ShieldCheck size={23} /><p>Core is the future home for the shared identity session. Project services will receive a scoped handoff instead of separate credentials.</p><button className="primary-button" type="button" onClick={() => setSessionOpen(true)}>Set up access <ChevronRight size={17} /></button></div>
        </section>

        <section className="license-section" id="billing">
          <p className="eyebrow">Licensing</p><h2>Buy the capability you need.</h2><p>Licenses remain independent per project, with suite-level visibility here. Billing and entitlements will attach to an organization account when the Core service is connected.</p>
        </section>
      </main>

      <footer className="footer"><span>DataSnare / app.datasnare.com</span><span>Core shell v0.1</span></footer>

      {sessionOpen && <div className="modal-backdrop" role="presentation" onClick={() => setSessionOpen(false)}><section className="session-modal" role="dialog" aria-modal="true" aria-labelledby="session-title" onClick={(event) => event.stopPropagation()}><button className="modal-close" type="button" onClick={() => setSessionOpen(false)} aria-label="Close"><X size={18} /></button><p className="eyebrow">Shared identity</p><h2 id="session-title">Account connection is next.</h2><p>The shell is ready for the shared login contract. Connect the identity provider and organization licensing service here before production launch.</p><button className="primary-button" type="button" onClick={() => setSessionOpen(false)}>Close <Check size={17} /></button></section></div>}
    </div>
  );
}
