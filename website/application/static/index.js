// Adds a singular message unto the chat window
async function add_messages(msg, scroll) {
  if (typeof msg.name !== "undefined") {
    var date = dateNow();

    if (typeof msg.time !== "undefined") {
      var n = msg.time;
    } else {
      var n = date;
    }
    var global_name = await load_name();
    
    return await fetch("/get_color")
    .then(async function (response) {
      return await response.json();
    })
    .then(function (color) {
      var content =
      '<div class="container" style="background-color:#00000060; transition: 2s;">' +
      '<b style="color:#000;" class="right">' +
      msg.name +
      "</b><p>" +
      msg.message +
      '</p><span class="time-right">' +
      n +
      "</span></div>";
    if (global_name == msg.name) { // If message's sender = logged in user, make chatbox different (change align & color)
      content =
        '<div class="container darker" style="background-color:#00000080; transition: 2s;">' +
        '<b style="color:#000;" class="left">' +
        msg.name +
        "</b><p>" +
        msg.message +
        '</p><span class="time-left">' +
        n +
        "</span></div>";
    }
    // Actually update the page/chat window on user's screen
    var messageDiv = document.getElementById("messages");
    messageDiv.innerHTML += content;
      if (scroll) {
        scrollSmoothToBottom("messages");
      }

      // Updates color of chat window
      var chatwindow = document.getElementById("adaptivewindow");
      chatwindow.style.backgroundColor = color
      console.log(color);
      return color;
    });
  }

  if (scroll) {
    scrollSmoothToBottom("messages");
  }
}

async function load_name() {  // Loads name of user
  return await fetch("/get_name")
    .then(async function (response) {
      return await response.json();
    })
    .then(function (text) {
      return text["name"];
    });
}

async function load_messages() { // Loads messages from database
  return await fetch("/get_messages")
    .then(async function (response) {
      return await response.json();
    })
    .then(function (text) {
      console.log(text);
      return text;
    });
}

async function suppressor(message) {
  return await fetch("/check_message?message="+message)
    .then(async function (response) {
      return await response.json();
    })
    .then(function (text) {
      return text;
    });
}


// Sets size of chat window to be 70% of the full screen
$(function () { 
  $(".msgs").css({ height: $(window).height() * 0.7 + "px" });

  $(window).bind("resize", function () {
    $(".msgs").css({ height: $(window).height() * 0.7 + "px" });
  });
});

// Automatically scrolls chat window if there are too many messages
function scrollSmoothToBottom(id) { 
  var div = document.getElementById(id);
  $("#" + id).animate(
    {
      scrollTop: div.scrollHeight - div.clientHeight,
    },
    500
  );
}

// Gets date (in proper format)
function dateNow() {
  var date = new Date();
  var aaaa = date.getFullYear();
  var gg = date.getDate();
  var mm = date.getMonth() + 1;

  if (gg < 10) gg = "0" + gg;

  if (mm < 10) mm = "0" + mm;

  var cur_day = aaaa + "-" + mm + "-" + gg;

  var hours = date.getHours();
  var minutes = date.getMinutes();
  var seconds = date.getSeconds();

  if (hours < 10) hours = "0" + hours;

  if (minutes < 10) minutes = "0" + minutes;

  if (seconds < 10) seconds = "0" + seconds;

  return cur_day + " " + hours + ":" + minutes;
}

// Handles ALL socket tasks (receiving messages, sending messages, disconnections, and connections)
var socket = io.connect("http://" + document.domain + ":" + location.port);
socket.on("connect", async function () { // When any user connects to the server...
  var usr_name = await load_name();
  if (usr_name != "") {
    socket.emit("event", {
      message: usr_name + " just connected to the server!",
      connect: true,
    });
  }
  var form = $("form#msgForm").on("submit", async function (e) {
    e.preventDefault();

    // Handles getting input from message box
    let msg_input = document.getElementById("msg");
    let user_input = msg_input.value;
    let user_name = await load_name();

    // Clears message box value
    msg_input.value = "";

    // If user_input TOO NEGATIVE, RETURN!
    let pass = await suppressor(user_input.replace(/ /g,"_"))

    if(pass == 'TRUE'){
      // Sends message to all other users if it is deemed appropriate
      socket.emit("event", {  // Sends message to database as well
      message: user_input,
      name: user_name, 
    });
    }
    else
    {
      
      var warnmodal= 
      `<div class="modal fade" id="suppressor" data-backdrop="static" tabindex="-1" role="dialog" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="staticBackdropLabel">INAPPROPRIATE MESSAGE DETECTED</h5>
            </div>
            <div class="modal-body center">
              "${user_input}"
            </div>
            <div class="modal-body">
            Your message has been deemed inappropriate by our algorithms, please refrain from sending inappropriate messages!
            </div>
            <div class="modal-footer">
              <button onclick="window.location.href='/home';" class="btn btn-primary">I understand</button>
            </div>
          </div>
        </div>
      </div>`

      var page = document.getElementById("wholepage");
      page.innerHTML += warnmodal;
      $('#suppressor').modal('show');
    }
  });
});
socket.on("disconnect", async function (msg) {
  var usr_name = await load_name();
  socket.emit("event", { // When any user disconnects from server...
    message: usr_name + " just left the server...",
  });
});
socket.on("message response", function (msg) { // When a message is sent by any connected user...
  add_messages(msg, true);  // Add that msg to chat using add_messages
});

// On load of website, loads all past messages (from database) using /get_messages from index.js 
window.onload = async function () {
  var msgs = await load_messages(); // 
  for (i = 0; i < msgs.length; i++) {
    scroll = false;
    if (i == msgs.length - 1) {
      scroll = true;
    }
    add_messages(msgs[i], scroll);
  }

  let name = await load_name();
  if (name != "") { // If logged in...
    $("#login").hide();
  } else { // If logged out...
    $("#logout").hide();
    //$("#history").hide();
  }
};
