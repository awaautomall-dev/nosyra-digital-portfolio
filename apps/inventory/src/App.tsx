"use client";

import {
  Activity,
  ArrowDownToLine,
  ArrowRight,
  ArrowUpFromLine,
  BarChart3,
  Bell,
  BriefcaseBusiness,
  CalendarClock,
  Check,
  CheckCircle2,
  ChevronDown,
  ClipboardList,
  FileBarChart,
  FileText,
  FolderKanban,
  LayoutDashboard,
  LifeBuoy,
  LogOut,
  Menu,
  Package,
  Plus,
  Search,
  Settings2,
  ShieldCheck,
  SlidersHorizontal,
  Sparkles,
  Target,
  Trash2,
  Truck,
  UserRound,
  Users,
  WalletCards,
  X,
} from "lucide-react";
import { FormEvent, ReactNode, useEffect, useMemo, useState } from "react";

type RecordItem = {
  id: number;
  name: string;
  meta: string;
  status: string;
  tag: string;
  value: number;
  secondary: string;
  priority: string;
  owner: string;
};

type NavItem = { label: string; view: string; icon: string };
type Metric = { label: string; value: string; delta: string; tone: string };

type AppConfig = {
  slug: string;
  product: string;
  eyebrow: string;
  tagline: string;
  company: string;
  resourceLabel: string;
  singularLabel: string;
  nav: NavItem[];
  metrics: Metric[];
  pipeline: string[];
  seed: RecordItem[];
  activity: { label: string; value: number; note: string }[];
  demos: { role: string; name: string; email: string }[];
  specialTitle: string;
  specialCopy: string;
  specialCards: { title: string; value: string; note: string; tone: string }[];
  statusTone: Record<string, string>;
};

const config: AppConfig = {
  "slug": "inventory",
  "product": "Nosyra Inventory",
  "eyebrow": "Inventory & warehouse operations",
  "tagline": "Protect stock. Keep trade moving.",
  "company": "Harbourline Distribution",
  "resourceLabel": "Products & stock",
  "singularLabel": "product",
  "nav": [
    {
      "label": "Dashboard",
      "view": "dashboard",
      "icon": "dashboard"
    },
    {
      "label": "Products",
      "view": "records",
      "icon": "records"
    },
    {
      "label": "Stock movement",
      "view": "stock",
      "icon": "stock"
    },
    {
      "label": "Suppliers",
      "view": "suppliers",
      "icon": "suppliers"
    },
    {
      "label": "Purchase orders",
      "view": "purchases",
      "icon": "purchases"
    },
    {
      "label": "Reports",
      "view": "reports",
      "icon": "reports"
    },
    {
      "label": "Settings",
      "view": "settings",
      "icon": "settings"
    }
  ],
  "metrics": [
    {
      "label": "Total products",
      "value": "1,284",
      "delta": "4.2%",
      "tone": "neutral"
    },
    {
      "label": "Stock value",
      "value": "\u20a668.4m",
      "delta": "9.8%",
      "tone": "primary"
    },
    {
      "label": "Low-stock items",
      "value": "36",
      "delta": "3.1%",
      "tone": "neutral"
    },
    {
      "label": "Open POs",
      "value": "18",
      "delta": "6.4%",
      "tone": "neutral"
    }
  ],
  "pipeline": [
    "In stock",
    "Low stock",
    "Out of stock"
  ],
  "seed": [
    {
      "id": 201,
      "name": "14mm Reinforcement Bar",
      "meta": "SKU RBR-014 \u00b7 Steel",
      "status": "In stock",
      "tag": "Construction",
      "value": 380,
      "secondary": "380 units",
      "priority": "Low",
      "owner": "Warehouse A"
    },
    {
      "id": 202,
      "name": "Portland Cement 50kg",
      "meta": "SKU CEM-050 \u00b7 Building materials",
      "status": "Low stock",
      "tag": "Fast moving",
      "value": 76,
      "secondary": "76 units",
      "priority": "High",
      "owner": "Warehouse A"
    },
    {
      "id": 203,
      "name": "Copper Cable 6mm",
      "meta": "SKU CAB-006 \u00b7 Electrical",
      "status": "In stock",
      "tag": "Electrical",
      "value": 248,
      "secondary": "248 units",
      "priority": "Medium",
      "owner": "Warehouse B"
    },
    {
      "id": 204,
      "name": "Safety Helmet \u2014 Yellow",
      "meta": "SKU PPE-001 \u00b7 Safety equipment",
      "status": "Out of stock",
      "tag": "PPE",
      "value": 0,
      "secondary": "0 units",
      "priority": "High",
      "owner": "Warehouse B"
    },
    {
      "id": 205,
      "name": "PVC Pipe 110mm",
      "meta": "SKU PVC-110 \u00b7 Plumbing",
      "status": "In stock",
      "tag": "Plumbing",
      "value": 142,
      "secondary": "142 units",
      "priority": "Low",
      "owner": "Warehouse C"
    }
  ],
  "activity": [
    {
      "label": "Jun",
      "value": 66,
      "note": ""
    },
    {
      "label": "Jul",
      "value": 72,
      "note": ""
    },
    {
      "label": "Aug",
      "value": 58,
      "note": ""
    },
    {
      "label": "Sep",
      "value": 81,
      "note": ""
    },
    {
      "label": "Oct",
      "value": 74,
      "note": ""
    },
    {
      "label": "Nov",
      "value": 88,
      "note": ""
    }
  ],
  "demos": [
    {
      "role": "Administrator",
      "name": "Kelechi Nwosu",
      "email": "admin@harbourline.demo"
    },
    {
      "role": "Warehouse manager",
      "name": "Bisi Afolabi",
      "email": "warehouse@harbourline.demo"
    },
    {
      "role": "Staff",
      "name": "Sani Bello",
      "email": "staff@harbourline.demo"
    }
  ],
  "specialTitle": "Stock movement",
  "specialCopy": "",
  "specialCards": [],
  "statusTone": {
    "In stock": "success",
    "Low stock": "warning",
    "Out of stock": "danger"
  }
};
const iconMap: Record<string, ReactNode> = {
  dashboard: <LayoutDashboard size={17} />,
  records: <Users size={17} />,
  pipeline: <Target size={17} />,
  stock: <Package size={17} />,
  suppliers: <Truck size={17} />,
  purchases: <ClipboardList size={17} />,
  projects: <FolderKanban size={17} />,
  tasks: <CheckCircle2 size={17} />,
  workforce: <Users size={17} />,
  expenses: <WalletCards size={17} />,
  portal: <ShieldCheck size={17} />,
  reports: <FileBarChart size={17} />,
  followups: <CalendarClock size={17} />,
  settings: <Settings2 size={17} />,
};

