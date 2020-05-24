function displayCookies() {
    var fname = getCookie("firstname");
    if (fname == null) {
        fname = "";
    }
    if (fname != "") {
        fname = "firstname=" + fname;
    }
    var lname = getCookie("lastname");
    if (lname == null) {
        lname = "";
    }
    if (lname != "") {
        lname = "; lastname=" + lname;
    }
    alert(fname + lname);
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
} 
