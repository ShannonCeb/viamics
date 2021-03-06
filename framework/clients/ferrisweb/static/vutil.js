function hide(el){document.getElementById(el).style.display = 'none'}

function show(el,display){
    var display = display ? display : "block";
    document.getElementById(el).style.display = display;
}

function swap(a,b){hide(a);show(b);}

function set_disabled(el,newval)
{
    el.disabled = newval
}

function set_dependent(container, newval) 
{
    var inputs =container.getElementsByTagName("input");
    var selects = container.getElementsByTagName("select");
    $.each(inputs, function(i, el){ set_disabled(el,newval)});
    $.each(selects, function(i, el){ set_disabled(el,newval)});
}

function prepend(obj,new_element)
{
    p = obj.parentElement;
    p.insertBefore(new_element,obj);

}

function prepend_input(obj, i)
{
    prepend(obj, $('<p><label for="id_data_file'+i+'">Data file:</label> <input type="file" name="data_file'+i+'" id="id_data_file'+i+'" /></p>')[0])
}

$(document).ready(function(){
     
    $(".switcher li").bind("click",function(){		
		
		var act = $(this);
		
		$(act).parent().children('li').removeClass("active").end();
		$(act).addClass("active");
		
    });
	
});
