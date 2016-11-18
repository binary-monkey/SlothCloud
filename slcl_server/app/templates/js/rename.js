function rename(oldf){
    /*
     * TODO: Fix jQuery so it knows where the mouse right-clicked
     */
    oldf += get_text();
    console.log("oldf:")
    console.log(oldf.replace(/[^\w\s]/gi, ''))
    if (oldf.replace(/[^\w\s]/gi, '') == "") {
        alert("Incorrect file.");
        return;
    }
    console.log(oldf)
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
    var furl = oldf;
    console.log("OLDF: " + oldf)
    console.log("NEWF: " + newf)
    console.log( "{{ url_for('rename', old='') }}" + oldf + "&new=" + newf);
    var err = request.open("GET", "{{ url_for('rename', old='') }}" + oldf + "&new=" + newf, true);
    request.send(null);
    window.location = window.location;
}