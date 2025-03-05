import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from pythermalcomfort.models import pmv_ppd_iso
from pythermalcomfort.utilities import operative_tmp, v_relative, clo_dynamic_iso

# Valeurs par défaut
DEFAULT_TDB = 19.0
DEFAULT_TR = 16.0
DEFAULT_V = 0.1
DEFAULT_RH = 40.0
DEFAULT_MET = 1.2  # Correspond à "Activité légère, assis (bureau, école)"
DEFAULT_CLO = 0.7  # Correspond à "Tenue de travail légère"

# Calcul initial avec les valeurs par défaut
if 'pmv' not in st.session_state:
    vr = v_relative(DEFAULT_V, DEFAULT_MET)
    clo_dynamic_iso_val = clo_dynamic_iso(DEFAULT_CLO, DEFAULT_MET, DEFAULT_V)
    operative_tmp_val = operative_tmp(DEFAULT_TDB, DEFAULT_TR, vr)
    resultats_pmv = pmv_ppd_iso(tdb=DEFAULT_TDB, tr=DEFAULT_TR, vr=vr, rh=DEFAULT_RH, 
                               met=DEFAULT_MET, clo=clo_dynamic_iso_val, limit_inputs=False)
    
    st.session_state.pmv = resultats_pmv['pmv']
    st.session_state.ppd = resultats_pmv['ppd']
    st.session_state.operative_tmp = operative_tmp_val

# Titre de l'application
st.title("Calculateur de confort thermique")

# Introduction
st.markdown("""
### 🎯 Objectif
Cet outil permet d'évaluer le confort thermique d'un espace selon la norme ISO 7730, en calculant les indices PMV (Vote Moyen Prévisible) et PPD (Pourcentage Prévisible d'Insatisfaits).

### 📝 Comment utiliser cet outil ?
1. **Paramètres environnementaux** :
   - Renseignez la température de l'air et la température radiante moyenne
   - Indiquez la vitesse de l'air et l'humidité relative

2. **Paramètres individuels** :
   - Sélectionnez le type d'activité physique
   - Choisissez la tenue vestimentaire appropriée

Les résultats se mettent à jour automatiquement à chaque modification des paramètres.
""")

st.markdown("---")

# Définition des options d'habillement avec leurs valeurs clo
vetements = {
    "Nu": 0.0,
    "Short": 0.1,
    "Tenue tropicale type (short, chemise à col ouvert et à manches courtes, chaussettes légères et sandales)": 0.3,
    "Tenue d'été légère (pantalon léger, chemise à col ouvert et à manches courtes, chaussettes légères et chaussures)": 0.5,
    "Tenue de travail légère (chemise de travail en coton à manches longues, pantalon de travail, chaussettes de laine et chaussures)": 0.7,
    "Tenue d'intérieur pour l'hiver (chemise à manches longues, pantalon, pull-over à manches longues, chaussettes épaisses et chaussures)": 1.0,
    "Tenue de ville traditionnelle (complet avec pantalon, gilet et veston, chemise, chaussettes de laine et grosses chaussures)": 1.5
}

# Définition des activités avec leurs valeurs met
activites = {
    "Repos, couché": 0.8,
    "Repos, assis": 1.0,
    "Activité légère, assis (bureau, école)": 1.2,
    "Activité légère, debout (laboratoire, industrie légère)": 1.6,
    "Activité moyenne, debout (travail sur machine)": 2.0,
    "Activité soutenue (travail lourd sur machine)": 3.0
}

# Saisie des paramètres utilisateur
col1, col2 = st.columns(2)
with col1:
    tdb = st.number_input("Température de l'air (°C)", value=DEFAULT_TDB, step=1.0)
    tr = st.number_input("Température radiante moyenne (°C)", value=DEFAULT_TR, step=1.0)
    v = st.number_input("Vitesse de l'air (m/s)", value=DEFAULT_V, step=0.1)
