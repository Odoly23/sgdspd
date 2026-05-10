setInterval(function(){
    $.get('/api/notif/docente/monitoring/internship/social/',function(data) {
        document.getElementById("notifinternshipdocentesocial").innerHTML = data.value;

    });
}, 1000);
console.log(data.value)