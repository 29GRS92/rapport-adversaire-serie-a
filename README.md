# Rapport d'adversaire Serie A 2025/26

Un outil qui produit, pour chacune des 20 équipes de Serie A, un rapport d'adversaire complet à partir de **chiffres uniquement** (aucune vidéo). Chaque chiffre est comparé aux 19 autres équipes de la ligue : valeur, moyenne, médiane, rang et percentile.

**Site en ligne : [À COMPLÉTER : lien GitHub Pages]**

![Aperçu du site](docs/apercu.png)

## Ce que contient un rapport

1. **Comparaison avec la ligue** : une trentaine d'indicateurs d'équipe (style, attaque, défense, discipline, ce que l'équipe subit), avec points forts, points faibles et éléments de style.
2. **Coups de pied arrêtés et penaltys**, marqués et concédés.
3. **Joueurs dangereux** : tirs, passes menant à un tir, dépendance à un buteur.
4. **Effectif** : minutes, rôle de chaque joueur, joueurs à surveiller.
5. **Défense individuelle** : joueurs parmi les 10 % les plus défavorables de leur poste.
6. **Dynamique de la saison** : domicile et extérieur, forme récente, résultats selon le style de l'adversaire, moment des buts.
7. **Pistes à tester**, chacune liée à un chiffre précis. Il n'y a pas de plan de jeu général.

## Méthode

Le rapport suit trois niveaux, qui ne sont jamais mélangés :

1. **Les données** : ce que les chiffres montrent.
2. **L'analyse** : ce que ces chiffres veulent dire par rapport à la ligue.
3. **Les pistes à tester** : des idées, jamais des certitudes.

Les règles de lecture (seuils, minutes minimales, nombre minimal d'événements) sont écrites à l'avance dans le notebook et modifiables.

## Limites

- Les chiffres décrivent, ils ne prouvent pas : le rapport propose des pistes à tester.
- Il n'y a pas de score par équipe : plusieurs indicateurs racontent la même chose, donc compter les points forts et faibles n'a pas de sens.
- Les penaltys, les erreurs individuelles et les joueurs de moins de 900 minutes reposent sur peu d'événements.
- Le xG d'Understat surestime les buts d'environ 17 % sur toute la ligue : il sert à comparer les équipes entre elles. Le xG d'équipe vient de Sofascore.
- Une seule saison (2025/26) et un seul championnat.

## Sources

- [Understat](https://understat.com) : matchs, tirs, style de jeu (PPDA).
- [Sofascore](https://www.sofascore.com) : statistiques d'équipe et de joueurs, compositions.

Les données brutes ne sont pas publiées dans ce dépôt. Le notebook sait les retélécharger.

## Contenu du dépôt

| Fichier ou dossier | Rôle |
|---|---|
| `rapport_adversaire_serie_a.ipynb` | Le notebook complet : collecte, nettoyage, analyses, rapports, site |
| `sofascore_collecte.py` | Script de collecte Sofascore (écrit aussi par le notebook) |
| `data/processed/rapports_equipes.json` | Les 20 rapports produits |
| `docs/` | Le site : `modele.html` (modèle) et `index.html` (page générée) |

## Lancer le projet

1. Installer les bibliothèques : `pip install pandas numpy understatapi playwright`, puis `python -m playwright install chromium`.
2. Ouvrir le notebook et l'exécuter de haut en bas. La première exécution télécharge les tirs d'Understat (environ 7 minutes) et les fichiers de Sofascore (environ 25 minutes). Les exécutions suivantes réutilisent les fichiers déjà téléchargés.
3. Ouvrir `docs/index.html` dans un navigateur.

## Auteur

[À COMPLÉTER : ton nom et un lien vers ton profil LinkedIn ou ton portfolio]
