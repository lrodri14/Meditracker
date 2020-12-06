/* This settings.js files contains all the variable declarations, async and sync functions, and event listeners, needed
   to make the settings template work properly, this file is composed of 7 async functions, and one synchronous function.
   The file is also divided into three sections: Variable Declarations, Functions, Event Listeners.*/

/*###################################################### Variables ###################################################*/

var body = document.querySelector('body')
var tabs = document.querySelectorAll('.tab')
var wrapper = document.querySelector('.wrapper')
var modal = document.querySelector('.modal')
var modalContent = document.querySelector('.modal-content')
var backedUpContent

/*###################################################### Functions ###################################################*/

// Async Functions
async function displaySettingsAW(url){
    /* This displaySettingsAW async function is used to display the settings of the users choice, this async func will
       retrieve the content of that particular settings and display it inside the wrapper container, this async func
       accepts one single parameter: 'url' which we retrieve from the tab 'data-url' attribute, to make the 'GET'
       request. The response will be converted into JSON and returned for further processing.*/
    const result = await fetch(url)
    const data = await result.json()
    return data
}

async function showForm(url){
    /* This showForm async function is used to display the form for a particular use such as adding, deleting or updating
       any instances of any object, this form will be displayed in the modal container, this function accepts one single
       parameter: 'url' to make the 'GET' request, this response will be return as JSON for further response.*/
    const result = await fetch(url)
    const data = await result.json()
    return data
}

async function addUpdateElementAW(url, method, csrfmiddlewaretoken, formData){
    /* This addUpdateElementAW function is used to add or to update any objects, this function will display the corresponding
       form for the specific operation, this form will be displayed in the modal container, the function accepts, 4
       parameters: 'url' we collect from the form.action attribute, 'method' we grab from the form.method attribute,
       'csrfmiddlewaretoken' that we collect form the form's hidden input, and finally the 'formData' we collect from
       the form's inputs, the response will be returned in JSON format for further processing.*/
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken':csrfmiddlewaretoken}, body:formData})
    const data = await result.json()
    return data
}

async function deleteItemAW(url, method, csrfmiddlewaretoken){
    /* The deleteItemAW async function is used to delete items belonging to the current user, this function will display
       corresponding form for the operation, it will be displayed in the modal container, this function accepts,3 parameters:
       'url' we collect from the form.action attribute, the 'method' we collect from the form.method attribute and finally
       the 'csrfmiddlewaretoken' from the form's hidden input, the response will be returned in JSON Format for further
       processing.*/
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken':csrfmiddlewaretoken}, body:{'choice':'yes'}})
    const data = await result.json()
    return data
}

async function viewElementAW(url){
    /* This viewElementAW function is used to display the details of any object, this content will be displayed inside the
       modal container, the function accepts one single parameter: 'url' to make the 'GET' request, the response will
       be returned in JSON format, for further processing.*/
    const result = await fetch(url)
    const data = await result.json()
    return data
}

async function filterResultsAW(url, method, csrfmiddlewaretoken, formData){
    /* The filterResultsAW async function is used to filter items belonging to the current user, this function is called
       whenever an input event is fired in the filter inputs every table contains, this function accepts,4 parameters:
       'url' we collect from the form.action attribute, the 'method' we collect from the form.method attribute,
       the 'csrfmiddlewaretoken' from the form's hidden input, and finally the 'formData' we collect form the forms inputs
       the response will be returned in JSON Format for further processing.*/
    const result = await fetch(url, {method:method, headers: {'X-CSRFToken': csrfmiddlewaretoken}, body:formData})
    const data = await result.json()
    return data
}

async function updatePasswordAW(url, method, csrfmiddlewaretoken, formData){
    /* This updatePasswordAW function is used update the users password, this function will display the corresponding
       form for the specific operation, this form will be displayed in the modal container, the function accepts, 4
       parameters: 'url' we collect from the form.action attribute, 'method' we grab from the form.method attribute,
       'csrfmiddlewaretoken' that we collect form the form's hidden input, and finally the 'formData' we collect from
       the form's inputs, the response will be returned in JSON format for further processing.*/
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken':csrfmiddlewaretoken}, body:formData})
    const data = result.json()
    return data
}

// Functions

function addData(){
    /* The sync function addData, is used to create the levitating effect on the 'fa-plus' signs, whenever the
       filtering returned an empty querySet or the user is new and there are no register yet, this function will
       grab the 'add-data' element, will also call a setInterval function that will be executed every .5s, what this
       interval will execute is the style changing of the top attribute, in the addData element, it will change it to
       '90%' every time the top attribute is '88%' and vice versa.*/
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

/*###################################################### Events Listeners ############################################*/


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