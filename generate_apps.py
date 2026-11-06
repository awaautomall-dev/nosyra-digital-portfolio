from pathlib import Path
import json

ROOT = Path('/home/ubuntu/nosyra/apps')

COMMON_MAIN = r'''import { createRoot } from "react-dom/client";
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
import "./styles.css";

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

const config: AppConfig = __CONFIG__;
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
  try {
    const stored = localStorage.getItem(storageKey);
    return stored ? JSON.parse(stored) : config.seed;
  } catch {
    return config.seed;
  }
}

function loadSettings() {
  try {
    const stored = localStorage.getItem(settingsKey);
    return stored ? JSON.parse(stored) : { companyName: config.company, primary: "#__PRIMARY__", secondary: "#__SECONDARY__", contact: "hello@nosyradigital.com" };
  } catch {
    return { companyName: config.company, primary: "#__PRIMARY__", secondary: "#__SECONDARY__", contact: "hello@nosyradigital.com" };
  }
}

function formatMoney(value: number) {
  return new Intl.NumberFormat("en-NG", { style: "currency", currency: "NGN", maximumFractionDigits: 0 }).format(value);
}

const pathToView: Record<string, string> = { "/": "dashboard", "/login": "login", "/dashboard": "dashboard", "/reports": "reports", "/settings": "settings" };
config.nav.forEach((item) => { pathToView[`/${item.view}`] = item.view; });
function viewFromPath() { return pathToView[window.location.pathname] ?? "dashboard"; }
function pathFromView(view: string) { return view === "dashboard" ? "/dashboard" : `/${view}`; }

function App() {
  const [loggedIn, setLoggedIn] = useState(() => localStorage.getItem(sessionKey) === "true" && viewFromPath() !== "login");
  const [currentView, setCurrentView] = useState(viewFromPath);
  const [records, setRecords] = useState<RecordItem[]>(loadRecords);
  const [settings, setSettings] = useState(loadSettings);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [toast, setToast] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<RecordItem | null>(null);
  const [draft, setDraft] = useState({ name: "", meta: "", owner: "" });

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
  const filteredRecords = useMemo(() => records.filter((item) => `${item.name} ${item.meta} ${item.owner} ${item.tag}`.toLowerCase().includes(query.toLowerCase())), [records, query]);

  if (!loggedIn) return <Login onLogin={login} />;

  return (
    <div className="app-shell">
      <aside className={`sidebar ${mobileOpen ? "is-open" : ""}`}>
        <div className="brand-lockup">
          <div className="brand-mark">N</div>
          <div><strong>{config.product}</strong><span>by Nosyra Digital</span></div>
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
      {toast && <div className="toast"><Check size={16} />{toast}</div>}
      {modalOpen && <RecordModal editing={editing} draft={draft} setDraft={setDraft} onClose={() => setModalOpen(false)} onSave={saveRecord} />}
    </div>
  );
}

function Login({ onLogin }: { onLogin: (role?: string) => void }) {
  const [email, setEmail] = useState(config.demos[0].email);
  const [password, setPassword] = useState("demo-password");
  return <div className="login-shell"><div className="login-art"><div className="login-art-top"><div className="brand-mark">N</div><span>Nosyra Digital</span></div><div className="art-copy"><p className="eyebrow">{config.eyebrow}</p><h1>{config.tagline}</h1><p>One focused workspace for teams who want the next action to be obvious.</p></div><div className="art-stat"><span>Demo environment</span><strong>{config.company}</strong><small>Fictional records · safe for client walkthroughs</small></div></div><div className="login-panel"><div className="login-card"><p className="eyebrow">Secure workspace access</p><h2>Sign in to {config.product}</h2><p className="muted">Use a demo identity below to explore the product.</p><form onSubmit={(event) => { event.preventDefault(); onLogin("Demo administrator"); }}><label>Work email<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} /></label><label>Password<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} /></label><button className="primary-button full-width" type="submit">Enter demo workspace <ArrowRight size={16} /></button></form><div className="demo-access"><div className="section-kicker"><span>Demo access</span><span className="mini-badge">No real data</span></div>{config.demos.map((demo) => <button className="demo-row" key={demo.role} onClick={() => { setEmail(demo.email); onLogin(demo.role); }}><div className="avatar">{demo.name.split(" ").map((word) => word[0]).join("")}</div><div><strong>{demo.role}</strong><span>{demo.name} · {demo.email}</span></div><ArrowRight size={15} /></button>)}</div><p className="login-footnote">Testing build: changes are stored in this browser only.</p></div></div></div>;
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

function mount() {
  const root = document.getElementById("root");
  if (!root) throw new Error("Root element missing");
  root.innerHTML = "";
  createRoot(root).render(<App />);
}

mount();
'''

