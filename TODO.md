# Nosyra Digital Portfolio — Delivery TODO

## Current request

- [x] Create a branded landing page at `/` with links to the CRM (`/crm`), Inventory (`/inventory`), and ProjectFlow (`/projectflow`) workspaces. Use the shared Nosyra navy/teal team colors across all four services, show a white logo on dark surfaces and the original logo on light surfaces, and provide a mobile bottom bar with four icon tabs (Dashboard, the main module, Reports, and More) so remaining pages are available under More. All four production builds pass.

## Completed in this testing build

- [x] Three separate application directories exist: `apps/crm`, `apps/inventory`, and `apps/projectflow`; each has its own source, package manifest, build config, README, database notes, API notes, and Vercel config.
- [x] Each app has an independent login/demo-access screen, a responsive dashboard, sidebar navigation, top navigation, notifications affordance, search, forms, detail-style panels, settings, report surfaces, empty/loading/error-friendly UI states, and working navigation.
- [x] CRM includes realistic professional-services demo records, lead search, create/edit/delete interactions, pipeline stages New, Contacted, Qualified, Proposal Sent, Negotiation, Won, Lost, stage movement, follow-up/task views, customer surfaces, reports, and local persistence.
- [x] Inventory includes realistic wholesale/distribution demo records, product management, stock-in and stock-out controls, supplier and purchase-order views, sales summary, warehouse views, alerts, reports, and local persistence.
- [x] ProjectFlow includes realistic construction/engineering demo records, project views, task views, workforce views, expense recording, milestones, client-portal presentation, reports, and local persistence.
- [x] All three applications have mobile-first layouts, collapsible navigation, responsive cards/tables, touch-friendly controls, and route manifests for `/`, `/login`, `/dashboard`, `/records`, `/reports`, and `/settings`.
- [x] White-label settings are represented in each application with editable company name, primary colour, secondary colour, and contact details persisted in the browser.
- [x] Independent Vercel deployment instructions and known limitations are documented.

## Open production outcomes

- [ ] Replace the browser-only local data adapter with an independent PHP 8 REST API and MySQL database for each application; enforce prepared statements, server-side validation, secure password hashing, CSRF protection where applicable, rate limiting, secure sessions, and backend role authorization.
- [ ] Implement real password reset, session management, protected API routes, staff roles and permissions, and client-portal access isolation in the production backend.
- [ ] Add real file storage and validated uploads for CRM documents, Inventory product images, and ProjectFlow documents.
- [ ] Add real CSV export generation, server-backed report queries, database migrations, independent seed/reset commands, and production error logging.
- [ ] Configure real custom domains, SSL, environment variables, deployment pipelines, and separate MySQL credentials after hosting decisions are supplied.
- [ ] Run the full functional/security/mobile acceptance suite against the production backend and record evidence; this testing build must not be presented as completion of those backend requirements.
