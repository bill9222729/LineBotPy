$(document).ready(function () {
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

    var user_id;
    //初始化LIFF
    var initializeLiff = function initializeLiff(myLiffId) {
        liff
            .init({
                liffId: myLiffId
            })
            .then(() => {
                // start to use LIFF's api
                liff.getProfile().then(function (profile) {
                    user_id = profile.userId;
                }).catch(function (error) {
                    window.alert(error);
                });
            })
            .catch((err) => {
                alert(err);
            });
    }
    //填入LIFF的ID
    initializeLiff('1654173476-7lybVOAP');

    $("#test").click(function () {
        var URL = 'https://notify-bot.line.me/oauth/authorize?';
        URL += 'response_type=code';
        URL += '&client_id=SUMVZ46FKbFjW6FBYnIEX0';
        URL += '&redirect_uri=https://e593cda5c426.ngrok.io/hookNotify?userid=' + user_id;
        URL += '&scope=notify';
        URL += '&state=NO_STATE';
        window.location.href = URL;
    });
});