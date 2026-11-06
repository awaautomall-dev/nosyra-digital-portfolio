# Nosyra Digital Business Software Portfolio

This repository contains a Nosyra Digital landing page and three independent Next.js demo applications:

- `apps/landing` — the root launch page linking to all workspaces
- `apps/crm` — Nosyra CRM
- `apps/inventory` — Nosyra Inventory
- `apps/projectflow` — Nosyra ProjectFlow

The landing page and each app are separate deployables. Each app owns its own package manifest, frontend source, demo data, local persistence, database schema starting point, API notes, route manifest, and Vercel configuration.

All four services share Nosyra navy and teal. The workspace apps use a white wordmark on dark surfaces and the original logo on light surfaces. On mobile, each workspace shows four icon tabs—Dashboard, the main module, Reports, and More—with secondary pages grouped under More.

Each sign-in screen and authenticated workspace provides an **All workspaces** return link. The profile menu shows the demo identity and current workspace, with shortcuts to workspace settings and log out.

## Run locally

```bash
npm install --prefix apps/crm
npm install --prefix apps/inventory
npm install --prefix apps/projectflow
npm install --prefix apps/landing
npm run build
```

For interactive development, run `npm --prefix apps/landing run dev` for the landing page, or use the equivalent app folder, then open the Next.js URL.

## Deploy as one Vercel Services project

The root `vercel.json` configures the repository as a Vercel Services project. In Vercel, import this repository as **one project** and keep its **Root Directory at the repository root** (do not select one of the `apps/*` folders). Vercel Services must be available for the account/project. The root route serves the landing page, while each of the three app services builds from its own folder and uses a matching Next.js `basePath`:

- `/` — landing page with links to the workspaces
- `/crm` — CRM service
- `/inventory` — Inventory service
- `/projectflow` — ProjectFlow service

Each service is built independently with its own Next.js application. A push to the connected GitHub branch triggers a new grouped deployment. If Vercel reports that `services` is unsupported or unavailable, the account cannot use the one-project setup yet; use the four standalone projects below until Services is enabled. Do not deploy multiple app folders as Root Directories inside the same standard Vercel project.

## Deploy as four standalone Vercel projects

Alternatively, create four Vercel projects from this repository and set the matching **Root Directory**:

1. `apps/landing`
2. `apps/crm`
3. `apps/inventory`
4. `apps/projectflow`

Vercel should detect the Next.js runtime automatically. Use `npm run build` if prompted. The service configuration at the repository root is only needed for grouped Services deployment.

## Testing-build boundary

This version is intentionally optimized for immediate UI/workflow testing on Vercel. It stores demo records in browser localStorage and does not claim the requested production PHP 8/MySQL backend, real authentication, file storage, or multi-tenant data isolation. Each app documents the backend and deployment work still required in its own README.
