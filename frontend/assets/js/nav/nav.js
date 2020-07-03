
memoria.addEventListener("change", e => {
    e.preventDefault();
    const memoria = document.getElementById("memoria")
    const endpoint  = 'http://localhost:8000/api/nav';
    let data = {'memoria': e.target.value};
    fetch(endpoint, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),

    }).catch(console.error);
});

kernel.addEventListener("change", e => {
    e.preventDefault();
    const kernel = document.getElementById("kernel")
    const endpoint  = 'http://localhost:8000/api/nav';
    let data = {'kernel': e.target.value};
    fetch(endpoint, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),

    }).catch(console.error);
});

quantum.addEventListener("change", e => {
    e.preventDefault();
    const quantum = document.getElementById("quantum")
    const endpoint  = 'http://localhost:8000/api/nav';
    let data = {'quantum': e.target.value};
    fetch(endpoint, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),

    }).catch(console.error);
});