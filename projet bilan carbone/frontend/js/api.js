import Chart from 'chart.js/auto'

//cette fonction effectue une requette au serveur à partir de l'url passée en parametre 
//et renvoie les données fournies par le serveur 
export async function getdataFromServer(url) {

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Erreur de reseau ou probleme aavec la requete');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erreur lors de la récupération des données :', error);
        throw error;
    }
}

export async function createAnnualEmissionsChart(data) {
    try {

        // on crée des tableaux distincts pour les labels (années) et les datasets (valeurs par client et ou service) 
        const labels = Object.keys(data);
        const datasets = [];

        // Sélectionner le client ou le service ayant le plus de données
        let maxDataCount = 0;
        let exactCategory = '';
        for (const year of labels) {
            const dataCount = Object.keys(data[year]).length;
            if (dataCount > maxDataCount) {
                maxDataCount = dataCount;
                exactCategory = year;
            }
        }
        // on crée un dataset pour chaque client ou service
        for (const item in data[exactCategory]) {
            const itemValues = Object.values(data).map(yearData => yearData[item] || 0);
            const backgroundColors = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.6)`;

            datasets.push({
                label: item,
                data: itemValues,
                backgroundColor: backgroundColors,
                borderWidth: 1
            });
        }

        const ctx = document.getElementById('acquisitions').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Valeur CO2'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Année'
                        }
                    }
                }
            }
        });
        //return myChart;
    } catch (error) {
        console.error('Erreur lors de la création du diagramme :', error);
    }
}


