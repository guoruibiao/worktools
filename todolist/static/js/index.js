/**
 * Created by biao on 2018/2/21.
 */

/**
 * 打开首页就会调用的方法，用来及时的展示数据。
 */
function get_index_data(){
    var urlidmap = {
        "week": "/week",
        "today": "/daily",
        "yesterday": "/yesterday",
        "all": "/all",
        "finished": "/allfinished",
        "unfinished": "/allunfinished",
    };
    // 默认显示本周的数据
    $("#datacontainer").children().remove();
    renderdatabyurl("/week");
    $("#week").click(function(){
        $("#datacontainer").children().remove();
        renderdatabyurl("/week");
    });
    $("#today").click(function(){
        $("#datacontainer").children().remove();
        renderdatabyurl("/daily");
    });
    $("#yesterday").click(function(){
        $("#datacontainer").children().remove();
        renderdatabyurl("/yesterday");
    });
    $("#all").click(function(){
        $("#datacontainer").children().remove();
        renderdatabyurl("/all");
    });
    $("#finished").click(function(){
        $("#datacontainer").children().remove();
        renderdatabyurl("/allfinished");
    });
    $("#unfinished").click(function(){
        $("#datacontainer").children().remove();
        renderdatabyurl("/allunfinished");
    });
}
function renderdatabyurl(url){
    $.ajax({
        url: url,
        method: "GET",
        dataType: "json",
        success: function (res) {
            var schema = res['data'][1];
            var data = res["data"][2];
             console.log(data);
            render_to_index($("#datacontainer") , schema, data);
        },
        error: function (err) {
            console.log(err);
        }
    });
}
/**
 * 计算两个字符串形式的日期的时间差。
 * 输入：2018-02-23 12::59:20
 * 输出：XX天 HH小时MM分钟SS秒
 * */
function get_time_diff(starttimestr, endtimestr) {
    var starttime = new Date(starttimestr);
    var endtime = new Date(endtimestr);
    var seconds = (endtime.getTime() - starttime.getTime())/1000;
    var days = hours = minutes = 0;
    if(seconds > 86400) {
        days = parseInt(seconds/86400);
        seconds = seconds - 86400 * days;
    }
    if(seconds > 3600) {
        hours = parseInt(seconds/3600);
        seconds = seconds - hours * 3600;
    }
    if(seconds > 60) {
        minutes = parseInt(seconds / 60);
        seconds = seconds - minutes * 60;
    }
    // 组织返回字符串
    return "共耗时"+days + "天" +hours+"小时"+minutes+"分钟"+seconds+"秒";
}
function render_to_index(container, schema, data){
    // console.log(data);
    for(var index=0; index < data.length; index++) {
        // console.log(data[index][0]);
        var isfinished = parseInt(data[index][2]);
        var span = '<span class="glyphicon glyphicon-remove"></span>&nbsp;&nbsp;&nbsp;';
        var small = '&nbsp;&nbsp;&nbsp;<small>创建于'+data[index][3]+'</small>';
        var tipmsg = "该条目创建于 " + data[index][3] + ".";
        if(isfinished == 1) {
            span = '<span class="glyphicon glyphicon-ok"></span>&nbsp;&nbsp;&nbsp;';
            var starttimestr = data[index][3];
            var endtimestr = data[index][4];
            var timerange = get_time_diff(starttimestr, endtimestr);
            small = '&nbsp;&nbsp;&nbsp;<small>完成于'+data[index][4]+'('+timerange+')</small>';
        }
        var child = '<li class="list-group-item" >'+span+'<a target="_blank" title="'+tipmsg+'" href="/detail/'+data[index][0]+'">'+data[index][1]+'</a><span class="createtime">'+small+'</span></li>';
        $(container).append(child);
    }
}

function add_newone(btnobj, inputobj, desc) {
    $(btnobj).click(function(){
       var desc =  $(inputobj).val();
       console.log(desc);
       if(desc=="") {
           return;
       }
       $.ajax({
           url: "/add",
           data: {"description": desc},
           method: "POST",
           success: function(res) {
               console.log(res);
               location.reload();
           },
           error: function(err) {
               console.log(err);
           }
       });
    });
}

$(document).ready(function(){
    // 首次加载即显示所有数据
    get_index_data();
    // 点击添加按钮时持久化到数据库中
    add_newone($("#btn_add"), $("#desc"), desc);
});
