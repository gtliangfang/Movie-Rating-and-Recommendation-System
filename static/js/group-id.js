$(function(){
    $('#join').click(function(){
        var input = $('#confirm').val();
        var url = window.location.href;
        var patt = /gp+[0-9]*/g;
        url = url.match(patt)[0];
        patt = /[^0-9]/g;
        var group_id = url.replace(patt, '');
        $.getJSON($SCRIPT_ROOT + '/_join_group',
            {group_id: group_id, confirm:input},
            function(data){
                if(data.status == 'joined'){
                    alert('joined!');
                }else if(data.status == 'fail'){
                    alert('fail!!');
                }else if(data.status == 'non-ex') {
                    alert('non-ex!');
                }
                location.reload();
        });
    });
});

$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('#quit').click(function(){
            var url = window.location.href;
            var patt = /gp+[0-9]*/g;
            url = url.match(patt)[0];
            patt = /[^0-9]/g;
            var group_id = url.replace(patt, '');
            $.getJSON($SCRIPT_ROOT + '/_quit_group',
                {group_id: group_id},
                function(data){
                    if(data.status == '0'){
                        alert('fail!!');
                    }else if(data.status == '1') {
                        location.reload();
                    }
            });
        });
    });
});

$(function(){
    $('.createDiscussion').submit(function(e){
        e.preventDefault();
        var title = $('#discuss-title').val();
        var content = $('#discuss-content').val();
        // alert(title);
        if(!title){
            alert('Title cannot be empty!');
        }else if(!content) {
            alert('Topic cannot be empty!');
        }else{
            var url = window.location.href;
            var patt = /gp+[0-9]*/g;
            url = url.match(patt)[0];
            patt = /[^0-9]/g;
            var group_id = url.replace(patt, '');
            $.getJSON($SCRIPT_ROOT + '/_create_discussion/' + group_id,
                {title: title, content: content},
                function (data) {
                    if (data.status == '1') {
                        location.hash = 'discussions';
                        location.reload();
                    }else{
                        alert(data.status);
                    }
                });
        }
    });
});

$(function(){
    $('.createBulletin').submit(function(e){
        e.preventDefault();
        var title = $('#bulletin-title').val();
        var text = $('#bulletin-text').val();
        if(!title){
            alert('Title cannot be empty!');
        }else if(!text) {
            alert('Topic cannot be empty!');
        }else{
            var url = window.location.href;
            var patt = /gp+[0-9]*/g;
            url = url.match(patt)[0];
            patt = /[^0-9]/g;
            var group_id = url.replace(patt, '');
            $.getJSON($SCRIPT_ROOT + '/_create_bulletin/' + group_id,
                {title: title, text: text},
                function (data) {
                    if (data.status == '1') {
                        location.hash = 'bulletin';
                        location.reload();
                    }else{
                        alert(data.status);
                    }
                });
        }
    });
});

$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('.discuss-delete').click(function(){
            var discuss_id = Number($(this).attr('victim'));
            var div = $(this).parent();
            console.log(discuss_id);
            $.getJSON($SCRIPT_ROOT + '/_delete_discussion',
                {discuss_id: discuss_id},
                function(data){
                    if(data.success == '0'){
                        alert('failed');
                    }else{
                        location.reload();
                    }
            });
        });
    });
});

$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('.bulletin-delete').click(function(){
            var bulletin_id = Number($(this).attr('victim'));
            var div = $(this).parent();
            console.log(bulletin_id);
            $.getJSON($SCRIPT_ROOT + '/_delete_bulletin',
                {bulletin_id: bulletin_id},
                function(data){
                    if(data.success == '0'){
                        alert('failed');
                    }else{
                        location.reload();
                    }
            });
        });
    });
});


