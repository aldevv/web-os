import {getData, getRunAll, getPaso} from '../retrieving/data.js';

// let memory_table = document.getElementById('memory')

let variables_table   = document.getElementById('var');
let tags_table        = document.getElementById('tag');
let instruction_table = document.getElementById('instruction');
let registers_table   = document.getElementById('registers');
let memory_table      = document.getElementById('memory-table');
let monitor           = document.getElementById('monitor');
let printer           = document.getElementById('printer');
export let mode              = document.getElementById('mode');

let variables = [];
let tags      = [];
let programs  = [];
let memory    = [];
let originalHtml = {'variables': null, 'tags': null, 'instruction': null, 'registers': null, 'memory': null};
let colors = ["#212121", "#330077",'#7a1b6c', '#303030', "blue", "green"];

getData()
.then(data => {
    update_forms(data);
})
.then(() => {
    const correrButton = document.getElementById("correr")
    correrButton.addEventListener("click", e => {
        getRunAll()
        .then(data => {
            showLogDataRun(data);
            showMonitorAndPrinter(data);
            refreshMemory(data);
            mode.setAttribute("src", "assets/images/Usuario.png")
        });
    });

    const paso   = document.getElementById("paso")
    paso.addEventListener("click", e => {
        e.preventDefault();
        const endpoint  = 'http://localhost:8000/api/step'
        fetch(endpoint, {
            method: "POST",
            body:   null,
        })
        .catch(console.error)
        .then(()=> {
            getPaso()
            .then(data => {
                showInMonitor(data, monitor);
                refreshMemory(data);
            });
        });
    });

    const limpiarButton = document.getElementById("limpiar")
    limpiarButton.addEventListener("click", e => {
        e.preventDefault();
        const endpoint  = 'http://localhost:8000/api/clean';
        monitor.innerHTML           = "";
        variables_table.innerHTML   = originalHtml['variables'];
        tags_table.innerHTML        = originalHtml['tags'];
        instruction_table.innerHTML = originalHtml['instruction'];
        registers_table.innerHTML   = originalHtml['register'];
        memory_table.innerHTML      = originalHtml['memory'];
        const memoria = document.getElementById("memoria");
        const kernel = document.getElementById("kernel");
        const acumulador = document.getElementById("acumulador");
        let data = {'memoria': memoria.value, 'kernel': kernel.value, 'acumulador': acumulador.value};
        fetch(endpoint, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        }).catch(console.error);
    });
});

function refreshMemory(data) {
    memory = [];
    memory_table.innerHTML = originalHtml['memory'];
    data['memory'].forEach(slot => memory.push(slot));
    createTableMemory(memory);
}

function showInMonitor(data, monitor) {
    if (data['steps'].length != 0) {
        let elem = data['steps'].pop();
        monitor.innerHTML = elem + "\ ";
    }

    if (data['printer'].length > 0) {
        printer.innerHTML = "impresora: ";
        data['printer'].forEach(element => {
            printer.innerHTML +=  element + " |  ";
        });
    }
}

export function update_forms(data) {
    consoleLogDataCompile(data);
    data['variables'].forEach(element => variables.push(element));
    createTable(variables_table, variables);
    data['tags'].forEach(element => tags.push(element));
    createTable(tags_table, tags);
    data['programs'].forEach(program => programs.push(program));
    createTableInstructions(programs);
    createTableRegisters(data);
    data['memory'].forEach(slot => memory.push(slot));
    createTableMemory(memory);
}

function showLogDataRun(data) {
    console.log("after_run: " , data['stdout']);
    console.log("steps: "     , data['steps']);
    console.log("memory: "    , data['memory']);
}

function showMonitorAndPrinter(data) {
    data['stdout'].forEach(element => {
        monitor.innerHTML += element + "<br>";
    });

    if (data['printer'].length > 0) {
        printer.innerHTML = "impresora: ";
        data['printer'].forEach(element => {
            printer.innerHTML +=  element + " |  ";
        });
    }
}


function createTableRegisters(data) {
    if (data['programs'].length >= 1)
        formatRegisters(data['registers']);
}

