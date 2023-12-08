const express = require('express');
const path = require('path');
const app = express();
const port = 3000; // Port sur lequel le serveur écoutera


// Route simple pour la page d'accueil
const publicPath = path.join(__dirname, '..');
app.use(express.static(publicPath));
app.get('/', (req, res) => {
    res.sendFile(path.join(publicPath, 'index.html'));
});

// Démarrer le serveur
app.listen(port, () => {
    console.log(`Le serveur est lancé sur le port ${port}`);
});
