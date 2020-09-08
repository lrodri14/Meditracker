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

if (document.querySelector('button') !== 'undefined' && document.querySelector('form') !== 'null'){
    var button = document.querySelector('button')
}

if (document.querySelector('form') !== 'undefined' && document.querySelector('form') !== 'null'){
    var form = document.querySelector('form')
}


//Async Functions
async function filterResultsAW(url, method, csrfmiddlewaretoken, formData){
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken':csrfmiddlewaretoken}, body:formData})
    const data = result.json()
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

        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.add('button-form-hover')
        }

    })

    //Wrapper mouse out
    wrapper.addEventListener('mouseout', (e) => {

        if (e.target.nodeName === 'I'){
            e.target.classList.remove('button-hover')
        }

        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.remove('button-form-hover')
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

// Button
if (button){
    button.addEventListener('mouseover', function(){
        this.classList.add('button-form-hover')
    })

    button.addEventListener('mouseout', function(){
        this.classList.remove('button-form-hover')
    })
}