function loadNotif() {
    $.get('/API/Membru/api/notif/badge/', function(data) {
        var badge = document.getElementById('notifbadge');
        if (data.value > 0) {
            badge.innerHTML = data.value;
            badge.style.display = 'inline';
        } else {
            badge.style.display = 'none';
        }
    });

    $.get('/API/Membru/api/notif/items/', function(data) {
        var container = document.getElementById('notif-items');
        if (data.items && data.items.length > 0) {
            var html = '';
            data.items.forEach(function(item) {
                html += '<a class="dropdown-item" href="' + item.url + '">' +
                        item.label +
                        ' (<strong>' + item.count + '</strong>)' +
                        '</a>';
            });
            container.innerHTML = html;
        } else {
            container.innerHTML = '<a class="dropdown-item text-muted"><em>Laiha notifikasaun.</em></a>';
        }
    });
}

loadNotif();
setInterval(loadNotif, 10000);