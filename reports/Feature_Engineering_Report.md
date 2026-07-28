# Feature 1 : Confort_Score (Indicateur de Confort)

Pourquoi ? (Justification issue de l'EDA)
L'analyse des 5 variables binaires (Salon, SalleDeBainInterieure, Parking, Meuble, Jardin) a révélé deux éléments :

Ces commodités sont fortement corrélées entre elles (les maisons "luxueuses" les possèdent toutes).

Bien que Parking ait un impact quasi-nul sur le loyer pris isolément, la combinaison de ces 5 équipements crée un signal global de "standing" bien plus puissant que la somme de ses parties. Les utiliser séparément ajoute du bruit et de la dimensionnalité inutile.

Bénéfice attendu

Réduction de dimensionnalité : Nous passons de 5 colonnes à 1 seule colonne (de 0 à 5), simplifiant le modèle et accélérant l'entraînement.

Interprétabilité métier améliorée : Le score permet de classer facilement une maison de "basique" (score 0-1) à "haut de gamme" (score 4-5).

Réduction de la multicolinéarité : En fusionnant les variables, on évite que le modèle sur-pondère l'effet "confort" via de multiples colonnes.

Impact mesuré (Protocole d'évaluation)
Nous mesurerons l'impact en comparant deux modèles LinearRegression (ou Random Forest) :

- Modèle A : Utilise les 5 colonnes binaires distinctes.
- Modèle B : Utilise la colonne unique Confort_Score.

Métriques de comparaison : MAE (Mean Absolute Error), RMSE, et R².

Résultat attendu : Le Modèle B devrait avoir un RMSE et un MAE légèrement inférieurs ou égaux, tout en étant beaucoup plus simple et robuste.


# Feature 2 : Chambres_par_Superficie (Densité de l'habitat)

Pourquoi ? (Justification issue de l'EDA)
L'EDA a mis en évidence une multicolinéarité parfaite (0.98) entre Chambres et Superficie_m2, ce qui nous a obligé à supprimer la colonne Chambres pour ne conserver que la superficie.
Cependant, supprimer Chambres nous prive d'un signal métier subtil : une maison avec 4 chambres mais seulement 80 m² est beaucoup plus dense qu'une maison de 4 chambres de 250 m².
Le ratio Chambres / Superficie capture cette notion de "densité" tout en étant orthogonal (non corrélé) à la superficie brute.

Bénéfice attendu

Extraction de signal caché : Le modèle pourra désormais distinguer les appartements/maisons "compartimentés" et "exigus" des logements "spacieux".

Aucune multicolinéarité : Ce ratio est décorrélé de la superficie, ce qui permet de garder l'information "nombre de chambres" sans casser les mathématiques du modèle.

Impact mesuré (Protocole d'évaluation)
Nous comparerons les performances du Random Forest (qui capte bien les non-linéarités) :

- Modèle A : Superficie_m2 seulement.
- Modèle B : Superficie_m2 + Chambres_par_Superficie.

Métriques de comparaison : MAE, RMSE, R².

Résultat attendu : Le RMSE devrait s'améliorer (diminuer) car le modèle peut désormais ajuster le prix en fonction de la densité de la maison (les maisons denses étant souvent plus chères au m²).


# Feature 3 : Quartier_Grouped (Regroupement des Quartiers à faible effectif)

Pourquoi ? (Justification issue de l'EDA)
Le boxplot des quartiers a montré que la géographie est le prédicteur le plus influent. Cependant, certains quartiers de Bujumbura (comme Jabe, Gasekebuye) ont moins de 25 occurrences dans le jeu de données. Lors d'un encodage One-Hot, le modèle va créer un coefficient spécifique pour ces quartiers, mais avec si peu d'exemples, il va mémoriser ces quelques maisons au lieu d'apprendre une tendance générale pour la zone. Cela provoque du sur-apprentissage (overfitting) et dégrade la performance sur les nouvelles maisons.

Bénéfice attendu

Meilleure généralisation : En regroupant les quartiers rares dans une catégorie "Autres", le modèle apprendra une valeur de loyer moyenne pour les zones "atypiques", sans sur-pondérer les cas extrêmes et rares.

Robustesse : L'application Streamlit sera plus robuste, car un utilisateur venant d'un de ces quartiers rares obtiendra une estimation réaliste (basée sur la moyenne des quartiers "Autres") plutôt qu'une estimation aberrante.

Impact mesuré (Protocole d'évaluation)
Nous comparerons la Validation Croisée (Cross-Validation) du modèle Random Forest :

- Modèle A : Quartiers bruts (One-Hot Encoding sur les 14 classes).
- Modèle B : Quartiers regroupés (One-Hot Encoding sur les classes rares renommées "Autres").

Métriques de comparaison : Écart-type du R² sur les différents plis de la Cross-Validation.

Résultat attendu : Le Modèle B devrait avoir un écart-type du R² plus faible, prouvant une plus grande stabilité et moins de variance liée au hasard des données.


# Prix_par_m2

Pourquoi il n'est PAS inclus en tant que feature ?
Le cahier des charges mentionnait "Prix_par_m2 (si disponible en amont)". Dans notre contexte, le prix au m² est mathématiquement calculé comme LoyerMensuel_BIF / Superficie_m2.

Si nous l'utilisons en tant que feature (X), nous commettons une fuite de données (Data Leakage) massive. Le modèle apprendrait simplement que Loyer = Prix_par_m2 * Superficie_m2 sans rien apprendre du tout sur le marché réel.

Décision : Nous n'utilisons pas cette feature. En revanche, nous avons transformé la cible en *Log_Loyer* pour normaliser sa distribution, ce qui remplit l'objectif mathématique de mieux modéliser la structure des prix.