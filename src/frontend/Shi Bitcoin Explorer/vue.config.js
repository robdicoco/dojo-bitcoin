module.exports = {
  devServer: {
    proxy: {
      '/': {
        target: 'http://172.236.149.45:5000',
        changeOrigin: true,
        pathRewrite: { '^/': '' },
      },
    },
  },
}
