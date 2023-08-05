const verifyUser = require('./verify.js');
const verifyPc = require('./verify.js')
const ips = require('../ips.json');
const patternNumber = /^\d+$/;

module.exports = (app, currentConnection) => {
    app.put('/alquimyUpgradeDone', verifyUser, verifyPc, (req, res) => {
        let connection = currentConnection();

        const postData = req.body;

        let mail = postData.mail || '';
        let server = postData.server || '';

        if (!mail) {
            res.json({status: 203, message: 'Mail not found.'});
        } else if (!server || !['8', '7', '5', '4'].includes(server)) {
            res.json({status: 203, message: 'server not found.'});
        } else {
            if (server == '8') {
                tableName = 'gerAccounts';
            } else if (server == '7') {
                tableName = 'teuAccounts';
            } else if (server == '5') {
                tableName = 'italyAccounts';
            } else if (server == '4') {
                tableName = 'iberiaAccounts';
            } else if (server === '3') {
                tableName = 'polskaAccounts';
            }

            connection.query(`UPDATE ${tableName} SET setting='', run_pc=0, run_status=0, run_slot=0, end_time=NOW(), alquimy_status=1, alquimy_last_up=NOW(), wait_transfer=1, cor_count=0, first_run=0, locked=0 WHERE mail=? LIMIT 1`, [mail], (error, results) => {
                if (error) {
                    res.json({status: 500, error});
                } else {
                    res.json({status: 200});
                }
            });
        }
    });

    app.put('/alquimyStartSlot', verifyUser, verifyPc, (req, res) => {
        let connection = currentConnection();

        const postData = req.body;

        let mail = postData.mail || '';
        let server = postData.server || '';

        let remoteAddress = req.connection.remoteAddress.split(':').pop();
        let pc = Object.keys(ips.jonyIps).find(ip => ips.jonyIps[ip] === remoteAddress);

        if (server == '8') {
            tableName = 'gerAccounts';
        } else if (server == '7') {
            tableName = 'teuAccounts';
        } else if (server == '5') {
            tableName = 'italyAccounts';
        } else if (server == '4') {
            tableName = 'iberiaAccounts';
        } else if (server === '3') {
            tableName = 'polskaAccounts';
        }

        connection.query(`UPDATE ${tableName} SET run_pc=?, run_status=1 WHERE mail=? LIMIT 1`, [pc, mail], (error, results) => {
            if (error) {
                res.json({status: 500, error});
            } else {
                res.json({status: 200});
            }
        });
    });

    app.put('/updateSageInfos', verifyUser, verifyPc, (req, res) => {
        let connection = currentConnection();

        const postData = req.body;
        let mail = postData.mail || '';
        let server = postData.server || '';
        let setting = postData.setting || '';
        let channel = postData.channel || '';
        let runStatus = postData.runStatus || '';
        let runSlot = postData.runSlot || '';
        let proxy = postData.proxy || '';
        let lastAuth = postData.lastAuth || '';
        let twoFactor = postData.twoFactor || '';
        let alquimyCharacter = postData.alquimyCharacter || '';

        let remoteAddress = req.connection.remoteAddress.split(':').pop();
        let pc = Object.keys(ips.jonyIps).find(ip => ips.jonyIps[ip] === remoteAddress);

        if (!mail) {
            res.json({status: 404, message: 'mail', runSlot});
        } else if (!server || !['8', '7', '5', '4'].includes(server)) {
            res.json({status: 404, message: 'server', runSlot});
        } else {
            if (server == '8') {
                tableName = 'gerAccounts';
            } else if (server == '7') {
                tableName = 'teuAccounts';
            } else if (server == '5') {
                tableName = 'italyAccounts';
            } else if (server == '4') {
                tableName = 'iberiaAccounts';
            } else if (server === '3') {
                tableName = 'polskaAccounts';
            }

            if (server == '4') {
                connection.query(`UPDATE ${tableName} SET run_pc=?, run_status=?, run_slot=?, channel=?, setting=?, proxy=?, sage_last_auth=?, alquimy_character=?, 2fa=? WHERE mail=? LIMIT 1`, [pc, runStatus, runSlot, parseInt(channel) + 1, setting, proxy, lastAuth, alquimyCharacter, twoFactor, mail], (error, results) => res.json({status: 200}));
            } else {
                connection.query(`UPDATE ${tableName} SET run_pc=?, run_status=?, run_slot=?, channel=?, setting=?, proxy=?, sage_last_auth=?, alquimy_character=? WHERE mail=? LIMIT 1`, [pc, runStatus, runSlot, parseInt(channel) + 1, setting, proxy, lastAuth, alquimyCharacter, mail], (error, results) => res.json({status: 200}));
            }
        }
    });

    app.put('/startSlot', verifyUser, verifyPc, (req, res) => {
        let connection = currentConnection();

        const postData = req.body;

        let mail = postData.mail || '';
        let server = postData.server || '';

        let remoteAddress = req.connection.remoteAddress.split(':').pop();
        let pc = Object.keys(ips.jonyIps).find(ip => ips.jonyIps[ip] === remoteAddress);

        if (server == '8') {
            tableName = 'gerAccounts';
        } else if (server == '7') {
            tableName = 'teuAccounts';
        } else if (server == '5') {
            tableName = 'italyAccounts';
        } else if (server == '4') {
            tableName = 'iberiaAccounts';
        } else if (server === '3') {
            tableName = 'polskaAccounts';
        }

        connection.query(`UPDATE ${tableName} SET run_pc=?, run_status=1, start_time=NOW(), end_time=NULL WHERE mail=? LIMIT 1`, [pc, mail], (error, results) => {
            if (error) {
                res.json({status: 500, error});
            } else {
                res.json({status: 200});
            }
        });
    });

    app.put('/stopSlot', verifyUser, verifyPc, (req, res) => {
        let connection = currentConnection();

        const postData = req.body;

        let mail = postData.mail || '';
        let server = postData.server || '';

        if (!mail) {
            res.json({status: 404});
        } else if (!server || !['8', '7', '5', '4'].includes(server)) {
            res.json({status: 404});
        } else {
            if (server == '8') {
                tableName = 'gerAccounts';
            } else if (server == '7') {
                tableName = 'teuAccounts';
            } else if (server == '5') {
                tableName = 'italyAccounts';
            } else if (server == '4') {
                tableName = 'iberiaAccounts';
            } else if (server === '3') {
                tableName = 'polskaAccounts';
            }

            connection.query(`UPDATE ${tableName} SET run_pc=0, run_status=0, run_slot=0, channel=0, start_time=NULL, end_time=NULL, locked=0 WHERE mail=? LIMIT 1`, [mail], (error, results) => {
                if (error) {
                    res.json({status: 500, error});
                } else {
                    res.json({status: 200});
                }
            });
        }
    });

    app.put('/stopDoneSlot', verifyUser, verifyPc, (req, res) => {
        let connection = currentConnection();

        const postData = req.body;

        let mail = postData.mail || '';
        let server = postData.server || '';
        let totalCorCount = postData.totalCorCount || 0;

        if (!mail) {
            res.json({status: 203, message: 'Mail not found.'});
        } else if (!server || !['8', '7', '5', '4'].includes(server)) {
            res.json({status: 203, message: 'server not found.'});
        } else {
            if (server == '8') {
                tableName = 'gerAccounts';
            } else if (server == '7') {
                tableName = 'teuAccounts';
            } else if (server == '5') {
                tableName = 'italyAccounts';
            } else if (server == '4') {
                tableName = 'iberiaAccounts';
            } else if (server === '3') {
                tableName = 'polskaAccounts';
            }

            connection.query(`UPDATE ${tableName} SET run_pc=0, run_status=0, run_slot=0, end_time=NOW(), alquimy_status=1, cor_count=?, locked=0 WHERE mail=? LIMIT 1`, [totalCorCount, mail], (error, results) => {
                if (error) {
                    res.json({status: 500, error});
                } else {
                    res.json({status: 200});
                }
            });
        }
    });

    app.put('/stopBannedSlot', verifyUser, verifyPc, (req, res) => {
        let connection = currentConnection();

        const postData = req.body;

        let mail = postData.mail || '';
        let server = postData.server || '';

        if (!mail) {
            res.json({status: 404});
        } else {
            if (server == '8') {
                tableName = 'gerAccounts';
            } else if (server == '7') {
                tableName = 'teuAccounts';
            } else if (server == '5') {
                tableName = 'italyAccounts';
            } else if (server == '4') {
                tableName = 'iberiaAccounts';
            } else if (server === '3') {
                tableName = 'polskaAccounts';
            }

            connection.query(`SELECT flag, mail, password, username, channel, setting FROM ${tableName} WHERE mail=? LIMIT 1`, [mail], (error, results) => {
                if (error) {
                    res.json({status: 500, error});
                } else {
                    if (results.length > 0) {
                        connection.query("INSERT INTO bannedSlots (server, flag, mail, password, username, channel, setting, banned_time) VALUES (?, ?, ?, ?, ?, ?, ?, NOW())", [server, results[0].flag, results[0].mail, results[0].password, results[0].username, results[0].channel, results[0].setting], (error, results) => {
                            if (error) {
                                res.json({status: 500, error});
                            } else {
                                connection.query(`DELETE FROM ${tableName} WHERE mail=? LIMIT 1`, [mail], (error, results) => res.json({status: 200}));
                            }
                        });
                    } else {
                        res.json({status: 200});
                    }
                }
            });
        }
    });

    app.put('/changeClientError', verifyUser, verifyPc, (req, res) => {
        let connection = currentConnection();

        const postData = req.body;

        let mail = postData.mail || '';
        let server = postData.server || '';

        if (!mail) {
            res.json({status: 404});
        } else {
            if (server == '8') {
                tableName = 'gerAccounts';
            } else if (server == '7') {
                tableName = 'teuAccounts';
            } else if (server == '5') {
                tableName = 'italyAccounts';
            } else if (server == '4') {
                tableName = 'iberiaAccounts';
            } else if (server === '3') {
                tableName = 'polskaAccounts';
            }

            if (server == '4') {
                connection.query(`SELECT flag, mail, password, username, 2fa twoFactor FROM iberiaAccounts WHERE mail=? LIMIT 1`, [mail], (error, results) => {
                    if (error) {
                        res.json({status: 500, error});
                    } else {
                        if (results.length > 0) {
                            connection.query("INSERT INTO cl_error (server, flag, mail, password, username, error_time, 2fa) VALUES (?, ?, ?, ?, ?, NOW(), ?) LIMIT 1", [server, results[0].flag, results[0].mail, results[0].password, results[0].username, results[0].twoFactor], (error, results) => {
                                if (error) {
                                    res.json({status: 500, error});
                                } else {
                                    connection.query(`DELETE FROM iberiaAccounts WHERE mail=? LIMIT 1`, [mail], (error, results) => res.json({status: 200}));
                                }
                            });
                        } else {
                            res.json({status: 200});
                        }
                    }
                });
            } else {
                connection.query(`SELECT flag, mail, password, username FROM ${tableName} WHERE mail=?`, [mail], (error, results) => {
                    if (error) {
                        res.json({status: 500, error});
                    } else {
                        connection.query("INSERT INTO cl_error (server, flag, mail, password, username, error_time, 2fa) VALUES (?, ?, ?, ?, ?, NOW(), '')", [server, results[0].flag, results[0].mail, results[0].password, results[0].username], (error, results) => {
                            if (error) {
                                res.json({status: 500, error});
                            } else {
                                if (results.length > 0) {
                                    connection.query(`DELETE FROM ${tableName} WHERE mail=?`, [mail], (error, results) => res.json({status: 200}));
                                } else {
                                    res.json({status: 200});
                                }
                            }
                        });
                    }
                });
            }
        }
    });

    app.post('/saveSlotInfos', verifyUser, verifyPc, (req, res) => {
        let connection = currentConnection();

        const postData = req.body;

        let newMail = postData.newMail || '';
        let newPassword = postData.newPassword || '';
        let newUsername = postData.newUsername || '';
        let server = postData.server || '';
        let flag = postData.flag || '';
        let proxy = postData.proxy || '';
        let lastAuth = postData.lastAuth || '';
        let alquimyCharacter = postData.alquimyCharacter || '';

        if (server == '8') {
            tableName = 'gerAccounts';
        } else if (server == '7') {
            tableName = 'teuAccounts';
        } else if (server == '5') {
            tableName = 'italyAccounts';
        } else if (server === '3') {
            tableName = 'polskaAccounts';
        }

        if (server == '4') {
            let twoFactor = postData.twoFactor || '';
            connection.query(`INSERT INTO iberiaAccounts (flag, mail, password, username, setting, run_pc, run_status, run_slot, channel, start_time, end_time, alquimy_status, cor_count, proxy, sage_last_auth, 2fa, alquimy_character, first_run, locked) VALUES (?, ?, ?, ?, '', 0, 0, 0, 0, NULL, NULL, 0, 0, ?, ?, ?, ?, 1, 0)`, [flag, newMail, newPassword, newUsername, proxy, lastAuth, twoFactor, alquimyCharacter], (error, results) => {
                if (error) {
                    res.json({status: 500, error});
                } else {
                    res.json({status: 200});
                }
            });
        } else {
            connection.query(`INSERT INTO ${tableName} (flag, mail, password, username, setting, run_pc, run_status, run_slot, channel, start_time, end_time, alquimy_status, cor_count, proxy, sage_last_auth, alquimy_character, first_run, locked) VALUES (?, ?, ?, ?, '', 0, 0, 0, 0, NULL, NULL, 0, 0, ?, ?, ?, 1, 0)`, [flag, newMail, newPassword, newUsername, proxy, lastAuth, alquimyCharacter], (error, results) => {
                if (error) {
                    res.json({status: 500, error});
                } else {
                    res.json({status: 200});
                }
            });
        }
    });

    app.get('/getAlquimySlots', verifyUser, (req, res) => {
        let connection = currentConnection();

        let slotInfos = []

        let remaining = 4
        let complete = () => {
            remaining--;
            if (remaining == 0) {
                res.json({status: 200, slotInfos});
            }
        }

        let tableNames = ['gerAccounts', 'teuAccounts', 'iberiaAccounts', 'italyAccounts', 'polskaAccounts'];
        let servers = {
            gerAccounts: 8,
            teuAccounts: 7,
            iberiaAccounts: 4,
            italyAccounts: 5,
        };

        tableNames.forEach(tableName => {
            let selectColumns = tableName === 'iberiaAccounts'
                ? 'flag, mail, password, username, proxy, sage_last_auth, 2fa, alquimy_character'
                : 'flag, mail, password, username, proxy, sage_last_auth, alquimy_character';

            connection.query(`SELECT ${selectColumns} FROM ${tableName} WHERE run_status=0 AND wait_transfer=1`, [], (error, results) => {
                if (error) {
                    res.json({ status: 500, error });
                } else if (results.length > 0) {
                    results.forEach(slotInfo => {
                        slotInfo.server = servers[tableName];
                        slotInfos.push(slotInfo);

                        const { mail } = slotInfo;

                        connection.query(`UPDATE ${tableName} SET wait_transfer=0 WHERE mail=?`, [mail], (error, results) => {});
                    });
                }
                complete();
            });
        });
    });

    app.get('/pcRunInfo/:pc', verifyUser, (req, res) => {
        let connection = currentConnection();

        let pc = patternNumber.test(req.params.pc) ? req.params.pc : -1;
        let key = ips.jonyIps[pc] || null;
        let pcInfos = []

        if (!key) {
            res.json({status: 203, message: 'PC NOT FOUND.'});
        } else {
            let remaining = 4
            let complete = () => {
                remaining--;
                if (remaining == 0) {
                    res.json({status: 200, pcInfos});
                }
            }

            let tableNames = ['gerAccounts', 'teuAccounts', 'iberiaAccounts', 'italyAccounts', 'polskaAccounts'];

            tableNames.forEach(tableName => {
                connection.query(`SELECT mail, run_slot, channel, DATE_ADD(start_time, INTERVAL 1 HOUR) start_time, cor_count FROM ${tableName} WHERE run_pc=? AND run_status=1`, [pc], (error, results) => {
                    if (error) {
                        res.json({status: 500, error});
                    } else if (results.length > 0) {
                        results.forEach(slotInfo => {
                            slotInfo.server = tableName
                            pcInfos.push(slotInfo);
                        });
                    }
                    complete();
                });
            });
        }
    });

    app.put('/resetAllSlot', verifyUser, verifyPc, (req, res) => {
        let connection = currentConnection();

        let remoteAddress = req.connection.remoteAddress.split(':').pop();
        let pc = Object.keys(ips.jonyIps).find(ip => ips.jonyIps[ip] === remoteAddress);

        connection.query("UPDATE gerAccounts SET setting='', run_pc=0, run_status=0, run_slot=0, channel=0, start_time=NULL, end_time=NULL, locked=0 WHERE run_pc=?", [pc], (error, result) => {});
        connection.query("UPDATE iberiaAccounts SET setting='', run_pc=0, run_status=0, run_slot=0, channel=0, start_time=NULL, end_time=NULL, locked=0 WHERE run_pc=?", [pc], (error, result) => {});
        connection.query("UPDATE italyAccounts SET setting='', run_pc=0, run_status=0, run_slot=0, channel=0, start_time=NULL, end_time=NULL, locked=0 WHERE run_pc=?", [pc], (error, result) => {});
        connection.query("UPDATE teuAccounts SET setting='', run_pc=0, run_status=0, run_slot=0, channel=0, start_time=NULL, end_time=NULL, locked=0 WHERE run_pc=?", [pc], (error, result) => {});
        connection.query("UPDATE polskaAccounts SET setting='', run_pc=0, run_status=0, run_slot=0, channel=0, start_time=NULL, end_time=NULL, locked=0 WHERE run_pc=?", [pc], (error, result) => {});
        res.json({status: 200})
    });
}