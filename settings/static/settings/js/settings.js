// Checked
//Checked

if (document.querySelector('.wrapper') !== 'undefined' && document.querySelector('.wrapper') !== 'null'){
    var wrapper = document.querySelector('.wrapper')
}

if (document.querySelector('.modal') !== 'undefined' && document.querySelector('.modal') !== 'null'){
    var modal = document.querySelector('.modal')
    var modalContent = document.querySelector('.modal-content')
}

var body = document.querySelector('body')

// Async Functions
async function displaySettingsAW(url){
    const result = await fetch(url)
    const data = await result.json()
    return data
}

async function showForm(url){
    const result = await fetch(url)
    const data = await result.json()
    return data
}

async function addUpdateElementAW(url, method, csrfmiddlewaretoken, formData){
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken':csrfmiddlewaretoken}, body:formData})
    const data = await result.json()
    return data
}

async function deleteItemAW(url, method, csrfmiddlewaretoken){
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken':csrfmiddlewaretoken}, body:{'choice':'yes'}})
    const data = await result.json()
    return data
}

async function viewElementAW(url){
    const result = await fetch(url)
    const data = await result.json()
    return data
}

// Functions
//Add Data
function addData(){
    if (document.querySelector('.add-data') !== 'undefined' && document.querySelector('.add-data') !== 'null'){
        var addData = document.querySelector('.add-data')
        setInterval(function(){
        if (addData.style.top == '90%'){
            addData.style.top = '88%'
        } else {
            addData.style.top = '90%'
        }
        },500)
        console.log(addData)
    }
}

// Body Event Listeners

body.addEventListener('click', (e) => {
    if (e.target.nodeName === 'A' || e.target.nodeName === 'LI'){
        const items = document.querySelectorAll('ul > li')
        const url = e.target.nodeName === 'A' ? e.target.href : e.target.firstElementChild.href
        const item = e.target.nodeName === 'A' ? e.target.parentNode : e.target
        for (let i = 0; i<items.length; i++){
            if (items[i].classList.contains('li-active') && items[i] !== item){
                items[i].classList.remove('li-active')
                wrapper.innerHTML = ''
            }
        }
        e.preventDefault()
        e.stopPropagation()
        if (item.classList.contains('li-active')){
            item.classList.remove('li-active')
            wrapper.innerHTML = ''
        }else{
            item.classList.add('li-active')
            displaySettingsAW(url)
            .then(data => {
                wrapper.innerHTML = data['html']
            })
        }
}
})

body.addEventListener('mouseover', (e) => {

    if (e.target.nodeName === 'A' || e.target.nodeName === 'LI'){
        item = e.target.nodeName === 'A' ? e.target.parentNode : e.target
        item.classList.add('li-hover')
    }

})

body.addEventListener('mouseout', (e) => {

    if (e.target.nodeName === 'A' || e.target.nodeName === 'LI'){
        item = e.target.nodeName === 'A' ? e.target.parentNode : e.target
        item.classList.remove('li-hover')
    }

})


// Wrapper Event Listeners

if (wrapper){

    var backedUpContent = wrapper.innerHTML

    wrapper.addEventListener('mouseover', (e) => {

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

        if (e.target.classList.contains('fa-filter')){
            e.target.classList.add('fa-filter-hover')
        }

        if (e.target.classList.contains('fa-plus')){
            e.target.classList.add('fa-plus-hover')
        }

        if (e.target.nodeName === 'INPUT'){
            e.target.classList.add('input-hover')
        }

    })

    wrapper.addEventListener('mouseout', (e) => {

        if (e.target.classList.contains('fa-filter')){
            e.target.classList.remove('fa-filter-hover')
        }

        if (e.target.classList.contains('fa-plus')){
            e.target.classList.remove('fa-plus-hover')
        }

        if (e.target.nodeName === 'INPUT'){
            e.target.classList.remove('input-hover')
        }


    })

    wrapper.addEventListener('click', (e) => {

        if (e.target.nodeName === 'TD'){
            const url = e.target.parentNode.getAttribute('data-url')
            viewElementAW(url)
            .then(data => {
                modal.classList.add('show-modal')
                modalContent.innerHTML = data['html']
            })
        }

        if (e.target.classList.contains('fa-filter')){
            const form = document.querySelector('.filter-form')
            form.classList.contains('show-filter-form') ? form.classList.remove('show-filter-form') : form.classList.add('show-filter-form')
        }

        if (e.target.classList.contains('fa-plus')){
            e.preventDefault()
            e.stopPropagation()
            const url = e.target.parentNode.href
            showForm(url)
            .then(data => {
                modal.classList.add('show-modal')
                modalContent.innerHTML = data['html']
            })
        }

        if (e.target.classList.contains('fa-edit')){
            e.preventDefault()
            e.stopPropagation()
            const url = e.target.parentNode.href
            showForm(url)
            .then(data => {
                modal.classList.add('show-modal')
                modalContent.innerHTML = data['html']
            })
        }

        if (e.target.classList.contains('fa-trash')){
            e.preventDefault()
            e.stopPropagation()
            const url = e.target.parentNode.href
            showForm(url)
            .then(data => {
                modal.classList.add('show-modal')
                modalContent.innerHTML = data['html']
            })
        }
    })
}


// Modal Event Listeners
if (modal){

    modal.addEventListener('click', (e) => {

        if (e.target === modal){
            modal.classList.remove('show-modal')
        }

        if (e.target.value === 'no'){
            e.preventDefault()
            e.stopPropagation()
            modal.classList.remove('show-modal')
        }

    })

    modal.addEventListener('mouseover', (e) => {

        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.add('button-hover')
        }

        if (e.target.nodeName === 'INPUT'){
            e.target.classList.add('input-hover')
        }

    })

    modal.addEventListener('mouseout', (e) => {

        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.remove('button-hover')
        }

         if (e.target.nodeName === 'INPUT'){
            e.target.classList.remove('input-hover')
        }

    })

    modal.addEventListener('submit', (e) => {
         if (e.target.nodeName === 'FORM'){
            e.preventDefault()
            e.stopPropagation()
            const form = e.target
            const url = form.action
            const method = form.method
            const csrfmiddlewaretoken = document.querySelector('.' + e.target.className + ' > [name=csrfmiddlewaretoken]').value
            const data = new FormData(form)
            if (e.target.classList.contains('add') || e.target.classList.contains('update')){
                addUpdateElementAW(url, method, csrfmiddlewaretoken, data)
                .then(data => {
                    if ('html' in data){
                        modalContent.innerHTML = data['html']
                    }else{
                        wrapper.innerHTML = data['updated_html']
                        modal.classList.remove('show-modal')
                    }
                })
            } else{
                deleteItemAW(url, method, csrfmiddlewaretoken)
                .then(data => {
                    wrapper.innerHTML = data['updated_html']
                    modal.classList.remove('show-modal')
                    }
                )
            }

         }
    })
}