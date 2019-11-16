var my_lat = document.getElementById("lat");
var my_long = document.getElementById("long");

function getLocation(){

  console.log("intitial loading")
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position){
  stored_lat = Math.round(position.coords.latitude * 100) / 100;
  stored_long = Math.round(position.coords.longitude * 100) / 100;
  lat.innerHTML = "Latitude: " + stored_lat;
  long.innerHTML = "<br>Longitude: " + stored_long;

  console.log("testing", stored_lat, stored_long)
  $.ajax({
           // Specify the endpoint URL the request should be sent to.
           url: '/POST',
           // The request type.
           type: 'POST',
           // The data, which is now most commonly formatted using JSON because of its
           // simplicity and is native to JavaScript.
           data: JSON.stringify({ lat: stored_lat }),// Specify the format of the data which will be sent.
           contentType: "application/json; charset=utf-8",
           // The data type itself.
           dataType: "json",
           // Define the function which will be triggered if the request is received and
           // a response successfully returned.
           // The function which will be triggered if any error occurs.

           error: function(error){
               console.log(error);
           }
       });

    console.log("testing", stored_lat, stored_long)

}
