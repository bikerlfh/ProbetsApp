
const createProxyMiddleware  = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'https://559315232fd4.ngrok.io',
      changeOrigin: true,
      router: {
        // when request.headers.host == 'dev.localhost:3000',
        // override target 'http://www.example.org' to 'http://localhost:8000'
        'localhost:3000': 'http://localhost:8000',
      },
    })
  );
};