// optionready_instant is used in instant
function optionReady_instant(){
    var options = 0;
    $('.addOption').click(function(){
        ++options;
        if (options > 26)
        {
            --options;
            alert("the number is limited to 26");
            return;
        }

        //get num
        var vote_options_num = document.getElementById('vote-options-num');
        //update num
        vote_options_num.setAttribute('value',options.toString());

        //create option
        var vote_option_content = document.createElement('input');
        vote_option_content.setAttribute('class','vote-option-content form-control');
        vote_option_content.setAttribute('name','vote-option-content-'+options.toString());
        vote_option_content.readOnly = true;
        vote_option_content.setAttribute('value','double click to change value');

        // remove button
        option_remove_button = document.createElement('i');
        option_remove_button.setAttribute('class', 'fa fa-lg fa-minus-square-o');
        option_remove_button.setAttribute('id', 'remove-option-'+options.toString());

        vote_option_content.ondblclick = function()
        {
            this.value = ''
            this.readOnly = false;
            this.className = "vote-option-content-edit";
        }
        vote_option_content.onblur = function()
        {
            if (this.value == '')
            {
                this.value = "double click to change value";
            }

            this.readOnly = true;
            this.className = "vote-option-content";
        }

        option_remove_button.onclick = function()
        {
            if (options<=1)
            {
                alert ("options can't be empty");
                return;
            }
            options--;
            vote_options_num.setAttribute('value',options.toString());
            var tempArray = vote_option_content.name.split('-');
            var currentNum = parseInt(tempArray[tempArray.length - 1]);
            var next = vote_wrap.nextSibling;
            while( next.value != "Add new choices" )
            {
                next.firstChild.innerHTML = String.fromCharCode(64+currentNum);
                next.firstChild.nextSibling.name = 'vote-option-content-'+currentNum.toString();
                next.lastChild.setAttribute('id', 'remove-option-'+currentNum.toString());
                next = next.nextSibling;
                currentNum++;
            }
            vote_wrap.parentNode.removeChild(vote_wrap);
        }
        //var vote_change_row = document.createElement('br');
        var vote_order = String.fromCharCode(64+options); //limit to 26 options

        var vote_wrap = document.createElement('div');
        vote_wrap.innerHTML = "<span>"+vote_order+"</span>";
        //vote_wrap.appendChild(vote_option);
        vote_wrap.appendChild(vote_option_content);
        vote_wrap.appendChild(option_remove_button);
        vote_wrap.setAttribute('class', 'vote-wrap');

        var vote_add_form = document.getElementById("vote-add-form");
        var vote_add_button = document.getElementById("vote-add-button");

        vote_add_form.insertBefore(vote_wrap,vote_add_button);
    });
}


function optionReady(toAdd){
    var options = 0;
    $(toAdd).find('input.addOption').click(function(){
        ++options;
        if (options > 26)
        {
            --options;
            alert("the number is limited to 26");
            return;
        }

        this.disable = true;

        var vote_add_target = this.parentNode;
        var target_id = $(vote_add_target).attr("id");
        //get the number in the id
        var vote_order = target_id.replace(/[^0-9]/ig,"");

        //uodate num
        var vote_options_num = document.getElementById('vote-options-num-'+vote_order); // specify it
        vote_options_num.setAttribute('value',options.toString());

        //create option
        var vote_option_content = document.createElement('input');
        vote_option_content.setAttribute('class','vote-option-content form-control');
        vote_option_content.setAttribute('name',target_id+'-option-content-'+options.toString());
        vote_option_content.readOnly = true;
        vote_option_content.setAttribute('value','double click to change value');
        
        // remove button
        option_remove_button = document.createElement('i');
        option_remove_button.setAttribute('class', 'fa fa-lg fa-minus-square-o vote-option-remove');
        option_remove_button.setAttribute('id', target_id+'-remove-option-'+options.toString());        

        option_remove_button.onmouseover = function() {
            this.style.display = "inline-block";
        }

        vote_option_content.ondblclick = function()
        {
            this.value = '';
            this.readOnly = false;
            this.className = "vote-option-content-edit";
        };
        vote_option_content.onblur = function()
        {
            if (this.value == '')
            {
                this.value = "double click to change value";
            }
            this.readOnly = true;
            this.className = "vote-option-content";
        };
        option_remove_button.onclick = function()
        {
            if (options<=1)
            {
                alert ("options can't be empty");
                return;
            }
            options--;
            vote_options_num.setAttribute('value',options.toString());
            var tempArray = vote_option_content.name.split('-');
            var currentNum = parseInt(tempArray[tempArray.length - 1]);
            var next = vote_wrap.nextSibling;
            while( next.value != "Add new choices" )
            {
                next.firstChild.innerHTML = String.fromCharCode(64+currentNum);

                next.firstChild.nextSibling.name = target_id+'-option-content-'+currentNum.toString();
                next.lastChild.setAttribute('id', target_id+'-remove-option-'+currentNum.toString());
                next = next.nextSibling;
                currentNum++;
            }
            vote_wrap.parentNode.removeChild(vote_wrap);
        }

        //wrap the option
        var vote_wrap = document.createElement('div');
        var option_order = String.fromCharCode(64+options); //limit to 26 options
        var vote_add_button = vote_add_target.getElementsByClassName("addOption")[0];

        vote_wrap.innerHTML = "<span class='vote-option-title'>"+option_order+"</span>";
        vote_wrap.setAttribute('class', 'vote-option');
        vote_wrap.appendChild(vote_option_content);
        vote_wrap.appendChild(option_remove_button);


        vote_add_target.insertBefore(vote_wrap, vote_add_button);
        this.disable = false;
    });
};

