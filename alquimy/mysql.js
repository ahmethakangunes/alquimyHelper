const mysql = require('mysql2');

let connection;

function createPool() {
    connection = mysql.createPool({
        host: '127.0.0.1',
        user: 'xxxxxx',
        password: 'xxxxxxx',
        database: 'xxxxxx',
        connectionLimit: 200
    });

    connection.getConnection(error => {
        if (error) {
            setTimeout(createPool, 2000);
        }
    });
}

function currentConnection() {
    return connection;
}

module.exports = {createPool, currentConnection};