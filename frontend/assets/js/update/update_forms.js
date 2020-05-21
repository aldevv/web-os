import {getData, runAll} from '../retrieving/data.js';

// let memory_table = document.getElementById('memory')

let variables    = [];
let tags         = [];
let instructions = [];
getData()
.then(data => {
    consoleLogData(data);

    let variables_table = document.getElementById('var');
    data['variables'].forEach(element => variables.push(element));
    createTable(variables_table, variables);

    let tags_table = document.getElementById('tag');
    data['tags'].forEach(element => tags.push(element) );
    createTable(tags_table, tags);

    let instruction_table = document.getElementById('instruction')
    data['instructions'].forEach(element => instructions.push(element));
    createTableInstructions(instruction_table, instructions);
})
.then(() => {
    const correrButton = document.getElementById("correr")
    correrButton.addEventListener("click", e => {
        runAll()
        .then(data => {
            console.log("after_run: ", data)
            let monitor = document.getElementById('monitor')
            data['stdout'].forEach(element => {
                monitor.innerHTML += element+"\ ";
            });

        });
    });
});

function consoleLogData(data) {

    console.log("All: ", data);
    console.log("acumulador: ", data['acumulador']);
    console.log("tags: ", data['tags']);
    console.log("instructions: ", data['instructions']);
    console.log("variables: ", data['variables']);
}

function createLeaForm() {
    let form = document.getElementById('myform')
    let original = form.innerHTML;
    form.innerHTML += '<input id="lea" type="input" placeholder="ingrese un valor" ">'
    form.innerHTML += '<input id="leaButton" type="button" value="enter" ></input>';
    let leaButton = document.getElementById('leaButton');
    leaButton.addEventListener("click", e => {
        e.preventDefault();
        let lea = document.getElementById('lea');
        let data = {'lea': lea.value};
        const endpoint  = 'http://localhost:8000/api/lea';
        fetch(endpoint, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        })
        .then(() => {
            // make it work for any number of lea
            // form.innerHTML = original;
        })
        .catch(console.error);
    });
}

function createTable(table, listElements) {
    let id = 0;
    let current_color = 0;
    let colors = ["#212121", '#303030', "purple", "blue", "green"];
    listElements.forEach(program => {
        program.forEach(element => {
            table.innerHTML += '<tbody style="background-color:'+colors[current_color]+ '" >\ <tr> \ <td>' + id++ + '</td> \ <td>' + element + '</td> \ </tr>\ </tbody>';
        });
        current_color++;
    });
}

function createTableInstructions(table, listElements) {

    let id = 0;
    listElements.forEach(element =>{
        if(element[0] == "lea") {
            createLeaForm()        
        }
        element = element.join(' ')
        table.innerHTML += "<tbody>\ <tr> \ <td>" + id++ + "</td> \ <td>" + element + "</td> \ </tr>\ </tbody>";
    });
}
