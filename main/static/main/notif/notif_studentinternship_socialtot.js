setInterval(function(){
    $.get('/api/notif/student/internship/social/tot/',function(data) {
        document.getElementById("notifinternshipstudentsocialtot").innerHTML = data.value;

    });
}, 1000);
console.log(data.value)