function rename(oldf){
    /*
     * TODO: Fix jQuery so it knows where the mouse right-clicked
     */
    $(document).click(function(event) {
        var text = $(event.target).text();
    });

    if (oldf.replace(/[^\w\s]/gi, '') == "") {
        alert("Incorrect file.");
        return;
    }
    var permitted_chars = " /-_.";
    var newf = prompt("New relative path (name) to file:");
    newf = newf.replace(/[\w\s].concat([permitted_chars])/gi, ''); // remove all unsafe characters
    newf = newf.replace("//", "/");
    newf = newf.replace("\\\\", "\\");
    newf = newf.replace("\\", "/");
    if (newf.replace(/["/\\. "]/, '') == ''){
        alert("Invalid folder name.");
        return;
    }
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (request.readyState === 4) {
            if (request.status === 200) {
                document.body.className = 'ok';
                var err = request.responseText;
                err ? alert(err) : "";
            } else {
                document.body.className = 'error';
            }
        }
    };
    console.log( "{{ url_for('rename', old=oldf, new=newf) }}" );
    var furl = oldf + text;
    var err = request.open("GET", "{{ url_for('rename', old=furl, new=newf)}}" , true);
    request.send(null);
    window.location = window.location;
}
