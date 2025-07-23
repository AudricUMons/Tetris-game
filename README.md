# 🎮 Tetris – Version Python & Web

Ce projet contient deux versions du jeu **Tetris** :

1. 🐍 Une version **Python/Pygame** optimisée et modulaire
2. 🌐 Une version **HTML/JavaScript** jouable en ligne via GitHub Pages

---

## 📁 Structure du projet

```
Tetris_game/
├── main.py                    # Lancement de la version Python
├── requirements.txt           # Dépendances Python
├── README.md                  # Ce fichier
├── assets/                    # Sons du jeu (WAV)
│   ├── rotate.wav
│   ├── place.wav
│   ├── clear.wav
│   └── gameover.wav
├── tetris/                    # Logique interne du Tetris Python
│   ├── __init__.py
│   ├── core.py
│   ├── settings.py
│   └── assets.py
└── Tetris_online/             # Version HTML/JS du jeu
    ├── index.html             # Point d'entrée pour GitHub Pages
    ├── style.css              # Feuille de style
    └── tetris.js              # Logique JavaScript
```

---

## ▶️ Lancer la version Python (Pygame)

```bash
cd Tetris_game
pip install -r requirements.txt
python main.py
```

---

## 🌐 Jouer en ligne (version Web)

Accède à la version HTML/JavaScript (100% navigateur) :

👉 [Jouer en ligne sur GitHub Pages](https://<ton-utilisateur>.github.io/Tetris_game)

> Remplace `<ton-utilisateur>` par ton pseudo GitHub.

---

## 🎮 Contrôles

| Touche         | Action                          |
|----------------|----------------------------------|
| Flèche gauche  | Déplacer la pièce à gauche      |
| Flèche droite  | Déplacer la pièce à droite      |
| Flèche bas     | Accélérer la descente           |
| Flèche haut    | Rotation                        |
| Espace         | Instant Drop (descente directe) |
| R              | Recommencer une nouvelle partie |

---

## ✨ Fonctionnalités

- ✅ Ghost piece (ombre de la pièce)
- ✅ Animation de suppression de lignes (fondu avec délai)
- ✅ Sons intégrés (rotation, placement, suppression, game over)
- ✅ UI claire avec score, niveau, lignes, pièce suivante
- ✅ Contrôles clavier fluides
- ✅ Version web jouable sans installation

---

## 📦 Dépendances (pour Python)

- Python ≥ 3.8
- pygame

Voir `requirements.txt`.

---

## 🔊 Crédits sons

Sons libres de droits ou générés pour test. Tu peux les remplacer dans le dossier `assets/`.

---

## 📌 Auteur

Projet réalisé par [Ton Nom ou Pseudo]
