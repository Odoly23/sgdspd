setInterval(function(){
    $.get('/api/notif/student/internship/social/',function(data) {
        document.getElementById("notifinternshipstudentsocial").innerHTML = data.value;

    });
}, 1000);
console.log(data.value)