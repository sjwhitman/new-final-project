 // fetch user information from flask instance. then call updateUser to update HTML
    //this function returns a promise to return the response object
    // async function fetchUserInfo() {
    //     try {
    //         const response = await fetch('/api/user_info');
    //         //try to store json response data in variable, wait for server's reply
    //         const userData = await response.json();

    //         updateUser(userData);
    //     //if server never replies, execute error code (which is just a message in the debug console)
    //     } catch (error) {
    //         console.error('Cannot fetch user information');
    //     }
    // }

    // // updates html elements with new user data
    // function updateUser(userData) {
    //     //target the p elements with ids 'work-session-time' and 'break-session-time;
    //     const workSessionTimeBlock = document.getElementById('work-session-time');
    //     const breakSessionTimeBlock = document.getElementById('break-session-time');

    //     // check if the two p elements are connected to frontend.js
    //     if (workSessionTimeBlock && breakSessionTimeBlock) {
    //         // update p tag content with userdata object
    //         workSessionTimeBlock.textContent = `Work Session Time: ${userData.work_session_time} minutes`;
    //         breakSessionTimeBlock.textContent = `Break Session Time: ${userData.break_session_time} minutes`;
    //     }
    // }