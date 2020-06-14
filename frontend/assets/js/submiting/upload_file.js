import {mode} from '../update/update_forms.js';

myform.addEventListener("submit", e => {
    e.preventDefault();
    mode.setAttribute("src", "assets/images/Kernel.png");
    const myform = document.getElementById("myform");
    const myfile = document.getElementById("myfile");
    const endpoint  = myform.getAttribute("action");
    const formData  = new FormData();
    let numFiles = myfile.files.length;
    for(var i=0; i<numFiles; i++)
        formData.set("file["+i+"]", myfile.files[i]);

    fetch(endpoint, {
        method: "POST",
        body:   formData,

    })
    .then(text => console.log(text))
    .catch(console.error);
});