function voteReady()
{
    //total votes
    var votes = 1;              
    var votes_num = $("#votes-num"); 
    $(votes_num).val(votes.toString());
    $('.addVote').click(function()
    {
        ++votes;
        //get num actually votes = votes_num    0.0 
        var votes_num = $("#votes-num"); 
        $(votes_num).val(votes.toString());
        var vote_li = document.createElement('li');
        $(vote_li).attr('class','list-group-item');
        $(vote_li).attr('id','vote'+votes.toString());

        ///add content
        $(vote_li).html(
            "<label for=\"vote-content-"+votes+"\">Title of the item</label>" +              //question
            "<input class=\"vote-content form-control\" type=\"text\" name=\"vote-content-"+votes+
            "\" id=\"vote-content-"+votes+"\"/>" +                                          
            "<input class=\"form-control\" type=\"text\" name=\"vote-options-num-"+votes+
            "\" id=\"vote-options-num-"+votes+"\" style=\"display:none;\" value=\"0\"/><br>" +  //options num
            "<input type=\"button\" class=\"addOption btn btn-default\"" +
            "value=\"Add new choices\"/>"
        );

        var votes_content_set = document.getElementById("votes_content_set");
        votes_content_set.appendChild(vote_li);                    //insert the vote
        optionReady(vote_li);                                      //add listener
        $(vote_li).find('input.addOption').click();                //ensure at least one option
    }
    );
}


$(function(){
    $('#instant_vote').click(function(){
        // $('#vote-add-form').html("");
        $('#vote-add-form').html(
            "<label for=\"vote-content\">Vote Title</label>" +                                 //title and question are the same
            "<input class=\"form-control\" type=\"text\" name=\"vote-content\"" +                   
            "id=\"vote-content\"/>" +
            "<input class=\"form-control\" type=\"text\" name=\"vote-options-num\"" +                 //the number of options
            "id=\"vote-options-num\" style=\"display:none;\" value=\"0\"/><br>" +
            "<input type=\"button\" class=\"addOption btn btn-default\" id=\"vote-add-button\"" +       //the button to add options
            "value=\"Add new choices\"/><br><br>" +
            "<input class=\"form-control\" type=\"text\" id=\"endtime-selection\"" +
            "name=\"endtime-selection\" value = \"0\" style=\"display:none\"/>" +                   //if 0 instant
            "<input type=\"text\" id=\"endtime\" name=\"endtime\"" +
            "class=\"countdown_timepicker form-control\" value=\"00:00:00\" /><br>" +                
            "<button type=\"submit\" id=\"validcheck\" class=\"btn btn-default\">let's vote!</button>"
        );
        $(".countdown_timepicker").datetimepicker({
        //showOn: "button",
        //buttonImage: "./css/images/icon_calendar.gif",
        //buttonImageOnly: true,
        showButtonPanel: false,
        timeOnly: true,
        showSecond: true,
        timeFormat: 'hh:mm:ss',
        stepHour: 1,
        stepMinute: 1,
        stepSecond: 1
        });

        optionReady_instant();

        $("#validcheck").click(
            function()
            {
                var ops = new Array();
                var order = 0;
                var status = true;

                if ($("#vote-content").val() == "")
                {
                    alert("the title can't be empty");
                    return false;
                }

                $(".vote-option-content").each(function(key,value){
                    ops[key] = $(this).val();
                    ++order;
                    if (ops[key] == "double click to change value")
                        {
                            alert("the No."+order+" option hasn't been setted");
                            status = false;
                            return false;
                        }
                    
                }
                    );

                if (!status) return false;

                return $(".countdown_timepicker").val().isCountTime();
            }
        );                                                         
        //add listener to the button that adds options
        $('#vote-add-form').find("input.addOption").click();                          //ensure at least one option
    }
    )
}
);



String.prototype.isTime = function()
{
  var r = this.match(/^(\d{1,4})(-|\/)(\d{1,2})\2(\d{1,2}) (\d{1,2}):(\d{1,2}):(\d{1,2})$/);
  if(r==null)return false; var d = new Date(r[1], r[3]-1,r[4],r[5],r[6],r[7]);
  var isTime = d.getFullYear()==r[1]&&(d.getMonth()+1)==r[3]&&d.getDate()==r[4]&&d.getHours()==r[5]&&d.getMinutes()==r[6]&&d.getSeconds()==r[7];
  var Now = new Date();
  if (!isTime)
    {
        alert("time format is not right");
        return false;
    }
  if (d<=Now)
  {
    alert("time format is invalid");
    return false;
  }
  else
    if (d-Now < 15000)
        alert("warning: the time is too tight\nplease reset it");

  return true;
}

String.prototype.isCountTime = function()
{
    var r = this.match(/^(\d{2}):(\d{2}):(\d{2})$/);
    if (r == null)
    {
        alert("invalid time format");
    }
    if (r[1]<"24" && r[2]<"60" && r[3]<"60")
    {
        if (r[1] == "00" && r[2] == "00")
            if (r[3] < "15")
            {
                alert ("the time is too tight\n please reset it");
                return false;
            }
        return true;
    }
    else
    {
        alert("invalid time format");
        return false;
    }
}
//function isDate()

