fetch('/API/Report/mem/mun/')
.then(response => response.json())
.then(data => {

    Highcharts.mapChart('container-map', {
        accessibility: {
            enabled: false
        },

        chart: {
            map: 'countries/tl/tl-all'
        },

        title: {
            text: 'Total Dadus Companeiro Kada Munisipiu'
        },

        mapNavigation: {
            enabled: true,
            buttonOptions: {
                verticalAlign: 'bottom'
            }
        },

        colorAxis: {
            min: 0
        },

        series: [{
            data: data,   
            joinBy: 'hc-key',

            name: 'Total Companeiros',

            states: {
                hover: {
                    color: '#BADA55'
                }
            },

            dataLabels: {
                enabled: true,
                format: '{point.name}'
            },

            tooltip: {
                pointFormatter: function () {
                    return `<b>${this.name}</b><br/>Total Alumni: ${this.value || 0}`;
                }
            }
        }]
    });

});