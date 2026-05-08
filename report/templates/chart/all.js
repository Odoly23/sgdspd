async function loadAll() {
  try {
    const urls = [
      "/API/Report/api/sexu/",
      "/API/Report/api/estado/",
      "/API/Report/api/umur/",
      "/API/Report/api/tahun/",
      "/API/Report/api/sexu-estado/",
       "/API/Report/api/edukasaun/"
    ];

    const responses = await Promise.all(urls.map(url => fetch(url)));

    const data = await Promise.all(responses.map(r => {
      if (!r.ok) throw new Error("API error: " + r.url);
      return r.json();
    }));

    const [rSexu, rCivil, rUmur, rTinan, rGabung, rEdu] = data;

    // ================= SAFE TOTAL =================
    const total = (rSexu.obj || []).reduce((a, b) => a + b, 0);

    const pctMane = document.getElementById('pct-mane');
    const pctFeto = document.getElementById('pct-feto');

    if (pctMane && pctFeto && total > 0) {
      pctMane.textContent = Math.round((rSexu.obj[0] || 0) / total * 100) + '%';
      pctFeto.textContent = Math.round((rSexu.obj[1] || 0) / total * 100) + '%';
    }

    // ================= DESTROY OLD CHART =================
    function createChart(id, config) {
      const el = document.getElementById(id);
      if (!el) return;

      if (el.chart) {
        el.chart.destroy();
      }

      el.chart = new Chart(el, config);
    }

    // ================= SEXU =================
    createChart('cSexu', {
      type: 'doughnut',
      data: {
        labels: rSexu.label || [],
        datasets: [{
          data: rSexu.obj || [],
          backgroundColor: ['#378ADD','#D4537E'],
          borderWidth: 1.5,
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        cutout: '60%',
        plugins: { legend: { display: false } }
      }
    });

    // ================= ESTADO CIVIL =================
    createChart('cCivil', {
      type: 'bar',
      data: {
        labels: rCivil.label || [],
        datasets: [{
          data: rCivil.obj || [],
          backgroundColor: ['#B5D4F4','#85B7EB','#378ADD','#185FA5'],
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: 'rgba(0,0,0,0.05)' } }
        }
      }
    });

    // ================= UMUR =================
    createChart('cUmur', {
      type: 'bar',
      data: {
        labels: rUmur.label || [],
        datasets: [{
          data: rUmur.obj || [],
          backgroundColor: '#1D9E75',
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: 'rgba(0,0,0,0.05)' } }
        }
      }
    });

    // ================= TAHUN =================
    createChart('cTinan', {
      type: 'line',
      data: {
        labels: rTinan.label || [],
        datasets: [{
          data: rTinan.obj || [],
          borderColor: '#7F77DD',
          backgroundColor: 'rgba(127,119,221,0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.35
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: 'rgba(0,0,0,0.05)' } }
        }
      }
    });

    // ================= SEXU + CIVIL =================
    createChart('cGabung', {
      type: 'bar',
      data: {
        labels: rGabung.label || [],
        datasets: [
          {
            label: 'Mane',
            data: rGabung.mane || [],
            backgroundColor: '#378ADD',
            borderRadius: 4
          },
          {
            label: 'Feto',
            data: rGabung.feto || [],
            backgroundColor: '#D4537E',
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: 'rgba(0,0,0,0.05)' } }
        }
      }
    });
    createChart('cEdu', {
      type: 'bar',
      data: {
        labels: rEdu.label || [],
        datasets: [{
          data: rEdu.obj || [],
          backgroundColor: '#378ADD',
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          x: {
            grid: {
              display: false
            }
          },
          y: {
            grid: {
              color: 'rgba(0,0,0,0.05)'
            }
          }
        }
      }
    });

  } catch (error) {
    console.error("ERROR LOAD CHART:", error);
  }
}

// ================= AUTO LOAD =================
document.addEventListener("DOMContentLoaded", loadAll);