COMMON_CSS = r''':root {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #172033;
  background: #f4f7f8;
  font-synthesis: none;
  --brand-primary: #0b1d3a;
  --brand-secondary: #1ca6b5;
  --accent-soft: #e5f5f5;
  --ink: #172033;
  --muted: #738094;
  --line: #e4e9ee;
  --surface: #ffffff;
  --surface-soft: #f7f9fa;
  --warning: #c88624;
  --danger: #c1535d;
  --success: #268268;
  --custom-primary: var(--brand-primary);
  --custom-secondary: var(--brand-secondary);
}
* { box-sizing: border-box; }
body { margin: 0; min-width: 320px; background: #f4f7f8; }
button, input, select { font: inherit; }
button { cursor: pointer; }
button:focus-visible, input:focus-visible, select:focus-visible { outline: 3px solid color-mix(in srgb, var(--custom-secondary) 35%, transparent); outline-offset: 2px; }
.app-shell { min-height: 100vh; display: flex; }
.sidebar { width: 258px; flex: 0 0 258px; background: var(--custom-primary); color: #eaf5f5; padding: 24px 16px 18px; display: flex; flex-direction: column; gap: 22px; min-height: 100vh; }
.brand-lockup { display: flex; gap: 11px; align-items: center; padding: 0 8px; }
.brand-lockup strong { display: block; font-size: 15px; letter-spacing: -.02em; }
.brand-lockup span { display: block; color: rgba(255,255,255,.58); font-size: 10px; margin-top: 3px; }
.brand-mark { width: 33px; height: 33px; border-radius: 10px; display: grid; place-items: center; color: var(--custom-primary); background: #fff; font-weight: 900; letter-spacing: -.1em; }
.workspace-switcher { display: flex; gap: 8px; align-items: center; border: 1px solid rgba(255,255,255,.14); color: rgba(255,255,255,.82); border-radius: 10px; padding: 10px 11px; font-size: 12px; }
.workspace-switcher svg { margin-left: auto; opacity: .65; }
.status-dot { width: 7px; height: 7px; border-radius: 50%; background: #64d1af; box-shadow: 0 0 0 4px rgba(100,209,175,.13); }
.nav-label, .eyebrow { color: var(--custom-secondary); text-transform: uppercase; letter-spacing: .14em; font-weight: 800; font-size: 10px; }
.nav-label { color: rgba(255,255,255,.42); margin: 0 10px 7px; }
.primary-nav { display: grid; gap: 3px; }
.nav-item { min-height: 44px; border: 0; background: transparent; color: rgba(255,255,255,.68); border-radius: 9px; display: flex; align-items: center; gap: 11px; padding: 0 11px; text-align: left; font-size: 13px; width: 100%; }
.nav-item:hover { background: rgba(255,255,255,.08); color: #fff; }
.nav-item.active { background: rgba(255,255,255,.13); color: #fff; box-shadow: inset 3px 0 var(--custom-secondary); }
.sidebar-footer { margin-top: auto; display: grid; gap: 4px; }
.account-row { border-top: 1px solid rgba(255,255,255,.13); padding: 15px 6px 0; margin-top: 12px; display: flex; align-items: center; gap: 9px; }
.account-row strong { display: block; font-size: 12px; }
.account-row span { display: block; font-size: 10px; color: rgba(255,255,255,.55); margin-top: 3px; }
.account-row .icon-button { margin-left: auto; color: rgba(255,255,255,.65); }
.main-panel { flex: 1; min-width: 0; }
.topbar { height: 74px; background: rgba(255,255,255,.82); border-bottom: 1px solid var(--line); display: flex; align-items: center; justify-content: space-between; padding: 0 36px; position: sticky; top: 0; z-index: 5; backdrop-filter: blur(14px); }
.breadcrumbs { display: flex; align-items: center; gap: 10px; color: #95a1b1; font-size: 12px; }
.breadcrumbs strong { color: var(--ink); }
.topbar-actions { display: flex; align-items: center; gap: 12px; }
.global-search, .table-search { display: flex; align-items: center; gap: 9px; color: #93a0b0; background: #f5f7f8; border: 1px solid #edf0f2; border-radius: 8px; padding: 0 11px; height: 38px; }
.global-search input, .table-search input { border: 0; outline: 0; background: transparent; width: 205px; color: var(--ink); font-size: 12px; }
.icon-button { border: 0; background: transparent; color: #718094; min-width: 36px; min-height: 36px; border-radius: 8px; display: inline-grid; place-items: center; }
.icon-button:hover { background: #eef3f5; color: var(--ink); }
.notification-button { position: relative; }
.notification-button i { width: 6px; height: 6px; border-radius: 50%; background: #dc6f74; position: absolute; top: 7px; right: 8px; border: 2px solid #fff; }
.avatar { width: 31px; height: 31px; border-radius: 9px; background: color-mix(in srgb, var(--custom-secondary) 18%, white); color: var(--custom-primary); display: grid; place-items: center; font-weight: 800; font-size: 11px; flex: 0 0 auto; }
.avatar-small { width: 32px; height: 32px; border-radius: 50%; border: 0; }
.page-content { padding: 34px 36px 60px; max-width: 1500px; margin: 0 auto; }
.page-header { display: flex; align-items: flex-end; justify-content: space-between; gap: 24px; margin-bottom: 29px; }
.eyebrow { margin: 0 0 8px; color: var(--custom-secondary); }
h1, h2, h3, p { margin-top: 0; }
h1 { font-size: clamp(27px, 3vw, 41px); letter-spacing: -.055em; line-height: 1.08; margin-bottom: 11px; color: var(--ink); }
h2 { font-size: 18px; letter-spacing: -.035em; margin-bottom: 0; }
h3 { font-size: 15px; letter-spacing: -.02em; }
.page-copy, .muted { color: var(--muted); font-size: 13px; line-height: 1.55; max-width: 630px; margin-bottom: 0; }
.primary-button, .secondary-button, .text-button { min-height: 42px; border-radius: 8px; border: 1px solid transparent; padding: 0 14px; display: inline-flex; align-items: center; justify-content: center; gap: 8px; font-weight: 750; font-size: 12px; white-space: nowrap; }
.primary-button { color: #fff; background: var(--custom-primary); box-shadow: 0 6px 16px color-mix(in srgb, var(--custom-primary) 17%, transparent); }
.primary-button:hover { filter: brightness(1.13); transform: translateY(-1px); }
.secondary-button { color: var(--ink); background: #fff; border-color: var(--line); }
.secondary-button:hover { border-color: color-mix(in srgb, var(--custom-secondary) 45%, var(--line)); background: var(--accent-soft); }
.text-button { color: var(--custom-primary); background: transparent; padding: 0; min-height: 34px; }
.full-width { width: 100%; }
.metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 18px; }
.metric-card { padding: 18px 19px; background: var(--surface); border: 1px solid var(--line); border-radius: 12px; min-height: 135px; box-shadow: 0 6px 18px rgba(17,35,56,.025); }
.metric-card:nth-child(2) { background: var(--custom-primary); color: #fff; border-color: var(--custom-primary); }
.metric-card:nth-child(2) .metric-top, .metric-card:nth-child(2) small { color: rgba(255,255,255,.64); }
.metric-top { display: flex; justify-content: space-between; align-items: center; color: #7b8797; font-size: 11px; font-weight: 700; margin-bottom: 24px; }
.metric-card strong { display: block; font-size: 28px; letter-spacing: -.06em; margin-bottom: 7px; }
.metric-card small { color: #8996a5; font-size: 10px; }
.trend-up { color: #3b9b7b; font-weight: 800; }
.metric-card:nth-child(2) .trend-up { color: #9ce6cf; }
.dashboard-grid, .lower-grid, .report-grid, .followup-layout { display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(340px, .8fr); gap: 18px; margin-bottom: 18px; }
.lower-grid { grid-template-columns: .85fr 1.15fr; }
.panel { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 20px; box-shadow: 0 6px 18px rgba(17,35,56,.022); }
.panel-heading { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; margin-bottom: 22px; }
.panel-heading .eyebrow { margin-bottom: 7px; }
.bar-chart { height: 220px; display: flex; align-items: flex-end; gap: 15px; padding: 12px 3px 0; border-bottom: 1px solid var(--line); }
.bar-column { flex: 1; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 10px; }
.bar-track { height: calc(100% - 20px); width: 100%; display: flex; align-items: flex-end; background: linear-gradient(to top, rgba(28,166,181,.07), transparent); border-radius: 6px 6px 0 0; }
.bar-fill { width: 100%; border-radius: 5px 5px 0 0; background: linear-gradient(to top, var(--custom-primary), var(--custom-secondary)); min-height: 18px; transition: height .4s ease; }
.bar-column span { color: #8894a2; font-size: 10px; }
.chart-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 15px; font-size: 11px; color: var(--muted); }
.chart-footer span { display: flex; gap: 7px; align-items: center; }
.legend-dot { width: 7px; height: 7px; background: var(--custom-secondary); border-radius: 50%; }
.chart-footer strong { color: var(--success); font-size: 13px; }
.chart-footer strong small { color: var(--muted); font-size: 10px; font-weight: 500; }
.queue-list { display: grid; gap: 5px; margin-bottom: 14px; }
.queue-row { display: grid; grid-template-columns: 32px minmax(0,1fr) auto 15px; gap: 10px; align-items: center; border: 0; border-bottom: 1px solid #eef1f3; background: transparent; padding: 10px 0; text-align: left; color: var(--ink); }
.queue-row:hover strong { color: var(--custom-primary); }
.queue-icon { width: 30px; height: 30px; display: grid; place-items: center; border-radius: 8px; color: var(--custom-secondary); background: var(--accent-soft); }
.queue-info strong, .queue-value strong { display: block; font-size: 11px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 180px; }
.queue-info span, .queue-value span { display: block; color: var(--muted); font-size: 10px; margin-top: 3px; }
.queue-value { text-align: right; }
.insight-panel { display: flex; align-items: flex-start; gap: 15px; background: color-mix(in srgb, var(--custom-secondary) 8%, #fff); border-color: color-mix(in srgb, var(--custom-secondary) 22%, var(--line)); }
.insight-panel h3 { font-size: 18px; line-height: 1.3; margin-bottom: 8px; }
.insight-icon { width: 39px; height: 39px; flex: 0 0 auto; display: grid; place-items: center; color: var(--custom-primary); background: #fff; border-radius: 10px; }
.activity-row, .owner-row, .doc-row { display: flex; align-items: center; gap: 11px; padding: 12px 0; border-bottom: 1px solid #eef1f3; }
.activity-row:last-child, .owner-row:last-child, .doc-row:last-child { border-bottom: 0; }
.timeline-dot { width: 8px; height: 8px; flex: 0 0 auto; background: var(--custom-secondary); border-radius: 50%; box-shadow: 0 0 0 4px var(--accent-soft); }
.activity-row div:nth-child(2), .owner-row div:nth-child(2), .doc-row div:nth-child(2) { min-width: 0; flex: 1; }
.activity-row strong, .owner-row strong, .doc-row strong { display: block; font-size: 11px; }
.activity-row span, .owner-row span, .doc-row span { display: block; color: var(--muted); font-size: 10px; margin-top: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.activity-row small { color: #9ba6b3; }
.table-panel { padding: 0; overflow: hidden; }
.table-toolbar { display: flex; justify-content: space-between; align-items: center; gap: 15px; padding: 17px 20px; border-bottom: 1px solid var(--line); }
.toolbar-actions { display: flex; gap: 7px; }
.records-table { overflow-x: auto; min-width: 720px; }
.table-head, .table-row { display: grid; grid-template-columns: 2fr 1.3fr 1fr 1fr 80px; gap: 14px; align-items: center; padding: 13px 20px; }
.table-head { color: #98a3b1; text-transform: uppercase; letter-spacing: .1em; font-size: 9px; font-weight: 800; border-bottom: 1px solid var(--line); }
.table-row { min-height: 71px; border-bottom: 1px solid #eef1f3; font-size: 11px; }
.table-row:hover { background: #fbfcfc; }
.table-row > div:not(.record-cell):not(.row-actions) strong { display: block; }
.table-row > div:not(.record-cell):not(.row-actions) span { display: block; color: var(--muted); font-size: 10px; margin-top: 4px; }
.record-cell { display: flex; gap: 10px; align-items: center; min-width: 0; }
.record-cell > div:last-child { min-width: 0; }
.record-cell strong { display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.record-cell span { display: block; color: var(--muted); font-size: 10px; margin-top: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.record-icon { width: 32px; height: 32px; display: grid; place-items: center; color: var(--custom-primary); background: var(--accent-soft); border-radius: 9px; font-size: 12px; font-weight: 850; flex: 0 0 auto; }
.status-pill, .mini-badge, .count-badge { display: inline-flex; align-items: center; gap: 5px; border-radius: 999px; font-size: 10px; font-weight: 750; white-space: nowrap; }
.status-pill { padding: 5px 8px; background: #f0f3f5; color: #6d7886; }
.status-pill.success { color: #23785f; background: #e4f4ee; }
.status-pill.warning { color: #9b681c; background: #fff3d9; }
.status-pill.info { color: #247d8b; background: #e1f4f5; }
.status-pill.danger { color: #a44c57; background: #fae8e9; }
.mini-badge { padding: 4px 7px; background: var(--accent-soft); color: var(--custom-primary); }
.count-badge { min-width: 24px; height: 24px; justify-content: center; background: #f0f3f5; color: #667384; }
.row-actions { display: flex; justify-content: flex-end; gap: 2px; }
.danger-button:hover { color: var(--danger); background: #fae8e9; }
.table-footer { display: flex; justify-content: space-between; gap: 15px; padding: 14px 20px; font-size: 10px; color: #98a3b1; }
.empty-state { text-align: center; padding: 65px 20px; color: var(--muted); }
.empty-state svg { color: var(--custom-secondary); }
.empty-state h3 { color: var(--ink); margin: 12px 0 5px; }
.empty-state p { font-size: 12px; margin: 0; }
.pipeline-board { display: grid; grid-template-columns: repeat(7, minmax(170px, 1fr)); gap: 10px; overflow-x: auto; padding-bottom: 8px; }
.pipeline-column { min-height: 460px; background: #eef3f4; border-radius: 11px; padding: 10px; }
.pipeline-heading { display: flex; justify-content: space-between; align-items: center; gap: 8px; padding: 4px 3px 12px; }
.pipeline-heading > div { display: flex; align-items: center; gap: 7px; min-width: 0; }
.pipeline-heading strong { font-size: 11px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.stage-index { color: var(--custom-secondary); font-size: 9px; font-weight: 800; }
.pipeline-cards { display: grid; gap: 8px; }
.pipeline-card { background: #fff; border: 1px solid var(--line); border-radius: 9px; padding: 12px; box-shadow: 0 5px 12px rgba(17,35,56,.035); }
.card-top, .project-card-top { display: flex; align-items: center; justify-content: space-between; gap: 7px; }
.pipeline-card h3 { margin: 13px 0 5px; font-size: 12px; }
.pipeline-card p, .project-card p, .stock-card p { color: var(--muted); font-size: 10px; line-height: 1.4; margin-bottom: 14px; }
.card-meta { display: flex; justify-content: space-between; gap: 6px; align-items: center; color: var(--muted); font-size: 10px; }
.card-meta span { display: inline-flex; align-items: center; gap: 4px; }
.card-meta strong { font-size: 10px; color: var(--ink); }
.pipeline-move { border-top: 1px solid #eef1f3; margin-top: 11px; padding-top: 9px; }
.pipeline-move label { font-size: 9px; color: var(--muted); display: flex; align-items: center; justify-content: space-between; gap: 5px; }
.pipeline-move select { border: 0; color: var(--custom-primary); font-size: 9px; font-weight: 800; background: transparent; max-width: 85px; }
.stock-alert { display: flex; align-items: center; gap: 12px; background: #fff8e9; border: 1px solid #f4dfad; border-radius: 11px; padding: 13px 16px; margin-bottom: 18px; }
.alert-icon { width: 34px; height: 34px; display: grid; place-items: center; color: #9f711e; background: #ffefc3; border-radius: 8px; }
.stock-alert > div:nth-child(2) { flex: 1; }
.stock-alert strong { display: block; font-size: 12px; }
.stock-alert span { display: block; color: #98794b; font-size: 10px; margin-top: 3px; }
.stock-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
.stock-card-top { display: flex; align-items: center; justify-content: space-between; }
.stock-card h3 { margin: 18px 0 5px; }
.stock-number { padding: 15px 0; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); margin: 14px 0; }
.stock-number strong { display: block; font-size: 30px; letter-spacing: -.07em; color: var(--custom-primary); }
.stock-number span { color: var(--muted); font-size: 10px; }
.stock-actions { display: flex; gap: 7px; }
.stock-actions button { flex: 1; padding: 0 7px; }
.portal-banner { display: flex; align-items: center; gap: 15px; border-radius: 13px; color: #fff; background: var(--custom-primary); padding: 23px; margin-bottom: 18px; }
.portal-avatar { width: 44px; height: 44px; border-radius: 12px; display: grid; place-items: center; color: var(--custom-primary); background: #fff; font-weight: 900; }
.portal-banner > div:nth-child(2) { flex: 1; }
.portal-banner .eyebrow { color: color-mix(in srgb, var(--custom-secondary) 65%, #fff); }
.portal-banner h2 { margin-bottom: 6px; }
.portal-banner p:not(.eyebrow) { margin: 0; color: rgba(255,255,255,.62); font-size: 11px; }
.portal-banner .status-pill { background: rgba(255,255,255,.13); color: #d6fff1; }
.portal-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 18px; }
.project-card-top > span:last-child { color: var(--muted); font-size: 10px; }
.project-card h3 { margin: 18px 0 5px; }
.progress-line { height: 7px; border-radius: 99px; background: #eef2f3; overflow: hidden; }
.progress-line span { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, var(--custom-primary), var(--custom-secondary)); }
.project-card-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; }
.project-card-footer strong { font-size: 11px; }
.doc-icon { width: 31px; height: 31px; display: grid; place-items: center; color: var(--custom-primary); background: var(--accent-soft); border-radius: 8px; }
.doc-row .text-button { margin-left: auto; }
.followup-layout { grid-template-columns: .8fr 1.2fr; }
.calendar-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
.calendar-head strong { font-size: 13px; }
.calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; }
.calendar-day-label { text-align: center; font-size: 10px; color: #9aa5b3; padding-bottom: 7px; }
.calendar-day { border: 0; background: transparent; border-radius: 8px; min-height: 37px; color: #6d7886; font-size: 11px; }
.calendar-day:hover { background: var(--accent-soft); }
.calendar-day.has-event { color: var(--custom-primary); font-weight: 800; text-decoration: underline; text-decoration-color: var(--custom-secondary); text-underline-offset: 4px; }
.calendar-day.selected { color: #fff; background: var(--custom-primary); font-weight: 800; }
.followup-row { display: grid; grid-template-columns: 60px minmax(0,1fr) auto; gap: 12px; align-items: center; padding: 14px 0; border-bottom: 1px solid #eef1f3; }
.time-block strong { display: block; font-size: 12px; }
.time-block span { display: block; font-size: 9px; color: var(--muted); margin-top: 2px; }
.followup-row > div:nth-child(2) { min-width: 0; }
.followup-row > div:nth-child(2) strong { display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.followup-row > div:nth-child(2) span { display: block; font-size: 10px; color: var(--muted); margin-top: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.report-highlight { background: var(--custom-primary); color: #fff; border-color: var(--custom-primary); }
.report-highlight .eyebrow, .report-highlight .report-highlight-top svg { color: var(--custom-secondary); }
.report-highlight h2 { max-width: 360px; line-height: 1.25; }
.report-highlight-top { display: flex; justify-content: space-between; align-items: flex-start; }
.report-stat-row { display: flex; gap: 30px; padding: 28px 0 24px; }
.report-stat-row strong { display: block; font-size: 23px; letter-spacing: -.05em; }
.report-stat-row span { display: block; color: rgba(255,255,255,.57); font-size: 10px; margin-top: 4px; }
.report-bars { height: 130px; display: flex; align-items: flex-end; gap: 13px; padding-top: 12px; border-bottom: 1px solid rgba(255,255,255,.16); }
.report-bars > div { flex: 1; height: 100%; display: flex; align-items: center; flex-direction: column; justify-content: flex-end; gap: 8px; }
.report-bars span { display: block; width: 100%; background: linear-gradient(to top, var(--custom-secondary), color-mix(in srgb, var(--custom-secondary) 45%, #fff)); border-radius: 4px 4px 0 0; min-height: 16px; }
.report-bars small { font-size: 9px; color: rgba(255,255,255,.53); }
.owner-progress { width: 70px; height: 5px; background: #edf1f2; border-radius: 99px; overflow: hidden; }
.owner-progress span { display: block; height: 100%; background: var(--custom-secondary); border-radius: inherit; }
.owner-row > strong { font-size: 10px; }
.report-footnote { display: flex; align-items: center; gap: 11px; color: var(--custom-primary); }
.report-footnote div { min-width: 0; }
.report-footnote strong { display: block; font-size: 11px; }
.report-footnote span { display: block; color: var(--muted); font-size: 10px; line-height: 1.45; margin-top: 3px; }
.settings-layout { display: grid; grid-template-columns: minmax(0, 1fr) minmax(340px, .8fr); gap: 18px; }
.settings-card { display: grid; gap: 16px; }
.settings-card .panel-heading { margin-bottom: 2px; }
.settings-card label, .modal-card label, .login-card label { display: grid; gap: 7px; color: #5c697a; font-size: 11px; font-weight: 750; }
.settings-card input, .modal-card input, .login-card input { height: 43px; border: 1px solid var(--line); background: #fbfcfc; border-radius: 8px; padding: 0 12px; color: var(--ink); }
.settings-card input:focus, .modal-card input:focus, .login-card input:focus { border-color: var(--custom-secondary); outline: 0; background: #fff; }
.color-fields { display: grid; grid-template-columns: 1fr 1fr; gap: 13px; }
.color-input { display: flex; align-items: center; gap: 9px; height: 43px; border: 1px solid var(--line); border-radius: 8px; padding: 5px 9px; background: #fbfcfc; }
.color-input input { width: 31px; height: 31px; padding: 0; border: 0; background: transparent; }
.color-input span { color: var(--muted); font-size: 11px; }
.preview-card { background: linear-gradient(135deg, #f3f8f8, #fff); display: flex; flex-direction: column; justify-content: space-between; min-height: 380px; }
.preview-window { width: 100%; border: 1px solid var(--line); background: #fff; border-radius: 11px; overflow: hidden; box-shadow: 0 12px 35px rgba(17,35,56,.08); }
.preview-window-top { display: flex; gap: 5px; padding: 10px 12px; border-bottom: 1px solid var(--line); }
.preview-window-top span { width: 6px; height: 6px; border-radius: 50%; background: #dbe2e7; }
.preview-window-body { display: grid; place-items: center; padding: 35px 20px; text-align: center; }
.preview-logo { width: 42px; height: 42px; border-radius: 13px; color: #fff; display: grid; place-items: center; font-weight: 900; margin-bottom: 13px; }
.preview-window-body strong { font-size: 16px; }
.preview-window-body > span { color: var(--muted); font-size: 10px; margin-top: 5px; }
.preview-button { color: #fff; border-radius: 7px; font-size: 10px; padding: 9px 16px; margin-top: 21px; }
.preview-card h2 { margin-bottom: 8px; }
.modal-backdrop { position: fixed; inset: 0; z-index: 20; background: rgba(14,25,42,.48); display: grid; place-items: center; padding: 20px; }
.modal-card { background: #fff; border-radius: 14px; width: min(470px, 100%); padding: 23px; box-shadow: 0 24px 70px rgba(14,25,42,.25); display: grid; gap: 15px; }
.modal-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 5px; }
.modal-header h2 { margin-top: 0; }
.modal-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 6px; }
.toast { position: fixed; z-index: 30; right: 24px; bottom: 24px; display: flex; align-items: center; gap: 9px; background: var(--custom-primary); color: #fff; border-radius: 9px; padding: 12px 15px; font-size: 12px; font-weight: 700; box-shadow: 0 15px 40px rgba(10,25,50,.2); }
.mobile-menu { display: none; }
.login-shell { min-height: 100vh; display: grid; grid-template-columns: 1.05fr .95fr; background: #f4f7f8; }
.login-art { background: var(--brand-primary); padding: 40px 8vw 45px; color: #fff; display: flex; flex-direction: column; min-height: 100vh; position: relative; overflow: hidden; }
.login-art::after { content: ""; position: absolute; width: 480px; height: 480px; border-radius: 50%; border: 1px solid rgba(255,255,255,.12); right: -210px; bottom: -180px; box-shadow: 0 0 0 42px rgba(255,255,255,.03), 0 0 0 85px rgba(255,255,255,.025); }
.login-art-top { display: flex; align-items: center; gap: 10px; font-size: 13px; font-weight: 800; }
.login-art-top .brand-mark { color: var(--brand-primary); background: #fff; }
.art-copy { margin: auto 0; position: relative; z-index: 1; max-width: 490px; }
.art-copy .eyebrow { color: var(--brand-secondary); }
.art-copy h1 { font-size: clamp(38px, 5vw, 66px); color: #fff; max-width: 530px; margin-bottom: 18px; }
.art-copy p:not(.eyebrow) { color: rgba(255,255,255,.65); font-size: 14px; line-height: 1.6; max-width: 380px; }
.art-stat { border-left: 2px solid var(--brand-secondary); padding-left: 14px; position: relative; z-index: 1; }
.art-stat span, .art-stat small { display: block; color: rgba(255,255,255,.52); font-size: 10px; }
.art-stat strong { display: block; margin: 6px 0; font-size: 14px; }
.login-panel { display: grid; place-items: center; padding: 30px; }
.login-card { width: min(430px, 100%); background: #fff; border: 1px solid var(--line); border-radius: 15px; padding: clamp(24px, 4vw, 42px); box-shadow: 0 16px 45px rgba(17,35,56,.06); }
.login-card h2 { font-size: 27px; margin: 0 0 10px; letter-spacing: -.05em; }
.login-card form { display: grid; gap: 14px; margin: 25px 0 24px; }
.demo-access { border-top: 1px solid var(--line); padding-top: 18px; }
.section-kicker { display: flex; justify-content: space-between; align-items: center; margin-bottom: 9px; color: #8591a0; font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: .1em; }
.demo-row { width: 100%; border: 0; border-bottom: 1px solid #eef1f3; background: transparent; display: flex; align-items: center; gap: 9px; text-align: left; padding: 10px 0; color: var(--ink); }
.demo-row:last-child { border-bottom: 0; }
.demo-row > div:nth-child(2) { flex: 1; min-width: 0; }
.demo-row strong, .demo-row span { display: block; }
.demo-row strong { font-size: 11px; }
.demo-row span { color: var(--muted); font-size: 10px; margin-top: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.demo-row > svg { color: var(--custom-secondary); }
.login-footnote { color: #a0aab5; font-size: 10px; text-align: center; margin: 19px 0 0; }
@media (max-width: 1100px) {
  .metric-grid { grid-template-columns: repeat(2, 1fr); }
  .dashboard-grid, .lower-grid, .report-grid, .followup-layout { grid-template-columns: 1fr; }
  .stock-grid, .portal-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 760px) {
  .sidebar { position: fixed; z-index: 10; left: -275px; transition: left .2s ease; box-shadow: 20px 0 50px rgba(17,35,56,.14); }
  .sidebar.is-open { left: 0; }
  .topbar { height: 64px; padding: 0 16px; }
  .mobile-menu { display: inline-grid; margin-right: 6px; }
  .breadcrumbs span, .breadcrumbs svg { display: none; }
  .global-search { display: none; }
  .page-content { padding: 25px 16px 45px; }
  .page-header { align-items: flex-start; flex-direction: column; gap: 16px; }
  .page-header .primary-button { width: 100%; }
  .metric-grid { gap: 9px; }
  .metric-card { min-height: 118px; padding: 14px; }
  .metric-top { margin-bottom: 18px; }
  .metric-card strong { font-size: 23px; }
  .panel { padding: 15px; }
  .bar-chart { height: 170px; gap: 7px; }
  .chart-footer { align-items: flex-start; flex-direction: column; gap: 8px; }
  .table-toolbar { align-items: stretch; flex-direction: column; padding: 13px 15px; }
  .table-search input { width: 100%; }
  .toolbar-actions { display: grid; grid-template-columns: 1fr 1fr; }
  .table-head { display: none; }
  .records-table { min-width: 0; }
  .table-row { display: grid; grid-template-columns: 1fr auto; gap: 9px; padding: 14px 15px; }
  .table-row > div:nth-child(2), .table-row > div:nth-child(3), .table-row > div:nth-child(4) { grid-column: 1 / 2; padding-left: 42px; }
  .table-row > div:nth-child(2) { margin-top: -7px; }
  .table-row > div:nth-child(3), .table-row > div:nth-child(4) { display: inline-flex; padding-left: 0; margin-right: 5px; }
  .row-actions { grid-column: 2; grid-row: 1; }
  .table-footer { padding: 12px 15px; flex-direction: column; }
  .stock-grid, .portal-grid { grid-template-columns: 1fr; }
  .stock-alert { align-items: flex-start; flex-wrap: wrap; }
  .stock-alert .text-button { margin-left: 46px; }
  .portal-banner { align-items: flex-start; flex-wrap: wrap; padding: 16px; }
  .portal-banner .status-pill { margin-left: 59px; }
  .settings-layout { grid-template-columns: 1fr; }
  .color-fields { grid-template-columns: 1fr; }
  .login-shell { display: block; }
  .login-art { min-height: 340px; padding: 25px 24px; }
  .art-copy { margin: 64px 0 30px; }
  .art-copy h1 { font-size: 38px; }
  .art-stat { display: none; }
  .login-panel { padding: 20px 16px 35px; margin-top: -30px; position: relative; }
  .login-card { padding: 24px 19px; }
  .report-stat-row { gap: 15px; flex-wrap: wrap; }
  .report-stat-row > div { min-width: 70px; }
  .owner-progress { width: 44px; }
  .followup-row { grid-template-columns: 47px minmax(0,1fr); }
  .followup-row .status-pill { grid-column: 2; justify-self: start; }
}
@media (max-width: 390px) {
  .metric-grid { grid-template-columns: 1fr 1fr; }
  .metric-card strong { font-size: 20px; }
  h1 { font-size: 29px; }
  .topbar-actions { gap: 4px; }
}
'''