with col2:
    rh = st.number_input("Humidité relative (%)", value=DEFAULT_RH)
    activite_selectionnee = st.selectbox("Type d'activité", 
                                       options=list(activites.keys()),
                                       index=list(activites.keys()).index("Activité légère, assis (bureau, école)"))
    met = activites[activite_selectionnee]
    tenue_selectionnee = st.selectbox("Type d'habillement", 
                                    options=list(vetements.keys()),
                                    index=list(vetements.keys()).index("Tenue de travail légère (chemise de travail en coton à manches longues, pantalon de travail, chaussettes de laine et chaussures)"))
    clo = vetements[tenue_selectionnee]

# Calcul automatique
vr = v_relative(v, met)
clo_dynamic_iso = clo_dynamic_iso(clo, met, v)

# Calcul operative temperature
st.session_state.operative_tmp = operative_tmp(tdb, tr, vr)

# Calcul PMV standard
resultats_pmv = pmv_ppd_iso(tdb=tdb, tr=tr, vr=vr, rh=rh, met=met, clo=clo_dynamic_iso, limit_inputs = False)
st.session_state.pmv = resultats_pmv['pmv']
st.session_state.ppd = resultats_pmv['ppd']

# Affichage des résultats
st.markdown("---")
st.markdown("### 📊 Résultats PMV (ISO 7730)")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="PMV", value=f"{st.session_state.pmv:.2f}")
with col2:
    st.metric(label="PPD", value=f"{st.session_state.ppd:.1f}%")
with col3:
    st.metric(label="Température opérative", value=f"{st.session_state.operative_tmp:.2f}°C")

st.markdown("#### Graphique PMV-PPD")

# Création du graphique
fig, ax = plt.subplots(figsize=(10, 6))
pmv_range = np.linspace(-3, 3, 100)
ppd_range = 100 - 95 * np.exp(-0.03353 * pmv_range**4 - 0.2179 * pmv_range**2)

ax.plot(pmv_range, ppd_range, label='Courbe de référence ISO 7730', color='blue')
if st.session_state.pmv != 0 or st.session_state.ppd != 0:
    ax.scatter(st.session_state.pmv, st.session_state.ppd, color='red', s=100, label='Résultat actuel')
ax.set_title('Relation PMV-PPD selon la norme ISO 7730')
ax.set_xlabel('PMV')
ax.set_ylabel('PPD (%)')
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Section explicative
st.markdown("### 📖 Comment interpréter les résultats ?")

st.markdown("""
#### PMV (Vote Moyen Prévisible)
Le PMV est un indice qui prédit la valeur moyenne des votes d'un groupe important de personnes sur une échelle de sensation thermique à 7 niveaux :
- **-3** : Très froid
- **-2** : Froid
- **-1** : Légèrement froid
- **0** : Neutre (optimal)
- **+1** : Légèrement chaud
- **+2** : Chaud
- **+3** : Très chaud

Une valeur PMV entre -0.5 et +0.5 est considérée comme confortable.

#### PPD (Pourcentage Prévisible d'Insatisfaits)
Le PPD indique le pourcentage de personnes susceptibles d'être insatisfaites dans un environnement thermique donné :
- Le PPD minimal théorique est de 5% (même dans des conditions optimales)
- Un PPD inférieur à 10% est considéré comme acceptable
- Plus le PMV s'écarte de 0, plus le PPD augmente

#### Température opérative
La température opérative est un indicateur qui combine :
- La température de l'air
- La température radiante moyenne (température des surfaces environnantes)
- L'effet de la vitesse de l'air

C'est la température ressentie par les occupants, plus représentative du confort thermique que la simple température de l'air. Elle permet de prendre en compte l'effet du rayonnement des parois et des mouvements d'air sur le confort thermique.

#### Lecture du graphique
- La **courbe bleue** montre la relation théorique entre PMV et PPD selon la norme ISO 7730
- Le **point rouge** représente votre situation actuelle
- La zone de confort optimal se situe entre -0.5 et +0.5 sur l'axe PMV, correspondant à un PPD inférieur à 10%
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: grey; padding: 20px;'>
Développé avec ❤️ en utilisant :<br>
<a href='https://pypi.org/project/pythermalcomfort/' target='_blank'>PythermalComfort</a> | 
<a href='https://streamlit.io' target='_blank'>Streamlit</a> | 
<a href='https://matplotlib.org/' target='_blank'>Matplotlib</a><br>
Nathan Chateau<br>
</div>
""", unsafe_allow_html=True)
