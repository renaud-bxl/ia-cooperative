# Le logiciel expliqué simplement

## Ce que l’on veut construire

Un petit programme installé sur chaque ordinateur. Il indique « je peux aider », reçoit un travail compatible avec la limite choisie, puis rend ses ressources quand son propriétaire en a besoin. Un cercle réunit des machines autorisées ; une demande peut utiliser certaines machines du cercle et pas nécessairement toutes.

Partager 20 % ne signifie pas donner définitivement un cinquième de son ordinateur. C’est un plafond révisable. La mémoire et le calcul restent chez le participant ; les machines échangent les données nécessaires au travail.

## Ce qui fonctionne aujourd’hui dans ce dépôt

| Action | Disponible | Ce qu’elle fait |
|---|---|---|
| Calculer sa contribution | Oui | Calcul hors ligne à partir de valeurs saisies. |
| Estimer un partage de couches | Oui | Plan fictif avec contrôle des budgets et autorisations. |
| Reproduire les simulations | Oui | Expériences et résultats JSON. |
| Mesurer un modèle Ollama existant | Outil fourni | Exécution réelle à lancer sur sa machine ; pas encore mesurée ici. |
| Installer une application graphique signée | À construire | Le dépôt ne livre pas encore de .dmg, .msi ou AppImage. |
| Joindre des ordinateurs et exécuter un modèle partagé | À construire | Aucun réseau réel n’est créé par les commandes de démonstration. |

## Démarrer sur Mac, maintenant

1. Sur la page GitHub du projet, choisir **Code → Download ZIP**, puis décompresser.
2. Vérifier que Python 3.11+ est installé. Si nécessaire, utiliser l’installateur officiel de [python.org](https://www.python.org/downloads/).
3. Ouvrir `Demarrer.command`. Si l’ouverture du fichier n’est pas proposée par macOS, ouvrir Terminal dans le dossier et lancer `bash Demarrer.command`. Aucun changement des protections du système n’est demandé.
4. Lire le résultat de démonstration. Le parc affiché est fictif ; aucune mesure automatique du Mac n’est prétendue.
5. Pour essayer ses propres valeurs, employer la commande `quota` présentée dans le README.

Le script vérifie Python, explique ce qu’il exécute et lance les tests. Il n’installe rien en arrière-plan et ne transmet aucune donnée.

## Installer la future application : parcours à développer

L’objectif est un installateur signé pour macOS, puis Windows et Linux. Au premier démarrage, trois écrans suffisent : **Mon cercle**, **Ma contribution**, **Vérification**. Le téléchargement des modèles doit afficher volume, espace nécessaire et consentement avant de démarrer. Une barre explique chaque étape : téléchargement, vérification, chargement, test.

L’application doit proposer un modèle qui tient réellement dans le budget du cercle et afficher son identité. Un pourcentage de RAM ne suffit pas pour choisir un modèle. Les modèles et les moteurs peuvent nécessiter des conditions d’utilisation propres ; ils ne sont pas inclus implicitement.

## Les messages compréhensibles à prévoir

| Message | Action proposée |
|---|---|
| Prêt à contribuer | Afficher le plafond actuel et le bouton Arrêter. |
| Votre ordinateur a besoin de mémoire | Réduire la contribution, sans blâmer l’utilisateur. |
| Invitation expirée | Demander une nouvelle invitation au créateur du cercle. |
| Connexion indirecte | Expliquer que les données passent par un relais chiffré et que cela peut ralentir. |
| Cette machine ne peut pas charger le modèle | Expliquer mémoire, format ou moteur incompatible. |
| Un participant s’est déconnecté | Reprendre, proposer un autre modèle explicitement, ou expliquer l’arrêt. |

Critère de validation proposé : une personne sans expérience réseau doit pouvoir rejoindre un cercle test et comprendre le bouton d’arrêt sans ouvrir Terminal. Cet objectif n’est pas encore atteint par le socle de recherche actuel.
