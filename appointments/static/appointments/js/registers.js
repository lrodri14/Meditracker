//Checked
if (document.querySelector('.wrapper') !== 'undefined' && document.querySelector('.wrapper') !== 'null'){
    var wrapper = document.querySelector('.wrapper')
}

if (document.querySelectorAll('tr') !== 'undefined' && document.querySelectorAll('tr') !== 'null'){
    var rows = document.querySelectorAll('tr')
}
if (document.querySelector('.fa-filter') !== 'undefined' && document.querySelector('.fa-filter') !== 'null'){
    var i = document.querySelector('.fa-filter')
}
if (document.querySelectorAll('button') !== 'undefined' && document.querySelectorAll('form') !== 'null'){
    var button = document.querySelectorAll('button')
}
if (document.querySelector('form') !== 'undefined' && document.querySelector('form') !== 'null'){
    var form = document.querySelector('form')
}

// Async Functions
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
        var form = document.querySelector('form')
        return {
            modal: modal,
            modalContent: modalContent,
            form: form
        }
    }

    //Wrapper mouse over
    wrapper.addEventListener('mouseover', (e) => {

        if (e.target.classList.contains('fa-filter')){
            e.target.classList.add('fa-filter-hover')
        }

        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.add('button-form-hover')
        }

        if (e.target.nodeName === 'TD' || (e.target.classList.contains('fa-edit') || e.target.classList.contains('fa-check') || e.target.classList.contains('fa-times-circle'))){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = '#C7E8F3'
            row.style.color = '#496897'

        }

    })

    //Wrapper mouse out
    wrapper.addEventListener('mouseout', (e) => {

        if (e.target.classList.contains('fa-filter')){
            e.target.classList.remove('fa-filter-hover')
        }

        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.remove('button-form-hover')
        }

        if (e.target.nodeName === 'TD' || !e.target.classList.contains('fa-filter')){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = ''
            row.style.color = ''
        }

    })

    //Wrapper Click
    wrapper.addEventListener('click', (e) => {
        const form = retrieveItems()['form']
        if (e.target.classList.contains('fa-filter')){
            !form.classList.contains('show-form') ? form.classList.add('show-form') : form.classList.remove('show-form')
        }

    })

    //Wrapper Submit
    wrapper.addEventListener('submit', (e) => {
        if (e.target.nodeName === 'FORM'){
            e.preventDefault()
            const form = e.target
            const url = form.action
            const method = form.method
            const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            const data = new FormData(form)
            filterResultsAW(url, method, csrfmiddlewaretoken, data)
            .then(data => {
                wrapper.innerHTML = data['html']
                document.querySelector('form').classList.add('show-form')
            })
        }
    })

}