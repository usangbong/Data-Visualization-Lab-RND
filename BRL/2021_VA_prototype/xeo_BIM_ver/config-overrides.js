const apiMocker = require("connect-api-mocker"),
{ override,overrideDevServer,addWebpackModuleRule,addBabelPlugins,disableEsLint } = require("customize-cra");

const devServerConfig = () => config => {
return {
    ...config,
    before: (app,server)=> {
        //call cra before function to not break code
        config.before(app, server);
        //Then add our mocker url and folder 
        app.use(apiMocker('/api', 'mocks/api'));
    } 
}
}



module.exports = {
  webpack: override(
    // usual webpack plugin
    disableEsLint(),
    ...addBabelPlugins(
      "babel-plugin-react-scoped-css"
    ),
    addWebpackModuleRule({test: /\.(sc|c|sa)ss$/, use: [
      {
        loader: 'style-loader',
      },
      {
        loader: 'css-loader',
        options: {
          sourceMap: true,
          importLoaders: 2,
        },
      },
      { loader: 'scoped-css-loader' },
    ],})
  ),
  devServer: overrideDevServer(
    devServerConfig()
)
};