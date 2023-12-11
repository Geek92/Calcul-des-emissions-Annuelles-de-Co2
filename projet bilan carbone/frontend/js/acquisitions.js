import Chart from 'chart.js/auto'
import { createAnnualEmissionsChart } from './api'
import { getdataFromServer } from './api'

//get_travel_ghg_emission  get_commuting_ghg_emission
const url_domicile_travail = 'http://localhost/get_commuting_ghg_emission';
const url_deplacements_pro = 'http://localhost/get_travel_ghg_emission';
const selectedElement = document.getElementById('selection');
let chartStatus = null;

//fonction qui recupere les données provenants de backend et genere le graphe
async function fetchDataAndCreateChart() {
    try {
        let url = '';
        const selectedValue = selectedElement.value;
        if (selectedValue.toLowerCase() === "deplacements_pro") {
            url = url_deplacements_pro;
        } else {
            url = url_domicile_travail;
        }
        const data = await getdataFromServer(url);
        chartStatus = Chart.getChart("acquisitions");
        if (chartStatus != undefined) {
            chartStatus.destroy();
        }
        //on utilise les données récupérées pour créer le graphique
        createAnnualEmissionsChart(data);

    } catch (error) {
        console.error('Erreur lors de la récupération ou de la création du graphique :', error);
    }
}
selectedElement.addEventListener('change', fetchDataAndCreateChart);




