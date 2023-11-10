const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/main/'
    
);


let last_user ;



socket.onmessage = function(e){
    const data = JSON.parse(e.data);

    var full_name = data.full_name;
    var uuid = data.uuid;

    

    if (last_user != full_name) {

        var c = `لقد نشر ${full_name} حالة جديدة هل تريد مشاهدة الحالة ؟`
        var msg = confirm(c);
        if (msg){
            window.location.href = '/status/' + uuid
        }
        
        last_user = full_name;
    }

}

