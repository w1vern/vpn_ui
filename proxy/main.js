var http = require("http"), 
  httpProxy = require("http-proxy"); 
 
var frontProxy = new httpProxy.createProxyServer({ 
  target: { 
    host: "localhost", 
    port: 3000, 
  }, 
}); 
var backProxy = new httpProxy.createProxyServer({ 
  target: { 
    host: "localhost", 
    port: 8000, 
  }, 
}); 
var server = http.createServer(function (req, res) { 
  console.log(req.url); 
  if (req.url.startsWith("/api")) { 
    backProxy.web(req, res); 
  } else { 
    frontProxy.web(req, res); 
  } 
}); 
server.on("upgrade", function (req, socket, head) { 
  frontProxy.ws(req, socket, head); 
}); 
port = 8081
console.log(`listening on port ${port}`); 
server.listen(port);