const storageKey = `nosyra-${config.slug}-records`;
const settingsKey = `nosyra-${config.slug}-settings`;
const sessionKey = `nosyra-${config.slug}-session`;

function loadRecords(): RecordItem[] {
  if (typeof window === "undefined") return config.seed;
  try {
    const stored = localStorage.getItem(storageKey);
    return stored ? JSON.parse(stored) : config.seed;
  } catch {
    return config.seed;
  }
}

function loadSettings() {
  const defaults = { companyName: config.company, primary: "#0b1d3a", secondary: "#1ca6b5", contact: "hello@nosyradigital.com" };
  if (typeof window === "undefined") return defaults;
  try {
    const stored = localStorage.getItem(settingsKey);
    if (!stored) return defaults;
    const saved = JSON.parse(stored) as Partial<typeof defaults> | null;
    if (!saved || typeof saved !== "object") return defaults;
    return {
      ...defaults,
      ...saved,
      primary: !saved.primary || saved.primary === "#153b35" ? defaults.primary : saved.primary,
      secondary: !saved.secondary || saved.secondary === "#d49b45" ? defaults.secondary : saved.secondary,
    };
  } catch {
    return defaults;
  }
}

function formatMoney(value: number) {
  return new Intl.NumberFormat("en-NG", { style: "currency", currency: "NGN", maximumFractionDigits: 0 }).format(value);
}

