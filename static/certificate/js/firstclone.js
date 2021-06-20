var input = document.querySelector('.search-form');
var search = document.querySelector('input')
var button = document.querySelector('.button');
button.addEventListener('click', function(e) {
  e.preventDefault();
  input.classList.toggle('active');
})
search.addEventListener('focus', function() {
  input.classList.add('focus');
})

search.addEventListener('blur', function() {
  search.value.length != 0 ? input.classList.add('focus') : input.classList.remove('focus');
})

document.addEventListener('DOMContentLoaded', function () {
  particleground(document.getElementById('particles'), {
    dotColor: '#fff',
    lineColor: '#000',
    directionX: 'right',
    density: '7000',
    particleRadius: '12',
    lineWidth: '0.5',
  });
  var intro = document.getElementById('intro');
  intro.style.marginTop = - intro.offsetHeight / 2 + 'px';
}, false);


// var canvas = document.querySelector('canvas');
// var c = canvas.getContext('2d');

// canvas.width = window.innerWidth;
// canvas.height = window.innerHeight;

// window.addEventListener("resize", function() {
//   canvas.width = window.innerWidth;
//   canvas.height = window.innerHeight;		
// });
// function Star() {
//   this.radius = (Math.random() * 10) + 5;
//   this.x = this.radius + (canvas.width - this.radius * 2) * Math.random();
//   this.y = -10; 
//   this.dx = (Math.random() - 0.5) * 20;
//   this.dy = 30;
//   this.gravity = .5;
//   this.friction = .54;

//   this.update = function() {

//     // Bounce particles off the floor of the canvas
//     if (this.y + this.radius + this.dy >= canvas.height - groundHeight) {
//       this.dy = -this.dy * this.friction;
//       this.dx *= this.friction;
//       this.radius -= 3;

//       explosions.push(new Explosion(this));
//     } else {
//       this.dy += this.gravity;
//     }

//     // Bounce particles off left and right sides of canvas
//     if (this.x + this.radius + this.dx >= canvas.width || this.x - this.radius + this.dx < 0) {
//       this.dx = -this.dx;
//       this.dx *= this.friction;
//       explosions.push(new Explosion(this));
//     };

//     // Move particles by velocity
//     this.x += this.dx;
//     this.y += this.dy;

//     this.draw();

//     // Draw particles from explosion
//     for (var i = 0; i < explosions.length; i++) {
//         explosions[i].update();
//     }

//   }
//   this.draw = function() {
//     c.save();
//     c.beginPath();
//     c.arc(this.x, this.y, Math.abs(this.radius), 0, Math.PI * 2, false);

//     c.shadowColor = '#E3EAEF';
//     c.shadowBlur = 20;
//     c.shadowOffsetX = 0;
//     c.shadowOffsetY = 0;

//     c.fillStyle = "#E3EAEF";
//     c.fill();
//     c.closePath();
//     c.restore();
//   }
// }

// function Particle(x, y, dx, dy) {
//   this.x = x;
//   this.y = y; 
//   this.size = {
//     width: 2,
//     height: 2
//   };
//   this.dx = dx;
//   this.dy = dy;
//   this.gravity = .09;
//   this.friction = 0.88;
//   this.timeToLive = 3;
//   this.opacity = 1;

//   this.update = function() {
//     if (this.y + this.size.height + this.dy >= canvas.height - groundHeight) {
//       this.dy = -this.dy * this.friction;
//       this.dx *= this.friction;
//     } else {
//       this.dy += this.gravity;
//     }

//     if (this.x + this.size.width + this.dx >= canvas.width || this.x + this.dx < 0) {
//       this.dx = -this.dx;
//       this.dx *= this.friction;
//     };
//     this.x += this.dx;
//     this.y += this.dy;

//     this.draw();

