/* This records_list.js file contains all the variable declarations, async function and event listeners for the
   records main page to work properly, this file is divided into three sections: variable declarations, async functions
   and event listeners.*/

/*############################################# Variable Declarations ####################################*/

if (document.querySelector('.wrapper') !== 'undefined' && document.querySelector('.wrapper') !== 'null'){
    var wrapper = document.querySelector('.wrapper')
    var dataTable = document.querySelector('.table')
    var rows = document.querySelectorAll('tr')
    var i = document.querySelector('.fa-filter')
    var button = document.querySelector('button')
    var form = document.querySelector('form')
}

/*#################################################### Functions #########################################*/

async function requestPageAW(url){
    /* This async function will be used to collect the data from the previous or next page, this content will be
    received as a promise, so we need to return it in JSON format so we can process it, this content will be set to
    the dataTable dynamically.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function filterResultsAW(url){
    /* This async function will be used to collect the data from the server through a GET request and some parameters
    declared, this content will be received as a promise, so we need to return it in JSON format so we can process it,
    this content will be set to the dataTable dynamically.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

/*#################################################### Event Listeners ###################################*/

// Wrapper Event Listeners
if (wrapper){

    //Wrapper mouse over
    wrapper.addEventListener('mouseover', (e) => {

        // This event will be fired every time the target is a 'fa-angle', this event will add the 'fa-angle-hover' to its classList.
        if (e.target.classList.contains('fa-angle-left') || e.target.classList.contains('fa-angle-right')){
            e.target.classList.add('fa-angle-hover')
        }

        // This event will be fired if the classList contains the 'fa-filter' class and it will add the 'fa-filter-hover' class.
        if (e.target.classList.contains('fa-filter')){
            e.target.classList.add('fa-filter-hover')
        }

        // This event will be fired if nodeName is 'BUTTON' and it will add the 'button-hover' class.
        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.add('button-form-hover')
        }

        /*This event will be fired every time a mouseover occurs over a 'TD' or the target contains 'fa-edit'
        class in it's classList, This will make changes inside this row.*/
        if (e.target.nodeName === 'TD' || ((e.target.classList.contains('fa-trash') || e.target.classList.contains('fa-edit')))){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = '#C7E8F3'
            row.style.color = '#496897'
        }

    })

    //Wrapper mouse out
    wrapper.addEventListener('mouseout', (e) => {

        // This event will be fired every time the target is a 'fa-angle', this event will remove the 'fa-angle-hover' to its classList.
        if (e.target.classList.contains('fa-angle-left') || e.target.classList.contains('fa-angle-right')){
            e.target.classList.remove('fa-angle-hover')
        }

        // This event will be fired if the classList contains the 'fa-filter' class and it will remove the 'fa-filter-hover' class.
        if (e.target.classList.contains('fa-filter')){
            e.target.classList.remove('fa-filter-hover')
        }

        // This event will be fired if nodeName is 'BUTTON' and it will remove the 'button-hover' class.
        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.remove('button-form-hover')
        }

        /*This event will be fired every time a mouse out occurs from a 'TD' or the target contains 'fa-edit'
        class in it's classList, This will make changes inside this row.*/
        if (e.target.nodeName === 'TD' || ((e.target.classList.contains('fa-trash') || e.target.classList.contains('fa-edit')))){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = ''
            row.style.color = ''
        }

    })

    //Wrapper Click
    wrapper.addEventListener('click', (e) => {

    /* This event will be fired every time an angle icon is clicked, this event will grab the url for the
       GET request, then the response will be added to the tbody, as well as the paginator will be deleted
       to get the current one.*/
        if (e.target.classList.contains('fa-angle-left') || e.target.classList.contains('fa-angle-right')){
            let query_date_from = e.target.getAttribute('data-date-from');
            let query_date_to = e.target.getAttribute('data-date-to');
            let url = e.target.getAttribute('data-url')
            requestPageAW(url)
            .then(data => {
                if (document.querySelector('#paginator')){
                    document.querySelector('#paginator').remove()
                }
                dataTable.innerHTML = data['html']
            })
        }

        /* This event will be fired every time the target's classList contains the 'fa-filter' class, this event will either
            show or hide the filter form depending on the current state*/
        if (e.target.classList.contains('fa-filter')){
            !form.classList.contains('show-form') ? form.classList.add('show-form') : form.classList.remove('show-form')
        }

    })

    //Wrapper Submit
    wrapper.addEventListener('submit', (e) => {
        /*This event will be fired every time a submit occurs and the target is the filter results form
        this event will stop the itself, and collect the data needed to filter the records, this consists of
        the url , once this data is collected from the form, we proceed to call our asynchronous function, the
        response is dynamically displayed in our table.*/
        if (e.target.nodeName === 'FORM'){
            e.preventDefault()
            let fromDay = document.querySelector('#id_date_from_day').value
            let fromMonth = document.querySelector('#id_date_from_month').value
            let fromYear = document.querySelector('#id_date_from_year').value
            let toDay = document.querySelector('#id_date_to_day').value
            let toMonth = document.querySelector('#id_date_to_month').value
            let toYear = document.querySelector('#id_date_to_year').value
            let fromDate = fromYear + "-" + fromMonth + "-" + fromDay
            let toDate = toYear + "-" + toMonth + "-" + toDay
            const url = e.target.action + '?date_from=' + fromDate + '&date_to=' + toDate
            filterResultsAW(url)
            .then(data => {
                dataTable.innerHTML = data['html']
            })
        }
    })

}