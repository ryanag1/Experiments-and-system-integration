function getHost(){
  //let domain;
  //let port;
  //if(process.env.NODE_ENV==="production")
//[domain, port] = process.env.VUE_APP_HOST.split(":");
  //else
//[domain, port] = process.env.VUE_APP_DEV_HOST.split(":");

  //if(port=="80" || port=="443")  return domain;
  //return "DOMAINNAME:80";
  
  //if(port=="80" || port=="443")  return domain;
  //else return "DOMAINNAME:80";
  return "DOMAINNAME";
}

module.exports = {
  publicPath: '/',
  devServer: {
      port: 80,
      public: getHost(),
  },
  outputDir: 'dist/dist',
  configureWebpack: {
      resolve: { symlinks: false },
      devtool: 'source-map',
      devServer: {
          watchOptions: {
              poll: true
          }
      },
  }
};
