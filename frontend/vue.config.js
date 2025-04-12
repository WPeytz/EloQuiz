const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  publicPath: '/',
  outputDir: 'dist',
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        }
      }
    },
    client: {
      webSocketTransport: 'ws',
      webSocketURL: 'ws://localhost:5001/ws',
    },
    compress: false,
    historyApiFallback: true
  }
});