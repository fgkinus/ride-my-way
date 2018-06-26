'use strict';

const data_trip_offers = [
    {
        "id": 4,
        "origin": "cbd",
        "destination": "westlands",
        "departure_time": "2018-06-12 18:11:40.984000",
        "vehicle_model": "fielder",
        "vehicle_capacty": 5,
        "route": "waiyaki way]",
        "time_aded": null,
        "driver": "jdoe"
    },
    {
        "id": 3,
        "origin": "yaya",
        "destination": "cbd",
        "departure_time": "2018-06-11 23:11:20.109000",
        "vehicle_model": "passat",
        "vehicle_capacty": 4,
        "route": "uhuhuru highway",
        "time_aded": null,
        "driver": "jsmith"
    },
    {
        "id": 2,
        "origin": "juja",
        "destination": "rosambu",
        "departure_time": "2018-06-15 18:11:04.828000",
        "vehicle_model": "passsat",
        "vehicle_capacty": 4,
        "route": "thika road",
        "time_aded": null,
        "driver": "jsmith"
    },
    {
        "id": 1,
        "origin": "ngara",
        "destination": "thika",
        "departure_time": "2018-05-14 18:10:46.703000",
        "vehicle_model": "fielder",
        "vehicle_capacty": 5,
        "route": "thika road",
        "time_aded": null,
        "driver": "jdoe"
    },
    {
        "id": 5,
        "origin": "kinoo",
        "destination": "westlands",
        "departure_time": "2018-06-12 06:12:03.031000",
        "vehicle_model": "passat",
        "vehicle_capacty": 4,
        "route": "wiyakiway",
        "time_aded": null,
        "driver": "jmsmith"
    }
]

const data_trip_requests = [
    {
        "id": 1,
        "trip_id": 1,
        "requester": "psycho"
    },
    {
        "id": 2,
        "trip_id": 1,
        "requester": "jripper"
    },
    {
        "id": 3,
        "trip_id": 2,
        "requester": "psycho"
    },
    {
        "id": 4,
        "trip_id": 3,
        "requester": "psycho"
    },
    {
        "id": 5,
        "trip_id": 4,
        "requester": "jripper"
    }
]

const data_trip_notifications = [
    {
        "from": "jsmith",
        "id": 3,
        "trip_id": 5,
        "action": "accepted",
        "time": "2018-06-15 06:56:54.459000"
    },
    {
        "from": "jsmith",
        "id": 2,
        "trip_id": 3,
        "action": "rejecte",
        "time": "2018-06-15 06:56:52.584000"
    },
    {
        "from": "jdoe",
        "id": 5,
        "trip_id": 4,
        "action": "accepted",
        "time": "2018-06-15 10:57:17.896000"
    },
    {
        "from": "jsmith",
        "id": 1,
        "trip_id": 2,
        "action": "accepted",
        "time": "2018-06-15 06:56:29.943000"
    },
    {
        "from": "jdoe",
        "id": 4,
        "trip_id": 1,
        "action": "accepted",
        "time": "2018-06-15 19:59:58.381000"
    }
]

var  t = document.querySelector('#trip-offers');
var trip = document.querySelector('#trip-offer');
var clone = trip.content.cloneNode(true);

var s=document.querySelector('#trip-requests');
var request = document.querySelector('#trip-request');

var q=document.querySelector('#notifications');
var notification = document.querySelector('#trip-notification');

var my_trip_offers = document.querySelector('#my-trip-offers');


function showTripOffers() {
     var temp, item, a, i;
    //get the template element:

     for (i=0; i<data_trip_offers.length; i++){
         temp = trip.content.querySelectorAll('span');
         a = trip.content.querySelector('input');
         a.setAttribute("id",i.toString());
         item= trip.content.querySelector('label');
         item.setAttribute('for',i.toString());

         temp[1].textContent= data_trip_offers[i].driver;
         temp[2].textContent= data_trip_offers[i].destination;
         temp[3].textContent= data_trip_offers[i].id.toString();
         temp[4].textContent= data_trip_offers[i].time_aded;
         temp[5].textContent= data_trip_offers[i].destination;
         temp[6].textContent= data_trip_offers[i].origin;
         temp[7].textContent= data_trip_offers[i].departure_time;
         temp[8].textContent= data_trip_offers[i].route;
         temp[9].textContent= data_trip_offers[i].vehicle_model;
         temp[10].textContent= data_trip_offers[i].vehicle_capacty.toString();
         t.appendChild(trip.content.cloneNode(true));
     };
 };
