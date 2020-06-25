var script = document.createElement("script")
document.head.appendChild(script)
script.type = "text/javascript"
script.src = "https://code.jquery.com/jquery-3.5.0.js"

function validate()
{
    $("#archive").css("opacity", "0")
    var search_box = document.getElementById("search-box")
    var search_string = /^([a-zA-Z0-9])([a-zA-Z0-9\s-:\.]+)$/
    if(search_string.test(search_box.value))
    {
        if(/[\s\.:-]{2}/.test(search_box.value))
        {
            search_box.style.border = "3px solid red"
            $("#wrong-name").css("opacity", "1")
            return false
        }

        else
        {
            search_box.style.border = "2px solid black"
            $("#wrong-name").css("opacity", "0")
            $("#loading-gif").css("opacity", "1")
            return true
        }
    }

    else
    {
        search_box.style.border = "3px solid red"
        $("#wrong-name").css("opacity", "1")
        return false
    }
}



script.onload = function(){
    $(document).ready(function(){

    })
}