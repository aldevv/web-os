export const getData = ()=> fetch("http://localhost:8000/api/compile")
                            .then(response => response.json())
                            .catch(console.error);


export const getRunAll = ()=>   fetch("http://localhost:8000/api/run")
                            .then(response => response.json())
                            .catch(console.error);

export const getPaso = ()=>   fetch("http://localhost:8000/api/step")
                            .then(response => response.json())
                            .catch(console.error);

// export const createLea = ()=>   fetch("http://localhost:8000/api/leaCreateForm")
//                             .then(response => response.json())
//                             .catch(console.error);

// const runAll = document.getElementById("correr")
// runAll.addEventListener("click", e => {
