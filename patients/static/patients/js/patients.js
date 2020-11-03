////Checked
////Sound
if (document.querySelector('.wrapper') !== 'undefined' && document.querySelector('.wrapper') !== 'null'){
    var wrapper = document.querySelector('.wrapper')
    var i = document.querySelector('.fa-filter')
    var form = document.querySelector('form')
    var input = document.querySelector('#id_patient')
    var button = document.querySelectorAll('button')
    var table = document.querySelector('table')
    var tbody = document.querySelector('tbody')
    var deletion = document.querySelectorAll('.delete')
    var modal = document.querySelector('.modal')
    var modalContent = document.querySelector('.modal-content')
    var info = document.querySelector('.info')
    var infoContent = document.querySelector('.info-content')
}

if (document.querySelector('#add_patients') !== 'undefined' && document.querySelector('#add_patients') !== 'null'){
    var addPatient = document.querySelector('#add_patients')
}

if (tbody){
    var backedUpData = tbody.innerHTML
}


// Async Functions

// Delete button event
async function deleteAW(url){
    const result = await fetch(url)
    const data = await result.json()
    return data
}

// Result's filter
async function filterResults(url, method, csrfmiddlewaretoken, formData){
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken':csrfmiddlewaretoken}, body:formData})
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

    addPatient.addEventListener('mouseover', () => {
        addPatient.classList.add('add-patient-hover')
    })

    addPatient.addEventListener('mouseout', () => {
        addPatient.classList.remove('add-patient-hover')
    })

}

// Wrapper
if (wrapper){

    wrapper.addEventListener('mouseover', (e) => {

        if (e.target.nodeName === 'TD' || ((e.target.classList.contains('fa-trash') || e.target.classList.contains('fa-edit')))){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = '#0ff5fc'
            row.classList.add('tr-hover')
            for (let i = 0; i<row.childNodes.length; i++){
                if (row.childNodes[i].nodeName === 'TD'){
                    row.childNodes[i].classList.add('td-hover')
                }
            }
        }

        //*********************************************************
        // These deletion elements have a parent with a click event
        // So event delegation can not be set to the table tag, but td and tr's are added dynamically
        // How to deal with these situations?
        let deletion = document.querySelectorAll('.delete')
        for (let i = 0; i<deletion.length; i++){
            deletion[i].addEventListener('click', (e) => {
            e.preventDefault()
            e.stopPropagation()
            deleteAW(deletion[i].getAttribute('data-url'))
            .then(data => {
                modal.classList.add('modal-show')
                modalContent.innerHTML = data['html']
            })
            })
        }

        let update = document.querySelectorAll('.update')
        for (let i = 0; i<update.length; i++){
            update[i].addEventListener('click', (e) => {
                e.stopPropagation()
                let url = e.target.classList.contains('fa-edit') ? e.target.parentNode.getAttribute('data-url') : e.target.getAttribute('data-url')
                window.location.href = url
            })
        }

        if (e.target.classList.contains('info-tab') || e.target.parentNode.classList.contains('info-tab')){
            let tab = e.target.classList.contains('info-tab') ? e.target : e.target.parentNode
            tab.classList.add('tab-hover')
        }

        if (e.target.classList.contains('quit') || e.target.parentNode.classList.contains('quit')){
            let tab = e.target.classList.contains('quit') ? e.target : e.target.parentNode
            tab.classList.add('quit-hover')
        }

        if (e.target.nodeName === 'INPUT'){
            const input = e.target
            input.style.width = '75%'
        }

        if (e.target.nodeName === 'BUTTON'){
            const button = e.target
            button.classList.add('button-form-hover')
        }

       if (e.target.classList.contains('fa-plus')){
            e.target.classList.add('fa-plus-hover')
        }

       if (e.target.classList.contains('fa-trash')){
            e.target.classList.add('fa-trash-hover')
        }

       if (e.target.classList.contains('fa-edit')){
            e.target.classList.add('fa-edit-hover')
        }

        if (e.target.classList.contains('fa-filter')){
            e.target.classList.add('button-hover')
        }

        })

    wrapper.addEventListener('mouseout', (e) => {

      if (e.target.nodeName === 'TD' || ((e.target.classList.contains('fa-trash') || e.target.classList.contains('fa-edit')))){
        let row
        e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
        row.style.backgroundColor = ''
        row.classList.remove('tr-hover')
        for (let i = 0; i<row.childNodes.length; i++){
            if (row.childNodes[i].nodeName === 'TD'){
                row.childNodes[i].classList.remove('td-hover')
            }
        }
      }

    // Elements to open modal not working because of parent, it has a click event too and is being fired.
    // How to deal with this?
        //    table.addEventListener('click', () => {
        //        if (e.target.classList.contains('fa-trash')){
        //            const url = e.target.parentNode.href
        //            e.stopPropagation()
        //            e.preventDefault()
        //            deleteAW(url)
        //            .then(data => {
        //                modal.classList.add('modal-show')
        //                modalContent.innerHTML = data['html']
        //            })
        //        }
        //    })

        if (e.target.nodeName === 'INPUT'){
            const input = e.target
            input.style.width = ''
        }

        if (e.target.nodeName === 'BUTTON'){
            const button = e.target
            button.classList.remove('button-form-hover')
        }

       if (e.target.classList.contains('fa-plus')){
            e.target.classList.remove('fa-plus-hover')
        }

       if (e.target.classList.contains('fa-trash')){
            e.target.classList.remove('fa-trash-hover')
        }

       if (e.target.classList.contains('fa-edit')){
            e.target.classList.remove('fa-edit-hover')
        }

        if (e.target.classList.contains('fa-filter')){
            e.target.classList.remove('button-hover')
        }

     })

    wrapper.addEventListener('click', (e) => {

        if (e.target === modal){
            modal.classList.remove('modal-show')
        }

        if (e.target.value === 'no' || e.target.textContent === 'Ok'){
            e.stopPropagation()
            e.preventDefault()
            modal.classList.remove('modal-show')
        }

        if (e.target.classList.contains('fa-filter')){
            !form.classList.contains('show-form') ? form.classList.add('show-form') : form.classList.remove('show-form')
        }

    })

    wrapper.addEventListener('submit', (e) => {

        const form = document.querySelector('#modal-form')
        const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
        if (e.target === form){
            e.preventDefault()
            submitFormAW(form, csrfmiddlewaretoken, button)
            .then(data => {
                if (data.hasOwnProperty('patients')){
                    modalContent.innerHTML = data['html']
                    tbody.innerHTML = data['patients']
                    backedUpData = tbody.innerHTML
                }else{
                    modalContent.innerHTML = data['html']
                }
            })
        }

    })

    wrapper.addEventListener('input', (e) => {

        if (e.target.nodeName === 'INPUT'){
            const url = form.action
            const method = form.method
            const input = document.querySelector('[type=text]')
            const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            const data = new FormData(form)
            if (input.value !== ''){
                filterResults(url, method, csrfmiddlewaretoken, data)
                .then(data => {
                    tbody.innerHTML = data['html']
                })
            } else{
                tbody.innerHTML = backedUpData
            }
        }

    })

}