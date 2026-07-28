# Projet ML: Système de Prédiction de Loyer — Bujumbura

## 1. Contexte et Problématique Métier

**À quel problème répondons-nous ?**

Au Burundi, et plus spécifiquement à Bujumbura, la fixation du loyer mensuel d'une maison repose aujourd'hui exclusivement sur l'expérience individuelle et l'intuition des agents immobiliers. Cette approche empirique génère des disparités de prix importantes d'un quartier à l'autre et d'un agent à l'autre pour des maisons pourtant similaires.

Ce manque de standardisation entraîne une perte de confiance chez les propriétaires (qui peuvent sous-évaluer leur bien) et les locataires (qui peuvent payer un prix excessif), tout en ralentissant les transactions immobilières.

**Pour qui ?**

Le projet est destiné à **MEDIABOX Burundi**, aux **agences immobilières partenaires**, et aux **propriétaires** de la ville de Bujumbura. L'outil final devra être utilisable par un personnel non-technique.

## 2. Objectif du Projet

L'objectif principal est de construire un pipeline de Machine Learning complet, depuis l'analyse exploratoire (EDA) jusqu'au déploiement, capable de prédire le **LoyerMensuel_BIF** d'une maison. Le modèle devra atteindre une précision suffisante pour être déployé en production et remplacer les estimations subjectives des agents.

Il s'agit d'un problème de **Régression supervisée** dont la finalité est de fournir un outil d'aide à la décision.

## 3. Valeur Business Attendue

Le projet apportera trois bénéfices métier majeurs :

1. **Standardisation** : Uniformiser les estimations de loyer entre les agents et les quartiers de Bujumbura.
2. **Efficacité Opérationnelle** : Réduire drastiquement le temps de mise sur le marché d'une nouvelle maison à louer en fournissant un prix instantané et objectif.
3. **Accessibilité** : Proposer un outil interne (application Streamlit) accessible sans compétence technique, permettant à un propriétaire d'obtenir une estimation fiable en quelques clics.

## 4. Analyse du Jeu de Données et Cible

**Avec quelles données ?**
Le jeu de données `rent_prediction.csv` contient **510 observations** (maisons) et **12 colonnes**, dont une colonne d'identifiant à exclure. Les colonnes incluent des caractéristiques physiques (ex: `Superficie_m2`), des caractéristiques d'équipement (catégorielles : `Salon`, `Parking`, `Meuble`), et la localisation (`Quartier`).

**Contraintes identifiées sur les données :**

* **Valeurs manquantes** : 4,9 % des lignes sont incomplètes sur 10 des 11 caractéristiques, suggérant un mécanisme de données manquantes qui devra être documenté et traité lors de l'EDA.
* **Colonne à exclure** : `IdentifiantMaison` (n'apporte aucun signal prédictif).

**Quelle est la cible (Variable dépendante) ?**

* **Variable cible (Y)** : `LoyerMensuel_BIF` (Montant du loyer mensuel en Francs Burundais).
* **Unités d'observation** : Une maison individuelle située à Bujumbura.

## 5. Solution Technique et Usage Final

**Pour quel usage final ?**
Les étapes du pipeline seront structurées pour :

1. Auditer et préparer les données (EDA, Traitement des valeurs manquantes, Encodage, Normalisation).
2. Créer des variables dérivées pertinentes (Feature Engineering).
3. Établir un modèle de base (Baseline) pour référence.
4. Expérimenter et comparer plusieurs algorithmes de régression (Ridge, Random Forest, Gradient Boosting, etc.) via une validation croisée rigoureuse.
5. Optimiser le meilleur modèle par recherche d'hyperparamètres.
6. Déployer le modèle via une application **Streamlit** : l'utilisateur final pourra remplir un formulaire avec les caractéristiques de la maison et obtenir une prédiction instantanée du loyer. Le modèle final sera également simplifié en identifiant les 5 features les plus importantes pour la prédiction.

## 6. Critères de Succès du Projet

Le projet sera considéré comme réussi si :

* Un modèle de régression supervisée est entraîné, validé et sauvegardé (`best_model_tuned.pkl`).
* Le pipeline de prétraitement est entièrement reproductible via `scikit-learn`.
* L'application Streamlit tourne sans erreur et affiche une prédiction claire à l'utilisateur.
* La documentation permet à un autre ingénieur de reproduire le projet à l'identique en utilisant uniquement le dépôt GitHub.
* Le modèle final surpasse significativement le modèle de baseline (Dummy Regressor) en MAE, RMSE et R².
