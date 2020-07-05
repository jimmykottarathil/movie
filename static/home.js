
var script = document.createElement("script")
document.head.appendChild(script)
script.type = "text/javascript"
script.src = "https://code.jquery.com/jquery-3.5.0.js"

function show(id)
{
    if(id == "whatsapp-ico")
    {
        $("#whatsapp-no").animate({

              left: "-20px",
              opacity: "1"
        })
    }

    else if(id == "twitter-ico")
    {
        $("#twitter-id").animate({

            left: "-20px",
            opacity: "1"
      })
    }

    else if(id == "gmail-ico")
    {
        $("#gmail-id1, #gmail-id2").animate({

            left: "-20px",
            opacity: "1"
      })
    }

    else
    {
        $("#phone-no").animate({

            left: "-20px",
            opacity: "1"
      })
    }
    
}

function hide()
{
    $("#whatsapp-no, #twitter-id,#phone-no").animate({
        left: "100px",
        opacity: "0"
    })

    $("#gmail-id1, #gmail-id2").animate({
        left: "170px",
        opacity: "0"
    })
}


script.onload = function(){
   $(document).ready(function(){
       $(".section-3>img").mouseenter(function(){
           if($("#whatsapp-ico:hover").length != 0)
           {
               show("whatsapp-ico")
            //    alert("1111")
            
           }

           else if($("#twitter-ico:hover").length !=0)
           {
               show("twitter-ico")
            //    alert("11")
           }

           else if($("#gmail-ico:hover").length !=0)
           {
               show("gmail-ico")
           }

           else
           {
               show("phone-ico")
           }
       })

       $(".section-3>img").mouseleave(function(){
           hide()
       })

    //    $("#button-1").mouseenter(function(){
    //        alert($("#button").css("width"))
    //    })

   })
       
}





