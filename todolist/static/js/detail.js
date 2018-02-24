/**
 * Created by biao on 2018/2/21.
 */

function update_status(valueobj, showobj) {
    var statuscode = parseInt($(valueobj).val());
    // console.log($(valueobj).val());
    // console.log(statuscode);
    if (statuscode == 1) {
        $(showobj).html("已完成");
        $(showobj).attr("class", "label label-success");
    } else {
        $(showobj).html("未完成");
        $(showobj).attr("class", "label label-danger");
    }
}

function finish_todo(idobj, statusobj, btnobj) {
    $(btnobj).click(function () {
        var issure = confirm('确实完成了吗？');
        if (!issure) return;
        var todoid = parseInt($(idobj).val());
        var status = parseInt($(statusobj).val());
        if (status == 0 && todoid > 0) {
            $.ajax({
                url: "/updatestatus",
                data: {todoid: todoid, status: 1},
                method: "POST",
                success: function (res) {
                    var issuccess = res.data;
                    if (issuccess == true) {
                        // 刷新status
                        location.reload();
                    }
                },
                error: function (err) {
                    console.log(err);
                }
            });
        }
    });
}

$(document).ready(function () {
    // 更新todo的状态
    update_status($("#statuscode"), $("#statusshow"));
    // 点击提交按钮完成任务
    finish_todo($("#todoid"), $("#statuscode"), $("#btn_finish"));
});
