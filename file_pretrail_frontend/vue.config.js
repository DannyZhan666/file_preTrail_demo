const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: 'warning',
  configureWebpack: {
    cache: {
      type: 'filesystem',
    },
  },
  devServer: {
    hot: true,
    client: {
      overlay: false, // 将 overlay 移到 client 对象中
    },
  },
});