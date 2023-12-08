from fastapi import FastAPI
import csv
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#permets d'autoriser des requetes venant de notre frontend etant données 
#qu'il a des origines differentes de celles du backend 
origins = [
    "http://localhost",
    "http://localhost:1234",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#on configure fastapi pour servir les fichiers statiques depuis le dossier frontend
#app.mount("/static", StaticFiles(directory="/app/frontend"), name="static")

#les facteurs d'emission liés aux transports
facteurs_emission = {"Avion court courrier,sans traînées":{"2022":0.1416, "2020":0.1412},
                     "Avion moyen courrier,sans traînées":{"2022":0.1027, "2020":0.1023},
                     "Avion long courrier,sans traînées":{"2022":0.0833, "2020":0.083},
                     "Avion court courrier,avec traînées":{"2022":0.2586, "2020":0.2582},
                     "Avion moyen courrier,avec traînées":{"2022":0.1875, "2020":0.1871},
                     "Avion long courrier,avec traînées":{"2022":0.152, "2020":0.1517},
                     "TGV":{"2021":0.0033, "2019":0.0023,"2018":0.0025},
                     "train courte distance":{"2019":0.018},
                     "train international":{"2019":0.037},
                     "train mixe":{"2019":0.016},
                     "RER Transilien":{"2021":0.0094,"2019":0.0073,"2018":0.0077},
                     "Tram moyenne ville":{"2018":0.005},
                     "Tram grande ville":{"2018":0.0033},
                     "Métro Ile de France":{"2021":0.004,"2019":0.0027,"2018":0.0028},
                     "Autocar - trajets intercités":{"2021": 0.0306,"2020":0.0364},
                     "Autobus moyen grande ville":{"2021":0.137,"2019":0.146,"2014":1.9698},
                     "Autobus moyen petite ville":{"2021":0.146,"2019":0.156},
                     "Ferry de jour":{"2019": 0.979},
                     "Voiture a motorisation essence":{"2018":0.2234},
                     "Voiture a motorisation gazole":{"2018": 0.2121},
                     "Voiture a motorisation moyenne":{"2018":0.2156},
                     "Voiture a motorisation GPL":{"2018":0.2174},
                     "Voiture a motorisation GNV":{"2018":0.2218},
                     "Voiture a motorisation E85":{"2018":0.1467},
                     "Voiture hybride":{"2020": 0.1828},
                    "Voiture ellectrique":{"2020": 0.1034},
                    "Moto >= 250 cm3 mixte":{"2018":0.1913, "2015":0.2037},
                    "Byciclette musculaire":{"2019":0.005},
                    "VAE, bicyclette a assistance électrique":{"2020":0.0109},
                    "Trotinette electrique":{"2020":0.0249},
                    "avion Essence aviation (AvGas) France continentale":{"2014":3.0113},
                    "Helicoptere Essence aviation (AvGas) France continentale":{"2014":3.0113},
                    "Avion Kérosène Jet A1 ou A France continentale":{"2018":3.0791},
                    "Helicopter Kérosène Jet A1 ou A France continentale":{"2014":3.0791},
                    "Bateau Essence - Supercarburant":{"2021":6.5051, "2016":4.4863},
                    "HFO":{"2014":2.9329},
                    "LFO":{"2014":3.0506},
                    "MDO":{"2014":3.0506},
                    "Bateau oceanographique avec couchage à bord":{"2019": 910},
                    "Bateau oceanographique local sans couchage à bord":{"2019": 7.6}
                     }

def valeur_co2_correspondant_au_mode_transport(mode_transport,annee):
    """
    Description: retourne le facteur d'emission du moyen de transport passé en parametre.
    Args:
    mode_transport(str): mode transport.
    annee (int): l'anné pour laquelle on desire récuperer le facteur d'émission.
    Returns:
    int : facteur d'émission du mode de transport.
    """
    valeur_co2_facteur_emission = 0.0
    str_annee = str(annee)
    for key in facteurs_emission.keys():
        if key == mode_transport and (str_annee in facteurs_emission[mode_transport].keys()):
            valeur_co2_facteur_emission = facteurs_emission[key][str_annee]
            break
    return valeur_co2_facteur_emission 


@app.get('/get_travel_ghg_emission')
def calculer_quantite_annuelle_de_co2_deplacements_pro():
    """
    Description: retourne la valeur totale de co2 groupé par année et par object de mission.
    Args: None
    Returns:
    dict : un dictionnaire contenant les quantités totales de co2 émises par annéé et par ordre de mission.
    """
    fichier_csv = 'csv/Deplacements.csv' #fichier csv produit par le SI-Deplacement
    mode_transport =''
    distance = 0.0
    quantite_annuelle_de_co2_deplacements_pro = {}
    with open(fichier_csv, newline='') as csv_file:
        lecteur_csv = csv.DictReader(csv_file)
        for line in lecteur_csv:
            date = datetime.strptime(line['Date'], "%d/%m/%Y")
            annee = date.year
            mode_transport = line['Mode de transport']
            distance = float(line['Distance'])
            object_mission = line['Objet mission']
            #on calcule la distance totale parcourue en considerant le fait que le chemin a été parcourue en allé et retour
            distance_totale = distance * 2
            valeur_co2 = valeur_co2_correspondant_au_mode_transport(mode_transport,annee)
            quantité_annuelle_co2 = distance_totale * valeur_co2
            if annee not in quantite_annuelle_de_co2_deplacements_pro.keys():
                quantite_annuelle_de_co2_deplacements_pro[annee]= {object_mission:quantité_annuelle_co2}
            else:
                if object_mission in quantite_annuelle_de_co2_deplacements_pro[annee].keys():
                    quantite_annuelle_de_co2_deplacements_pro[annee][object_mission]+= quantité_annuelle_co2
                else:
                    quantite_annuelle_de_co2_deplacements_pro[annee][object_mission] = quantité_annuelle_co2
    
    return quantite_annuelle_de_co2_deplacements_pro    


@app.get('/get_commuting_ghg_emission')
def calculer_quantite_co2_deplacement_domicile_travavail():
    """
    Description: retourne la valeur totale de co2 groupé par année et par service.
    Args: None
    Returns:
    dict : un dictionnaire contenant les quantités totales de co2 émises par annéé et par service.
    """
    fichier_csv = 'csv/RH.csv'  #fichier csv produit par le SI-RH 
    quantite_co2_deplacement_domicile_travavail = {}
    with open(fichier_csv, newline='') as csv_file:
        lecteur_csv = csv.DictReader(csv_file)
        for line in lecteur_csv:
            annee = line['Année']
            distance = int(line['Distance domicile travail'])
            mode_transport = line['Mode de transport']
            nombre_jours = int(line['Nombre de jours travaillé'])
            service = line['Service']
            distance_annuelle = distance * nombre_jours * 2
            #on calcule la valeur de co2 equivalent à la distance annuelle parcourue
            valeur_co2 = valeur_co2_correspondant_au_mode_transport(mode_transport,annee)
            valeur_annuelle_co2 = distance_annuelle * valeur_co2
            if annee not in quantite_co2_deplacement_domicile_travavail.keys():
                quantite_co2_deplacement_domicile_travavail[annee] ={service:valeur_annuelle_co2}
            else:
                if service in quantite_co2_deplacement_domicile_travavail[annee].keys():
                    quantite_co2_deplacement_domicile_travavail[annee][service]+=valeur_annuelle_co2
                else:
                    quantite_co2_deplacement_domicile_travavail[annee][service] = valeur_annuelle_co2
    
    return quantite_co2_deplacement_domicile_travavail