APPS = {
  'crm': {
    'title': 'Nosyra CRM', 'eyebrow': 'Customer relationship management', 'tagline': 'Move every relationship forward.', 'company': 'Apexline Advisory', 'resource': 'Leads & customers', 'singular': 'lead', 'primary': '0b1d3a', 'secondary': '1ca6b5',
    'nav': [
      {'label':'Dashboard','view':'dashboard','icon':'dashboard'}, {'label':'Leads','view':'records','icon':'records'}, {'label':'Sales pipeline','view':'pipeline','icon':'pipeline'}, {'label':'Customers','view':'customers','icon':'records'}, {'label':'Follow-ups','view':'followups','icon':'followups'}, {'label':'Reports','view':'reports','icon':'reports'}, {'label':'Settings','view':'settings','icon':'settings'}],
    'metrics': [
      {'label':'Total leads','value':'248','delta':'12.6%','tone':'neutral'}, {'label':'Pipeline value','value':'₦42.8m','delta':'18.4%','tone':'primary'}, {'label':'Won this month','value':'19','delta':'8.9%','tone':'neutral'}, {'label':'Follow-ups due','value':'14','delta':'5.2%','tone':'neutral'}],
    'pipeline': ['New','Contacted','Qualified','Proposal Sent','Negotiation','Won','Lost'],
    'seed': [
      {'id':101,'name':'Aderonke Properties','meta':'Real estate partnership','status':'Qualified','tag':'Referral','value':18500000,'secondary':'Lagos','priority':'High','owner':'Amara Dike'},
      {'id':102,'name':'Kora Buildworks','meta':'Construction retainer','status':'Proposal Sent','tag':'Website','value':12400000,'secondary':'Due in 2d','priority':'High','owner':'Tomi Adeyemi'},
      {'id':103,'name':'Northwind Studio','meta':'Brand transformation','status':'New','tag':'LinkedIn','value':7200000,'secondary':'Last touched 1h','priority':'Medium','owner':'Amara Dike'},
      {'id':104,'name':'Mile 7 Advisory','meta':'Quarterly consulting','status':'Won','tag':'Partner','value':8900000,'secondary':'Closed Oct 30','priority':'Low','owner':'Femi Okafor'},
      {'id':105,'name':'Sable & Co.','meta':'Digital growth plan','status':'Contacted','tag':'Event','value':5600000,'secondary':'Call tomorrow','priority':'Medium','owner':'Tomi Adeyemi'}],
    'activity': [{'label':'Jun','value':42,'note':''},{'label':'Jul','value':60,'note':''},{'label':'Aug','value':53,'note':''},{'label':'Sep','value':76,'note':''},{'label':'Oct','value':66,'note':''},{'label':'Nov','value':92,'note':''}],
    'demos': [{'role':'Administrator','name':'Amara Dike','email':'admin@apexline.demo'},{'role':'Sales representative','name':'Tomi Adeyemi','email':'sales@apexline.demo'}],
    'specialTitle':'Revenue rhythm', 'specialCopy':'', 'specialCards':[], 'statusTone': {'New':'info','Contacted':'neutral','Qualified':'success','Proposal Sent':'warning','Negotiation':'warning','Won':'success','Lost':'danger'}
  },
  'inventory': {
    'title': 'Nosyra Inventory', 'eyebrow': 'Inventory & warehouse operations', 'tagline': 'Protect stock. Keep trade moving.', 'company': 'Harbourline Distribution', 'resource': 'Products & stock', 'singular': 'product', 'primary': '153b35', 'secondary': 'd49b45',
    'nav': [
      {'label':'Dashboard','view':'dashboard','icon':'dashboard'}, {'label':'Products','view':'records','icon':'records'}, {'label':'Stock movement','view':'stock','icon':'stock'}, {'label':'Suppliers','view':'suppliers','icon':'suppliers'}, {'label':'Purchase orders','view':'purchases','icon':'purchases'}, {'label':'Reports','view':'reports','icon':'reports'}, {'label':'Settings','view':'settings','icon':'settings'}],
    'metrics': [
      {'label':'Total products','value':'1,284','delta':'4.2%','tone':'neutral'}, {'label':'Stock value','value':'₦68.4m','delta':'9.8%','tone':'primary'}, {'label':'Low-stock items','value':'36','delta':'3.1%','tone':'neutral'}, {'label':'Open POs','value':'18','delta':'6.4%','tone':'neutral'}],
    'pipeline': ['In stock','Low stock','Out of stock'],
    'seed': [
      {'id':201,'name':'14mm Reinforcement Bar','meta':'SKU RBR-014 · Steel','status':'In stock','tag':'Construction','value':380,'secondary':'380 units','priority':'Low','owner':'Warehouse A'},
      {'id':202,'name':'Portland Cement 50kg','meta':'SKU CEM-050 · Building materials','status':'Low stock','tag':'Fast moving','value':76,'secondary':'76 units','priority':'High','owner':'Warehouse A'},
      {'id':203,'name':'Copper Cable 6mm','meta':'SKU CAB-006 · Electrical','status':'In stock','tag':'Electrical','value':248,'secondary':'248 units','priority':'Medium','owner':'Warehouse B'},
      {'id':204,'name':'Safety Helmet — Yellow','meta':'SKU PPE-001 · Safety equipment','status':'Out of stock','tag':'PPE','value':0,'secondary':'0 units','priority':'High','owner':'Warehouse B'},
      {'id':205,'name':'PVC Pipe 110mm','meta':'SKU PVC-110 · Plumbing','status':'In stock','tag':'Plumbing','value':142,'secondary':'142 units','priority':'Low','owner':'Warehouse C'}],
    'activity': [{'label':'Jun','value':66,'note':''},{'label':'Jul','value':72,'note':''},{'label':'Aug','value':58,'note':''},{'label':'Sep','value':81,'note':''},{'label':'Oct','value':74,'note':''},{'label':'Nov','value':88,'note':''}],
    'demos': [{'role':'Administrator','name':'Kelechi Nwosu','email':'admin@harbourline.demo'},{'role':'Warehouse manager','name':'Bisi Afolabi','email':'warehouse@harbourline.demo'},{'role':'Staff','name':'Sani Bello','email':'staff@harbourline.demo'}],
    'specialTitle':'Stock movement', 'specialCopy':'', 'specialCards':[], 'statusTone': {'In stock':'success','Low stock':'warning','Out of stock':'danger'}
  },
  'projectflow': {
    'title': 'Nosyra ProjectFlow', 'eyebrow': 'Project & workforce management', 'tagline': 'Keep delivery visible.', 'company': 'Meridian Civil & Engineering', 'resource': 'Projects & delivery', 'singular': 'project', 'primary': '35233f', 'secondary': '69b8cb',
    'nav': [
      {'label':'Dashboard','view':'dashboard','icon':'dashboard'}, {'label':'Projects','view':'records','icon':'projects'}, {'label':'Tasks','view':'tasks','icon':'tasks'}, {'label':'Workforce','view':'workforce','icon':'workforce'}, {'label':'Expenses','view':'expenses','icon':'expenses'}, {'label':'Client portal','view':'portal','icon':'portal'}, {'label':'Reports','view':'reports','icon':'reports'}, {'label':'Settings','view':'settings','icon':'settings'}],
    'metrics': [
      {'label':'Active projects','value':'12','delta':'8.3%','tone':'neutral'}, {'label':'Project budgets','value':'₦284m','delta':'11.2%','tone':'primary'}, {'label':'Tasks in progress','value':'87','delta':'6.8%','tone':'neutral'}, {'label':'Overdue tasks','value':'9','delta':'2.4%','tone':'neutral'}],
    'pipeline': ['Planning','In progress','At risk','Complete'],
    'seed': [
      {'id':301,'name':'Eko Heights Residences','meta':'Client: Meridian Estates','status':'In progress','tag':'Construction','value':185000000,'secondary':'68% complete','priority':'High','owner':'Ifeoma Nnadi'},
      {'id':302,'name':'Lekki Drainage Upgrade','meta':'Client: Lagos Works Bureau','status':'At risk','tag':'Infrastructure','value':74000000,'secondary':'41% complete','priority':'High','owner':'David Mensah'},
      {'id':303,'name':'Airport Logistics Hub','meta':'Client: Nuru Logistics','status':'Planning','tag':'Engineering','value':52000000,'secondary':'Brief approved','priority':'Medium','owner':'Ifeoma Nnadi'},
      {'id':304,'name':'Cedar Grove Offices','meta':'Client: Cedar Grove Ltd','status':'Complete','tag':'Architecture','value':33000000,'secondary':'Signed off','priority':'Low','owner':'Chidi Obi'},
      {'id':305,'name':'Ikoyi Energy Retrofit','meta':'Client: Eko Facilities','status':'In progress','tag':'Retrofit','value':46000000,'secondary':'27% complete','priority':'Medium','owner':'David Mensah'}],
    'activity': [{'label':'Jun','value':48,'note':''},{'label':'Jul','value':58,'note':''},{'label':'Aug','value':63,'note':''},{'label':'Sep','value':57,'note':''},{'label':'Oct','value':79,'note':''},{'label':'Nov','value':87,'note':''}],
    'demos': [{'role':'Administrator','name':'Ifeoma Nnadi','email':'admin@meridian.demo'},{'role':'Project manager','name':'David Mensah','email':'pm@meridian.demo'},{'role':'Client','name':'Nura Ibrahim','email':'client@meridian.demo'}],
    'specialTitle':'Delivery pulse', 'specialCopy':'', 'specialCards':[], 'statusTone': {'Planning':'info','In progress':'success','At risk':'warning','Complete':'success'}
  }
}

