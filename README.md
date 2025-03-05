# Calculateur de Confort Thermique

Application web développée avec Streamlit pour calculer et visualiser les indices de confort thermique PMV (Vote Moyen Prévisible) et PPD (Pourcentage Prévisible d'Insatisfaits) selon la norme ISO 7730.

## 🌡️ Fonctionnalités

- Calcul du PMV et PPD selon la norme ISO 7730
- Visualisation graphique de la relation PMV-PPD
- Calcul de la température opérative
- Interface utilisateur intuitive
- Mise à jour en temps réel des résultats

## 🚀 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/calculateur-confort-thermique.git
cd calculateur-confort-thermique
```

2. Créez un environnement virtuel et activez-le :
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix/macOS
venv\Scripts\activate     # Sur Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 📦 Dépendances

- streamlit
- matplotlib
- numpy
- pythermalcomfort

## 🎮 Utilisation

1. Lancez l'application :
```bash
streamlit run app.py
```

2. Ouvrez votre navigateur à l'adresse indiquée (généralement http://localhost:8501)

3. Ajustez les paramètres :
   - Température de l'air
   - Température radiante moyenne
   - Vitesse de l'air
   - Humidité relative
   - Type d'activité
   - Type d'habillement

Les résultats se mettent à jour automatiquement à chaque modification des paramètres.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 