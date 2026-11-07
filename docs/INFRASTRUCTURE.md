# Faut-il une infrastructure extérieure ?

**Le calcul peut s’exécuter de machine en machine.** L’application graphique est locale. Un serveur central qui héberge toute l’IA n’est pas indispensable à l’architecture envisagée.

| Situation | Calcul | Services auxiliaires |
|---|---|---|
| Deux à quatre ordinateurs sur le même réseau | Directement sur les participants | Réseau local et modèle déjà téléchargé ; pas de service extérieur indispensable pendant le calcul |
| Plusieurs logements | Direct entre pairs lorsque les connexions le permettent | Adresses connues ou rendez-vous ; parfois relais à cause des routeurs |
| Réseau international accessible simplement | Groupes de calcul adaptés aux connexions | Plusieurs points de rendez-vous et capacité de relais, avec supervision et gestion des versions |

Un rendez-vous est un carnet d’adresses qui aide les machines à se trouver. Un relais transporte les échanges quand elles ne peuvent pas communiquer directement. Ni l’un ni l’autre n’a besoin d’héberger tout le modèle. Des machines de participants peuvent remplir ces rôles si elles sont accessibles, autorisées et suffisamment disponibles.

Un petit serveur administré reste une option pratique pour fournir une adresse stable. Ce n’est pas une obligation d’acheter un centre de données. Inversement, si toutes les machines sont derrière des réseaux qui empêchent le contact direct, il faut un intermédiaire accessible : on ne peut pas garantir une connexion universelle sans prévoir cette possibilité.

## Ce qui doit rester local

Les préférences, les clés privées et le contrôle du partage. Le coordinateur d’une demande peut tourner sur la machine qui la lance. Le calcul suit les participants retenus ; les conversations sensibles ne sont admises que dans un cercle approprié ou restent sur une machine.

## Ce qui peut nécessiter une disponibilité collective

Les points de rendez-vous, le catalogue signé de versions, les paquets d’installation et parfois les relais. Les fichiers peuvent être distribués par un hébergeur, par les pairs ou copiés hors ligne. Le premier téléchargement peut peser plusieurs gigaoctets ; une fois les composants présents, un essai local peut fonctionner sans accès Internet.

## Plan retenu

1. Essai local : aucun cloud de calcul, deux à quatre machines.
2. Essai entre deux ou trois adresses : mesurer liens directs, relais, débit montant et déconnexions.
3. Réseau élargi : répéter rendez-vous et services auxiliaires, mesurer leurs coûts et tester leur panne.

Les offres de Tailscale ou une installation Headscale sont des moyens possibles d’établir un réseau privé pour le pilote. Elles n’apportent pas automatiquement notre moteur distribué, son interface ni sa politique de quotas. Le recours éventuel à ces services doit apparaître dans l’interface ; il ne doit pas être présenté comme une indépendance complète de tout tiers.
