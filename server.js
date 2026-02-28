const express = require('express');

const app = express();
const port = process.env.PORT || 3000;

app.get('/', (_req, res) => {
  res.status(200).json({
    name: 'Universe',
    status: 'ok',
    message: 'Vercel-ready web app server is running'
  });
});

app.get('/health', (_req, res) => {
  res.status(200).send('healthy');
});

app.use((_req, res) => {
  res.status(404).json({ error: 'Not Found' });
});

if (require.main === module) {
  app.listen(port, () => {
    // eslint-disable-next-line no-console
    console.log(`Server listening on http://localhost:${port}`);
  });
}

module.exports = app;
