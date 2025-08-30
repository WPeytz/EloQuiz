const { defineConfig } = require('@vue/cli-service');

// Allow overriding the dev proxy target via env when needed:
// e.g. VUE_APP_API_PROXY=https://adaptivelearning-backend-xxxxxxxxxxx.europe-west1.run.app
const BACKEND_TARGET = process.env.VUE_APP_API_PROXY || 'http://localhost:5001';

process.env.WS_NO_PER_MESSAGE_DEFLATE = '1';

module.exports = defineConfig({
  publicPath: '/',           // correct asset base for Cloud Run at domain root
  outputDir: 'dist',
  filenameHashing: true,
  productionSourceMap: false,
  // Keep default js/css subfolders; removing custom assetsDir avoids path mismatches
  devServer: {
    webSocketServer: {
      options: {
        perMessageDeflate: false
      }
    },
    proxy: {
      '^/api': {
        target: BACKEND_TARGET,
        changeOrigin: true,
        ws: true,
        // no pathRewrite needed; keep /api as-is
      },
    },
    historyApiFallback: true, // SPA routing in dev
    compress: false,
  },
});