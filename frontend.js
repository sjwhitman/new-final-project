// any import statements

// countdown timer
function timerCounter(){

  // Convert both dates to seconds
  var date1_ms = date1.getTime();
  var date2_ms = date2.getTime();

  // Calculate the time interval
  var difference_ms = date2_ms - date1_ms;

  if (difference_ms < 0) {
    //notify user that timer has finished
    // alert(`Your ${timer_type} timer is finished`)
  }
};

//need this JS file to get loaded on the front end(by the html file)
//use script tag to import js into html 
//need tasks and users table from the db
//need timer thats updating. use setInterval