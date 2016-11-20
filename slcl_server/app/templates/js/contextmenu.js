/*
 * TODO: Hide contextmenu when not hover or in contextmenu.
 */
function ShowMenu(control, e) {
    $(document).mousedown(function(event) {
        if( e.button == 2 ) {
        auxtext = $(event.target).text();
            if (auxtext != "Rename")
                text = auxtext.replace(/^\s+|\s+$/g, '');
//                console.log(text)
        }
    });
    if (get_text() == "")
    return;
     // left position of pointer
    var posx = e.clientX +window.pageXOffset +'px';
    // top position of pointer
    var posy = e.clientY + window.pageYOffset + 'px';
    document.getElementById(control).style.position = 'absolute';
    document.getElementById(control).style.display = 'inline';
    document.getElementById(control).style.left = posx;
    document.getElementById(control).style.top = posy;
}
function HideMenu(control) {
    document.getElementById(control).style.display = 'none';
}