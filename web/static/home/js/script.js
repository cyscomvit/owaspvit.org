/*
VIEW IN FULL SCREEN MODE
FULL SCREEN MODE: http://salehriaz.com/404Page/404.html

DRIBBBLE: https://dribbble.com/shots/4330167-404-Page-Lost-In-Space
*/
window.addEventListener("load", ()=> {
	const loader = document.querySelector(".pre_loader");
	const hom_lod=document.querySelector(".load_test");
	setTimeout(function(){
		loader.style.display='none';
		hom_lod.classList.remove("home_load");
	},200);	
})