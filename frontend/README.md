React + Vite frontend

Build & deploy into the existing FastAPI static folder:

1. Install

```bash
cd frontend
npm install
```

2. Development

```bash
npm run dev
```

3. Build for production (this will output files directly to `app/static`):

```bash
npm run build
```

After `npm run build`, start the FastAPI server and the new SPA will be available at `/`.