//     this.timeToLive -= 0.01;
//     this.opacity -= 1 / (this.timeToLive / 0.01);
//   }
//   this.draw = function() {
//     c.save();
//     c.fillStyle = "rgba(227, 234, 239," + this.opacity + ")";
//     c.shadowColor = '#E3EAEF';
//     c.shadowBlur = 20;
//     c.shadowOffsetX = 0;
//     c.shadowOffsetY = 0;
//     c.fillRect(this.x, this.y, this.size.width, this.size.height);
//     c.restore();
//   }

//   this.isAlive = function() {
//     return 0 <= this.timeToLive;
//   }
// }

// function Explosion(star) {
//   this.particles = [];

//   this.init = function(parentStar) {
//     for (var i = 0; i < 8; i++) {
//       var velocity = {
//         x: (Math.random() - 0.5) * 5,
//         y: (Math.random() - 0.5) * 15, 
//       }
//         this.particles.push(new Particle(parentStar.x, parentStar.y, velocity.x, velocity.y));
//     }
//   }

//   this.init(star);

//   this.update = function() {
//     for (var i = 0; i < this.particles.length; i++) {
//         this.particles[i].update();
//         if (this.particles[i].isAlive() == false) {
//           this.particles.splice(i, 1);
//         }
//     }
//   }
// }


// function createMountainRange(mountainAmount, height,  color) {
//   for (var i = 0; i < mountainAmount; i++) {
//     var mountainWidth = canvas.width / mountainAmount;
//     c.beginPath();
//     c.moveTo(i * mountainWidth, canvas.height);
//     c.lineTo(i * mountainWidth + mountainWidth + 325, canvas.height);
//     c.lineTo(i * mountainWidth + mountainWidth / 2, canvas.height - height);
//     c.lineTo(i * mountainWidth - 325, canvas.height);
//     c.fillStyle = color;
//     c.fill();
//     c.closePath();
//   }
// }
// function MiniStar() {
//   this.x = Math.random() * canvas.width;
//   this.y = Math.random() * canvas.height;
//   this.radius = Math.random() * 3;

//   this.draw = function() {
//     c.save();
//     c.beginPath();
//       c.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);

//       c.shadowColor = '#E3EAEF';
//     c.shadowBlur = (Math.random() * 10) + 10;
//     c.shadowOffsetX = 0;
//     c.shadowOffsetY = 0;

//       c.fillStyle = "white";
//       c.fill();

//       c.closePath();	
//       c.restore();
//   }
// }
// var timer = 0;
// var stars = [];
// var explosions = [];
// var groundHeight = canvas.height * 0.15;
// var randomSpawnRate = Math.floor((Math.random() * 25) + 60)
// var backgroundGradient = c.createLinearGradient(0,0,0, canvas.height);
// backgroundGradient.addColorStop(0,"#171e26");
// backgroundGradient.addColorStop(1,"#3f586b");

// var miniStars = [];
// for (var i = 0; i < 150; i++) {
//   miniStars.push(new MiniStar());
// }




// function animate() {
//   window.requestAnimationFrame(animate);
//   c.fillStyle = backgroundGradient;
//   c.fillRect(0, 0, canvas.width, canvas.height);

//   for (var i = 0; i < miniStars.length; i++) {
//     miniStars[i].draw();
//   }
//   createMountainRange(1, canvas.height - 50, "#384551");
//   createMountainRange(2, canvas.height - 100,  "#2B3843");
//   createMountainRange(3, canvas.height - 300 , "#26333E");

//   c.fillStyle = "#182028";
//   c.fillRect(0, canvas.height - groundHeight, canvas.width, groundHeight);

    
  
//   for (var i = 0; i < stars.length; i++) {
//       stars[i].update();
//     // console.log(stars[0].isAlive());

//       if (stars[i].radius <= 0) {
//         stars.splice(i, 1);
//       }
//   }

//   for (var i = 0; i < explosions.length; i++) {
//       if (explosions[i].length <= 0) {
//         explosions.splice(i, 1);
//       }
//   }

//   timer ++;
//   // console.log(timer);
//   if (timer % randomSpawnRate == 0) {
//     stars.push(new Star());
//     randomSpawnRate = Math.floor((Math.random() * 10) + 75)
//   }

// }

// animate();