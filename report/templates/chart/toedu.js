async function loadEduSukuChart() {
    try {
        const response = await fetch("{% url 'api-edu-suku' %}");
        const resData = await response.json();

        const ctx = document.getElementById('chartEduSuku').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: resData.labels, 
                datasets: resData.datasets 
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { stacked: true }, // Menumpuk ke atas
                    y: { stacked: true, beginAtZero: true }
                },
                plugins: {
                    legend: { position: 'bottom' },
                    title: {
                        display: true,
                        text: 'Nivel Edukasaun bazeia ba Suku'
                    }
                }
            }
        });
    } catch (error) {
        console.error("Erro load grafiku edukasaun:", error);
    }
}

document.addEventListener('DOMContentLoaded', loadEduSukuChart);
