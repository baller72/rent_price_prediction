# 🏠 Système de prédiction de loyer — MEDIABOX Burundi

<!-- ![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.0-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen) -->

## 📌 Vue d'ensemble du projet

Ce projet, commandité par **MEDIABOX Burundi**, a pour objectif de construire un pipeline de Machine Learning complet (de l'EDA au déploiement) pour prédire le loyer mensuel (`LoyerMensuel_BIF`) d'une maison à Bujumbura en fonction de ses caractéristiques physiques et de sa localisation.

Aujourd'hui, l'estimation des loyers repose sur l'expérience individuelle des agents immobiliers, ce qui entraîne des incohérences de prix entre les quartiers. **Ce système permet de standardiser ces estimations, d'accélérer la mise en marché des biens, et de fournir un outil interne accessible aux non-techniciens via une application Streamlit.**

---

## 🎯 Problème et valeur business

- **Problème** : Manque de standardisation des loyers due à des estimations subjectives.
- **Solution** : Un modèle de régression entraîné sur les données historiques du marché de Bujumbura.
- **Valeur Business** :
  1. Uniformisation des estimations entre agents et quartiers.
  2. Réduction du temps de mise sur le marché d'une nouvelle maison.
  3. Outil interne (Streamlit) utilisable sans compétence technique.

---

## 📊 Description du dataset

- **Fichier** : `rent_prediction.csv`
- **Taille** : 510 lignes, 12 colonnes.
- **Données manquantes** : ~4,9 % (25 lignes) réparties uniformément, traitées lors de l'EDA.

| Colonne | Type | Description |
| :--- | :--- | :--- |
| `IdentifiantMaison` | int | ID unique (exclu du modèle) |
| `Chambres` | float | Nombre de chambres |
| `Salon` | catégoriel | Oui/Non |
| `SalleDeBainInterieure` | catégoriel | Oui/Non |
| `Parking` | catégoriel | Oui/Non |
| `Meuble` | catégoriel | Oui/Non |
| `Jardin` | catégoriel | Oui/Non |
| `Superficie_m2` | float | Surface en m² |
| `DistanceRoute_m` | float | Distance à la route principale (m) |
| `Quartier` | catégoriel | Quartier de Bujumbura |
| `AgeMaison` | float | Âge de la maison (années) |
| **`LoyerMensuel_BIF`** | **int** | **Variable Cible (Régression)** |

---

## ⚙️ Implementation du projet & Decisions techniques

Le projet a été mené en **9 phases**, conformément aux spécifications d'ingénierie.

### Phase 1 — Business Understanding

Définition du problème métier, des parties prenantes, et de la cible (`LoyerMensuel_BIF`).

### Phase 2 — Exploratory Data Analysis (EDA)

- **Cible** : Détection d'une **asymétrie positive** (skewness = 0.59) et d'un **plafonnement artificiel** à 2 500 000 BIF.
- **Numériques** : Découverte d'une **multicolinéarité parfaite (0.98)** entre `Chambres` et `Superficie_m2`. `DistanceRoute_m` et `AgeMaison` n'ont pas de corrélation linéaire avec le prix (0.02), mais restent pertinents pour les modèles non-linéaires.
- **Catégorielles** : Le quartier a un impact ultra-prédominant. Les variables binaires (Salon, Jardin) ont un fort impact, tandis que le `Parking` a un effet quasi-nul.

### Phase 3 & 4 — Data Preparation & Feature Engineering

*(Toutes les décisions sont justifiées par l'EDA)*

1. **Nettoyage** : Suppression des 25 lignes contenant des `NaN` et des lignes plafonnées à 2.5M BIF.
2. **Suppression de `Chambres`** : Pour éliminer la multicolinéarité.
3. **Création de `Confort_Score`** : Somme des 5 commodités (Salon, SDB, Parking, Meuble, Jardin). Suppression des 5 colonnes binaires.
4. **Création de `Chambres_par_Superficie`** : Ratio de densité de l'habitat.
5. **Regroupement des Quartiers** : Les quartiers avec < 25 occurrences sont groupés en une catégorie **"Autres"** pour éviter le sur-apprentissage.
6. **Transformation de la cible** : `np.log1p()` appliqué sur `LoyerMensuel_BIF` pour normaliser la distribution.

### Phase 5 — Baseline Models

Création de références objectives :

- **Dummy Regressor (Moyenne)** : MAE = `[MAE]` BIF, R² = 0.0.
- **Linear Regression** : MAE = `[MAE]` BIF, R² = `[R²]`.

### Phase 6 & 7 — Model Experiments & Hyperparameter Tuning

Comparaison rigoureuse via **5-Fold Cross-Validation** (CV) sur 7 algorithmes (`Ridge`, `Lasso`, `Decision Tree`, `Random Forest`, `Gradient Boosting`, etc.).

- **Sélection du meilleur modèle** : Random Forest / Gradient Boosting (selon vos résultats).
- **Optimisation** : Utilisation de **`GridSearchCV`** pour trouver les paramètres optimaux (`max_depth`, `n_estimators`, etc.). Amélioration de `[MAE_Avant]` BIF à `[MAE_Après]` BIF.

### Phase 8 — Feature Importance & Simplification

Extraction des 5 features les plus importantes. Comparaison des performances du **modèle complet** vs un **modèle réduit (Top 5)**.

- **Résultats** : Une dégradation minime de la performance (MAE augmenté de seulement `[X]` BIF) pour une simplification massive du pipeline. Le modèle réduit est recommandé pour le déploiement.

### Phase 9 — Deployment (Streamlit)

Développement d'une interface web interactive avec **Streamlit**. Le modèle chargé recalcule automatiquement le `Confort_Score` et le ratio densité à partir des entrées de l'utilisateur. L'application effectue la prédiction en Log et la retransforme en BIF via `np.expm1()`.

---

## 📁 Structure du repository

rent_price_prediction/<br>
│<br>
├── data/ # Données brutes et traitées<br>
│ └── rent_prediction.csv<br>
│<br>
├── notebooks/ # Notebooks Jupyter (Phases 1 à 8)<br>
│ ├── 01_EDA_and_Preprocessing.ipynb<br>
│ ├── 02_Feature_Engineering.ipynb<br>
│ ├── 03_Baseline_Model.ipynb<br>
│ ├── 04_Model_Experiments.ipynb<br>
│ ├── 05_Hyperparameter_Tuning.ipynb<br>
│ └── 06_Feature_Importance.ipynb<br>
│<br>
├── streamlit/ # Application Web de déploiement<br>
│ └── app.py<br>
│<br>
├── models/ # Modèles sauvegardés (.pkl)<br>
│ └── best_model_tuned.pkl # Pipeline final (Preprocessor + Modèle)<br>
│<br>
├── reports/ # Rapports et documents PDF<br>
│ ├── EDA_Report.pdf<br>
│ ├── Feature_Engineering_Report.md<br>
│ └── Final_Technical_Report.pdf<br>
│<br>
├── figures/ # Visualisations exportées<br>
│ └── feature_importance.png<br>
│<br>
├── logs/ # Suivi des expériences<br>
│ └── experiment_log.csv<br>
│<br>
├── requirements.txt # Dépendances Python exactes<br>
├── README.md # Documentation du projet<br>
└── .gitignore # Exclusion des fichiers inutiles<br>

---

## 🛠️ Installation & Dependencies

Pour reproduire ce projet dans un environnement propre, suivez ces étapes :

1. **Cloner le dépôt GitHub** :

   ```bash
    git clone [URL_DU_DEPOT_GITHUB]
    cd rent_price_prediction
   ```

2. **Créer un environnement virtuel** :

   ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS / Linux
    source venv/bin/activate
   ```

3. **Installer les dépendances** :

   ```bash
    pip install -r requirements.txt
   ```

## 🚀 Comment exécuter le project

### 1. Exécuter les Notebooks (dans l'ordre chronologique)

Ouvrez Jupyter Notebook ou Jupyter Lab depuis le dossier racine :

```bash
    jupyter notebook
```

Exécutez les notebooks dans cet ordre pour reproduire le pipeline :

```bash
    01_EDA_and_Preprocessing.ipynb
    02_Feature_Engineering.ipynb
    03_Baseline_Model.ipynb
    04_Model_Experiments.ipynb
    05_Hyperparameter_Tuning.ipynb
    06_Feature_Importance.ipynb
```

### 2. Lancer l'application Streamlit

Assurez-vous d'être à la racine du projet et que le fichier models/best_model_tuned.pkl est présent. Exécutez la commande suivante :

```bash
streamlit run streamlit/app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse <http://localhost:8501>.

## 💼 Résultats & Valeur Business

L'application Streamlit permet désormais aux agents de MEDIABOX et aux propriétaires de :

- Saisir les caractéristiques d'un bien en moins de 1 minute.

- Obtenir une estimation instantanée, transparente et standardisée.

- Anticiper les fluctuations du marché grâce à des données historiques.

Le pipeline est totalement reproductible, et toutes les décisions d'ingénierie (suppression de colonnes, transformation log, création de features) sont strictement justifiées par les observations de l'EDA, conformément à la philosophie d'ingénierie du projet.

## 👥 Auteurs

    Ingénieur: Dorian Axel DUSHIME
    Encadré par : MEDIABOX Burundi (Projet d'Ingénierie - Spécifications v1.0)
