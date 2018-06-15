"use strict";


function autoResizeDiv(element) {
    // a function to resize elements and te iframe
    window.onload = function () {
        document.getElementById(element).style.height= window.innerHeight+'px';
    }
    window.onresize = autoResizeDiv(element);
    return this;
}

function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("openNav").style.display = 'none';
}
function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
}

function open_modal() {
    var modal = document.getElementById('add_trip');
    modal.style.display  = 'block';
}

function close_IFrame()
{
    var modal = document.getElementById('add_trip');
    modal.style.display = 'none';
}

    var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.maxHeight){
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
}


// ##############################################################################

// ####################################################################

// resize the container footer
autoResizeDiv('container-footer');
