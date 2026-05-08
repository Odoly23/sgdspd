async function loadStatusSukuTinan() {
    try {
        const response = await fetch("{% url 'api-tinan' %}"); 
        const resData = await response.json();

        const ctx = document.getElementById('chartStatusSuku');
        if (!ctx) return;

        new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                // Sumbu X: Nama Suku di atas, Tahun di bawahnya
                labels: resData.labels.map(suku => [suku, resData.tinan]),
                datasets: resData.datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Status Membru bazeia ba Suku iha Tinan ' + resData.tinan
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            font: { size: 10 }
                        }
                    },
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error("Erro load grafiku:", error);
    }
}

document.addEventListener('DOMContentLoaded', loadStatusSukuTinan);
