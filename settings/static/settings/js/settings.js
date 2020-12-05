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
var tabs = document.querySelectorAll('.tab')

var backedUpContent

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

async function filterResultsAW(url, method, csrfmiddlewaretoken, formData){
    const result = await fetch(url, {method:method, headers: {'X-CSRFToken': csrfmiddlewaretoken}, body:formData})
    const data = await result.json()
    return data
}

async function updatePasswordAW(url, method, csrfmiddlewaretoken, formData){
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken':csrfmiddlewaretoken}, body:formData})
    const data = result.json()
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
    if (e.target.classList.contains('tab')){
        e.preventDefault()
        e.stopPropagation()
        tabs.forEach(tab => tab.classList.remove('li-active'))
        wrapper.innerHTML = ''
        e.target.classList.add('li-active')
        let url = e.target.getAttribute('data-url')
        displaySettingsAW(url)
        .then(data => {
            wrapper.innerHTML = data['html']
            backedUpContent = wrapper.innerHTML
        })
    }
})

body.addEventListener('mouseover', (e) => {

    if (e.target.classList.contains('tab')){
        e.target.classList.add('li-hover')
    }

})

body.addEventListener('mouseout', (e) => {

    if (e.target.classList.contains('tab')){
        e.target.classList.remove('li-hover')
    }

})


// Wrapper Event Listeners

if (wrapper){

    var backedUpContent = wrapper.innerHTML

    wrapper.addEventListener('mouseover', (e) => {

        if (e.target.nodeName === 'TD' || ((e.target.classList.contains('fa-trash') || e.target.classList.contains('fa-edit')))){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = '#C7E8F3'
            row.style.color = '#496897'
        }

        if (e.target.classList.contains('fa-filter')){
            e.target.classList.add('fa-filter-hover')
        }

        if (e.target.classList.contains('fa-plus')){
            e.target.classList.add('fa-plus-hover')
        }

        if (e.target.classList.contains('fa-edit')){
            e.target.classList.add('fa-edit-hover')
        }

        if (e.target.classList.contains('fa-trash')){
            e.target.classList.add('fa-trash-hover')
        }

        if (e.target.nodeName === 'INPUT'){
            e.target.classList.add('input-hover')
        }

        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.add('button-hover')
        }

    })

    wrapper.addEventListener('mouseout', (e) => {

      if (e.target.nodeName === 'TD' || ((e.target.classList.contains('fa-trash') || e.target.classList.contains('fa-edit')))){
        let row
        e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = ''
            row.style.color = ''
      }

        if (e.target.classList.contains('fa-filter')){
            e.target.classList.remove('fa-filter-hover')
        }

        if (e.target.classList.contains('fa-plus')){
            e.target.classList.remove('fa-plus-hover')
        }

        if (e.target.classList.contains('fa-edit')){
            e.target.classList.remove('fa-edit-hover')
        }

        if (e.target.classList.contains('fa-trash')){
            e.target.classList.remove('fa-trash-hover')
        }

        if (e.target.nodeName === 'INPUT'){
            e.target.classList.remove('input-hover')
        }

        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.remove('button-hover')
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
            const url = e.target.parentNode.getAttribute('data-url')
            showForm(url)
            .then(data => {
                modal.classList.add('show-modal')
                modalContent.innerHTML = data['html']
            })
        }

        if (e.target.classList.contains('fa-trash')){
            e.preventDefault()
            e.stopPropagation()
            const url = e.target.parentNode.getAttribute('data-url')
            showForm(url)
            .then(data => {
                modal.classList.add('show-modal')
                modalContent.innerHTML = data['html']
            })
        }

        if (e.target.nodeName === 'BUTTON'){
            let url = e.target.getAttribute('data-url')
            modal.classList.add('show-modal')
            showForm(url)
            .then(data => {
                modalContent.innerHTML = data['html']
                modal.classList.add('show-modal')
            })
        }
    })

    wrapper.addEventListener('input', (e) => {
        if (e.target.nodeName === 'INPUT'){
            let form = e.target.parentNode.parentNode
            let url = form.action
            let method = form.method
            let csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            let data = new FormData(form)
            filterResultsAW(url, method, csrfmiddlewaretoken, data)
            .then(data => {
                console.log(data)
                var tbody = document.querySelector('tbody')
                var start = data['updated_html'] ? data['updated_html'].search('<tbody>') : backedUpContent.search('<tbody>')
                var end = data['updated_html'] ? data['updated_html'].search('</tbody>') : backedUpContent.search('</tbody>')
                if (data['updated_html']){
                    var newData = data['updated_html'].slice(start + 8,end)
                    tbody.innerHTML = newData
                }else{
                    var newData = backedUpContent.slice(start + 8,end)
                    tbody.innerHTML = newData
                }
                })
            }})
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
            console.log(url)
            const method = form.method
            const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            const data = new FormData(form)

            if (e.target.classList.contains('add') || e.target.classList.contains('update')){
                addUpdateElementAW(url, method, csrfmiddlewaretoken, data)
                .then(data => {
                    if ('html' in data){
                        modalContent.innerHTML = data['html']
                    }else{
                        wrapper.innerHTML = data['updated_html']
                        backedUpContent = wrapper.innerHTML
                        modal.classList.remove('show-modal')
                    }
                })
            }

            if (e.target.id === 'delete'){
                deleteItemAW(url, method, csrfmiddlewaretoken)
                .then(data => {
                    wrapper.innerHTML = data['updated_html']
                    modal.classList.remove('show-modal')
                    backedUpContent = wrapper.innerHTML
                    }
                )
            }

            if (e.target.classList.contains('password-form')){
                updatePasswordAW(url, method, csrfmiddlewaretoken, data)
                .then(data => {
                    if (data['html']){
                        modalContent.innerHTML = data['html']
                    }else{
                        modal.classList.remove('show-modal')
                    }
                })
            }


         }
    })
}