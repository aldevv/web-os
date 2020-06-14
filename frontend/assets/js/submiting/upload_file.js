import {mode} from '../update/update_forms.js';

myform.addEventListener("submit", e => {
    e.preventDefault();
    mode.setAttribute("src", "assets/images/Kernel.png")
    const myform = document.getElementById("myform")
    const myfile = document.getElementById("myfile")
    const endpoint  = myform.getAttribute("action")
    const formData  = new FormData();
    formData.append("file", myfile.files[0])
    // console.log(myfile.files)
    fetch(endpoint, {
        method: "POST",
        body:   formData,

    })
    .then(text => console.log(text))
    .catch(console.error);
});



