const express = require('express');
const fs = require('fs');
const path = require('path');
const multer = require('multer');
const { exec } = require('child_process');
const app = express();
const PORT = 5500;

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'files'); // Carpeta donde se guardarán los archivos
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname); // Mantener el nombre original del archivo
    }
});

const upload = multer({ storage: storage });

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'inicio.html'));
});

app.get('/clientes', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'clientes.html'));
});

app.get('/files', (req, res) => {
    const directoryPath = path.join(__dirname, 'files');
    function getFilesRecursively(dir, fileList = []) {
        const files = fs.readdirSync(dir);
        files.forEach(file => {
            const filePath = path.join(dir, file);
            if (file === '.DS_Store') return;
            if (fs.statSync(filePath).isDirectory()) {
                fileList.push({
                    name: file, // Mostrar solo el nombre del directorio
                    type: 'directory',
                    children: getFilesRecursively(filePath),
                    path: path.relative(directoryPath, filePath) // Mantener la ruta relativa para acceso
                });
            } else {
                fileList.push({
                    name: file, // Mostrar solo el nombre del archivo
                    type: 'file',
                    path: path.relative(directoryPath, filePath) // Mantener la ruta relativa para acceso
                });
            }
        });
        return fileList;
    }
    const files = getFilesRecursively(directoryPath);
    res.json(files);
});

app.get('/file', (req, res) => {
    const filePath = path.join(__dirname, 'files', req.query.name);
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error('Error reading file:', err);
            return res.status(500).send('Unable to read file');
        }
        res.send(data);
    });
});

app.post('/upload', upload.single('file'), (req, res) => {
    res.status(200).send('File uploaded successfully');
});

app.post('/execute', (req, res) => {
    const command = 'python D:/Clases/InteligenciaArtificial/Practicas/Prueba2/TextToText.py D:/Clases/InteligenciaArtificial/Practicas/Prueba2/entrada.txt'; // Comando predefinido
    exec(command, (error, stdout, stderr) => {
        console.log(`Command output: ${stdout}`);
        res.send('Command executed successfully');
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
