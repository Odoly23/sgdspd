function createHighcharts(data) {
  Highcharts.setOptions({
    lang: {
      thousandsSep: ","
    }
  });
  Highcharts.chart("chart", {
    title: {
      text: "DataTables to Highcharts"
    },
    subtitle: {
      text: "Data from worldometers.info"
    },
    xAxis: [
      {
        categories: data[0],
        labels: {
          rotation: -45
        }
      }
    ],
    yAxis: [
      {
        // first yaxis 
        title: {
          text: "Population (2017)"
        }
      },
      {
        // secondary yaxis 
        title: {
          text: "Density (P/Km²)"
        },
        min: 0,
        opposite: true
      }
    ],
    series: [
      {
        name: "Population (2017)",
        color: "#0071A7",
        type: "column",
        data: data[1],
        tooltip: {
          valueSuffix: " M"
        }
      },
      {
        name: "Density (P/Km²)",
        color: "#FF404E",
        type: "spline",
        data: data[2],
        yAxis: 1
      }
    ],
    tooltip: {
      shared: true
    },
    legend: {
      backgroundColor: "#ececec",
      shadow: true
    },
    credits: {
      enabled: false
    },
    noData: {
      style: {
        fontSize: "16px"
      }
    }
  });
}