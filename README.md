# Nosyra Digital Business Software Portfolio

This repository contains three independent Next.js demo applications for Nosyra Digital:

- `apps/crm` — Nosyra CRM
- `apps/inventory` — Nosyra Inventory
- `apps/projectflow` — Nosyra ProjectFlow

They are intentionally separate deployables. Each app owns its own package manifest, frontend source, demo data, local persistence, database schema starting point, API notes, route manifest, and Vercel configuration.

## Run locally

```bash
npm install --prefix apps/crm
npm install --prefix apps/inventory
npm install --prefix apps/projectflow
npm run build
```

For interactive development, run `npm --prefix apps/crm run dev` (or the equivalent app folder) and open the Next.js URL.

## Deploy as one Vercel Services project

The root `vercel.json` configures the repository as a Vercel Services project. In Vercel, import this repository as **one project** and keep its **Root Directory at the repository root** (do not select one of the `apps/*` folders). Vercel Services must be available for the account/project. Each service builds from its own app folder and has a matching Next.js `basePath`, so pages and static assets remain under that service's route:

- `/crm` — CRM service
- `/inventory` — Inventory service
- `/projectflow` — ProjectFlow service

Each service is built independently with its own Next.js application. A push to the connected GitHub branch triggers a new grouped deployment. If Vercel reports that `services` is unsupported or unavailable, the account cannot use the one-project setup yet; use the three standalone projects below until Services is enabled. Do not deploy all three app folders as three Root Directories inside the same standard Vercel project.

## Deploy as three standalone Vercel projects

Alternatively, create three Vercel projects from this repository and set the matching **Root Directory**:

1. `apps/crm`
2. `apps/inventory`
3. `apps/projectflow`

Vercel should detect the Next.js runtime automatically. Use `npm run build` if prompted. The service configuration at the repository root is only needed for grouped Services deployment.

## Testing-build boundary

This version is intentionally optimized for immediate UI/workflow testing on Vercel. It stores demo records in browser localStorage and does not claim the requested production PHP 8/MySQL backend, real authentication, file storage, or multi-tenant data isolation. Each app documents the backend and deployment work still required in its own README.
