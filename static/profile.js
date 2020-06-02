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
    initializeLiff('1654173476-GO8zxXn6');

    //向server提出修改資料的要求
    $("#change_all").click(function () {
        alert("修改中");
        var info = {
            data: JSON.stringify({
                "user_id": user_id,
                "user_name_custom": $("#name_input").val(),
                "home_address": $("#home_address_input").val(),
                "company_address": $("#company_address_input").val(),
                "phone_number": $("#phone_number_input").val(),
            })
        }
        $.ajax({
            url: "/setProfile",
            type: "POST",
            data: info,
            success: function (msg) {
                if (msg == "OK") {
                    alert("修改成功");
                } else
                    alert("修改失敗")
            }
        })
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
                    alert(msg["user_name_custom"]);
                    $("#name_input").attr({
                        'VALUE': msg["user_name_custom"],
                    })
                    $("#home_address_input").attr({
                        'VALUE': msg["home_address"],
                    })
                    $("#company_address_input").attr({
                        'VALUE': msg["company_address"],
                    })
                    $("#phone_number_input").attr({
                        'VALUE': msg["phone_number"],
                    })
                }
            })
        }).catch(function (error) {
            window.alert(error);
        })
    }
    getUserProfile();
})