# Une IA coopérative : partager des ressources sans fabriquer une RAM géante

**Proposition et orientation : Renaud Ben Lakhal**  
**Contact : contact@renaud.brussels**  
7 novembre 2026. Recherche, formalisation et simulations avec assistance IA. Architecture exploratoire ; aucun réseau de participants ni modèle de langage complet n’a été testé dans ce travail.

Et si une partie des ressources nécessaires à l’IA venait des ordinateurs que nous possédons déjà ? Mon point de départ est volontairement simple : chacun pourrait proposer une fraction de sa mémoire et de son processeur, lorsqu’il n’en a pas besoin, puis profiter du service collectif.

La question technique est moins simple. Mille machines qui proposent quelques gigaoctets ne constituent pas une carte graphique géante. Le réseau oblige à choisir ce que l’on partage, à quelle distance et à quel rythme.

## Partager le travail au bon endroit

La proposition distingue trois espaces. L’espace personnel conserve le contrôle des quotas, des destinataires et des données sensibles. Un petit groupe de machines autorisées et bien connectées héberge des blocs contigus d’un modèle et les calcule sur place. Un réseau plus large accueille des travaux autonomes : indexation de documents publics, évaluations ou traitement de lots.

Les poids restent près des processeurs qui les utilisent. On échange surtout les états nécessaires entre blocs. Un registre de reçus comptabilise les contributions ; une blockchain peut éventuellement l’appuyer, mais elle ne transporte pas les tenseurs et n’intervient pas à chaque token.

Les participants gardent le droit de reprendre leurs ressources. Le contrôleur doit réagir à l’activité, à la pression mémoire et à l’alimentation. Le partage doit pouvoir s’arrêter.

## Pourquoi étudier 20 % ?

Ce pourcentage est un point de départ à tester, pas une valeur optimale démontrée. Sur une machine de 16 Go, il représente un plafond de 3,2 Go ; sur 36 Go, 7,2 Go. Le quota effectif reste limité par la mémoire disponible, une réserve de confort et le choix de l’utilisateur.

Une population hypothétique de 1 000 machines totalisant 32,8 To de RAM proposerait 6,56 To à 20 %. En supposant 40 % de disponibilité simultanée, 80 % de capacité exploitable après provision et deux copies des données, il resterait 1,0496 To de budget agrégé. Ce calcul ne garantit ni placement réalisable, ni débit, ni confidentialité.

## Une simulation qui montre aussi les échecs

Un programme a simulé huit scénarios, avec vingt répétitions de 1 000 demandes chacun : 160 000 demandes au total. Chaque demande comporte 512 tokens d’entrée et 64 de sortie. Les temps de calcul sont des hypothèses : 1,280 seconde pour traiter le contexte et produire le premier token, puis 80 millisecondes par token suivant, auxquels s’ajoutent les échanges.

Sous ces hypothèses, une demande isolée prend environ 6,56 secondes avec quatre machines reliées en réseau local, contre 12,57 secondes sur Internet à 100 Mbit/s et 20 ms par trajet. À une arrivée toutes les dix secondes en moyenne, le groupe Internet reçoit plus de travail qu’il ne peut en terminer : la file s’accumule. Ajouter des machines à une même chaîne peut donc dégrader le service.

Une autre organisation utilise huit groupes locaux de quatre machines et une file commune. Avec huit fois plus d’arrivées au total, le délai au 95e percentile est de 8,62 secondes, contre 29,58 secondes pour un groupe local isolé. Ce résultat mesure l’effet de mutualisation des pointes sous le modèle choisi. Il utilise 32 machines actives et n’accélère pas le calcul d’une demande isolée.

La simulation traite une conversation à la fois par groupe. Elle exclut le batching, le chargement des poids à froid et la contention entre groupes. Ce sont des résultats simulés, pas des performances de matériel mesurées. Les hypothèses et le code doivent accompagner les chiffres.

## Ce qui existe déjà et ce que cette proposition cherche à organiser

L’inférence collaborative existe notamment dans [Petals](https://arxiv.org/abs/2312.08361). [exo](https://github.com/exo-explore/exo) et [Prima](https://arxiv.org/abs/2504.08791) explorent eux aussi des machines distribuées. Le calcul décentralisé et les mécanismes de vérification ont également des précédents, notamment dans [Hivemind](https://github.com/learning-at-home/hivemind) et [Gensyn](https://www.gensyn.ai/infrastructure).

Je ne revendique pas l’invention de ces briques. L’orientation proposée est d’articuler participation personnelle, quotas adaptatifs, groupes constitués selon les connexions et la confiance, tâches distantes autonomes et comptabilité du service réellement utile.

D’autres supports ont été examinés : ADN, verre, mémoires analogiques et photonique. Ils répondent à des usages différents. Le stockage biologique ne fournit pas une RAM directement interchangeable avec celle d’un ordinateur. La récupération de chaleur, illustrée par [heata](https://heata.co/compute), peut compléter l’usage du calcul lorsqu’un besoin thermique réel existe ; elle ne rend pas l’électricité gratuite.

## La prochaine expérience

Le premier prototype utile serait modeste : un modèle identifié, deux à quatre machines de confiance et des mesures de mémoire, de qualité, de délai, de reprise après panne et d’énergie. Il faudrait comparer à la même tâche sur une seule machine et remplacer les temps supposés du simulateur par ces mesures.

Le dossier de 46 pages décrit les composants, les contrats d’échange, les quotas, le cache des conversations, les pannes et le protocole d’essai. Il comprend les scripts et leurs résultats. La proposition reste ouverte à la critique, y compris à un résultat montrant qu’une variante n’apporte aucun avantage.

Renaud Ben Lakhal — contact@renaud.brussels
