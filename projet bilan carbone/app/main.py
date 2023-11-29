from fastapi import FastAPI
import csv
from datetime import datetime

app = FastAPI()

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
                     "Ferry de jour":{"2019": 0.979}
                     }

def calculer_distance_annuelle_par_mode_transport(fichier_csv):
    '''
    Description de la fonction: cette fonction calcule la distance annuelle parcourue pour chaque mode de transport
    Args:
    parametre1 (csv): fichier csv qui contient les informations de l'entreprise sur les deplacements professionels
    returns:
    dict: dictionaire contenant les distances parcourues par an et par mode de transport
    
    '''
    distance_annuelle_par_transport_plus_annee = {}
    mode_transport = ''
    distance = 0.0
    with open(fichier_csv, newline='') as csv_file:
        lecteur_csv = csv.DictReader(csv_file)
        
        for line in lecteur_csv:
            date = datetime.strptime(line['Date'], "%d/%m/%Y")
            annee = date.year
            mode_transport = line['Mode de transport']
            distance = float(line['Distance'])
            if annee in distance_annuelle_par_transport_plus_annee:
                if mode_transport in distance_annuelle_par_transport_plus_annee[annee].keys():
                    distance_annuelle_par_transport_plus_annee[annee][mode_transport] += distance
                else:
                    distance_annuelle_par_transport_plus_annee[annee][mode_transport] = distance
            else:
                distance_annuelle_par_transport_plus_annee[annee] = {mode_transport:distance}
               
    return distance_annuelle_par_transport_plus_annee


@app.get('/co2GenereParDeplacementsPro')
def calculer_quantite_annuelle_de_co2_induite():
    fichier_csv = 'csv/test.csv'
    distance_annuelle_par_transport_plus_annee = calculer_distance_annuelle_par_mode_transport(fichier_csv)
    taux_annuel_de_co2 = 0.0
    taux_annuel_de_co2_par_moyen_de_transport = {}
    try:
        for annee in distance_annuelle_par_transport_plus_annee.keys():
            for moyen_de_transport in distance_annuelle_par_transport_plus_annee[annee].keys():
                if ((moyen_de_transport in facteurs_emission.keys()) and (str(annee) in facteurs_emission[moyen_de_transport].keys())):
                    taux_co2_par_moyen_de_transport = distance_annuelle_par_transport_plus_annee[annee][moyen_de_transport] * facteurs_emission[moyen_de_transport][str(annee)]
                    if annee not in taux_annuel_de_co2_par_moyen_de_transport.keys():
                        taux_annuel_de_co2_par_moyen_de_transport[annee] = {moyen_de_transport: taux_co2_par_moyen_de_transport}
                    else:
                        taux_annuel_de_co2_par_moyen_de_transport[annee][moyen_de_transport] = taux_co2_par_moyen_de_transport
    
    except:
        print("le facteur d'émission correspondant au ",moyen_de_transport, "pour l'année ",annee,"n'est pas disponible")
    return taux_annuel_de_co2_par_moyen_de_transport
