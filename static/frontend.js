
   // displays the countdown when inserted into HTML element
function formatTime(days, hours, minutes, seconds) {
  return days + "d " + hours + "h " + minutes + "m " + seconds + "s";
}

// create timer on page load or hard refresh
document.addEventListener('DOMContentLoaded', function () {
    // data in the datetime input field that user manipulates
    var userTime = document.getElementById("countdown-input");

    // create new div element with id=timer
    var countdown = document.createElement("div");
    countdown.id = "timer";
    //add new div to list of body elements. this element will show the seconds counting down
    document.body.appendChild(countdown);

    //timer control function
    function updateCountdown() {
        // user's date and time from input field
        var userDateTime = new Date(userTime.value).getTime();

        // set interval checks if timer has reached 0, every second
        var x = setInterval(function () {
            // timestamp from when user types in input field
            const now = new Date().getTime();

            // difference between user entered time and now
            var difference = userDateTime - now;

            // time calculations
            var days = Math.floor(difference / (1000 * 60 * 60 * 24));
            var hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((difference % (1000 * 60)) / 1000);

            // update new div with output of format time, which displays the countdown
            countdown.innerHTML = formatTime(days, hours, minutes, seconds);

            // notify user when countdown is finished
            if (difference < 0) {
                clearInterval(x);
                countdown.innerHTML = "timer done";
            }
        }, 1000);
    }

    // countdown updates whenever a user enters a datetime in the input field
    userTime.addEventListener('change', updateCountdown);
});