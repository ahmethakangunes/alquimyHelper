const {queryAsync} = require('../utils')
const verifyUser = require('../verify');
const verifyPc = require('../verify');
const ips = require('../ips');

const requestQueue = [];
let isProcessingQueue = false;

async function processQueue() {
    console.log(requestQueue.length)
    if (requestQueue.length === 0) {
        isProcessingQueue = false;
        return;
    }

    isProcessingQueue = true;
    const {connection, req, res, server, flag, tableName} = requestQueue.shift();

    const selectColumns = 'mail, password, username, proxy, cor_count, first_run, sage_last_auth' + (server === '4' ? ', 2fa' : '') + ', alquimy_character';
    const selectQuery = `SELECT ${selectColumns} FROM ${tableName} WHERE flag=${flag} AND run_status=0 AND alquimy_status=0 AND locked=0 LIMIT 1 FOR UPDATE`;
    const updateQuery = `UPDATE ${tableName} SET run_status=1, start_time=NOW(), run_pc=?, locked=1 WHERE mail=? LIMIT 1`;

    try {
        const results = await queryAsync(connection, selectQuery);

        if (results[0]) {
            let resultInfo = results;
            const mail = results[0].mail;

            let remoteAddress = req.connection.remoteAddress.split(':').pop();
            let pc = Object.keys(ips.jonyIps).find(ip => ips.jonyIps[ip] === remoteAddress);

            await queryAsync(connection, updateQuery, [pc, mail]);

            res.json({status: 200, slotInfo: resultInfo});
        } else {
            res.json({status: 203, server, message: 'Not enough accounts for the server.'});
        }
    } catch (error) {
        res.json({status: 500, error});
    }

    processQueue();
}

module.exports = (app, currentConnection) => {
    app.get('/needRunSlots', verifyUser, verifyPc, (req, res) => {
        const postData = req.body;

        let server = postData.server || '';
        let flag = postData.flag || '';

        let tableName = '';

        if (!server || server === '8') {
            tableName = 'gerAccounts';
        } else if (server === '7') {
            tableName = 'teuAccounts';
        } else if (server === '5') {
            tableName = 'italyAccounts';
        } else if (server === '4') {
            tableName = 'iberiaAccounts';
        } else if (server === '3') {
            tableName = 'polskaAccounts';
        }

        if (!flag) {
            res.json({ status: 500, error: 'Invalid server value' });
        } else {
            let connection = currentConnection();
            requestQueue.push({connection, req, res, server, flag, tableName});
            if (!isProcessingQueue) {
                processQueue();
            }
        }
    });

}