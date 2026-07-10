const http = require('http');

const server = http.createServer((req, res) => {
  res.setHeader('Content-Type', 'application/json');

  if (req.url === '/hello') {
    res.end(JSON.stringify({ message: "Hello, world!" }));
  } else if (req.url === '/status') {
    res.end(JSON.stringify({ status: "online", timestamp: new Date() }));
  } else {
    res.statusCode = 404;
    res.end(JSON.stringify({ error: "Not found" }));
  }
});

server.listen(3000, () => console.log('Server running at http://localhost:3000'));