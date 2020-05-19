import {getData, runAll} from '../retrieving/data.js';

// let memory_table = document.getElementById('memory')

getData()
.then(data => {
    console.log("All: ", data);
    console.log("acumulador: ", data['acumulador']);
    console.log("tags: ", data['tags']);
    console.log("instructions: ", data['instructions']);
    console.log("variables: ", data['variables']);
    let id = 0;
    let variables_table = document.getElementById('var')
    data['variables'].forEach(element => {
        variables_table.innerHTML += "<tbody>\ <tr> \ <td>" + id++ + "</td> \ <td>" + element + "</td> \ </tr>\ </tbody>";
    });

    id = 0;
    let tags_table = document.getElementById('tag')
    data['tags'].forEach(element => {
        tags_table.innerHTML += "<tbody>\ <tr> \ <td>" + id++ + "</td> \ <td>" + element + "</td> \ </tr>\ </tbody>";
    });

    id = 0;
    let instruction_table = document.getElementById('instruction')
    data['instructions'].forEach(element => {
        if(element[0] == "lea") {
            createLeaForm()        
        }
        element = element.join(' ')
        instruction_table.innerHTML += "<tbody>\ <tr> \ <td>" + id++ + "</td> \ <td>" + element + "</td> \ </tr>\ </tbody>";
    });
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

