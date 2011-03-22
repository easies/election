function on_load()
{
    for(var i = 0;i < on_load.load.length;i++)
    {
        on_load.load[i]();
    }
    return true;
}

on_load.load = []
on_load.add = function(f){ on_load.load.push(f); };

function OfficeDesc(obj,key)
{
    // Reset all the buttons
    $('.office').css('color','#336699');
    // Highlight the current office
    $(obj).css('color','red');
    
    $('#office_info').find('#title').load("/election/offices/" + key + " #office_title")
    $('#office_info').find('#desc_in').load("/election/offices/" + key + " #office_desc",function(){ $('#office_info').show();})
    
    close = function() { $('#office_info').hide();
            	             // Undo obj stuff
			     $('.office').css('color','#336699');
			     return false; }

    $('#office_info').find('#close').bind('click',close);
}

