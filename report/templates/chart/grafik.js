    new Chart(document.getElementById("barChart"), {
        type: 'bar',
        data: {
            labels: {{ muni_labels|safe }},
            datasets: [{
                label: 'Membru',
                data: {{ muni_data|safe }}
            }]
        }
    });

    // ================= PIE =================
    new Chart(document.getElementById("pieChart"), {
        type: 'pie',
        data: {
            labels: ['Mane', 'Feto'],
            datasets: [{
                data: [{{ male_count }}, {{ female_count }}]
            }]
        }
    });

    // ================= LINE =================
    new Chart(document.getElementById("lineChart"), {
        type: 'line',
        data: {
            labels: {{ year_labels|safe }},
            datasets: [{
                label: 'Growth',
                data: {{ year_data|safe }},
                fill: false
            }]
        }
    });

