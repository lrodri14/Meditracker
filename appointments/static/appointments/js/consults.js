//Checked

if (document.querySelectorAll('tr') !== 'undefined' && document.querySelectorAll('tr') !== 'null'){
    var table = document.querySelector('table')
}

if (document.querySelectorAll('button') !== 'undefined' && document.querySelectorAll('button') !== 'null'){
    var button = document.querySelectorAll('button')
}

if (document.querySelector('#add-consult') !== 'undefined' && document.querySelector('#add-consult') !== 'null'){
    var addConsult = document.querySelector('#add-consult')
    var noConsults = document.querySelector('#no-consults')
}

if (document.querySelector('.modal') !== 'undefined' && document.querySelector('.modal') !== 'null'){
    var modal = document.querySelector('.modal')
    var modalContent = document.querySelector('.modal-content')

}

// Icons
var plus = document.querySelector('.fa-plus')
var edit = document.querySelectorAll('.fa-edit')
var warnings = document.querySelectorAll('.fa-exclamation-circle')


var createConsultModal = document.querySelector('.create-consult-modal')

//Async Functions
async function addConsultAW(url){
    const result = await fetch(url)
    const data = await result.json()
    return data
}

async function submitConsultAW(url, csrfmiddlewaretoken, formData, method){
    const result = await fetch(url, {method: method, headers: {'X-CSRFTOKEN':csrfmiddlewaretoken}, body: formData})
    const data = result.json()
    return data
}

if (plus){

    plus.addEventListener('mouseover', () => {
        plus.classList.add('fa-plus-hover')
    })

    plus.addEventListener('mouseout', () => {
        plus.classList.remove('fa-plus-hover')
    })

}


if (edit){

    for (let i = 0; i<edit.length; i++){

        edit[i].addEventListener('mouseover', () => {
            edit[i].classList.add('fa-edit-hover')
        })

        edit[i].addEventListener('mouseout', () => {
            edit[i].classList.remove('fa-edit-hover')
        })

    }

}

if (warnings){

    for (let i = 0; i<warnings.length; i++){

        let popUp
        warnings[i].addEventListener('mouseover', (e) => {
            popUp = e.target.parentNode.childNodes[1]
            popUp.classList.add('popup-show')
        })

        warnings[i].addEventListener('mouseout', (e) => {
            popUp.classList.remove('popup-show')
        })

    }

}

//Modal
// Modal Click
modal.addEventListener('click', (e) => {
    if (e.target === modal || e.target === modalContent){
    modal.classList.remove('modal-show')
    if (noConsults && addConsult){
            addConsult.classList.remove('add-consults-hide')
            noConsults.classList.remove('no-consults-hide')
        }
    }
})

// Modal Hover
modal.addEventListener('mouseover', (e) => {
    if (e.target.nodeName === 'FORM'){

        const submitBtn = document.querySelector('form button')
        const formLink = document.querySelector('form a')

        submitBtn.addEventListener('mouseover', () => {
            submitBtn.classList.add('button-hover')
        })
        submitBtn.addEventListener('mouseout', () => {
            submitBtn.classList.remove('button-hover')
        })

        formLink.addEventListener('mouseover', () => {
            formLink.classList.add('add_new_patient_hover')
        })
        formLink.addEventListener('mouseout', () => {
            formLink.classList.remove('add_new_patient_hover')
        })
    }
})

// Open Modal
createConsultModal.addEventListener('click', (e) => {
    e.preventDefault()
    e.stopPropagation()
    addConsultAW(e.target.getAttribute('data-url'))
    .then(data => {
        modal.classList.add('modal-show')
        modalContent.innerHTML = data['html']
        if (noConsults && addConsult){
            addConsult.classList.add('add-consults-hide')
            noConsults.classList.add('no-consults-hide')
        }
    })
})

// Modal Submit
modalContent.addEventListener('submit', (e) => {
    if (e.target.nodeName === 'FORM'){
        e.preventDefault()
        e.stopPropagation()
        const formData = new FormData(e.target)
        const method = e.target.method
        const action = e.target.action
        const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
        submitConsultAW(action, csrfmiddlewaretoken, formData, method)
        .then(data => {
            if (data['success']){
                modal.classList.remove('modal-show')
                if (noConsults && addConsult){
                addConsult.classList.remove('add-consults-hide')
                noConsults.classList.remove('no-consults-hide')
                }
            } else {
                modalContent.innerHTML = data['html']
            }
        })
    }
})

if (table){

    table.addEventListener('mouseover', (e) => {

        if (e.target.nodeName === 'TD' ||  e.target.classList.contains('fa-edit')){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = '#C7E8F3'
            row.style.color = '#496897'
        }

    })

    table.addEventListener('mouseout', (e) => {

          if (e.target.nodeName === 'TD' ||  e.target.classList.contains('fa-edit')){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = ''
            row.style.color = ''
          }
    })

}

// Button
if (button){
    for (let i = 0; i<button.length; i++){
        button[i].addEventListener('mouseover', function(){
            this.classList.add('button-hover')
        })

        button[i].addEventListener('mouseout', function(){
            this.classList.remove('button-hover')
        })
    }
}

//Add consult
if (addConsult){
    setInterval(function(){
        if (addConsult.style.top == '90%'){
            addConsult.style.top = '88%'
        } else {
            addConsult.style.top = '90%'
        }
    },500)

    addConsult.addEventListener('mouseover', () => {
        addConsult.classList.add('add-consult-hover')
    })

    addConsult.addEventListener('mouseout', () => {
        addConsult.classList.remove('add-consult-hover')
    })

}