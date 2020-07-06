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

    const algorithm_options = document.getElementById("algoritmos");
    let chosen_algorithm = algorithm_options.options[algorithm_options.selectedIndex];
    console.log("chosen algorithm ", chosen_algorithm.value);
    formData.set("algorithm", chosen_algorithm.value);
    console.log("formDato", formData);

    fetch(endpoint, {
        method: "POST",
        body:   formData,

    })
    .then(text => console.log(text))
    .catch(console.error);
});



