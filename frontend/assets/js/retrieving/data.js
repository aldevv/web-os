export const getData = ()=> fetch("http://localhost:8000/api/compile")
                            .then(response => response.json())
                            .catch(console.error);


export const runAll = ()=>   fetch("http://localhost:8000/api/run")
                            .then(response => response.json())
                            .catch(console.error);


// const runAll = document.getElementById("correr")
// runAll.addEventListener("click", e => {
