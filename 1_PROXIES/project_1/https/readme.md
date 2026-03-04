# Notes:

### Client
* se connecte au proxy
* envoie une requête HTTP
* le proxy ouvre une connexion TCP vers le serveur cible
* forward les bytes
----
* ouvrir un socket TCP
* te connecter au proxy
* envoyer une requête HTTP brute (string)
* lire la réponse brute


### Server

* Un TCP proxy transport ne reçoit PAS une URL.
* Il reçoit une connexion TCP déjà établie.


