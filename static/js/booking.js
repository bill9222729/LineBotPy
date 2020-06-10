$(document).ready(function () {
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
    initializeLiff('1654173476-emvXlo37');

    //按鈕置底用
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

    //前面補零的函式，用來格式化時間
    function paddingLeft(str, lenght) {
        if (str.length >= lenght)
            return str;
        else
            return paddingLeft("0" + str, lenght);
    }

    //初始化時間
    var now = new Date();
    var hour = paddingLeft(now.getHours().toString(), 2);
    var minute = paddingLeft(now.getMinutes().toString(), 2);
    $("#time-picker").val(hour + ":" + minute);
    if (hour > 12)
        $("#book_time").html("下午 " + (hour - 12).toString() + "：" + minute);
    else
        $("#book_time").html("上午 " + hour + "：" + minute);

    //當時間被更改
    $("#time-picker").change(function () {
        var time = $("#time-picker").val();
        var time_hour = time.toString().split(":")[0];
        var time_minute = time.toString().split(":")[1];
        if (parseInt(time_hour) > 12)
            $("#book_time").html("下午 " + paddingLeft((parseInt(time_hour) - 12).toString(), 2) + "：" + time_minute);
        else
            $("#book_time").html("上午 " + time_hour + "：" + time_minute);
    })

    //初始化日期
    var day = ("0" + now.getDate()).slice(-2);
    var month = ("0" + (now.getMonth() + 1)).slice(-2);
    var today = now.getFullYear() + "-" + (month) + "-" + (day);
    $("#date-picker").val(today);
    $("#book_date").html(today);

    //當日期被更改
    $("#date-picker").change(function () {
        var date = $("#date-picker").val();
        var date_year = date.toString().split("-")[0];
        var date_month = date.toString().split("-")[1];
        var date_day = date.toString().split("-")[2];
        var full_day = date_year + "-" + date_month + "-" + date_day;
        $("#book_date").html(full_day);
    })

    //當人數被按下
    var people_number = 1;
    $("#one").click(function () {
        $("#two").css("background-color", "#ffffff");
        $("#three").css("background-color", "#ffffff");
        $("#four").css("background-color", "#ffffff");
        $("#people_picker").css("background-color", "#ffffff");
        $(this).css("background-color", "#FFD382");
        people_number = 1;
    })
    $("#two").click(function () {
        $("#one").css("background-color", "#ffffff");
        $("#three").css("background-color", "#ffffff");
        $("#four").css("background-color", "#ffffff");
        $("#people_picker").css("background-color", "#ffffff");
        $(this).css("background-color", "#FFD382");
        people_number = 2;
    })
    $("#three").click(function () {
        $("#one").css("background-color", "#ffffff");
        $("#two").css("background-color", "#ffffff");
        $("#four").css("background-color", "#ffffff");
        $("#people_picker").css("background-color", "#ffffff");
        $(this).css("background-color", "#FFD382");
        people_number = 3;
    })
    $("#four").click(function () {
        $("#one").css("background-color", "#ffffff");
        $("#two").css("background-color", "#ffffff");
        $("#three").css("background-color", "#ffffff");
        $("#people_picker").css("background-color", "#ffffff");
        $(this).css("background-color", "#FFD382");
        people_number = 4;
    })
    $("#people_picker").click(function () {
        $("#one").css("background-color", "#ffffff");
        $("#two").css("background-color", "#ffffff");
        $("#three").css("background-color", "#ffffff");
        $("#four").css("background-color", "#ffffff");
        $(this).css("background-color", "#FFD382");
    })

    $("#people_picker").change(function () {
        people_number = $("#people_picker").val();
    })

    //設定確定按鈕
    $("#confirm").click(function () {
        var full_date = $("#date-picker").val();
        var full_time = $("#time-picker").val();
        liff.sendMessages([{
                type: 'image',
                originalContentUrl:
                    'https://i.imgur.com/M626TFC.png?date=' + full_date + "&time=" + full_time + "&number=" + people_number + "&action=booking",
                previewImageUrl: 'https://i.imgur.com/M626TFC.png?date=' + full_date + "&time=" + full_time + "&number=" + people_number + "&action=booking",
            }]).then(function () {
                window.alert('Message sent');
            }).catch(function (error) {
                window.alert('Error sending message: ' + error);
            });
    })

    //使用者的ID
    var user_id;

    //用ajax向server請求資料庫內的資料並更新在欄位上
    var getUserProfile = function getUserProfile() {
        liff.getProfile().then(function (profile) {
            user_id = profile.userId;
            var userProfile = {
                data: JSON.stringify({
                    "user_id": profile.userId,
                    "user_name_custom": "None",
                    "home_address": "None",
                    "company_address": "None",
                    "phone_number": "None",
                })
            }
            $.ajax({
                url: "/getUserProfile",
                type: "POST",
                data: userProfile,
                success: function (msg) {
                    $("#user_name").attr({
                        'VALUE': msg["user_name_custom"],
                    })
                    $("#phone_number").attr({
                        'VALUE': msg["phone_number"],
                    })
                }
            })
        }).catch(function (error) {
            window.alert(error);
        })
    }
    getUserProfile();
});