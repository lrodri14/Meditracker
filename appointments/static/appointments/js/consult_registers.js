//Checked
if (document.querySelector('.wrapper') !== 'undefined' && document.querySelector('.wrapper') !== 'null'){
    var wrapper = document.querySelector('.wrapper')
}

if (document.querySelector('.modal') !== 'undefined' && document.querySelector('.modal') !== 'null'){
    var modal = document.querySelector('.modal')
}



// Async functions
async function cancelAW(url){
    const result = await fetch(url)
    const data = await result.json()
    return data
}

async function confirmAW(url){
    const result = await fetch(url)
    const data = await result.json()
    return data
}

async function updateAW(url){
    const result = await fetch(url)
    const data = await result.json()
    return data
}

async function submitCancelAW(url, method, csrfmiddlewaretoken){
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken': csrfmiddlewaretoken}})
    let data = await result.json()
    return data
}

async function submitUpdateAW(url, method, csrfmiddlewaretoken, formData){
    const result = await fetch(url, {method:method, headers:{'X_CSRFToken':csrfmiddlewaretoken}, body:formData})
    const data = await result.json()
    return data
}

async function filterResultsAW(url, method, csrfmiddlewaretoken, formData){
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken': csrfmiddlewaretoken}, body:formData})
    const data = await result.json()
    return data
}

// Event delegation capturing
if (wrapper){

    function retrieveItems(){
        var modal = document.querySelector('.modal')
        var modalContent = document.querySelector('.modal-content')
        var form = document.querySelector('.form > form')
        return {
            modal: modal,
            modalContent: modalContent,
            form: form
        }
    }

    //Wrapper mouse over
    wrapper.addEventListener('mouseover', (e) => {

        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.add('button-form-hover')
        }

        if (e.target.nodeName === 'I' && e.target.classList.contains('fa-filter')){
            e.target.classList.add('fa-filter-hover')
        }

        if (e.target.nodeName === 'TD' || (e.target.classList.contains('fa-edit') || e.target.classList.contains('fa-check') || e.target.classList.contains('fa-times-circle'))){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = '#C7E8F3'
            row.style.color = '#496897'
        }

        if (e.target.classList.contains('fa-edit')){
            e.target.classList.add('fa-edit-hover')
        }

        if (e.target.classList.contains('fa-check')){
            e.target.classList.add('fa-check-hover')
        }

        if (e.target.classList.contains('fa-times-circle')){
            e.target.classList.add('fa-times-circle-hover')
        }

    })

    //Wrapper mouse out
    wrapper.addEventListener('mouseout', (e) => {

        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.remove('button-form-hover')
        }

        if (e.target.nodeName === 'I' && e.target.classList.contains('fa-filter')){
            e.target.classList.remove('fa-filter-hover')
        }

        if (e.target.nodeName === 'TD' || !e.target.classList.contains('fa-filter')){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = ''
            row.style.color = ''
        }

        if (e.target.classList.contains('fa-edit')){
            e.target.classList.remove('fa-edit-hover')
        }

        if (e.target.classList.contains('fa-check')){
            e.target.classList.remove('fa-check-hover')
        }

        if (e.target.classList.contains('fa-times-circle')){
            e.target.classList.remove('fa-times-circle-hover')
        }

    })

    //Wrapper Click
    wrapper.addEventListener('click', (e) => {

        if (e.target.classList.contains('modal')){
            e.target.classList.remove('modal-show')
        }

        var form = retrieveItems()['form']
        if (e.target.classList.contains('fa-filter')){
            !form.classList.contains('show-form') ? form.classList.add('show-form') : form.classList.remove('show-form')
        }

        if (e.target.classList.contains('fa-edit')){
            var modal = retrieveItems()['modal']
            var modalContent = retrieveItems()['modalContent']
            e.preventDefault()
            e.stopPropagation()
            let url = e.target.parentNode.getAttribute('data-url')
            updateAW(url)
            .then(data => {
                modalContent.innerHTML = data['html']
                modal.classList.add('modal-show')
            })
        }

        if (e.target.classList.contains('fa-check')){
            e.preventDefault()
            e.stopPropagation()
            confirmAW(e.target.parentNode.getAttribute('data-url'))
            .then(data => {
                wrapper.innerHTML = data['html']
            })
        }

        if (e.target.classList.contains('fa-times-circle')){
            var modal = retrieveItems()['modal']
            var modalContent = retrieveItems()['modalContent']
            e.stopPropagation()
            e.preventDefault()
            cancelAW(e.target.parentNode.getAttribute('data-url'))
            .then(data => {
                modalContent.innerHTML = data['html']
                modal.classList.add('modal-show')
            })
        }

        if (e.target.value === 'no'){
            var modal = retrieveItems()['modal']
            e.preventDefault()
            modal.classList.remove('modal-show')
        }

    })


    //Wrapper Submit
    wrapper.addEventListener('submit', (e) => {
        var modal = retrieveItems()['modal']
        if (e.target.nodeName === 'FORM' && e.target.classList.contains('modal-cancel-form')){
            e.preventDefault()
            const form = e.target
            const url = form.action
            const method = form.method
            const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            submitCancelAW(url, method, csrfmiddlewaretoken)
            .then(data => {
                wrapper.innerHTML = data['html']
            })
            modal.classList.remove('modal-show')

        }else if (e.target.nodeName === 'FORM' && e.target.classList.contains('update-date-form')){
            e.preventDefault()
            const form = e.target
            const method = form.method
            const url = form.action
            const data = new FormData(form)
            const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            submitUpdateAW(url, method, csrfmiddlewaretoken, data)
            .then(data => {
                if (data['updated_html']){
                    wrapper.innerHTML = data['updated_html']
                    modal.classList.remove('modal-show')
                }else{
                    retrieveItems()['modalContent'].innerHTML = data['html']
                }
            })
        } else{
            e.preventDefault()
            const form = e.target
            const url = form.action
            const method = form.method
            const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            const data = new FormData(form)
            filterResultsAW(url, method, csrfmiddlewaretoken, data)
            .then(data => {
                wrapper.innerHTML = data['html']
                if(document.querySelector('.filter-results-form')){
                    document.querySelector('.filter-results-form').classList.add('show-form')
                }
            })
        }
    })

}

// Modal

if (modal){
    modal.addEventListener('mouseover', (e) => {
        if (e.target.id === 'add_new_patient'){
            e.target.classList.add('add_new_patient_hover')
        }
    })

    modal.addEventListener('mouseout', (e) => {
        if (e.target.id === 'add_new_patient'){
            e.target.classList.remove('add_new_patient_hover')
        }
    })
}