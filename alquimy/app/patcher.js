const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const multer = require('multer');
const verifyUser = require('./verify.js');

let uploadStatus = false;

module.exports = (app) => {
    const storage = multer.diskStorage({
        destination: '/root/alquimy/programs',
        filename: (req, file, cb) => {
          cb(null, file.originalname);
        }
    });

    const upload = multer({ storage: storage });

    function calculateHash(filePath) {
        return new Promise((resolve, reject) => {
            const hash = crypto.createHash('sha256');
      
            const stream = fs.createReadStream(filePath);
                stream.on('data', (chunk) => {
                hash.update(chunk);
            });
    
            stream.on('end', () => {
                const fileHash = hash.digest('hex');
                resolve(fileHash);
            });
    
            stream.on('error', (error) => {
                reject(error);
            });
        });
    }

    const verifyShaMiddleware = (req, res, next) => {
        const expectedSha = 'ef080de3e0a90730f51a9f597d6495416ad80684c8abb135834fbd868bfbdc33';
        const uploadSha = req.header('uploadSha');
      
        if (uploadSha == expectedSha) {
            next();
        } else {
            res.status(400).json();
        }
    };

    const uploadSingle = (req, res, next) => {
        uploadStatus = true
        upload.single('file')(req, res, (error) => {
            if (error) {
                res.status(400).json();
            } else {
                next();
            }
        });
    };

    app.post('/upload', verifyShaMiddleware, uploadSingle, (req, res) => { 
        uploadStatus = false
        res.status(200).json({ message: 'File uploaded successfully!' });
    });

    app.post('/patcher', verifyUser, (req, res) => {
        if (uploadStatus) {
            res.status(503).json({ message: 'Please wait, an upload is in progress' });
        } else {
            const postData = req.body;
    
            let version = postData.version || '';
            let downloadProgramName = postData.downloadProgramName || '';
        
            if (version != '2.4') {
                res.json({status: 203, message: 'Please use the updated version'});
            } else {
                if (!downloadProgramName) {
                    let programInfos = []
                    let remaining = 0;
                    let complete = () => {
                        remaining--;
                        if (remaining == 0) {
                            res.json({status: 200, programInfos})
                        }
                    }
            
                    const folderPath = './programs';
                    fs.readdir(folderPath, (error, folders) => {
                        if (error) {
                            res.json({status: 400, message: error});
                        } else if (!folders.length) {
                            res.json({status: 200, programInfos: []});
                        } else {
                            remaining += folders.length;
                            folders.forEach((programName) => {
                                let programPath = path.join(folderPath, programName);
                                calculateHash(programPath).then(programHash => {
                                    programInfos.push({programName, programHash});
                                    complete();
                                }).catch((error) => {
                                    res.json({status: 400, error});
                                    return
                                });;
                            });
                        }
                    });
                } else {
                    const filePath = path.join('./programs', downloadProgramName);
                    fs.readFile(filePath, (error, data) => {
                        if (error) {
                            res.json({status: 400, error});
                            return
                        } else {
                            res.setHeader('Content-disposition', `attachment; filename=${downloadProgramName}`);
                            res.setHeader('Content-type', 'application/octet-stream');
                            res.send(data);
                        }
                    });
                }
            }
        }
    });
}