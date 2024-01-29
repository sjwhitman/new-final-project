// alert("profile.js is connected!");

document.querySelector("#add_task_form").addEventListener('submit', function (evt) {
    evt.preventDefault();

var formInputs = {
    name_input: document.querySelector("#name_input").value,
    description_input: document.querySelector("#description_input").value,
    type_input: document.querySelector("#type_input").value,
    duration_input: document.querySelector("#duration_input").value
}
console.log(formInputs)

fetch("/add_task",  {
    method: 'POST',
    body: JSON.stringify(formInputs),
    headers: {
      'Content-Type': 'application/json',
    },
  })
//parse json response from server
.then((response) => response.json())
//update the dom object with the task data
.then((results) => {
    // select by the id "tasks-list"
    const tasksList = document.getElementById('tasks-list');
    //use insertAdjacentHTML
    tasksList.insertAdjacentHTML('beforeend', `<li> <strong>Task Name:</strong> ${results.task_name} <br> <strong>Task Description:</strong> ${results.task_description} <br> <strong>Timer Duration:</strong> ${results.duration} seconds <br> <form method="post" action="/delete_task/${results.task_id}"> <button type="submit">Delete</button> </form> </li>`);
  });
});

//currently having the timer fetch user preferences for timer, could switch it to on-click
document.addEventListener('DOMContentLoaded', function () {
  // should route to user_info api created in server.py
  fetch("/api/user_info")
      .then(response => response.json())
      //update dom object
      .then(user => {
          // Set up the countdown timer based on work_session_time
          setupCountdownTimer(user.work_session_time);

          //listen for work/break toggle
            // Add event listeners to toggle between work and break sessions
            document.getElementById('work-session-btn').addEventListener('click', function () {
              setupCountdownTimer(user.work_session_time);
          });

          //fill timer with break_session_time value instead
          document.getElementById('break-session-btn').addEventListener('click', function () {
              setupCountdownTimer(user.break_session_time);
          });
      })
    });

//using work_session_time fetched from last function
function setupCountdownTimer(minutes) {
  let timerElement = document.getElementById('countdown-timer');

  let totalTimeInSeconds = minutes * 60; // lets user enter time as minutes
  //add container to later store return value from setInterval
  let timerInterval = null;

  //format remaining time and update "countdown-timer"
  function updateTimerDisplay() {
      let minutes = Math.floor(totalTimeInSeconds / 60);
      let seconds = totalTimeInSeconds % 60;

      // return string to display time
      let formattedTime = `${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

      // update "countdown-timer"
      timerElement.innerText = formattedTime;
  }

  function startTimer() {
      timerInterval = setInterval(function () {
          //keep timer updating as long as it is still counting down
          if (totalTimeInSeconds > 0) {
              totalTimeInSeconds--;
              updateTimerDisplay();
          } else {
            // clear timer when its finished
              clearInterval(timerInterval);
          }
      }, 1000); // update every 1000 milliseconds, or every second
  }

  function stopTimer() {
      clearInterval(timerInterval);
  }

  // populate timer on page load
  updateTimerDisplay();

  // start the timer when a button is clicked
  document.getElementById('start-timer-btn').addEventListener('click', startTimer);

  // for stop button
  document.getElementById('stop-timer-btn').addEventListener('click', stopTimer);
}


