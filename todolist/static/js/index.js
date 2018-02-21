/**
 * Created by biao on 2018/2/21.
 */

/**
 * 打开首页就会调用的方法，用来及时的展示数据。
 */
function get_index_data(){
    $.ajax({
        url: "/week",
        method: "GET",
        dataType: "json",
        success: function (res) {
            var schema = res['data'][1];
            var data = res["data"][2];
            // console.log(data);
            render_to_index($("#datacontainer") , schema, data);
        },
        error: function (err) {
            console.log(err);
        }
    });
}

function render_to_index(container, schema, data){
    // console.log(data);
    for(var index=0; index < data.length; index++) {
        // console.log(data[index][0]);
        var child = '<li class="list-group-item" ><a target="_blank" href="/detail/'+data[index][0]+'">'+data[index][1]+'</a><span class="createtime"><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;创建于'+data[index][3]+'</small></span></li>';
        $(container).append(child);
    }
}

function add_newone(btnobj, inputobj, desc) {
    $(btnobj).click(function(){
       var desc =  $(inputobj).val();
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
