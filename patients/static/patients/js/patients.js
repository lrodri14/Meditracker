////Checked
////Sound

if (document.querySelector('#add_patients') !== 'undefined' && document.querySelector('#add_patients') !== 'null'){
    var addPatient = document.querySelector('#add_patients')
}

if (document.querySelector('.fa-filter') !== 'undefined' && document.querySelector('.fa-filter') !== 'null'){
    var i = document.querySelector('.fa-filter')
}

if (document.querySelector('form') !== 'undefined' && document.querySelector('form') !== 'null'){
    var form = document.querySelector('form')
}

if (document.querySelector('#id_patient') !== 'undefined' && document.querySelector('#id_patient') !== 'null'){
    var input = document.querySelector('#id_patient')
}

if (document.querySelectorAll('button') !== 'undefined' && document.querySelectorAll('button') !== 'null'){
    var button = document.querySelectorAll('button')
}

if (document.querySelector('table') !== 'undefined' && document.querySelector('table') !== 'null'){
    var table = document.querySelector('table')
    var tbody = document.querySelector('tbody')
}

if (document.querySelectorAll('.delete') !== 'undefined' && document.querySelectorAll('.delete') !== 'null'){
    var deletion = document.querySelectorAll('.delete')
}

if (document.querySelectorAll('.modal') !== 'undefined' && document.querySelectorAll('.modal') !== 'null'){
    var modal = document.querySelector('.modal')
    var modalContent = document.querySelector('.modal-content')
}

// Async Functions

// Delete button event
async function deleteAW(url){
    const result = await fetch(url)
    const data = await result.json()
    return data
}

// Form Submit
async function submitFormAW(form, csrfmiddlewaretoken, button){
    const result = await fetch(form.action, {method:'POST', headers:{'X-CSRFToken': csrfmiddlewaretoken}})
    const data = await result.json()
    return data
}

// Empty List
// Add Patient Button

if (addPatient){
    setInterval(function(){
        if (addPatient.style.top == '90%'){
            addPatient.style.top = '88%'
        } else {
            addPatient.style.top = '90%'
        }
    },500)
}

// Table
// Adding event listenera to rows and delete button

function collectRows(){
    let rows = document.querySelectorAll('tr')
    let deletion = document.querySelectorAll('.delete')
    return [rows,deletion]
}

if (table){
    table.addEventListener('mouseover', () => {
        var elements = collectRows()
        var rows = elements[0]
        var deletion = elements[1]

        // rows
        for(let i = 0; i<rows.length; i++){
        let childNodes = rows[i].childNodes
        if (rows[i].id === ''){
            rows[i].addEventListener('mouseover', function(e){
                rows[i].style.backgroundColor = 'cyan'
                rows[i].classList.add('tr-hover')
                for (let c = 0; c<childNodes.length; c++){
                    if (childNodes[c].nodeName != '#text'){
                        childNodes[c].style.color = '#12212b'
                        if (childNodes[c].children){
                            var children = childNodes[c].children
                            for (var cc = 0; cc<children.length; cc++){
                                children[cc].style.color = '#12212b'
                                children[cc].style.transition = '0.5s'
                                }
                            }
                        }
                    }
                })

        rows[i].addEventListener('mouseout', function(){
            rows[i].style.backgroundColor = ''
            rows[i].classList.remove('tr-hover')
            for (let c = 0; c<childNodes.length; c++){
                if (childNodes[c].nodeName != '#text'){
                    childNodes[c].style.color = 'cyan'
                    if (childNodes[c].children){
                            var children = childNodes[c].children
                            for (var cc = 0; cc<children.length; cc++){
                                children[cc].style.color = 'cyan'
                                }
                            }
                        }
                    }
                })
        }
    }
    for (let i = 0; i<deletion.length; i++){
        deletion[i].addEventListener('click', (e) => {
            e.preventDefault()
            e.stopPropagation()
            deleteAW(deletion[i].href)
            .then(data => {
                modal.classList.add('modal-show')
                modalContent.innerHTML = data['html']
            })
        })
    }

    })
}

//Modal event
if (modal){
    modal.addEventListener('click', (e) => {
        if (e.target === modal){
            modal.classList.remove('modal-show')
        }
    })
}

//Modal Form Buttons Hover
if (modal){
    modal.addEventListener('mouseover', (e) => {
        if (Array.prototype.slice.call(modal.classList).includes('modal-show')){
            const elements = document.querySelectorAll('button')
            for (let i = 0; i<elements.length; i++){
                elements[i].addEventListener('mouseover', () => {
                    elements[i].classList.add('button-form-hover')
                })
                elements[i].addEventListener('mouseout', () => {
                    elements[i].classList.remove('button-form-hover')
                })
            }
        }
    })
}

//Modal Form Buttons Click
if (modalContent){
    modalContent.addEventListener('click', (e) => {
        if (e.target.value === 'no' || e.target.textContent === 'Ok'){
            e.stopPropagation()
            e.preventDefault()
            modal.classList.remove('modal-show')
        }
    })
}

// Modal Submit
if (modalContent){
    modalContent.addEventListener('submit', (e) => {
        const form = document.querySelector('#modal-form')
        const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
        if (e.target === form){
            e.preventDefault()
            submitFormAW(form, csrfmiddlewaretoken, button)
            .then(data => {
               modalContent.innerHTML = data['html']
               tbody.innerHTML = data['patients']
            })
        }
    })
}

// Show filter button
if (i){
    i.addEventListener('mouseover', function(){
        this.classList.add('button-hover')
    })

    i.addEventListener('mouseout', function(){
        this.classList.remove('button-hover')
    })

    i.addEventListener('click', function(){
        !form.classList.contains('show-form') ? form.classList.add('show-form') : form.classList.remove('show-form')
    })
}

// Input
if (input){
    input.addEventListener('mouseover', function(){
        this.style.width = '75%'
    })

    input.addEventListener('mouseout', function(){
        this.style.width = ''
    })
}

// Button
if (button){
    for (let i = 0; i<button.length; i++){
        button[i].addEventListener('mouseover', function(){
            this.classList.add('button-form-hover')
        })

        button[i].addEventListener('mouseout', function(){
            this.classList.remove('button-form-hover')
        })
    }
}