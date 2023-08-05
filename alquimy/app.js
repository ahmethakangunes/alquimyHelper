const express = require('express');
const verifyUser = require('./verify');
const app = express();
const port = 2424;

app.use(express.json());

const {createPool, currentConnection} = require('./mysql');
createPool();

require('./autoStart')(app, currentConnection);
require('./app/needRunSlot')(app, currentConnection);
require('./proxy')(app, currentConnection);
require('./patcher')(app);
require('./anil')(app);

app.post('/login', verifyUser, (req, res) => {
    res.json({status: 200})
});

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
});