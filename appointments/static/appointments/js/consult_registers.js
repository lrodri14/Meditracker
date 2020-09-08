//Checked
if (document.querySelector('.wrapper') !== 'undefined' && document.querySelector('.wrapper') !== 'null'){
    var wrapper = document.querySelector('.wrapper')
}

if (document.querySelector('.registers') !== 'undefined' && document.querySelector('.registers') !== 'null'){
    var registers = document.querySelector('.registers')
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

        if (e.target.nodeName === 'I'){
            e.target.classList.add('button-hover')
        }

        if (e.target.nodeName === 'TD'){
            var rows = document.querySelectorAll('tr')
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
                                            children[cc].style.color = ''
                                        }
                            }
                            }
                            }
                        })
                }
                }
        }

    })

    //Wrapper mouse out
    wrapper.addEventListener('mouseout', (e) => {

        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.remove('button-form-hover')
        }

        if (e.target.nodeName === 'I'){
            e.target.classList.remove('button-hover')
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
            updateAW(e.target.parentNode.href)
            .then(data => {
                modalContent.innerHTML = data['html']
                modal.classList.add('modal-show')
            })
        }

        if (e.target.classList.contains('fa-check')){
            e.preventDefault()
            e.stopPropagation()
            confirmAW(e.target.parentNode.href)
            .then(data => {
                wrapper.innerHTML = data['html']
            })
        }

        if (e.target.classList.contains('fa-times-circle')){
            var modal = retrieveItems()['modal']
            var modalContent = retrieveItems()['modalContent']
            e.stopPropagation()
            e.preventDefault()
            cancelAW(e.target.parentNode.href)
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
                wrapper.innerHTML = data['html']
            })
            modal.classList.remove('modal-show')
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

//Registers

if (registers){
    registers.addEventListener('mouseover', function(){
        this.classList.add('registers-hover')
    })

    registers.addEventListener('mouseout', function(){
        this.classList.remove('registers-hover')
    })
}
