// there is a css transition property that smooths color change
// changed color format to rgb as as uses numbers so easy to make
window.setInterval(function() {
  $(".content-section").css(
    "background-color",
    `rgb(${getRandomColor()},${getRandomColor()},${getRandomColor()})`
  );
}, 2000);

// returns 255(white) minus random int from 0 to strength
// lower strength  = more white / 0 = white / 255 = full
function getRandomColor(strength = 50) {
  return 255 - (Math.round(Math.random() * 1000) % strength);
}

// bind the getLocation function to the button being clicked
$('#import_location_btn').click(getLocation);

function getLocation() {
  // go no further if not supported
  if (!"geolocation" in navigator) {
    // hide the button and display error message
    $('#import_location_btn').addClass('hidden');
    $('#location_status').addClass('text-error').text('Geolocation not supported by browser.');
    return;
  }
  // disable button whilst loading and set status text
  $('#import_location_btn').attr('disabled', 'disabled');
  $('#location_status').addClass('text-secondary').text('Getting location data...');
  $('#import_location_btn').html('<i class="fa fa-spinner fa-spin"></i>');
  // disable submit button whilst loading, is always undone
  $('#submit').attr('disabled', 'disabled');

  // get current location and set callbacks to handle response
  navigator.geolocation.getCurrentPosition(
    function(position) {
      // success callback, keep location accurate for db
      // const is the same as var but can never change
      const lat = position.coords.latitude.toFixed(6);
      const long = position.coords.longitude.toFixed(6);

      // toFixed take a number but returns a string to preserve 0's
      // which is fine for db but need to cast to int before next use
      // using the + symbol

      // update text status
      $('#location_status').removeClass('text-secondary').text(`Position saved (lat: ${(+lat).toFixed(2)}, long: ${(+long).toFixed(3)})`);

      // set hidden form fields to retrieved values so they're submitted with the form.
      $('#input_lat').attr('value', lat);
      $('#input_long').attr('value', long);

      $('#import_location_btn').text('Success');
      $('#submit').removeAttr('disabled');
    },
    function(err) {
      console.log(err);
      // this callback is called if an error occurs eg: user declines
      // permission etc.. hide the button and display error message
      $('#import_location_btn').addClass('d-none');
      $('#location_status').addClass('text-error').text('Geolocation unavailable.');
      $('#submit').removeAttr('disabled');
    }
  );
}
