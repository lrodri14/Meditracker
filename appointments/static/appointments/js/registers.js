/* This registers.js file contains all the variable definitions, async functions and event listeners needed to display
the consults registers template in the Appointments, app, this file consists of 1 async function.*/

/*#################################################### Variables #####################################################*/

if (document.querySelector('.wrapper') !== 'undefined' && document.querySelector('.wrapper') !== 'null'){
    var wrapper = document.querySelector('.wrapper')
    var tbody = document.querySelector('tbody')
    var rows = document.querySelectorAll('tr')
    var i = document.querySelector('.fa-filter')
    var button = document.querySelectorAll('button')
    var form = document.querySelector('form')
}

/*#################################################### Functions #####################################################*/

// Async Functions

async function requestPageAW(url){
    /* This async function will be used to collect the data from the previous or next page, this content will be
    received as a promise, so we need to return it in JSON format so we can process it, this content will be set to
    the tbody dynamically.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function filterResultsAW(url){
    /* This filterResultsAW async function is used to filter results from the Agenda based on a date query, this func
    takes four parameters, the 'url' which we collect from the form's action attribute, the 'method' we collect from
    the form's method attribute, csrfmiddlewaretoken we collect from the form's hidden input,and the 'formData' which
     we collect from the form and convert it into a formData object. The response will be converted into JSON before
     dynamically showing it.*/
    const result = await fetch(url)
    const data = await result.json()
    return data
}

/*#################################################### Event Listeners ###############################################*/

// Event delegation capturing
if (wrapper){

    //Wrapper mouse over
    wrapper.addEventListener('mouseover', (e) => {

        // This event will be fired every time the target is a 'fa-angle', this event will add the 'fa-angle-hover' to its classList.
        if (e.target.classList.contains('fa-angle-left') || e.target.classList.contains('fa-angle-right')){
            e.target.classList.add('fa-angle-hover')
        }

        /* This event will be fired every time a hover occurs on a target which classList contains 'fa-filter' this will add the
        fa-filter-hover class to the target.*/
        if (e.target.classList.contains('fa-filter')){
            e.target.classList.add('fa-filter-hover')
        }

        /* This event will be fired every time a hover occurs on a target which nodeName is 'BUTTON', this will add the
        button-form-hover class to the target.*/
        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.add('button-form-hover')
        }

        /* This event will be fired every time a hover occurs on a target which is a table data cell or classList
        contains 'fa-edit' or 'fa-check' this will add the some styles to the parent's row of this elements.*/
        if (e.target.nodeName === 'TD' || (e.target.classList.contains('fa-edit') || e.target.classList.contains('fa-check') || e.target.classList.contains('fa-times-circle'))){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = '#FFFFFF'
            row.style.color = '#000000'
        }

        /* This event is fired every time a hover occurs over an input tag, it will add the input-hover class to the target*/
        if (e.target.nodeName === 'INPUT'){
            e.target.classList.add('input-hover')
        }

    })

    //Wrapper mouse out
    wrapper.addEventListener('mouseout', (e) => {

        // This event will be fired every time the target is a 'fa-angle', this event will remove the 'fa-angle-hover' to its classList.
        if (e.target.classList.contains('fa-angle-left') || e.target.classList.contains('fa-angle-right')){
            e.target.classList.remove('fa-angle-hover')
        }

        /* This event will be fired every time a hover out occurs on a target which classList contains 'fa-filter' this will remove the
        fa-filter-hover class to the target.*/
        if (e.target.classList.contains('fa-filter')){
            e.target.classList.remove('fa-filter-hover')
        }

        /* This event will be fired every time a hover out occurs on a target which nodeName is 'BUTTON', this will remove the
        button-form-hover class to the target.*/
        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.remove('button-form-hover')
        }

        /* This event will be fired every time a hover out occurs on a target which is a table data cell or classList
        contains 'fa-edit' or 'fa-check' this will remove some styles to the parent's row of this elements.*/
        if (e.target.nodeName === 'TD' || !e.target.classList.contains('fa-filter')){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = ''
            row.style.color = ''
        }

        /* This event is fired every time a hover occurs over an input tag, it will add the input-hover class to the target*/
        if (e.target.nodeName === 'INPUT'){
            e.target.classList.remove('input-hover')
        }

    })

    //Wrapper Click

    /* This event will be fired every time a click occurs on the fa-filter icon, this will check if the filter form
    is shown or hidden, and perform the displaying or hiding depending on the previous condition.*/
    wrapper.addEventListener('click', (e) => {

        /* This event will be fired every time an angle icon is clicked, this event will grab the url for the
           GET request, then the response will be added to the tbody, as well as the paginator will be deleted
           to get the current one.*/
        if (e.target.classList.contains('fa-angle-left') || e.target.classList.contains('fa-angle-right')){
            url = e.target.getAttribute('data-url')
            requestPageAW(url)
            .then(data => {
                document.querySelector('#paginator') && document.querySelector('#paginator').remove()
                tbody.innerHTML = data['html']
            })
        }


        if (e.target.classList.contains('fa-filter')){
            form.classList.contains('show-form') ? form.classList.remove('show-form') : form.classList.add('show-form')
        }

    })

    //Wrapper Submit
    wrapper.addEventListener('submit', (e) => {
        /*This event will be fired every time a submit occurs and the target contains the 'modal-cancel-form' class in it's
        classlist, this event will stop the itself, and collect the data needed to cancel the consult, this consists of
        the url, method, csrfmiddlewaretoken and the form data, once this data is collected from the form, we proceed to
        call our asynchronous function, the response is dynamically displayed in our table.*/
        if (e.target.nodeName === 'FORM'){
            e.preventDefault()
            let patientQuery = document.querySelector('#id_patient').value
            let monthQuery = document.querySelector('#id_month').value
            let yearQuery = document.querySelector('#id_year').value
            let url = e.target.action + '?patient=' + patientQuery + '&month=' + monthQuery + '&year=' + yearQuery
            filterResultsAW(url)
            .then(data => {
                document.querySelector('#paginator') && document.querySelector('#paginator').remove()
                tbody.innerHTML = data['html']
            })
        }
    })
}