$(function(){
    $('#longlasting_vote').click(function(){
        // $("vote-add-form").html("");
        var timesetted = false;
        $("#vote-add-form").html(
            "<label for=\"title\">Vote Title</label>" +
            "<input class=\"form-control\" id=\"votetitle\" type=\"text\" name=\"title\"/>" +                      //title id !!!!
                "<ul id=\"votes_content_set\" class='list-group'>" +
                    "<li class=\"list-group-item\" id=\"vote1\">" +                                ///every li represents a subvote
                    "<label for=\"vote-content-1\">Title of the item</label>" +
                    "<input class=\"vote-content form-control\" type=\"text\" name=\"vote-content-1\"" +
                    "id=\"vote-content-1\"/>" +
                    "<input class=\"form-control\" type=\"text\" name=\"vote-options-num-1\"" + // the number of options
                    "id=\"vote-options-num-1\" style=\"display:none;\" value=\"0\"/><br>" +
                    "<input type=\"button\" class=\"addOption btn btn-default\"" +               // the button is used to add options
                    "value=\"Add new choices\"/>" +
                    "</li>" +
                "</ul>" +
            "<input class=\"form-control\" type=\"text\" name=\"votes-num\"" +
            "id=\"votes-num\" style=\"display:none;\" value=\"0\"/>" + // the number of votes
            "<input type=\"button\" class=\"addVote btn btn-default\"" +  //this button is used to add vote
            "value=\"Add new vote content\"/><br><br>" +
            "<input class=\"form-control\" type=\"text\" id=\"endtime-selection\"" +
            "name=\"endtime-selection\" value = \"1\" style=\"display:none\"/>" +  // if 1 longlasting
            "" +
            "<input type=\"text\" id=\"endtime\" name=\"endtime\" value=\"Click to set endtime\"" +
            "class=\"ui_timepicker form-control\" value=\"\"/><br>" +
            "<button type=\"submit\" id=\"validcheck\" class=\"btn btn-default\">let's vote!</button>" //change id!!!!!!!!!!!!!!!!!!
        )
        $(".ui_timepicker").datetimepicker({
        dateFormat: 'yy-mm-dd',
        showSecond: true,
        timeFormat: 'hh:mm:ss',
        stepHour: 1,
        stepMinute: 1,
        stepSecond: 1
        });


        $("#validcheck").click(
            function()
            {
                var ops = new Array();
                var status = true;
                var id_origin = "vote1";
                var order = 0;

                if ($("#votetitle").val() == '')
                    {
                        alert("votetitle can't be empty");
                        return false;
                    }


                $(".vote-option-content").each(function(key,value){
                    ops[key] = $(this).val();
                    target_id =$(this).parent().parent().attr("id");
                    if (target_id != id_origin)
                    {
                        id_origin = target_id;
                        order = 0;
                    }
                    ++order;
                    if (ops[key] == "double click to change value"||ops[key] == "")
                        {
                            var vote_order = target_id.replace(/[^0-9]/ig,"");
                            alert ("the No."+order+" option of the No."+vote_order+" hasn't been set");
                            status = false;
                            return false;
                        }
                })
                if (!status)
                    return false;

                var vts = new Array();
                order = 0;
                $(".vote-content").each(function(key,value){
                    vts[key] = $(this).val();
                    ++order;
                    if (vts[key] == "")
                    {
                        alert ("the title of the No."+order+" hasn't been set");
                        status = false;
                        return false;
                    }
                })

                if (!status)
                    return false;

                if (!$(".ui_timepicker").val().isTime())
                    {
                        return false;
                    };



                return true;
            }


            );

        voteReady();           // add listener to vote
        optionReady($("#vote1"));
        $("#vote1").find("input.addOption").click();
    }
    )
});

$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('.vote-delete').click(function(){
            var vote_id = Number($(this).attr('victim'));
            var div = $(this).parent();
            console.log(vote_id);
            $.getJSON($SCRIPT_ROOT + '/_delete_vote',
                {vote_id: vote_id},
                function(data){
                    if(data.success == '0'){
                        alert('failed');
                    }else{
                        location.reload();
                    }
            });
        });
    });
});


$(function(){
    $('.popover-options').on('shown.bs.popover', function(){
        $('.vote-end').click(function(){
            var vote_id = Number($(this).attr('victim'));
            var div = $(this).parent();
            console.log(vote_id);
            $.getJSON($SCRIPT_ROOT + '/_end_vote',
                {vote_id: vote_id},
                function(data){
                    if(data.success == '0'){
                        alert('failed');
                    }else{
                        location.reload();
                    }
            });
        });
    });
});