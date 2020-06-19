$(function () {
    //初始化LIFF
    var initializeLiff = function initializeLiff(myLiffId) {
        liff
            .init({
                liffId: myLiffId
            })
            .then(() => {
                // start to use LIFF's api
                getUserProfile();

            })
            .catch((err) => {
            });
    }
    //填入LIFF的ID
    initializeLiff('1654173476-vql6VGkn');

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
        window.alert("觸發")
        if($("#message").val() == ''){
            window.alert("要寫點東西才能發送ㄛ!");
            return
        }
        var content = {
            data: JSON.stringify({
                "message": $("#message").val(),
                "score":"None",
                "magnitude":"None"
            })
        }
        $.ajax({
            url: "/sentimentAnalysis",
            type: "POST",
            data: content,
            success: function (msg) {
                window.alert("感謝您ㄉ回饋")
                liff.closeWindow();
            }
        }).catch(function (error) {
            window.alert("發送失敗")
        })

    })

})