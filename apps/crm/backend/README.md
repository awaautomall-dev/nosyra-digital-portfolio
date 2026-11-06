# Nosyra CRM backend boundary

The Vercel-ready testing build intentionally keeps records in the browser so the user can test the interface immediately. The production implementation should replace this adapter with an independent PHP 8 REST API and MySQL database for Nosyra CRM.

Required next layer: password hashing and reset flow, secure session cookies, backend-enforced roles, prepared SQL statements, server-side validation, CSRF protection where applicable, rate limiting, structured error logging, uploads backed by object storage, database-backed reports, seed/reset commands, and isolated deployment configuration. Do not treat the current frontend demo as a secure production backend.
