# 🎮 Tetris Python (Pygame)

Ce projet est une version complète, optimisée et modulaire du jeu **Tetris**, développée avec **Python** et **Pygame**.

---

## 📁 Structure du projet

```
tetris_game/
├── main.py                    # Boucle principale (affichage + clavier)
├── requirements.txt          # Dépendances du projet
├── README.md                 # Ce fichier
├── assets/                   # Sons du jeu (WAV)
│   ├── rotate.wav
│   ├── place.wav
│   ├── clear.wav
│   └── gameover.wav
└── tetris/                   # Logique interne du jeu
    ├── __init__.py
    ├── core.py               # Classes Tetris, Piece
    ├── settings.py           # Constantes globales
    └── assets.py             # Chargement centralisé des sons
```

---

## ▶️ Lancer le jeu

```bash
cd tetris_game
pip install -r requirements.txt
python main.py
```

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

- Ghost piece (ombre de la pièce)
- Animation de suppression de lignes (clignotement)
- Sons personnalisés (rotation, placement, suppression, game over)
- Interface claire avec panneau latéral (score, niveau, lignes, pièce suivante)
- Structure modulaire (séparation logique / interface)

---

## 📦 Dépendances

- Python ≥ 3.8
- pygame

Voir `requirements.txt`.

---

## 🔊 Crédits sons

Sons libres de droits ou générés pour test. Tu peux les remplacer par tes propres effets personnalisés dans le dossier `assets/`.
