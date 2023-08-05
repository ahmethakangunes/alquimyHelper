const patternNumber = /^\d+$/;
const fetch = require('node-fetch');
const ips = require('../ips.json');

module.exports = (app) => {
    app.get('/anil/:id', (req, res) => {
        let id = patternNumber.test(req.params.id) ? req.params.id : -1;
        let key = ips.anilIps[id] || null;
    
        if (!key) {
            res.json({status: 404, message: 'PC NOT FOUND.'});
        } else {
            const apiUrl = `http://${key}:xxxx`;
            const params = {
                method: 'GET',
            };
    
            fetch(apiUrl, params)
            .then(response => response.json())
            .then(data => {res.send(({status: 200, message: data}))})
            .catch(error => res.send({status: 404, error: error}));   
        }
    });

    app.get('/pc/:id', (req, res) => {
        let id = patternNumber.test(req.params.id) ? req.params.id : -1;
        let key = ips.jonyIps[id] || null;
    
        if (!key) {
            res.json({status: 404, message: 'PC NOT FOUND.'});
        } else {
            const apiUrl = `http://${key}:xxxx`;
            const params = {
                method: 'GET',
            };
    
            fetch(apiUrl, params)
            .then(response => response.json())
            .then(data => {res.send(({status: 200, message: data}))})
            .catch(error => res.send({status: 404, error: error}));   
        }
    });
}