const verifyUser = require('./verify.js');
const {queryAsync} = require('./utils.js')

const requestQueue = [];
let isProcessingQueue = false;

async function processQueue() {
    if (requestQueue.length === 0) {
        isProcessingQueue = false;
        return;
    }

    isProcessingQueue = true;
    const { connection, res, country} = requestQueue.shift();

    const selectQuery = `SELECT proxy_password FROM ${country}Proxies LIMIT 1`;
    const deleteQuery = `DELETE FROM ${country}Proxies WHERE proxy_password = ? LIMIT 1`;

    try {
        const results = await queryAsync(connection, selectQuery);

        if (results[0]) {
            const proxy = results[0].proxy_password;

            await queryAsync(connection, deleteQuery, [proxy]);

            res.json({status: 200, proxy});
        } else {
            res.json({status: 203, server, message: 'Not enough proxy.'});
        }
    } catch (error) {
        res.json({status: 500, error});
    }

    processQueue();
}

module.exports = (app, currentConnection) => {
    app.get('/proxy/:country', verifyUser, (req, res) => {
        let country = req.params.country || '';
        if (!['de', 'es', 'fr', 'gb', 'it', 'ro'].includes(country)) {
            res.json({status: 400, message: 'Wrong country.'});
        } else {
            let connection = currentConnection();
            requestQueue.push({connection, res, country});
            if (!isProcessingQueue) {
                processQueue();
            }
        }
    });
}