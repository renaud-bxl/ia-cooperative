# Coopérative IA

[Site de présentation FR / EN](https://renaud-bxl.github.io/ia-cooperative/)

[English overview](README.en.md)

**Concept et orientation : Renaud Ben Lakhal — [contact@renaud.brussels](mailto:contact@renaud.brussels)**  
Recherche, formalisation et code préparés avec assistance IA.

Une base de réflexion et d’expérimentation pour partager volontairement une part de mémoire et de calcul entre ordinateurs. L’utilisateur conserve le contrôle ; le travail est placé selon les connexions, les ressources et la confiance.

**État : socle de recherche fonctionnel, pas encore une application d’IA distribuée.** Les outils calculent des quotas, proposent un placement fictif et reproduisent des simulations. Un outil séparé permet de mesurer un modèle Ollama déjà installé. Il n’existe pas encore d’installateur signé, de réseau de participants ou de moteur d’inférence partagé livré ici.

## Comprendre et démarrer

- [Le projet expliqué simplement et le premier démarrage](docs/GETTING_STARTED.md)
- [Comment le réseau maillé doit se former](docs/MESH.md)
- [Infrastructure : machine à machine ou services extérieurs ?](docs/INFRASTRUCTURE.md)
- [Plan du test mondial coordonné](docs/GLOBAL_TEST.md)
- [Catalogue des 10 logiciels candidats](docs/SOFTWARE.md), avec sources et révisions examinées
- [Architecture et limites du socle](docs/ARCHITECTURE.md)
- [Protocole de mesures réelles](docs/BENCHMARKS.md)
- [Feuille de route](docs/ROADMAP.md) et [questions de recherche](docs/RESEARCH_QUESTIONS.md)
- [Dossier PDF illustré](reports/IA_cooperative_v1.4.pdf)

## Essayer maintenant

Python 3.11 ou plus récent suffit. Aucun moteur IA, modèle ou compte cloud n’est installé automatiquement.

```bash
python3 -m coopai quota --installed-gb 36 --available-gb 12 --reserve-gb 2 --percent 20
python3 -m coopai plan examples/mac_circle.json
python3 -m unittest discover -s tests -v
```

Le premier calcul retourne **7,2 Go de plafond théorique**. Le second répartit 32 couches fictives sur trois machines du parc d’exemple. Ces résultats n’allouent aucune RAM, ne plafonnent pas le système d’exploitation et ne lancent aucun modèle. Sur Mac, [Demarrer.command](Demarrer.command) lance cette démonstration hors ligne avec une explication en français.

## Le parcours visé pour une application grand public

1. Installer une application signée et ouvrir « Créer mon cercle » ou « Rejoindre un cercle ».
2. Valider une invitation, puis les machines autorisées.
3. Choisir un plafond de contribution, avec un réglage initial de 20 % ajustable.
4. Laisser l’application vérifier connexions, moteur et budgets.
5. Voir « Prêt », « Contribution limitée » ou le problème à corriger ; pouvoir arrêter le partage.

Ce parcours constitue la spécification à construire. Le site de présentation doit montrer la différence entre cette cible et les outils disponibles aujourd’hui.

## Résultats déjà disponibles

Les quatre scripts dans [experiments](experiments) et leurs JSON reproduisent les calculs de mémoire, de réseau, une sélection numérique synthétique et une simulation de files de demandes : **huit scénarios, 160 000 demandes simulées**. Les temps de calcul IA y sont supposés. Aucun débit de GPU ni économie d’énergie réelle n’est démontré.

Les tests du socle vérifient notamment les budgets complets, le refus d’un placement incomplet, les frontières de confiance et le traitement des réponses interrompues. L’outil de benchmark a été testé sur des flux synthétiques, pas sur le Mac de Renaud.

## Participer à la réflexion

Proposer une modification de document, une expérience ou une mesure selon [CONTRIBUTING.md](CONTRIBUTING.md). Chaque idée doit préciser ce qui pourrait la réfuter. Le [journal de décisions](docs/decisions/0001-first-prototype.md) distingue choix provisoires, hypothèses et observations. Les modèles de tickets sont disponibles ; les discussions techniques peuvent également être consignées dans les documents versionnés.

Les logiciels tiers sont des antécédents et des candidats, pas des partenaires. Leur source n’est pas copiée dans le dépôt. [Attribution et statut de licence](ATTRIBUTION.md).
