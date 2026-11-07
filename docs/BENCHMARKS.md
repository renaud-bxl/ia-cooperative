# Mesurer avant de promettre

## Première mesure locale

Installer Ollama depuis sa source officielle si nécessaire et choisir un modèle local déjà téléchargé. Configurer le serveur avec `OLLAMA_NO_CLOUD=1`, puis le redémarrer. La [FAQ officielle](https://docs.ollama.com/faq) décrit aussi l’option `disable_ollama_cloud` du fichier serveur. Le script ne modifie pas cette configuration et ne vérifie pas cryptographiquement le fonctionnement local.

```bash
ollama list
python3 benchmarks/ollama_local.py --model NOM_EXACT_DE_LA_LISTE --out measurements/premier-essai.json
```

Le programme envoie un texte synthétique public au serveur `127.0.0.1:11434`. Il n’installe et ne télécharge aucun modèle. Il effectue un échauffement, puis trois mesures. Les textes produits ne sont pas enregistrés. Le nom du modèle, son empreinte, la version du moteur, les options et les compteurs sont conservés. Le nom d’une sortie existante est refusé pour préserver les observations.

Le temps du premier texte visible est distinct du premier événement d’activité, qui peut être du raisonnement. `num_predict=64` plafonne la génération sans garantir exactement 64 tokens. Le débit fourni par le serveur n’est pas le débit de bout en bout. Le même prompt répété peut bénéficier d’un cache : relever les compteurs et ne pas assimiler ce test à un préremplissage entièrement neuf.

Ce client et son parseur sont fournis ; **aucun modèle réel n’a été exécuté dans la validation du présent dépôt**. Les tests utilisent des flux synthétiques. Ni RAM maximale ni énergie ne sont encore mesurées par ce client.

## Comparaison distribuée à réaliser

Garder modèle, révision, quantification, tokenizer et tâches identiques. Comparer 1, 2 puis 4 machines. Mesurer : premier token, réponse complète, tokens réellement produits, pics mémoire par processus et appareil, octets réseau, qualité et consommation à la prise. Distinguer démarrage à froid, poids chargés, contexte réutilisé et contexte nouveau.

Introduire ensuite plusieurs utilisateurs, une déconnexion, une reprise d’activité et un lien lent. Conserver les échecs et le temps des reprises. Choisir le niveau de service attendu avant de sélectionner le meilleur moteur.

## Simulations existantes

Les résultats de `experiments/` restent des calculs synthétiques. Les huit scénarios de file représentent 160 000 demandes ; certains dépassent 100 % de charge offerte et ne disposent pas d’un régime stable. Leur P95 dépend de la durée de l’expérience. Les métriques du futur benchmark matériel ne doivent pas écraser ces JSON de référence.

Source des champs API : https://docs.ollama.com/api/generate
