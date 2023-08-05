const ips = require('../ips.json');

function verifyUser(req, res, next) {
    const postData = req.body;

    let remoteAddress = req.connection.remoteAddress.split(':').pop();

    let username = postData.username || '';
    let password = postData.password || '';
    let version = postData.version || '';

    console.log(username)
    if (version == 'web') {
        next();
    } else {
        const result = Object.values(ips.jonyIps).includes(remoteAddress) ? 1 : 0;

        if (!result) {
            res.json({status: 400, message: 'Wrong ip adress.'});
        } else if (username != 'xxxxxx' || password != 'xxxxxx') {
            res.json({status: 400, message: 'Wrong username or password.'});
        } else {
            next();
        }
    }
}

function verifyPc(req, res, next) {
    let remoteAddress = req.connection.remoteAddress.split(':').pop();
    let pc = Object.keys(ips.jonyIps).find(ip => ips.jonyIps[ip] === remoteAddress);

    if (!pc) {
        res.json({status: 404});
    } else {
        next();
    }
}
  
module.exports = verifyUser, verifyPc;