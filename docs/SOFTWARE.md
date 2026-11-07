# Catalogue logiciel

État documentaire au 7 novembre 2026. P0 : référence initiale ; P1 : essai après référence ; P2 : étude ultérieure. Aucun de ces moteurs tiers n’est installé par ce dépôt. Le benchmark appelle seulement une installation locale existante d’Ollama.

| Logiciel | Usage proposé | Priorité | Limite importante |
|---|---|---|---|
| [Ollama](https://github.com/ollama/ollama) | API locale simple pour mesurer un modèle déjà installé. | P0 | Ce n’est pas le moteur de partage entre participants. Désactiver le cloud côté serveur pour une référence locale. |
| [MLX](https://github.com/ml-explore/mlx) | Moteur à évaluer en priorité sur Apple Silicon ; opérations distribuées disponibles dans sa documentation. | P0 | Vérifier modèle, version, OS et transport. Le socle de ce dépôt ne l’intègre pas encore. |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | Référence d’inférence C/C++ et formats quantifiés, dont Metal et CPU. | P0 | Le module RPC est signalé expérimental et non sûr par ses auteurs ; essais isolés uniquement, hors réseau ouvert. |
| [exo](https://github.com/exo-explore/exo) | Candidat à comparer avant de développer un moteur distribué maison. | P1 | La liste des machines explicitement testées consultée ne cite pas le M3 Pro. Vérifier sa compatibilité ; ne pas présumer le support de tous les PC. |
| [Petals](https://github.com/bigscience-workshop/petals) | Antécédent d’inférence par blocs distribués et groupes privés. | P2 | Activité du dépôt et compatibilité à vérifier avant installation ; données sensibles uniquement dans un groupe de confiance explicite. |
| [Hivemind](https://github.com/learning-at-home/hivemind) | Référence pour découverte et apprentissage décentralisé sur PyTorch. | P2 | Son rôle principal ne correspond pas à un moteur de chat grand public prêt à brancher. |
| [gRPC](https://github.com/grpc/grpc) | Messages typés, flux et délais pour un futur protocole privé. | P1 | Il reste à implémenter l’authentification, les limites, l’admission et les reprises de notre protocole. |
| [psutil](https://github.com/giampaolo/psutil) | Mesures des processus, mémoire et charge CPU sur plusieurs OS. | P1 | Observer n’impose pas de limite dure ; la VRAM et la mémoire unifiée demandent une stratégie propre au moteur. |
| [Prometheus](https://github.com/prometheus/prometheus) | Collecte des métriques du futur pilote. | P2 | À ajouter quand plusieurs vrais nœuds existent ; aucun prompt ni contenu de session dans les métriques. |
| [Headscale](https://github.com/juanfont/headscale) | Option de serveur de contrôle auto-hébergé pour un réseau privé utilisant des clients compatibles. | P2 | Ne remplace ni la confiance entre hôtes ni l’authentification applicative ; ce composant n’accélère pas Internet. |

## Références figées

Les identifiants ci-dessous fixent les révisions examinées. Ils ne constituent pas un ensemble de versions testé ensemble. Les licences sont les identifiants déclarés par les métadonnées GitHub ; les modèles ont leurs propres conditions.

| Projet | Révision examinée | Licence déclarée |
|---|---|---|
| Ollama | [c053d1e98537](https://github.com/ollama/ollama/commit/c053d1e98537f208b24165446369bd376a015999) | MIT |
| MLX | [fc344c986c41](https://github.com/ml-explore/mlx/commit/fc344c986c4169d99f76b5d95ae6b4a58a359a63) | MIT |
| llama.cpp | [ca89968a23a1](https://github.com/ggml-org/llama.cpp/commit/ca89968a23a13e571a6b802a9891d22763153b61) | MIT |
| exo | [a60b95698ca8](https://github.com/exo-explore/exo/commit/a60b95698ca81737d367443674dd5563cbc9559b) | Apache-2.0 |
| Petals | [22afba627a7e](https://github.com/bigscience-workshop/petals/commit/22afba627a7eb4fcfe9418c49472c6a51334b8ac) | MIT |
| Hivemind | [4bd43b778950](https://github.com/learning-at-home/hivemind/commit/4bd43b77895019b20d18d81d0d0c1a5ab9a10847) | MIT |
| gRPC | [952c8d46d905](https://github.com/grpc/grpc/commit/952c8d46d90530ddc497d22bdf4b4ccfce4e903c) | Apache-2.0 |
| psutil | [d187ee23b1a9](https://github.com/giampaolo/psutil/commit/d187ee23b1a909d7e371b519fec2cf621c50577f) | BSD-3-Clause |
| Prometheus | [dd7aa6b0f19f](https://github.com/prometheus/prometheus/commit/dd7aa6b0f19f4e952a55cbebd6e15458fe0ad9c6) | Apache-2.0 |
| Headscale | [48416ce0894e](https://github.com/juanfont/headscale/commit/48416ce0894ef7bef0ef9c064609b4aa76a0d9b6) | BSD-3-Clause |

Le fichier [software.json](../catalog/software.json) permet d’exploiter ce catalogue dans un site de présentation. Python 3.11+ est le seul prérequis des outils de base. NumPy 2.3.5 n’est requis que par l’expérience de sélection adaptative. SQLite est une option de journal local pour un futur prototype, pas une dépendance actuelle.

## Choix proposé pour commencer

1. Une référence locale avec un modèle déjà installé dans Ollama, ou une mesure directe du même format dans llama.cpp/MLX.
2. Des quotas et une admission indépendants du moteur.
3. Une comparaison de deux à quatre machines avec exo ou un moteur compatible, après vérification de leur support matériel.
4. Un adaptateur distribué seulement après cette comparaison. Ne pas installer toutes les briques ensemble par défaut.

Sources complémentaires : [API Ollama](https://docs.ollama.com/api/generate), [cloud désactivé](https://docs.ollama.com/faq), [gRPC Python](https://grpc.io/docs/languages/python/), [SQLite Python](https://docs.python.org/3/library/sqlite3.html).