for slug, app in APPS.items():
    folder = ROOT / slug
    (folder / 'src').mkdir(parents=True, exist_ok=True)
    (folder / 'public').mkdir(exist_ok=True)
    (folder / 'backend').mkdir(exist_ok=True)
    (folder / 'database').mkdir(exist_ok=True)
    (folder / 'api').mkdir(exist_ok=True)
    ts_config = json.dumps({
        'compilerOptions': {'target':'ES2020','useDefineForClassFields':True,'lib':['ES2020','DOM','DOM.Iterable'],'allowJs':False,'skipLibCheck':True,'esModuleInterop':True,'allowSyntheticDefaultImports':True,'strict':True,'forceConsistentCasingInFileNames':True,'module':'ESNext','moduleResolution':'Bundler','resolveJsonModule':True,'isolatedModules':True,'noEmit':True,'jsx':'react-jsx'},
        'include':['src','vite.config.ts']
    }, indent=2)
    package = json.dumps({'name':f'nosyra-{slug}','private':True,'version':'0.1.0','type':'module','scripts':{'dev':'vite','build':'tsc -b && vite build','preview':'vite preview'},'dependencies':{'@vitejs/plugin-react':'latest','lucide-react':'latest','react':'latest','react-dom':'latest'},'devDependencies':{'@types/react':'latest','@types/react-dom':'latest','typescript':'latest','vite':'latest'}}, indent=2)
    nav = app['nav']
    config_json = json.dumps({'slug':slug,'product':app['title'],'eyebrow':app['eyebrow'],'tagline':app['tagline'],'company':app['company'],'resourceLabel':app['resource'],'singularLabel':app['singular'],'nav':nav,'metrics':app['metrics'],'pipeline':app['pipeline'],'seed':app['seed'],'activity':app['activity'],'demos':app['demos'],'specialTitle':app['specialTitle'],'specialCopy':'','specialCards':[],'statusTone':app['statusTone']}, indent=2)
    # Add the appropriate unique nav label to generic records screens through the existing active breadcrumb.
    main = COMMON_MAIN.replace('__CONFIG__', config_json).replace('__PRIMARY__', app['primary']).replace('__SECONDARY__', app['secondary'])
    (folder / 'package.json').write_text(package + '\n')
    (folder / 'tsconfig.json').write_text(ts_config + '\n')
    (folder / 'src/vite-env.d.ts').write_text('/// <reference types=\"vite/client\" />\n')
    (folder / 'src/main.tsx').write_text(main)
    css = COMMON_CSS.replace('#0b1d3a', f'#{app["primary"]}', 1).replace('#1ca6b5', f'#{app["secondary"]}', 1)
    (folder / 'src/styles.css').write_text(css)
    (folder / 'index.html').write_text(f'''<!doctype html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n    <meta name="theme-color" content="#{app['primary']}" />\n    <meta name="description" content="{app['title']} — {app['eyebrow']} by Nosyra Digital" />\n    <title>{app['title']} · Nosyra Digital</title>\n  </head>\n  <body>\n    <div id="root"></div>\n    <script type="module" src="/src/main.tsx"></script>\n  </body>\n</html>\n''')
    (folder / 'vite.config.ts').write_text('''import { defineConfig } from "vite";\nimport react from "@vitejs/plugin-react";\n\nexport default defineConfig({\n  plugins: [react()],\n  server: { host: "0.0.0.0", port: 3000 },\n});\n''')
    route_entries = [{'path':'/','title':app['title']},{'path':'/login','title':f'{app["title"]} Login'},{'path':'/dashboard','title':'Dashboard'}] + [{'path':f'/{item["view"]}','title':item['label']} for item in app['nav'] if item['view'] != 'dashboard']
    (folder / 'public/manus-routes.json').write_text(json.dumps({'routes':route_entries}, indent=2) + '\n')
    (folder / 'vercel.json').write_text(json.dumps({'buildCommand':'npm run build','outputDirectory':'dist','framework':'vite','rewrites':[{'source':'/(.*)','destination':'/index.html'}]}, indent=2) + '\n')
    (folder / 'README.md').write_text(f'''# {app['title']}\n\n{app['title']} is an independent Nosyra Digital testing application for {app['eyebrow'].lower()}. It has its own package, frontend source, public route manifest, Vercel configuration, demo identity, and browser-persisted sample records.\n\n## Run\n\n```bash\nnpm install\nnpm run dev\n```\n\n## Deploy to Vercel\n\nImport the repository into Vercel and set the project root directory to `apps/{slug}`. Use `npm run build` and `dist` if Vercel does not auto-detect the Vite defaults.\n\n## Demo access\n\nThe login page includes fictional role accounts for safe walkthroughs. No real credentials are required. Records created or changed in this testing build are stored in the current browser's localStorage. Use the browser's site data controls to reset the demo.\n\n## Testing-build limitation\n\nThis is a frontend testing build. It does not claim production authentication, a PHP 8 REST API, MySQL persistence, server-side authorization, validated file storage, rate limiting, or multi-tenant isolation. See `backend/README.md`, `database/schema.sql`, and `api/openapi.yaml` for the production starting points to implement next.\n''')
    (folder / 'backend/README.md').write_text(f'''# {app['title']} backend boundary\n\nThe Vercel-ready testing build intentionally keeps records in the browser so the user can test the interface immediately. The production implementation should replace this adapter with an independent PHP 8 REST API and MySQL database for {app['title']}.\n\nRequired next layer: password hashing and reset flow, secure session cookies, backend-enforced roles, prepared SQL statements, server-side validation, CSRF protection where applicable, rate limiting, structured error logging, uploads backed by object storage, database-backed reports, seed/reset commands, and isolated deployment configuration. Do not treat the current frontend demo as a secure production backend.\n''')
    if slug == 'crm':
        schema = '''CREATE TABLE users (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(160) NOT NULL, email VARCHAR(190) UNIQUE NOT NULL, password_hash VARCHAR(255) NOT NULL, role VARCHAR(80) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);\nCREATE TABLE leads (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(180) NOT NULL, email VARCHAR(190), phone VARCHAR(40), company VARCHAR(180), source VARCHAR(80), owner_id BIGINT, status VARCHAR(50) NOT NULL, priority VARCHAR(30), notes TEXT, follow_up_at DATETIME, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (owner_id) REFERENCES users(id));\nCREATE TABLE pipeline_history (id BIGINT PRIMARY KEY AUTO_INCREMENT, lead_id BIGINT NOT NULL, from_status VARCHAR(50), to_status VARCHAR(50) NOT NULL, changed_by BIGINT NOT NULL, changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (lead_id) REFERENCES leads(id), FOREIGN KEY (changed_by) REFERENCES users(id));\nCREATE TABLE tasks (id BIGINT PRIMARY KEY AUTO_INCREMENT, lead_id BIGINT, title VARCHAR(180) NOT NULL, due_at DATETIME, priority VARCHAR(30), completed_at DATETIME NULL, assigned_to BIGINT, FOREIGN KEY (lead_id) REFERENCES leads(id), FOREIGN KEY (assigned_to) REFERENCES users(id));\nCREATE TABLE customers (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(180) NOT NULL, company VARCHAR(180), email VARCHAR(190), notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);\n'''
    elif slug == 'inventory':
        schema = '''CREATE TABLE users (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(160) NOT NULL, email VARCHAR(190) UNIQUE NOT NULL, password_hash VARCHAR(255) NOT NULL, role VARCHAR(80) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);\nCREATE TABLE warehouses (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(160) NOT NULL, address VARCHAR(255));\nCREATE TABLE products (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(180) NOT NULL, sku VARCHAR(80) UNIQUE NOT NULL, barcode VARCHAR(120), category VARCHAR(100), unit VARCHAR(40), purchase_price DECIMAL(14,2), selling_price DECIMAL(14,2), reorder_level INT DEFAULT 0, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);\nCREATE TABLE stock_balances (product_id BIGINT NOT NULL, warehouse_id BIGINT NOT NULL, quantity INT NOT NULL DEFAULT 0, PRIMARY KEY(product_id, warehouse_id), FOREIGN KEY(product_id) REFERENCES products(id), FOREIGN KEY(warehouse_id) REFERENCES warehouses(id));\nCREATE TABLE stock_movements (id BIGINT PRIMARY KEY AUTO_INCREMENT, product_id BIGINT NOT NULL, warehouse_id BIGINT NOT NULL, movement_type VARCHAR(30) NOT NULL, quantity INT NOT NULL, reference VARCHAR(120), created_by BIGINT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(product_id) REFERENCES products(id), FOREIGN KEY(warehouse_id) REFERENCES warehouses(id), FOREIGN KEY(created_by) REFERENCES users(id));\nCREATE TABLE suppliers (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(180) NOT NULL, email VARCHAR(190), phone VARCHAR(40), balance DECIMAL(14,2) DEFAULT 0);\n'''
    else:
        schema = '''CREATE TABLE users (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(160) NOT NULL, email VARCHAR(190) UNIQUE NOT NULL, password_hash VARCHAR(255) NOT NULL, role VARCHAR(80) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);\nCREATE TABLE projects (id BIGINT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(180) NOT NULL, client_name VARCHAR(180), manager_id BIGINT, start_date DATE, end_date DATE, status VARCHAR(50), budget DECIMAL(14,2), progress TINYINT DEFAULT 0, FOREIGN KEY(manager_id) REFERENCES users(id));\nCREATE TABLE tasks (id BIGINT PRIMARY KEY AUTO_INCREMENT, project_id BIGINT NOT NULL, title VARCHAR(180) NOT NULL, assignee_id BIGINT, priority VARCHAR(30), due_date DATE, status VARCHAR(40), description TEXT, FOREIGN KEY(project_id) REFERENCES projects(id), FOREIGN KEY(assignee_id) REFERENCES users(id));\nCREATE TABLE expenses (id BIGINT PRIMARY KEY AUTO_INCREMENT, project_id BIGINT NOT NULL, category VARCHAR(100), amount DECIMAL(14,2) NOT NULL, incurred_on DATE, notes TEXT, created_by BIGINT NOT NULL, FOREIGN KEY(project_id) REFERENCES projects(id), FOREIGN KEY(created_by) REFERENCES users(id));\nCREATE TABLE milestones (id BIGINT PRIMARY KEY AUTO_INCREMENT, project_id BIGINT NOT NULL, title VARCHAR(180) NOT NULL, due_date DATE, status VARCHAR(40), approved_at DATETIME NULL, FOREIGN KEY(project_id) REFERENCES projects(id));\nCREATE TABLE project_documents (id BIGINT PRIMARY KEY AUTO_INCREMENT, project_id BIGINT NOT NULL, name VARCHAR(255) NOT NULL, storage_key VARCHAR(255) NOT NULL, visibility VARCHAR(30) NOT NULL DEFAULT 'internal', uploaded_by BIGINT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(project_id) REFERENCES projects(id), FOREIGN KEY(uploaded_by) REFERENCES users(id));\n'''
    (folder / 'database/schema.sql').write_text(schema)
    (folder / 'api/openapi.yaml').write_text(f'''openapi: 3.0.3\ninfo:\n  title: {app['title']} API\n  version: 0.1.0\n  description: Production API starting point for the independent {app['title']} deployment.\nservers:\n  - url: https://api.example.com\npaths:\n  /auth/login:\n    post:\n      summary: Start a secure session\n      responses:\n        '200': {{description: Session started}}\n        '401': {{description: Invalid credentials}}\n  /dashboard/summary:\n    get:\n      summary: Return database-backed dashboard metrics\n      responses:\n        '200': {{description: Summary returned}}\n  /records:\n    get:\n      summary: List records with pagination, filtering, and sorting\n      responses:\n        '200': {{description: Records returned}}\n    post:\n      summary: Create a record after server-side validation\n      responses:\n        '201': {{description: Record created}}\n  /records/{{id}}:\n    patch:\n      summary: Update an authorized record\n      responses:\n        '200': {{description: Record updated}}\n    delete:\n      summary: Delete an authorized record\n      responses:\n        '204': {{description: Record deleted}}\n''')

(Path('/home/ubuntu/nosyra/.gitignore')).write_text('node_modules\ndist\n.env\n.env.*\n.DS_Store\n')
print('generated', ', '.join(APPS))
