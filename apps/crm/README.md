# Nosyra CRM

Nosyra CRM is an independent Nosyra Digital testing application for customer relationship management. It has its own package, frontend source, public route manifest, Vercel configuration, demo identity, and browser-persisted sample records.

## Run

```bash
npm install
npm run dev
```

## Deploy to Vercel

Import the repository into Vercel and set the project root directory to `apps/crm`. Use `npm run build` and `dist` if Vercel does not auto-detect the Next.js defaults.

## Demo access

The login page includes fictional role accounts for safe walkthroughs. No real credentials are required. Records created or changed in this testing build are stored in the current browser's localStorage. Use the browser's site data controls to reset the demo.

## Testing-build limitation

This is a frontend testing build. It does not claim production authentication, a PHP 8 REST API, MySQL persistence, server-side authorization, validated file storage, rate limiting, or multi-tenant isolation. See `backend/README.md`, `database/schema.sql`, and `api/openapi.yaml` for the production starting points to implement next.
