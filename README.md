# projet EES

# Application pour le calcul des emissions  Annuelles de Co2  liées aux déplacements

## Description 

ce projet a été réalise dans le cadre de la matiere Enjeux Environnementaux et Société. Il s'agit d 'une application de type **tableau de bord** qui permets aux differentes organisations (université, entreprise) de  calculer les quantités de gas à effet de serre induits par les déplacements professionnels de l’organisation ainsi que les émissions de co2 qui sont nécessaires aux déplacements domicile-travail de ses personnels.

##  Structure du projet
le projet est divisé len deux grandes parties:
- le  front-end
- le back-end
### le back-end
il  s'agit d 'une API realisée en python à travers l'utilisation du framework **Fast Api** , et se compose esentiellement de deux services.
- Un premier service ``` @app.get('/get_travel_ghg_emission')
defcalculer_quantite_annuelle_de_co2_deplacements_pro():```
qui récupere dans le fichier **csv/Deplacements.csv**  la totalité des déplacements liées aux differents objets de mission, calcule et renvoie la quantité annuelle de CO2 induite par les déplacements professionels pour chaque ordre de mission.
la formule utilisée pour le calcul est la suivante :
**émission = distance parcourue annuellement * facteur d’émission du mode de transport**.


-  Un deuxieme service ``` @app.get('/get_commuting_ghg_emission')
def  calculer_quantite_co2_deplacement_domicile_travavail():```
qui récupere dans le fichier **csv/RH.csv**  l'ensemble des  déplacements domicile-travail  pour chaque service  de l'organisation. A partir de ces informations, il calcule et renvoie la quantité annuelle de CO2 induite par les déplacements domicile -travail pour chaque service.
la formule utilisée pour le calcul est la suivante :
**émission = distance parcourue annuellement * facteur d’émission du mode de transport**.

### le front-end

 [il se présente comme suit](frontend/img/captureFront.png)

il effectue des requetes à lApi en fonction des informations qu'on souhaite afficher et présente les données renvoyées sous forme de graphe. Celui a ètè realisé en **(Javascript, Html,Css)**. Pour l'affichage des graphes nous avons utilisé la librerie **Chart.js** et enfin pour géree la configuration et l'assemblage des fichiers nous avons utilisé l'outil de bundling **Parcel.js**.

le déploement et l'exécution de l'application se fait à travers l'utilisation de docker.

### Politique d'affichage des données au niveau du frontend
Concernant l'affichage des données, nous avons choisi d'adopter une perspective de type "top-down", c'est-à-dire que la présentation des données ne se focalise pas sur un individu ou un département précis au sein de l'organisation, mais plutôt sur toute l'organisation. De ce fait, nous présentons un aperçu de la totalité du dataset au niveau du front-end.

### installation et deploiement du projet
- cloner le repos ce repertoire 
- executer la commande docker-compose build
- executer la commande docker-compose up 
- se rendre à l'adresse http://localhost:1234/