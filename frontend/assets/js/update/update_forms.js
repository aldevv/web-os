import {getData, runAll} from '../retrieving/data.js';

// let memory_table = document.getElementById('memory')

let variables    = [];
let tags         = [];
let programs     = [];
let colors = ["#212121", "#330077",'#7a1b6c', '#303030', "blue", "green"];
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
    data['programs'].forEach(program => programs.push(program));
    createTableInstructions(instruction_table, programs);

    let registers_table = document.getElementById('registers')
    createTableRegisters(registers_table, data['registers'])


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
    console.log("variables: ", data['variables']);
    console.log("tags: ", data['tags']);
    console.log("programs: ", data['programs']);
    console.log("registers: ", data["registers"])
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
            console.log(original)
            console.log(form.innerHTML)
        })
        .catch(console.error);
    });
}

function createTable(table, listElements) {
    let id = 0;
    let current_color = 0;
    listElements.forEach(program => {
        program.forEach(element => {
            table.innerHTML += '<tbody style="background-color:'+ colors[current_color] + '" >\ <tr> \ <td>' + id++ + '</td> \ <td>' + element + '</td> \ </tr>\ </tbody>';
        });
        current_color++;
    });
}

function createTableInstructions(table, listInstructions) {

    let id = 0;
    let current_color = 0;
    listInstructions.forEach(instruction =>{
        instruction.forEach(element => {
            if(element[0] == "lea") {
                createLeaForm()        
            }
            element = element.join(' ')
            table.innerHTML += '<tbody style="background-color:'+ colors[current_color] + '" >\ <tr> \ <td>' + id++ + '</td> \ <td>' + element + '</td> \ </tr>\ </tbody>';
        });
        current_color++;
    });
}
let idProg = 1;
function createTableRegisters(table, registers) {
    let filenames       = registers[0]
    let instruction_num = registers[1]
    let rb              = registers[2]
    let rlc             = registers[3]
    let rlp             = registers[4]
    let length = rb.length
    for(let i=0; i< length; i++) {
            table.innerHTML += '<tbody style="background-color:'+colors[i]+ '" >\ <tr> \ <td> 000' + idProg++ + '</td> \ <td>' + filenames[i] + '</td> \ <td>' + instruction_num[i] + '</td> \ <td>' + rb[i] + '</td> \  <td>' + rlc[i] + '</td> \ <td>' + rlp[i] + '</td> \ </tr>\ </tbody>';
    }
}
