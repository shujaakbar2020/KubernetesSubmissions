const express = require('express');

const app = express();
const port = 8080;

app.get('/', (req, res) => {
  // mluukkai/hello:1 responds with "Hello, World!"
  // mluukkai/hello:2 responds with "Hello, New World!"
  res.send('Hello, World v2.'); 
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
