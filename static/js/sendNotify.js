$(function () {

    function mobile_send_btn() {
        $("button").css({
            "position": "fixed",
            "width": "100%",
            "padding": "0",
            "left": "0",
            "z-index": "100",
            "bottom": "0",
            "margin": "0"
        });
    }

    // 載入後執行
    mobile_send_btn();

    // 捲軸移動時
    $(window).bind("scroll", function () {

        mobile_send_btn();

    });

    $("button").click(function () {
        if($("#message").val() == ''){
            window.alert("要寫點東西才能發送ㄛ!");
            return
        }
        var content = {
            data: JSON.stringify({
                "message": $("#message").val(),
            })
        }
        $.ajax({
            url: "/sendNotify",
            type: "POST",
            data: content,
            success: function (msg) {
                window.alert("發送成功")
            }
        }).catch(function (error) {
            window.alert("發送失敗")
        })

    })

})