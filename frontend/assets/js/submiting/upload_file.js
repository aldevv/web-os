myform.addEventListener("submit", e => {
    e.preventDefault();
    const myform = document.getElementById("myform")
    const myfile = document.getElementById("myfile")
    const endpoint  = myform.getAttribute("action")
    const formData  = new FormData();
    formData.append("file", myfile.files[0])
    // console.log(myfile.files)
    fetch(endpoint, {
        method: "POST",
        body:   formData
    }).catch(console.error);
});

paso.addEventListener("click", e => {
    e.preventDefault();
    const paso   = document.getElementById("paso")
    const myfile = document.getElementById("myfile")
    const endpoint  = 'http://localhost:8000/api/step'
    const formData  = new FormData();
    formData.append("file", myfile.files[0])
    fetch(endpoint, {
        method: "POST",
        body:   formData
    }).catch(console.error);
});