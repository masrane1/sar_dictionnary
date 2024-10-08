const express = require('express');
const session = require('express-session');
const flash = require('connect-flash');
const path = require('path');
const mysql = require('mysql2');

const app = express();

// Configuration de la base de données
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'root',
  database: 'dictionary_db'
});

db.connect((err) => {
  if (err) {
    console.error('Erreur de connexion à la base de données :', err);
  } else {
    console.log('Connecté à la base de données MySQL');
  }
});

// Configuration du middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
  secret: 'votre_secret_ici',
  resave: false,
  saveUninitialized: true
}));
app.use(flash());

// Configuration du moteur de vue
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Routes
app.get('/', (req, res) => {
  const query = req.query.q;
  let sql = 'SELECT * FROM mots';
  let sqlParams = [];

  if (query) {
    sql += ' WHERE sig_mot_sar LIKE ? OR mot_sar LIKE ?';
    sqlParams = [`%${query}%`, `%${query}%`];
  }

  db.query(sql, sqlParams, (err, results) => {
    if (err) throw err;
    res.render('accueil', { mots: results, query: query, user: req.session.user });
  });
});

app.get('/mot/:id', (req, res) => {
  const motId = req.params.id;
  db.query('SELECT * FROM mots WHERE id = ?', [motId], (err, results) => {
    if (err) throw err;
    if (results.length > 0) {
      res.render('detail_mot', { mot: results[0], user: req.session.user });
    } else {
      res.status(404).send('Mot non trouvé');
    }
  });
});

app.get('/jeux', (req, res) => {
  db.query('SELECT * FROM mots ORDER BY RAND() LIMIT 4', (err, results) => {
    if (err) throw err;
    const mot = results[0];
    const choices = results.map(r => r.mot_sar);
    res.render('jeux', { mot: mot, choices: choices, user: req.session.user });
  });
});

app.post('/jeux', (req, res) => {
  // Logique pour vérifier la réponse et mettre à jour le score
  // À implémenter
});

app.get('/login', (req, res) => {
  res.render('login', { user: req.session.user, message: req.flash('error') });
});

app.post('/login', (req, res) => {
  // Logique de connexion à implémenter
});

app.get('/logout', (req, res) => {
  req.session.destroy((err) => {
    res.redirect('/');
  });
});

app.get('/profile', (req, res) => {
  if (!req.session.user) {
    return res.redirect('/login');
  }
  // Récupérer les informations de l'utilisateur depuis la base de données
  res.render('profile', { user: req.session.user });
});

// Routes d'administration
app.get('/admin', (req, res) => {
  if (!req.session.user || !req.session.user.isAdmin) {
    return res.redirect('/');
  }
  // Récupérer les statistiques pour le tableau de bord
  res.render('admin/dashboard', { user: req.session.user });
});

// Autres routes d'administration à implémenter

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Serveur en cours d'exécution sur le port ${PORT}`);
});