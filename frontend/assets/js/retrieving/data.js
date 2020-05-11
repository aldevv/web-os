const endpoint = "http://localhost:8000/api/prog"
fetch(endpoint)
.then(response => response.json())
.then(data => {
    console.log(data);
    console.log("acumulador: ", data['acumulador']);
    console.log(data['variables']);
    console.log(data['tags']);
    console.log("memory: ", data['memory']);
    console.log(data['stdout']);
});