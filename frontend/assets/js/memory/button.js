let memory = document.getElementById("mostrarMemoria");
memory.addEventListener("click", ()=> {
    toggleMemory();
});

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