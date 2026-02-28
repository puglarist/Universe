# Universe

Vercel-ready Node.js web app server using Express.

## Endpoints

- `GET /` returns app metadata and status JSON
- `GET /health` returns `healthy`

## Local development

```bash
npm install
npm run dev
```

Server runs on `PORT` if provided, otherwise `3000`.

## Deploy to Vercel

This repo includes `vercel.json` configured to route all requests to `server.js` using `@vercel/node`.
