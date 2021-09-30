const sidebar = document.querySelector(".sidebar-container");

const handleNav = () => {
    console.log("Clicked!");
    sidebar.className="sidebar-container-active";
}
const handleClose = () => {
    sidebar.className="sidebar-container";
}
// const modalControl = () => {
    
//     sidebar.className="sidebar-container";
//     if (!modal.style.display || modal.style.display=="none"){
//         modal.style.display="flex";
//         console.log("called!");
//     }
//     else {
//         modal.style.display="none";
//     }
// }
