import Chart from 'chart.js/auto'
import { createAnnualEmissionsChart } from './api'
import { getdataFromServer } from './api'

const url = 'http://localhost/get_travel_ghg_emission';
//get_travel_ghg_emission  get_commuting_ghg_emission
async function fetchDataAndCreateChart() {
    try {
        const data = await getdataFromServer(url);
        createAnnualEmissionsChart(data); // Utilisez les données récupérées pour créer le graphique
    } catch (error) {
        console.error('Erreur lors de la récupération ou de la création du graphique :', error);
    }
}

fetchDataAndCreateChart();