function consoleLogDataCompile(data) {

    console.log("All: "             , data);
    console.log("acumulador: "      , data['acumulador']);
    console.log("variables: "       , data['variables']);
    console.log("tags: "            , data['tags']);
    console.log("programs: "        , data['programs']);
    console.log("registers: "       , data["registers"])
    console.log("memory: "          , data["memory"])
    console.log("memory Available: ", data["memoryAvailable"])
    console.log("memory used: "     , data["memoryUsed"])
}

function createLeaForm(leaItems) { // pasa la liista, cuando presione el boton ok, continuar con next
    let numLea = leaItems.length;
    let lea = document.getElementById('lea');
    let leaButton = document.getElementById('leaButton');
    if(numLea == 0) {
        lea.setAttribute('style', "display: none");
        leaButton.setAttribute('style', "display: none");
        return;
    }
    lea.setAttribute('style', "display: block");
    leaButton.setAttribute('style', "display: block");
    lea.setAttribute('placeholder', "ingrese un valor para " + leaItems[0]);
    leaButton.addEventListener("click", function press() {
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
            lea.value = "";
            leaItems.shift();
            leaButton.removeEventListener("click", press);
            createLeaForm(leaItems);
        })
        .catch(console.error);
    });
}

function createTable(table, listElements) {
    let current_color = 0;
    if(table['id'] == 'var') {
        saveOriginalHtml('variables', table.innerHTML);
    } else {
        saveOriginalHtml('tags', table.innerHTML);

    }
    listElements.forEach(program => {
        program.forEach(element => {
            let pos = element[0];
            let varName = element[1];
            table.innerHTML += '<tbody style="background-color:'+ colors[current_color] + '" >\ <tr> \ <td>' + pos + '</td> \ <td>' + varName + '</td> \ </tr>\ </tbody>';
        });
        current_color++;
    });
}

function createTableInstructions(listInstructions) {

    let id = 0;
    let current_color = 0;
    let leaItems = []
    let numInstructions = listInstructions.length
    let current_instruction = 0;
    saveOriginalHtml('instruction', instruction_table.innerHTML);
    
    listInstructions.forEach(instruction =>{
        current_instruction++;
        instruction.forEach(element => {
            
            if(current_instruction == numInstructions) { // if last instruction check lea
                if(element[0] == "lea") {
                    leaItems.push(element[1]);
                }
            }
            element = element.join(' ')
            instruction_table.innerHTML += '<tbody style="background-color:'+ colors[current_color] + '" >\ <tr> \ <td>' + id++ + '</td> \ <td>' + element + '</td> \ </tr>\ </tbody>';
        });
        current_color++;
    });

    createLeaForm(leaItems);       
}

let idProg = 1;
function formatRegisters(registers) {
    let filenames       = registers[0];
    let instruction_num = registers[1];
    let rb              = registers[2];
    let rlc             = registers[3];
    let rlp             = registers[4];
    let length = rb.length;
    saveOriginalHtml('register', registers_table.innerHTML);
    for(let i=0; i< length; i++) {
            registers_table.innerHTML += '<tbody style="background-color:'+colors[i]+ '" >\ <tr> \ <td> 000' + idProg++ + '</td> \ <td>' + filenames[i] + '</td> \ <td>' + instruction_num[i] + '</td> \ <td>' + rb[i] + '</td> \  <td>' + rlc[i] + '</td> \ <td>' + rlp[i] + '</td> \ </tr>\ </tbody>';
    }
}

function createTableMemory(memory) {
    saveOriginalHtml('memory', memory_table.innerHTML);
    let current_color = 0;
    memory.forEach(slot => {
        memory_table.innerHTML += '<tbody style="background-color:' + colors[current_color] + '" >\ <tr> \ <td>' + slot[0] + '</td> \ <td>' + slot[1] + '</td> \ </tr>\ </tbody>';
    });
}

function saveOriginalHtml(type, table) {
    if (originalHtml[type] == null)
        originalHtml[type] = table;
}
