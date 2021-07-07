(function () {
    const second = 1000,
          minute = second * 60,
          hour = minute * 60,
          day = hour * 24;
  
    let event = "Jul 24, 2021 00:00:00",
        countDown = new Date(event).getTime(),
        x = setInterval(function() {    
  
          let now = new Date().getTime(),
              distance = countDown - now;
  
          document.getElementById("days").innerText = Math.floor(distance / (day)),
            document.getElementById("hours").innerText = Math.floor((distance % (day)) / (hour)),
            document.getElementById("minutes").innerText = Math.floor((distance % (hour)) / (minute)),
            document.getElementById("seconds").innerText = Math.floor((distance % (minute)) / second);
  
          //do something later when date is reached
          if (distance < 0) {
            let headline = document.getElementById("headline"),
                countdown = document.getElementById("countdown"),
                content = document.getElementById("content");
  
          
            countdown.style.display = "none";
            content.style.display = "block";
  
            clearInterval(x);
          }
          //seconds
        }, 0)
    }());

const modal = document.querySelector(".modal-container")
var sidebar = document.querySelector(".sidebar-container");

const handleNav = () => {
    console.log("Clicked!");
    sidebar.className="sidebar-container-active";
}
const handleClose = () => {
    sidebar.className="sidebar-container";
}
const modalControl = () => {
    
  sidebar.className="sidebar-container";
  if (!modal.style.display || modal.style.display=="none"){
      modal.style.display="flex";
      console.log("called!");
  }
  else {
      modal.style.display="none";
  }
}