const servicePrefix = "/inventory";
const pathToView: Record<string, string> = { "/": "dashboard", "/login": "login", "/dashboard": "dashboard", "/reports": "reports", "/settings": "settings" };
config.nav.forEach((item) => { pathToView[`/${item.view}`] = item.view; });
function viewFromPath() {
  if (typeof window === "undefined") return "dashboard";
  const pathname = window.location.pathname.startsWith(servicePrefix) ? window.location.pathname.slice(servicePrefix.length) || "/" : window.location.pathname;
  return pathToView[pathname] ?? "dashboard";
}
function pathFromView(view: string) { return `${window.location.pathname.startsWith(servicePrefix) ? servicePrefix : ""}${view === "dashboard" ? "/dashboard" : `/${view}`}`; }

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [currentView, setCurrentView] = useState(viewFromPath);
  const [records, setRecords] = useState<RecordItem[]>(loadRecords);
  const [settings, setSettings] = useState(loadSettings);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [moreOpen, setMoreOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [toast, setToast] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<RecordItem | null>(null);
  const [draft, setDraft] = useState({ name: "", meta: "", owner: "" });

  useEffect(() => {
    setLoggedIn(localStorage.getItem(sessionKey) === "true" && viewFromPath() !== "login");
  }, []);

  useEffect(() => {
    const handlePopState = () => setCurrentView(viewFromPath());
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  useEffect(() => {
    localStorage.setItem(storageKey, JSON.stringify(records));
  }, [records]);

  useEffect(() => {
    document.body.dataset.product = config.slug;
    document.documentElement.style.setProperty("--custom-primary", settings.primary);
    document.documentElement.style.setProperty("--custom-secondary", settings.secondary);
  }, [settings]);

  useEffect(() => {
    if (!toast) return;
    const timer = window.setTimeout(() => setToast(""), 3000);
    return () => window.clearTimeout(timer);
  }, [toast]);

  function navigate(view: string, replace = false) {
    const pathname = pathFromView(view);
    if (replace) window.history.replaceState({}, "", pathname);
    else window.history.pushState({}, "", pathname);
    setCurrentView(view);
  }

  function login(role = config.demos[0].role) {
    localStorage.setItem(sessionKey, "true");
    setLoggedIn(true);
    navigate("dashboard", true);
    setToast(`${role} demo session started`);
  }

  function logout() {
    localStorage.removeItem(sessionKey);
    setLoggedIn(false);
    navigate("login", true);
  }

  function exportCsv() {
    const header = "name,context,status,owner,priority\n";
    const body = records.map((item) => [item.name, item.meta, item.status, item.owner, item.priority].map((value) => `"${String(value).split('"').join('""')}"`).join(",")).join("\n");
    const blob = new Blob([header + body], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `${config.slug}-records.csv`;
    anchor.click();
    URL.revokeObjectURL(url);
    setToast("CSV exported from this demo workspace");
  }

  function openCreate() {
    setEditing(null);
    setDraft({ name: "", meta: "", owner: "" });
    setModalOpen(true);
  }

  function openEdit(item: RecordItem) {
    setEditing(item);
    setDraft({ name: item.name, meta: item.meta, owner: item.owner });
    setModalOpen(true);
  }

  function saveRecord(event: FormEvent) {
    event.preventDefault();
    if (!draft.name.trim()) return;
    if (editing) {
      setRecords((current) => current.map((item) => item.id === editing.id ? { ...item, ...draft } : item));
      setToast(`${config.singularLabel} updated`);
    } else {
      setRecords((current) => [{ id: Date.now(), name: draft.name, meta: draft.meta || "New business record", status: config.pipeline[0], tag: "New", value: 0, secondary: "Just added", priority: "Medium", owner: draft.owner || "Unassigned" }, ...current]);
      setToast(`${config.singularLabel} created`);
    }
    setModalOpen(false);
  }

  function deleteRecord(id: number) {
    setRecords((current) => current.filter((item) => item.id !== id));
    setToast(`${config.singularLabel} removed from this demo workspace`);
  }

  function moveRecord(id: number, status: string) {
    setRecords((current) => current.map((item) => item.id === id ? { ...item, status } : item));
    setToast(`Moved record to ${status}`);
  }

  function updateQuantity(id: number, amount: number) {
    setRecords((current) => current.map((item) => item.id === id ? { ...item, value: Math.max(0, item.value + amount), secondary: `${Math.max(0, item.value + amount)} units` } : item));
    setToast(amount > 0 ? "Stock received" : "Stock issued");
  }

  function saveSettings(event: FormEvent) {
    event.preventDefault();
    localStorage.setItem(settingsKey, JSON.stringify(settings));
    setToast("White-label settings saved locally");
  }

  const activeNav = config.nav.find((item) => item.view === currentView) ?? config.nav[0];
  const mobilePrimaryNav = config.nav.filter((item) => ["dashboard", "records", "reports"].includes(item.view));
  const mobileMoreNav = config.nav.filter((item) => !mobilePrimaryNav.some((primary) => primary.view === item.view));
  const filteredRecords = useMemo(() => records.filter((item) => `${item.name} ${item.meta} ${item.owner} ${item.tag}`.toLowerCase().includes(query.toLowerCase())), [records, query]);

  if (!loggedIn) return <Login onLogin={login} />;

  return (
    <div className="app-shell">
      <aside className={`sidebar ${mobileOpen ? "is-open" : ""}`}>
        <div className="brand-lockup">
          <img className="brand-logo" src="/inventory/nosyra-logo-white.png" alt="Nosyra Digital logo" />
          <div className="brand-product"><strong>{config.product}</strong><a href="https://www.nosyradigital.com.ng/" target="_blank" rel="noreferrer">Websites that convert</a></div>
        </div>
        <div className="workspace-switcher"><span className="status-dot" />{settings.companyName}<ChevronDown size={15} /></div>
        <nav className="primary-nav">
          <div className="nav-label">Workspace</div>
          {config.nav.map((item) => <button key={item.view} className={currentView === item.view ? "nav-item active" : "nav-item"} onClick={() => { navigate(item.view); setMobileOpen(false); }}><span>{iconMap[item.icon]}</span>{item.label}</button>)}
        </nav>
        <div className="sidebar-footer">
          <button className="nav-item" onClick={() => setToast("Support desk is available in the production workspace") }><LifeBuoy size={17} />Support desk</button>
          <button className="nav-item" onClick={() => navigate("settings")}><Settings2 size={17} />Workspace settings</button>
          <div className="account-row"><div className="avatar">{config.demos[0].name.split(" ").map((word) => word[0]).join("")}</div><div><strong>{config.demos[0].name}</strong><span>{config.demos[0].role}</span></div><button className="icon-button" onClick={logout} aria-label="Log out"><LogOut size={16} /></button></div>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <button className="mobile-menu icon-button" onClick={() => setMobileOpen((open) => !open)} aria-label="Open navigation"><Menu size={20} /></button>
          <div className="breadcrumbs"><span>{config.product}</span><ArrowRight size={14} /><strong>{activeNav.label}</strong></div>
          <div className="topbar-actions"><div className="global-search"><Search size={16} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder={`Search ${config.resourceLabel.toLowerCase()}...`} /></div><button className="icon-button notification-button" onClick={() => setToast("No new notifications in this demo workspace")} aria-label="Notifications"><Bell size={18} /><i /></button><button className="avatar avatar-small">{config.demos[0].name.split(" ").map((word) => word[0]).join("")}</button></div>
        </header>
        <div className="page-content">
          {currentView === "dashboard" && <Dashboard records={records} onNavigate={navigate} onCreate={openCreate} />}
          {currentView !== "dashboard" && currentView !== "reports" && currentView !== "settings" && currentView !== "pipeline" && currentView !== "stock" && currentView !== "portal" && currentView !== "followups" && <RecordsView title={activeNav.label} records={filteredRecords} query={query} onQuery={setQuery} onCreate={openCreate} onEdit={openEdit} onDelete={deleteRecord} onExport={exportCsv} />}
          {currentView === "pipeline" && <Pipeline records={records} onMove={moveRecord} />}
          {currentView === "stock" && <Stock records={records} onUpdate={updateQuantity} />}
          {currentView === "portal" && <ClientPortal records={records} />}
          {currentView === "reports" && <Reports records={records} />}
          {currentView === "settings" && <Settings settings={settings} setSettings={setSettings} onSave={saveSettings} />}
          {currentView === "followups" && <Followups records={filteredRecords} onCreate={openCreate} />}
        </div>
      </main>
      {moreOpen && (
        <>
          <button className="mobile-more-backdrop" type="button" aria-label="Close More menu" onClick={() => setMoreOpen(false)} />
          <div className="mobile-more-menu" id="mobile-more-menu" aria-label="More pages">
            <div className="mobile-more-title">More pages</div>
            {mobileMoreNav.map((item) => (
              <button key={item.view} type="button" className={currentView === item.view ? "mobile-more-item active" : "mobile-more-item"} onClick={() => { navigate(item.view); setMoreOpen(false); }}>
                {iconMap[item.icon]}<span>{item.label}</span><ArrowRight size={14} aria-hidden="true" />
              </button>
            ))}
          </div>
        </>
      )}
      <nav className="mobile-tabs" aria-label="Mobile workspace navigation">
        {mobilePrimaryNav.map((item) => (
          <button key={item.view} type="button" className={currentView === item.view ? "mobile-tab active" : "mobile-tab"} aria-current={currentView === item.view ? "page" : undefined} onClick={() => { navigate(item.view); setMoreOpen(false); }}>
            {iconMap[item.icon]}<span>{item.label}</span>
          </button>
        ))}
        <button type="button" className={moreOpen || mobileMoreNav.some((item) => item.view === currentView) ? "mobile-tab active" : "mobile-tab"} aria-expanded={moreOpen} aria-controls="mobile-more-menu" onClick={() => setMoreOpen((open) => !open)}>
          <Menu size={18} aria-hidden="true" /><span>More</span>
        </button>
      </nav>
      {toast && <div className="toast"><Check size={16} />{toast}</div>}
      {modalOpen && <RecordModal editing={editing} draft={draft} setDraft={setDraft} onClose={() => setModalOpen(false)} onSave={saveRecord} />}
    </div>
  );
}

function Login({ onLogin }: { onLogin: (role?: string) => void }) {
  const [email, setEmail] = useState(config.demos[0].email);
  const [password, setPassword] = useState("demo-password");
  return <div className="login-shell"><div className="login-art"><div className="login-art-top"><img className="login-brand-logo" src="/inventory/nosyra-logo-white.png" alt="Nosyra Digital logo" /><a className="login-brand-link" href="https://www.nosyradigital.com.ng/" target="_blank" rel="noreferrer">nosyradigital.com.ng</a></div><div className="art-copy"><p className="eyebrow">{config.eyebrow}</p><h1>{config.tagline}</h1><p>One focused workspace for teams who want the next action to be obvious.</p></div><div className="art-stat"><span>Demo environment</span><strong>{config.company}</strong><small>Fictional records · safe for client walkthroughs</small></div></div><div className="login-panel"><div className="login-card"><p className="eyebrow">Secure workspace access</p><h2>Sign in to {config.product}</h2><p className="muted">Use a demo identity below to explore the product.</p><form onSubmit={(event) => { event.preventDefault(); onLogin("Demo administrator"); }}><label>Work email<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} /></label><label>Password<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} /></label><button className="primary-button full-width" type="submit">Enter demo workspace <ArrowRight size={16} /></button></form><div className="demo-access"><div className="section-kicker"><span>Demo access</span><span className="mini-badge">No real data</span></div>{config.demos.map((demo) => <button className="demo-row" key={demo.role} onClick={() => { setEmail(demo.email); onLogin(demo.role); }}><div className="avatar">{demo.name.split(" ").map((word) => word[0]).join("")}</div><div><strong>{demo.role}</strong><span>{demo.name} · {demo.email}</span></div><ArrowRight size={15} /></button>)}</div><p className="login-footnote">Testing build: changes are stored in this browser only.</p></div></div></div>;
}

function PageHeader({ eyebrow, title, copy, action, onAction }: { eyebrow: string; title: string; copy: string; action?: string; onAction?: () => void }) {
  return <div className="page-header"><div><p className="eyebrow">{eyebrow}</p><h1>{title}</h1><p className="page-copy">{copy}</p></div>{action && <button className="primary-button" onClick={onAction}><Plus size={17} />{action}</button>}</div>;
}

function Dashboard({ records, onNavigate, onCreate }: { records: RecordItem[]; onNavigate: (view: string) => void; onCreate: () => void }) {
  const totalValue = records.reduce((sum, item) => sum + item.value, 0);
  return <><PageHeader eyebrow={`${config.product} / Overview`} title="Keep the next move visible." copy={`A live snapshot of ${config.company}'s ${config.resourceLabel.toLowerCase()}, health signals, and work in motion.`} action={`New ${config.singularLabel}`} onAction={onCreate} /><section className="metric-grid">{config.metrics.map((metric) => <div className={`metric-card ${metric.tone}`} key={metric.label}><div className="metric-top"><span>{metric.label}</span><Activity size={16} /></div><strong>{metric.label === "Pipeline value" || metric.label === "Stock value" || metric.label === "Project budgets" ? formatMoney(totalValue || 0) : metric.value}</strong><small><span className="trend-up">↗ {metric.delta}</span> vs last period</small></div>)}</section><div className="dashboard-grid"><section className="panel chart-panel"><div className="panel-heading"><div><p className="eyebrow">Momentum / 6 periods</p><h2>{config.specialTitle}</h2></div><button className="text-button" onClick={() => onNavigate("reports")}>View report <ArrowRight size={15} /></button></div><div className="bar-chart">{config.activity.map((bar) => <div className="bar-column" key={bar.label}><div className="bar-track"><div className="bar-fill" style={{ height: `${bar.value}%` }} /></div><span>{bar.label}</span></div>)}</div><div className="chart-footer"><span><i className="legend-dot" />Healthy operating rhythm</span><strong>+18.4% <small>since previous cycle</small></strong></div></section><section className="panel queue-panel"><div className="panel-heading"><div><p className="eyebrow">Focus queue</p><h2>Work that needs a signal</h2></div><button className="icon-button"><SlidersHorizontal size={17} /></button></div><div className="queue-list">{records.slice(0, 4).map((item) => <button className="queue-row" key={item.id} onClick={() => onNavigate("records")}><div className="queue-icon"><Sparkles size={16} /></div><div className="queue-info"><strong>{item.name}</strong><span>{item.meta}</span></div><div className="queue-value"><strong>{item.status}</strong><span>{item.secondary}</span></div><ArrowRight size={15} /></button>)}</div><button className="secondary-button full-width" onClick={() => onNavigate("records")}>Open all {config.resourceLabel.toLowerCase()}</button></section></div><section className="lower-grid"><section className="panel insight-panel"><div className="insight-icon"><BarChart3 size={21} /></div><div><p className="eyebrow">Operator note</p><h3>Momentum is strongest where ownership is explicit.</h3><p className="muted">Keep handoffs small, assign a next action, and let the workspace carry the context.</p></div></section><section className="panel activity-panel"><div className="panel-heading"><div><p className="eyebrow">Recent activity</p><h2>Today, in brief</h2></div></div>{records.slice(0, 3).map((item, index) => <div className="activity-row" key={item.id}><div className="timeline-dot" /><div><strong>{index === 0 ? "Status updated" : index === 1 ? "Record reviewed" : "Follow-up scheduled"}</strong><span>{item.name} · {item.owner}</span></div><small>{index + 1}h</small></div>)}</section></section></>;
}

function RecordsView({ title, records, query, onQuery, onCreate, onEdit, onDelete, onExport }: { title: string; records: RecordItem[]; query: string; onQuery: (value: string) => void; onCreate: () => void; onEdit: (item: RecordItem) => void; onDelete: (id: number) => void; onExport: () => void }) {
  return <><PageHeader eyebrow={`${config.product} / Workspace`} title={title} copy={`Search, sort, and keep ${config.resourceLabel.toLowerCase()} moving without losing context.`} action={`New ${config.singularLabel}`} onAction={onCreate} /><section className="panel table-panel"><div className="table-toolbar"><div className="table-search"><Search size={16} /><input value={query} onChange={(event) => onQuery(event.target.value)} placeholder={`Search ${config.resourceLabel.toLowerCase()}`} /></div><div className="toolbar-actions"><button className="secondary-button" onClick={() => onQuery("")}><SlidersHorizontal size={15} />Clear filter</button><button className="secondary-button" onClick={onExport}><FileText size={15} />Export CSV</button></div></div>{records.length ? <div className="records-table"><div className="table-head"><span>{config.singularLabel}</span><span>Owner / context</span><span>Status</span><span>Signal</span><span /></div>{records.map((item) => <div className="table-row" key={item.id}><div className="record-cell"><div className="record-icon">{item.name.slice(0, 1)}</div><div><strong>{item.name}</strong><span>{item.meta}</span></div></div><div><strong>{item.owner}</strong><span>{item.tag}</span></div><div><span className={`status-pill ${config.statusTone[item.status] || "neutral"}`}>{item.status}</span></div><div><strong>{item.priority}</strong><span>{item.secondary}</span></div><div className="row-actions"><button className="icon-button" onClick={() => onEdit(item)} aria-label={`Edit ${item.name}`}><Settings2 size={15} /></button><button className="icon-button danger-button" onClick={() => onDelete(item.id)} aria-label={`Delete ${item.name}`}><Trash2 size={15} /></button></div></div>)}</div> : <div className="empty-state"><Search size={24} /><h3>No matching records</h3><p>Try a different search or create the first record in this view.</p></div>}<div className="table-footer"><span>Showing {records.length} of {records.length} records</span><span>Local demo persistence enabled</span></div></section></>;
}

function Pipeline({ records, onMove }: { records: RecordItem[]; onMove: (id: number, status: string) => void }) {
  return <><PageHeader eyebrow={`${config.product} / Flow`} title="Move work forward, one signal at a time." copy="The pipeline is designed for quick scanning, clear ownership, and decisive next steps." /><div className="pipeline-board">{config.pipeline.map((stage) => <section className="pipeline-column" key={stage}><div className="pipeline-heading"><div><span className="stage-index">{String(config.pipeline.indexOf(stage) + 1).padStart(2, "0")}</span><strong>{stage}</strong></div><span className="count-badge">{records.filter((item) => item.status === stage).length}</span></div><div className="pipeline-cards">{records.filter((item) => item.status === stage).map((item) => <article className="pipeline-card" key={item.id}><div className="card-top"><span className="mini-badge">{item.tag}</span><button className="icon-button"><SlidersHorizontal size={14} /></button></div><h3>{item.name}</h3><p>{item.meta}</p><div className="card-meta"><span><UserRound size={13} />{item.owner}</span><strong>{item.value ? formatMoney(item.value) : item.secondary}</strong></div><div className="pipeline-move"><label>Move to<select value={item.status} onChange={(event) => onMove(item.id, event.target.value)}>{config.pipeline.map((option) => <option key={option}>{option}</option>)}</select></label></div></article>)}</div></section>)}</div></>;
}

function Stock({ records, onUpdate }: { records: RecordItem[]; onUpdate: (id: number, amount: number) => void }) {
  return <><PageHeader eyebrow={`${config.product} / Operations`} title="Protect stock availability." copy="Fast, traceable movement controls for the floor team and warehouse manager." /><div className="stock-alert"><div className="alert-icon"><ArrowDownToLine size={18} /></div><div><strong>3 items need attention</strong><span>Reorder levels are calculated from this demo's local transaction stream.</span></div><button className="text-button">Review alerts <ArrowRight size={15} /></button></div><section className="stock-grid">{records.map((item) => <article className="panel stock-card" key={item.id}><div className="stock-card-top"><div className="record-icon"><Package size={16} /></div><span className={`status-pill ${item.value < 100 ? "warning" : "success"}`}>{item.value < 100 ? "Reorder soon" : "Healthy"}</span></div><h3>{item.name}</h3><p>{item.meta}</p><div className="stock-number"><strong>{item.value}</strong><span>units on hand</span></div><div className="stock-actions"><button className="secondary-button" onClick={() => onUpdate(item.id, -5)}><ArrowDownToLine size={15} />Issue 5</button><button className="primary-button" onClick={() => onUpdate(item.id, 10)}><ArrowUpFromLine size={15} />Receive 10</button></div></article>)}</section></>;
}

function ClientPortal({ records }: { records: RecordItem[] }) {
  return <><PageHeader eyebrow="ProjectFlow / Client portal" title="Give clients the right view." copy="A clean, permission-aware snapshot for approvals, milestones, and shared project context." /><section className="portal-banner"><div className="portal-avatar">ME</div><div><p className="eyebrow">Previewing client access</p><h2>Meridian Estates</h2><p>Only approved project updates and shared documents are visible in this view.</p></div><span className="status-pill success"><ShieldCheck size={14} />Isolated view</span></section><div className="portal-grid">{records.slice(0, 3).map((item, index) => <article className="panel project-card" key={item.id}><div className="project-card-top"><span className="mini-badge">{index === 0 ? "Priority project" : "Active"}</span><span>{item.secondary}</span></div><h3>{item.name}</h3><p>{item.meta}</p><div className="progress-line"><span style={{ width: `${62 + index * 9}%` }} /></div><div className="project-card-footer"><strong>{62 + index * 9}% complete</strong><button className="text-button">Open update <ArrowRight size={14} /></button></div></article>)}</div><section className="panel shared-docs"><div className="panel-heading"><div><p className="eyebrow">Shared workspace</p><h2>Latest client-ready documents</h2></div><button className="secondary-button"><Plus size={15} />Share update</button></div>{["Programme overview.pdf", "Approved milestone notes.docx", "Site progress photos.zip"].map((doc) => <div className="doc-row" key={doc}><div className="doc-icon"><FileText size={16} /></div><div><strong>{doc}</strong><span>Shared with Meridian Estates · Today</span></div><button className="text-button">Preview <ArrowRight size={14} /></button></div>)}</section></>;
}

function Followups({ records, onCreate }: { records: RecordItem[]; onCreate: () => void }) {
  return <><PageHeader eyebrow={`${config.product} / Follow-ups`} title="Make the next conversation easy." copy="A focused queue for commitments, handoffs, and reminders that should not live in someone's head." action="Schedule follow-up" onAction={onCreate} /><div className="followup-layout"><section className="panel calendar-panel"><div className="calendar-head"><button className="icon-button">‹</button><strong>November 2026</strong><button className="icon-button">›</button></div><div className="calendar-grid">{["M", "T", "W", "T", "F", "S", "S"].map((day, index) => <span className="calendar-day-label" key={`${day}-${index}`}>{day}</span>)}{Array.from({ length: 30 }, (_, index) => <button className={index === 6 ? "calendar-day selected" : index % 7 === 4 ? "calendar-day has-event" : "calendar-day"} key={index}>{index + 1}</button>)}</div></section><section className="panel followup-list"><div className="panel-heading"><div><p className="eyebrow">Today and next</p><h2>Scheduled work</h2></div><span className="count-badge">{records.length}</span></div>{records.slice(0, 5).map((item, index) => <div className="followup-row" key={item.id}><div className="time-block"><strong>{index + 9}:30</strong><span>AM</span></div><div><strong>{item.name}</strong><span>{item.meta} · {item.owner}</span></div><span className="status-pill neutral">{index === 0 ? "Due today" : "Upcoming"}</span></div>)}</section></div></>;
}

function Reports({ records }: { records: RecordItem[] }) {
  return <><PageHeader eyebrow={`${config.product} / Intelligence`} title="Turn activity into a clear operating picture." copy="A compact report layer for conversations with your team and prospective clients." /><div className="report-grid"><section className="panel report-highlight"><div className="report-highlight-top"><div><p className="eyebrow">Current period</p><h2>Healthy signal across the workspace</h2></div><FileBarChart size={22} /></div><div className="report-stat-row"><div><strong>{records.length}</strong><span>active records</span></div><div><strong>{Math.round(records.length * 0.68)}%</strong><span>on track</span></div><div><strong>{formatMoney(records.reduce((sum, item) => sum + item.value, 0))}</strong><span>tracked value</span></div></div><div className="report-bars">{config.activity.map((bar) => <div key={bar.label}><span style={{ height: `${bar.value}%` }} /><small>{bar.label}</small></div>)}</div></section><section className="panel report-table"><div className="panel-heading"><div><p className="eyebrow">Record performance</p><h2>By owner</h2></div><button className="secondary-button"><FileText size={15} />CSV</button></div>{records.slice(0, 5).map((item) => <div className="owner-row" key={item.id}><div className="avatar avatar-small">{item.owner.slice(0, 2).toUpperCase()}</div><div><strong>{item.owner}</strong><span>{item.name}</span></div><div className="owner-progress"><span style={{ width: `${45 + (item.id % 5) * 9}%` }} /></div><strong>{45 + (item.id % 5) * 9}%</strong></div>)}</section></div><section className="panel report-footnote"><ShieldCheck size={18} /><div><strong>Report provenance</strong><span>All values shown here are derived from the records stored in this browser demo. Production reports should be powered by server-side queries.</span></div></section></>;
}

function Settings({ settings, setSettings, onSave }: { settings: any; setSettings: (value: any) => void; onSave: (event: FormEvent) => void }) {
  return <><PageHeader eyebrow={`${config.product} / Administration`} title="Make the workspace feel like yours." copy="These white-label controls are saved in this browser so a client walkthrough can use a familiar identity." /><form className="settings-layout" onSubmit={onSave}><section className="panel settings-card"><div className="panel-heading"><div><p className="eyebrow">Brand identity</p><h2>Workspace profile</h2></div><Settings2 size={20} /></div><label>Company name<input value={settings.companyName} onChange={(event) => setSettings({ ...settings, companyName: event.target.value })} /></label><label>Contact email<input type="email" value={settings.contact} onChange={(event) => setSettings({ ...settings, contact: event.target.value })} /></label><div className="color-fields"><label>Primary colour<div className="color-input"><input type="color" value={settings.primary} onChange={(event) => setSettings({ ...settings, primary: event.target.value })} /><span>{settings.primary}</span></div></label><label>Secondary colour<div className="color-input"><input type="color" value={settings.secondary} onChange={(event) => setSettings({ ...settings, secondary: event.target.value })} /><span>{settings.secondary}</span></div></label></div><button className="primary-button" type="submit">Save white-label settings <Check size={16} /></button></section><section className="panel preview-card"><div className="preview-window"><div className="preview-window-top"><span /><span /><span /></div><div className="preview-window-body"><div className="preview-logo" style={{ background: settings.primary }}>N</div><strong>{settings.companyName}</strong><span>Powered by {config.product}</span><div className="preview-button" style={{ background: settings.primary }}>Primary action</div></div></div><div><p className="eyebrow">Preview</p><h2>Client-ready, without rebuilding the UI.</h2><p className="muted">Production deployments should move these settings into an isolated tenant configuration.</p></div></section></form></>;
}

function RecordModal({ editing, draft, setDraft, onClose, onSave }: { editing: RecordItem | null; draft: { name: string; meta: string; owner: string }; setDraft: (draft: { name: string; meta: string; owner: string }) => void; onClose: () => void; onSave: (event: FormEvent) => void }) {
  return <div className="modal-backdrop" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}><form className="modal-card" onSubmit={onSave}><div className="modal-header"><div><p className="eyebrow">{editing ? "Edit record" : "Create record"}</p><h2>{editing ? `Update ${config.singularLabel.toLowerCase()}` : `Add a ${config.singularLabel.toLowerCase()}`}</h2></div><button className="icon-button" type="button" onClick={onClose}><X size={18} /></button></div><label>Name<input autoFocus required value={draft.name} onChange={(event) => setDraft({ ...draft, name: event.target.value })} placeholder="e.g. Meridian Estates" /></label><label>Context<input value={draft.meta} onChange={(event) => setDraft({ ...draft, meta: event.target.value })} placeholder="Short business context" /></label><label>Owner<input value={draft.owner} onChange={(event) => setDraft({ ...draft, owner: event.target.value })} placeholder="Assign a teammate" /></label><div className="modal-actions"><button className="secondary-button" type="button" onClick={onClose}>Cancel</button><button className="primary-button" type="submit">{editing ? "Save changes" : "Create record"}<ArrowRight size={15} /></button></div></form></div>;
}
