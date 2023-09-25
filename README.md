## Carte des Lieux de Pêche Réciprocitaires 🎣🗺

Ce projet est composé de deux principaux scripts: `generateur.py` et `constructeur.py`.

### generateur.py 🚀
Il s'agit du script qui génère une carte interactive basée sur les données des lacs et des régions, en se concentrant spécifiquement sur la région de l'Oise. Le script lit les données à partir de fichiers JSON et CSV, puis utilise des bibliothèques telles que Folium et Shapely pour visualiser les données sur une carte.

🔍 **Caractéristiques principales**:

- Affiche une carte avec des marqueurs pour les lacs et des polygones pour les régions.
- Utilise un icône 🐟 pour représenter les lacs.
- Génère des liens Google Maps pour chaque lac basé sur leurs coordonnées.
- Met en évidence les régions adjacentes à l'Oise.
- Ajoute une barre d'en-tête avec des liens et de la publicité.

### constructeur.py 🚧
Il s'agit d'un simple serveur Flask qui vous permet de sauvegarder des polygones (représentant des lacs) dans un fichier JSON. Il utilise Flask pour le backend et expose une API REST pour sauvegarder les données des polygones.

🔍 **Caractéristiques principales**:

- Exposition d'une API REST pour sauvegarder les polygones.
- Sauvegarde les polygones dans un fichier `Lacs.json`.
- Utilise Flask pour servir une interface simple.

## Comment démarrer 🚀

1. Assurez-vous d'avoir installé les dépendances nécessaires : 
   ```bash
   pip install folium pandas shapely flask flask_cors beautifulsoup4
   ```
   
2. Pour générer la carte, exécutez : 
   ```bash
   python generateur.py
   ```
   
   Cela générera un fichier `map.html` que vous pourrez ouvrir dans votre navigateur pour voir la carte.

3. Pour démarrer le serveur Flask, exécutez :
   ```bash
   python constructeur.py
   ```
   
   Rendez-vous sur `http://localhost:5000/` pour voir l'interface.

## Contribution 🤝

N'hésitez pas à contribuer ou à signaler des problèmes via les issues. Tout retour ou contribution est grandement apprécié! 🙌

## Contact 📬

Si vous souhaitez réaliser une carte dans ce style ou contribuer à celle-ci, n'hésitez pas à me contacter:

- 🌐 [Webanimus](https://webanimus.com)
- 📧 [Envoyer un e-mail](mailto:your@email.com)
- ☕ [Soutenir via PayPal](https://www.paypal.me/yourpaypal)
