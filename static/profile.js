// alert("profile.js is connected!");

/**
 * What we have now:
 * a countdown time that works, with start + stop functionality
 *
 * We we have kind of working:
 * - ability to add tasks
 * - ability to remove tasks
 * - ability to load tasks
 *
 * What we need for tasks to work
 * - Ability to start task
 * - Ability to end task
 *
 * What do we need for these?
 * - Persistence of a the timer
 * - We need to render timer updates
 *
 *
 * Option 2, reduced functionality:
 *
 *
 */

var intervalHandle = null;
var currTaskReference = null;
var currTaskId = null;

var trackedTimeById = {};

function startTask(taskId) {
  if (taskId === currTaskId) {
    return;
  } else {
    currTaskId = taskId;
  }
  var timeRemainingElId = `#duration-${taskId}`;
  var globalTimeRemainingElId = "#countdown-timer";
  function renderTimer(timeRemaining) {
    document.querySelector(timeRemainingElId).innerText = timeRemaining;
    document.querySelector(globalTimeRemainingElId).innerText = timeRemaining;
  }

  // this tracks time for multiple timers if
  // e.g. i start timer A, start timer B, then go back to A
  if (trackedTimeById[taskId] === undefined) {
    var taskDurationString =
      document.querySelector(timeRemainingElId).innerText;
    var duration = parseInt(taskDurationString, 10);
    trackedTimeById[taskId] = duration;
  }
  // render the current time
  renderTimer(trackedTimeById[taskId]);

  // clear any existing interval
  // so that no two timers are running at once
  if (intervalHandle) {
    clearInterval(intervalHandle);
  }

  // start ticking down the clock
  intervalHandle = setInterval(function () {
    // stop if we reach zero
    if (trackedTimeById[taskId] <= 0) {
      alert("we are done");
      intervalHandle;
      clearInterval(intervalHandle);
      return;
    }
    // decreemt the time by 1 second
    trackedTimeById[taskId]--;
    // render the update
    renderTimer(trackedTimeById[taskId]);

    // TODO delete the task from the DOM
    // TODO delete the task from the DB
  }, 1000);
}

function stopTask(taskId) {
  if (currTaskId !== taskId) {
    console.log("ya cant stop what ya havent started");
    return;
  }

  // clear the interval so we stop ticking down
  if (intervalHandle) {
    clearInterval(intervalHandle);
  }
  // clear the taskId so we don't get into a state
  // where we can't restart
  currTaskId = null;
}

document
  .querySelector("#add_task_form")
  .addEventListener("submit", function (evt) {
    evt.preventDefault();

    var formInputs = {
      name_input: document.querySelector("#name_input").value,
      description_input: document.querySelector("#description_input").value,
      type_input: document.querySelector("#type_input").value,
      duration_input: document.querySelector("#duration_input").value,
      timer_number: document.querySelector("#timer_number_input").value,
    };
    console.log(formInputs);

    fetch("/add_task", {
      method: "POST",
      body: JSON.stringify(formInputs),
      headers: {
        "Content-Type": "application/json",
      },
    })
      //parse json response from server
      .then((response) => response.json())
      //update the dom object with the task data
      .then((results) => {
        // select by the id "tasks-list"
        const tasksList = document.getElementById("tasks-list");
        //use insertAdjacentHTML
        tasksList.insertAdjacentHTML(
          "beforeend",
          `<li id=${results.task_id}>
             <strong>Task Name:</strong>
              ${results.task_name}
              <br>
              <strong>Task Description:</strong>
              ${results.task_description}
              <br>
              <strong>Timer Duration:</strong>
              <span id=${results.task_id}-timer>${results.duration}</span> seconds 
              <br> 
              <form method="post" action="/delete_task/${result.task_id}">
                <button type="submit">Delete</button>
              </form>
            </li>`
        );
      });
  });

//currently having the timer fetch user preferences for timer, could switch it to on-click
document.addEventListener("DOMContentLoaded", function () {
  // should route to user_info api created in server.py
  fetch("/api/user_info")
    .then((response) => response.json())
    //update dom object
    .then((user) => {
      // Set up the countdown timer based on work_session_time
      setupCountdownTimer(user.work_session_time);

      //listen for work/break toggle
      // Add event listeners to toggle between work and break sessions
      document
        .getElementById("work-session-btn")
        .addEventListener("click", function () {
          setupCountdownTimer(user.work_session_time);
        });

      //fill timer with break_session_time value instead
      document
        .getElementById("break-session-btn")
        .addEventListener("click", function () {
          setupCountdownTimer(user.break_session_time);
        });

      // Iterate over each task card and add event listeners
      // we don't have access to tasks table, only info stored in html
      //remember that getAttribute only gets the task id number
      //create a fetch request (and a new route in server) to get info for single task (post)
      //send task id via post request in that fetch request
      //in the .then of the fetch request, parse JSON and send info to profile.js
      // document.querySelectorAll(".start-task-btn").forEach((startBtn) => {
      //   const taskId = startBtn.dataset.taskId;
      //   console.log(taskId);
      //   const task = tasks.find((task) => task.task_id === parseInt(taskId));

      //   startBtn.addEventListener("click", function (evt) {
      //     // Start the timer with the task's work session time and timer_number
      //     setupCountdownTimer(task.duration, task.timer_number);
      //   });
      // });

      // Add event listeners for stop buttons
      document.querySelectorAll(".stop-task-btn").forEach((stopBtn) => {
        stopBtn.addEventListener("click", stopTimer);
      });
    });
});

//using work_session_time fetched from last function
function setupCountdownTimer(minutes, timer_number = 2) {
  let timerElement = document.getElementById("countdown-timer");

  let totalTimeInSeconds = minutes * 60; // lets user enter time as minutes
  //add container to later store return value from setInterval
  let timerInterval = null;
  let remainingCycles = timer_number;

  //format remaining time and update "countdown-timer"
  function updateTimerDisplay() {
    let minutes = Math.floor(totalTimeInSeconds / 60);
    let seconds = totalTimeInSeconds % 60;

    // return string to display time
    let formattedTime = `${minutes < 10 ? "0" : ""}${minutes}:${
      seconds < 10 ? "0" : ""
    }${seconds}`;

    // update "countdown-timer"
    timerElement.innerText = formattedTime;
  }

  function startTimer() {
    timerInterval = setInterval(function () {
      //keep timer updating as long as it is still counting down
      if (totalTimeInSeconds > 0 && remainingCycles > 0) {
        totalTimeInSeconds--;
        updateTimerDisplay();
      } else {
        // clear timer when its finished
        clearInterval(timerInterval);

        // alert the user when the timer completes all cycles
        if (remainingCycles === 0) {
          alert(`Time's up for ${task_name}!`);
        }
        //refill timer if still cycles to complete
        if (remainingCycles > 0) {
          remainingCycles--;
          totalTimeInSeconds = minutes * 60;
          //start timer on work cycle
          //each cycle handles a pair
          startTimer();
          //invoke break timer
        }
      }
    }, 1000); // update every 1000 milliseconds, or every second
  }

  function stopTimer() {
    clearInterval(timerInterval);
  }

  // populate timer on page load
  updateTimerDisplay();

  // start the timer when a button is clicked
  document
    .getElementById("start-timer-btn")
    .addEventListener("click", startTimer);

  // for stop button
  document
    .getElementById("stop-timer-btn")
    .addEventListener("click", stopTimer);
}
