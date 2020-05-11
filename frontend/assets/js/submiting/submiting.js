const myform = document.getElementById("myform")
const myfile = document.getElementById("myfile")

myform.addEventListener("submit", e => {
    e.preventDefault();
    const endpoint  = myform.getAttribute("action")
    const formData  = new FormData();
    formData.append("file", myfile.files[0])
    // console.log(myfile.files)
    fetch(endpoint, {
        method: "POST",
        body:   formData
    }).catch(console.error);
});