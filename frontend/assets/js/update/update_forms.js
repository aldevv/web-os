import {getData, runAll} from '../retrieving/data.js';

let monitor = document.getElementById('monitor')
let variables_table = document.getElementById('var')
let tags_table = document.getElementById('tag')
let instruction_table = document.getElementById('instruction')
// let memory_table = document.getElementById('memory')

getData()
.then(data => {
    console.log(data);
    console.log("acumulador: ", data['acumulador']);
    console.log(data['tags']);
    console.log("instructions: ", data['instructions']);
    console.log(data['stdout']);
    console.log(data['variables']);
    let id = 0;
    data['variables'].forEach(element => {
        variables_table.innerHTML += "<tbody>\ <tr> \ <td>" + id++ + "</td> \ <td>" + element + "</td> \ </tr>\ </tbody>";
    });

    id = 0;
    data['tags'].forEach(element => {
        tags_table.innerHTML += "<tbody>\ <tr> \ <td>" + id++ + "</td> \ <td>" + element + "</td> \ </tr>\ </tbody>";
    });

    id = 0;
    data['instructions'].forEach(element => {
        element = element.join(' ')
        instruction_table.innerHTML += "<tbody>\ <tr> \ <td>" + id++ + "</td> \ <td>" + element + "</td> \ </tr>\ </tbody>";
    });
});

const correrButton = document.getElementById("correr")
correrButton.addEventListener("click", e => {
    runAll()
    .then(data => {
        console.log(data)
        data['stdout'].forEach(element => {
            monitor.innerHTML += element+"\ ";
        });

    });
});