const memory = document.getElementById("mostrarMemoria");
memory.addEventListener("click", ()=> {

    // toggleProgram();
    console.log("i will toggle!");
    toggleMemory();
    console.log("i toggled!");
});

// function toggleProgram() {
//     var program = document.getElementById("something");
//     var display = window.getComputedStyle(program, null).getPropertyValue("display");
//     console.log(display);
//     if (display == "block")
//         program.style.display = "none";
//     else
//         program.style.display = "block";
// }

function toggleMemory() {
    var memory = document.getElementById("popup-memory");
    var display = window.getComputedStyle(memory, null).getPropertyValue("display");
    if (display == "none")
        setStyle(memory, "display: block; margin-top: 5%;");
    else
        setStyle(memory, "display: none; margin-top: 5%;");
}

function setStyle(el, css){
  el.setAttribute('style', css);
}