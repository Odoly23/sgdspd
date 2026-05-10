setInterval(function(){
    $.get('/api/notif/docente/monitoring/internship/social/tot/',function(data) {
        document.getElementById("notifinternshipdocentesocialtot").innerHTML = data.value;

    });
}, 1000);
console.log(data.value)