function showMyTripOffers(driver ) {
    var temp, item, a, i;
    //get the template element:

    for (i=0; i<data_trip_offers.length; i++){
        temp = trip.content.querySelectorAll('span');
        a = trip.content.querySelector('input');
        a.setAttribute("id",i.toString());
        item= trip.content.querySelector('label');
        item.setAttribute('for',i.toString());

        if (data_trip_offers[i].driver == 'jdoe'){
            temp[1].textContent= "You ";
            temp[2].textContent= data_trip_offers[i].destination;
            temp[3].textContent= data_trip_offers[i].id.toString();
            temp[4].textContent= data_trip_offers[i].time_aded;
            temp[5].textContent= data_trip_offers[i].destination;
            temp[6].textContent= data_trip_offers[i].origin;
            temp[7].textContent= data_trip_offers[i].departure_time;
            temp[8].textContent= data_trip_offers[i].route;
            temp[9].textContent= data_trip_offers[i].vehicle_model;
            temp[10].textContent= data_trip_offers[i].vehicle_capacty.toString();
            my_trip_offers.appendChild(trip.content.cloneNode(true));
        }
    };
};

function showRideRequests(){
     var tmp, item, a, i,trip_no,tr;
     //get the template element:

     for (i=0; i<data_trip_requests.length; i++){
         tmp =request.content.querySelectorAll('span');
         a =request.content.querySelector('input');
         item =request.content.querySelector('label');
         a.setAttribute("id",'rq'+i.toString());
         item.setAttribute('for','rq'+i.toString());

         trip_no= data_trip_requests[i].trip_id;
         tr = data_trip_offers[trip_no];

         tmp[1].textContent= data_trip_requests[i].requester;
         tmp[2].textContent= tr.destination;
         tmp[3].textContent= tr.id.toString();
         tmp[4].textContent= tr.time_aded;
         tmp[5].textContent= tr.destination;
         tmp[6].textContent= tr.origin;
         tmp[7].textContent= tr.departure_time;
         tmp[8].textContent= tr.route;
         tmp[9].textContent= tr.vehicle_model;
         tmp[10].textContent= tr.vehicle_capacty.toString();

         s.appendChild(request.content.cloneNode(true));
     }
 }

 function showNotifications() {
    let tmp, item, a, i,trip_no;
    let trip_detail=[];
    //get the template element:
    for (i=0;i<data_trip_notifications.length;i++){
        tmp =notification.content.querySelectorAll('span');
        a =notification.content.querySelector('input');
        item=notification.content.querySelector('label');
        a.setAttribute("id",'nt'+i.toString());
        item.setAttribute('for','nt'+i.toString());

        trip_no= data_trip_notifications[i].trip_id-1;
        trip_detail = data_trip_offers[trip_no];
        try{
            trip_detail = data_trip_offers[trip_no];
        }
        catch (e) {
            console.log("failed o iteration "+trip_no);
        }
        finally {
            console.log("it actualy worked");
            tmp[1].textContent= trip_detail.driver;
            tmp[2].textContent= data_trip_notifications[i].action;
            tmp[3].textContent= trip_detail.destination;

            let link =notification.content.querySelector('a');
            link.setAttribute('href','#'+trip_detail.id);
            link.setAttribute('for',trip_detail.id);
            q.appendChild(notification.content.cloneNode(true));
        }
    }
}


try{
    showTripOffers();
    showMyTripOffers(1);
}finally {
    try{
        showRideRequests();
    }finally {
        showNotifications();
    }

}
