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

    //設定確定按鈕
    $("#confirm").click(function () {
        liff.sendMessages([{
            'type': 'text',
            'text': "訂位:" + $("#user_name").val()
                + "\/" + $("#datepicker").val()
                + "\/" + $("#timepicker").val()
                + "\/" + $("#members").val()
                + "人\/"
        }]).then(function () {
            window.alert('Message sent');
        }).catch(function (error) {
            window.alert('Error sending message: ' + error);
        });
    })

    //抓取現在時間
    var today = new Date();
    var today_format = today.toString().split(" ")[4].split(":");
    //設定日期時間選擇器
    $("#datepicker").flatpickr({
        minDate: "today",
        dateFormat: "Y-m-d",
        defaultDate: "today"
    });
    $("#timepicker").flatpickr({
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        defaultDate: (parseInt(today_format[0]) + 1).toString() + "：" + today_format[1]
    });

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