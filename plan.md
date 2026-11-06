# Nosyra Digital Portfolio — Implementation Plan

## Delivery approach

This repository contains three independently deployable Next.js + React + TypeScript applications. Each product lives in its own folder with its own `package.json`, source tree, public route manifest, Vercel configuration, README, API notes, and database schema notes. They do not import code from one another and can be deployed as three separate Vercel projects.

This first delivery is a deployable product-demo MVP for rapid testing. It implements responsive dashboard experiences, realistic demo data, local CRUD-style interactions, role/demo-account presentation, pipeline or operational workflows, reporting surfaces, white-label settings, and browser local persistence. It intentionally does not claim to include the requested PHP 8/MySQL production backend, server-enforced authentication, real file storage, or production multi-tenancy. Those backend requirements are documented as the next implementation layer in each app's README and `backend/` notes.

## Project structure

- `apps/crm/`: Nosyra CRM, an independently deployable sales workspace.
- `apps/inventory/`: Nosyra Inventory, an independently deployable warehouse workspace.
- `apps/projectflow/`: Nosyra ProjectFlow, an independently deployable project and workforce workspace.
- Each app includes `src/main.tsx`, `src/styles.css`, `public/manus-routes.json`, `database/schema.sql`, `api/openapi.yaml`, `backend/README.md`, `README.md`, and `vercel.json`.
- Root documentation contains deployment instructions, implementation status, known limitations, and the execution plan.

## Design direction

Three candidate directions were considered:

- **Operational Atelier** (0.06): editorial B2B interfaces with strong typographic hierarchy and tactile data surfaces.
- **Signal Console** (0.04): dark, high-contrast command-center interfaces with glowing state cues.
- **Quiet Precision** (0.08): calm, spacious enterprise software with restrained accents and strong information density.

Chosen direction: **Operational Atelier**, interpreted distinctly per product. CRM uses navy, teal, and coral to signal relationships and deal momentum. Inventory uses deep forest, amber, and paper-like surfaces to feel physical and dependable. ProjectFlow uses plum, sky, and warm sand to make timelines and delivery progress feel collaborative rather than industrial.

### Shared principles

1. **Business context first:** each dashboard leads with an operational sentence, a clear next action, and database-shaped metrics rather than generic cards.
2. **Dense but breathable:** tables, pipelines, and activity feeds are compact enough for daily work while preserving hierarchy and touch-friendly spacing.
3. **State is visible:** status chips, progress bars, trend bars, and alerts communicate work health at a glance.
4. **Mobile is a first-class surface:** navigation collapses, tables become cards, controls remain at least 44px tall, and key workflows remain usable at narrow viewports.

### Typography and voice

The apps use a system sans stack for reliable Vercel rendering, with uppercase eyebrow labels, confident short headlines, and action copy that describes the business outcome: “Move the conversation forward”, “Protect stock availability”, and “Keep delivery visible”.

## Build and serving

Each app is a standalone Next.js Vercel build with `npm install` and `npm run build`; Vercel handles the Next.js output and route serving. The browser-side data layer uses localStorage so testers can create and edit records without a server. A future production layer should replace the local data adapter with a PHP 8 REST API and MySQL persistence, using the per-app SQL and OpenAPI starting points included here.
