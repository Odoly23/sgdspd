// Inisialisasi Grafik
  const ctx = document.getElementById('chartSukuStatus').getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'bar', // Grafik Kolom
    data: {
      labels: [], // Akan diisi dari API
      datasets: [] // Akan diisi dari API
    },
    options: {
      indexAxis: 'y', // Ubah ke 'x' jika ingin batang berdiri tegak
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom' }
      },
      scales: {
        x: { stacked: false, beginAtZero: true },
        y: { stacked: false }
      }
    }
  });

  // Fungsi memanggil API
  async function fetchData() {
    try {
      const response = await fetch("{% url 'api-sumariu-suku' %}");
      const data = await response.json();

      myChart.data.labels = data.labels;
      myChart.data.datasets = [
        {
          label: 'Ativu',
          data: data.ativu,
          backgroundColor: '#198754'
        },
        {
          label: 'La Ativu',
          data: data.la_ativu,
          backgroundColor: '#ffc107'
        },
        {
          label: 'Mate',
          data: data.mate,
          backgroundColor: '#dc3545'
        }
      ];
      myChart.update();
    } catch (error) {
      console.error("Gagal mengambil data API:", error);
    }
  }

  // Jalankan fungsi
  fetchData();