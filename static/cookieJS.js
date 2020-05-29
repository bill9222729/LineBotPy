 //以下為發送一個json到sendjson取得資料的ajsx範例
 $(document).ready(function() {
    var data = {
        data: JSON.stringify({
            "lesson": "Operation System",
            "score": 100
        })
    }
    $.ajax({
        url: "/sendjson",
        type: 'POST',
        data: data,
        success: function(msg) {
            alert(msg.name);
            alert(msg.lesson);
            alert(msg.score);
        }
    })
    $.ajax({
            url: "/getSQL",
            type: 'POST',
            data: data,
            success:function(msg) {
                for(i=1 ; i<msg.name.split(',').length ; i++){
                    $(".product").append("<p>"+msg.name.split(',')[i]+"</p>");
                }
                alert(msg.name.split(',')[1]);
            }
            })
    $(".aa").click(function(){
        $.ajax({
            url: "/getSQL",
            type: 'POST',
            data: data,
            success:function(msg) {
                for(i=1 ; i<msg.name.split(',').length ; i++){
                    $(".product").append("<p class=\"bb\">"+msg.name.split(',')[i]+"</p>");
                }
                alert(msg.name.split(',')[1]);
            }
        })
    });
    $("#change_name").click(function(){
        var name_data = {
        data: JSON.stringify({
            "name": $("#change").val(),
        })
        }
        $.ajax({
            url: "/setSQL",
            type: "POST",
            data: name_data,
            success:function(msg) {
                    if(msg == "OK"){
                        alert("修改成功");
                    }
                    else
                        alert("修改失敗")
                }
        })
    })
});


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