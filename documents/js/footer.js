"use strict";

function getYear(){
    // return the current year in the footer
    window.onload = function () {
        var date=new Date();
        console.log(date.getFullYear());
        document.getElementById("Year").innerHTML = date.getFullYear().toString();
    }
}

// get current year
getYear();