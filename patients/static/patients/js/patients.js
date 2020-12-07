/*This JS file contains all the variable declarations, Async functions and functions, and event listeners needed for
the Patients main page to work properly, it is divided into three sections: Variable Declarations, Functions and
event listeners, the Variable declarations section is divided into another two sections, for data availability and
no data present functionality, the data available section contains some an objects  which contain the respective
warning messages shown to the user in case there is any anomally in any patient's instance, it also contains a variable
called 'backedUpData', the purpose of this variable is to serve the data that present before a filtering operation.
The function section consists of 3 async functions and 1 sync function.*/

// ################################################ Variables ##########################################################

// Data available
var body = document.querySelector('body')

if (document.querySelector('.wrapper') !== 'undefined' && document.querySelector('.wrapper') !== 'null'){
    var wrapper = document.querySelector('.wrapper')
    var i = document.querySelector('.fa-filter')
    var form = document.querySelector('form')
    var filterForm = document.querySelector('.filter-form')
    var input = document.querySelector('#id_patient')
    var button = document.querySelectorAll('button')
    var table = document.querySelector('table')
    var tbody = document.querySelector('tbody')
    var deletion = document.querySelectorAll('.delete')
    var modal = document.querySelector('.modal')
    var modalContent = document.querySelector('.modal-content')
    var info = document.querySelector('.info')
    var infoContent = document.querySelector('.info-content')
    var warningPopup = document.querySelector('.popup')
    var warningPopupText = document.querySelector('.popup-text')

    // Warning Messages
    var warningMessages = {
        'no-id-registered' : "Individual over 18, ID information unknown",
        'expired-insurance' : "Medical Insurance's valid time concluded",
        'out-of-date-info' : "Patient's ID unknown and Medical Insurance information out of date",
        'in-order': "Individual's information up to date"
    }
}

// No Data Available
if (document.querySelector('#add_patients') !== 'undefined' && document.querySelector('#add_patients') !== 'null'){
    var addPatient = document.querySelector('#add_patients')
}

// ################################################ Functions ##########################################################

// Async Functions
async function deleteAW(url){
    /*This deleteAW async functions it's purpose is to retrieve the deletion form
      used to delete patient instances, it accepts a single argument 'url', after
      the data was retrieved from the server, it's converted to JSON format and
      returned*/
    const result = await fetch(url)
    const data = await result.json()
    return data
}

async function getPageAW(url){
    /* This async function will be used to collect the data from the previous or next page, this content will be
    received as a promise, so we need to return it in JSON format so we can process it, this content will be set to
    the tbody dynamically.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function filterResults(url, method, query){
    /*This filterResults async functions it's purpose is to retrieve the patients
      related data from the database based on a query the user inputs in the filter form,
      it accepts 4 arguments 'url' to where the POST request is done, the method which
      we retrieve from the form.action attribute, the 'csrfmiddlewaretoken' we retrieve
      from the input's hidden input and the formData, the data inputted into the form.
      after the data was retrieved from the server, it's converted to JSON format and
      returned*/
    const result = await fetch(url, {method:method, headers:{'QUERY': query}})
    const data = await result.json()
    return data
}

async function submitFormAW(form, csrfmiddlewaretoken){
    /*This submitFormAW async function it's purpose is to submit the deletion of patients
      from the database, it accepts 2 arguments 'url' to where the POST request is done, the method which
      we retrieve from the form.action attribute, the 'csrfmiddlewaretoken' we retrieve
      from the input's hidden input, after all this data is retrieved from the form, we make the request,
      this will return us some data from the server, after the data was retrieved from the server,
      it's converted to JSON format and returned*/
    const result = await fetch(form.action, {method:'POST', headers:{'X-CSRFToken': csrfmiddlewaretoken}})
    const data = await result.json()
    return data
}

// Sync Functions

// This function is used to retrieve the warning message that will be shown to the user, it expects one parameter, the code.
function retrieveWarningMessage(messageCode){
    return warningMessages[messageCode]
}

// ############################################ Event Listeners ########################################################

// addPatient Event Listeners, this events will be fired when there is not data available to show.
// addPatient Event Listeners
if (addPatient){
    /*This function will be called every time the addPatient element is present,
      It will create a levitating effect in this element.*/

    setInterval(function(){
        if (addPatient.style.top == '90%'){
            addPatient.style.top = '88%'
        } else {
            addPatient.style.top = '90%'
        }
    },500)

    /* Every time a hover occurs over this element, this event will be fired, it will add the add-patient-hover
       class to the element*/
    addPatient.addEventListener('mouseover', () => {
        addPatient.classList.add('add-patient-hover')
    })

    /* Every time a hover occurs over this element, this event will be fired, it will remove the add-patient-hover
       class from the element*/
    addPatient.addEventListener('mouseout', () => {
        addPatient.classList.remove('add-patient-hover')
    })
}

// Body Event Listeners

if (body){

    body.addEventListener('click', (e) => {
        /* This event will be fired every time an angle icon is clicked, this event will grab the url for the
           GET request, then the response will be added to the tbody, as well as the paginator will be deleted
           to get the current one.*/
        if (e.target.classList.contains('fa-angle-left') || e.target.classList.contains('fa-angle-right')){
            const url = e.target.getAttribute('data-url') + e.target.getAttribute('data-page')
            getPageAW(url)
            .then(data => {
                document.querySelector('#paginator').remove()
                tbody.innerHTML = data['html']
            })
        }
    })

    body.addEventListener('mouseover', (e) => {
        // This event will be fired, every time the user hovers over a 'fa-angle-right' or 'fa-angle-left', the fa-angle-hover class will be added.
        if (e.target.classList.contains('fa-angle-left') || e.target.classList.contains('fa-angle-right')){
            e.target.classList.add('fa-angle-hover')
        }
    })

    body.addEventListener('mouseout', (e) => {
        // This event will be fired, every time the user hover out occurs on a 'fa-angle-right' or 'fa-angle-left', the fa-angle-hover class will be removed.
        if (e.target.classList.contains('fa-angle-left') || e.target.classList.contains('fa-angle-right')){
            e.target.classList.remove('fa-angle-hover')
        }
    })

}

// Wrapper Event Listeners
if (wrapper){

    // Wrapper Mouseover Events
    wrapper.addEventListener('mouseover', (e) => {

        /* This event will be fired every time a hover occurs in the icons or a td cell, this will change many style
           properties from the row and add tr-hover and td-hover class*/
        if (e.target.nodeName === 'TD' || ((e.target.classList.contains('fa-trash') || e.target.classList.contains('fa-edit')))){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = '#C7E8F3'
            row.style.color = '#496897'
        }

        let deletion = document.querySelectorAll('.fa-trash')
        for (let i = 0; i<deletion.length; i++){
            /******************************************/
            /*So we were having a dilemma in here, we were trying to add a click event to the fa-trash icon, so every
              time we clicked it, a modal will pop up with some content to either perform the delete action or to cancel
              the process, so what we did is to, every time a hover over the wrapper occurs, we set the listener to all
              the icons present, why this? because the rows were added dynamically from deleting an filter, and also
              the parent of this icons had another click event, this will fire the parent click event if the listener
              was set to the wrapper, how can we deal with this? *This event is fired every time a click occurs on a
              fa-trash icon, this will pop-up a modal with the content needed to perform or cancel the deletion operati
              on.*
            */
            deletion[i].addEventListener('click', (e) => {
            e.preventDefault()
            e.stopPropagation()
            deleteAW(deletion[i].parentNode.getAttribute('data-url'))
            .then(data => {
                modal.classList.add('modal-show')
                modalContent.innerHTML = data['html']
            })
            })
        }

        let update = document.querySelectorAll('.fa-edit')
        for (let i = 0; i<update.length; i++){
            /******************************************/
            /* So we were having a dilemma in here, we were trying to add a click event to the fa-edit icon, so every
              time we clicked it,this will grab all the 'url' from the data-url attribute and call the async function and
              redirect us to that location. so what we did is to, every time a hover over the wrapper occurs,
              we set the listener to all the icons present, why this? because the rows were added dynamically from
              deleting an filter, and also the parent of this icons had another click event, this will fire the parent
              click event if the listener was set to the wrapper, how can we deal with this? *This event is fired every
              time a click occurs on a fa-edit icon, this will grab all the 'url' from the data-url attribute and call
              the async function and redirect us to that location.*/
            update[i].addEventListener('click', (e) => {
                e.stopPropagation()
                let url = e.target.parentNode.getAttribute('data-url')
                window.location.href = url
            })
        }

        let warnings = document.querySelectorAll('.fa-exclamation-circle, .fa-check-circle')
        for (let i = 0; i<warnings.length; i++){
            /*This event will be fired every time the target contains the fa-exclamation-circle class in its classlist,
              what this function will perform is the display of the warning pop-up aside of the table row for that
              specific patient instance, in case there is any anomally in the registered information, if not, it will
              display a pop-up indicating every thing is in order.*/
            warnings[i].addEventListener('mouseover', (e) => {
                form.classList.remove('show-form')
                let positionY = e.clientY - 12
                let messageCode = e.target.getAttribute('data-message-code')
                warningPopupText.innerText = retrieveWarningMessage(messageCode)
                warningPopup.classList.add('popup-show')
                messageCode === 'in-order' ? warningPopupText.classList.add('popup-text-in-order') : warningPopupText.classList.remove('popup-text-in-order')
                warningPopup.style.top = String(positionY + 'px')
            })

            warnings[i].addEventListener('mouseout', (e) => {
                warningPopup.classList.remove('popup-show')
            })
        }


        // This event will be fired, every time the user hovers over an input, the input-hover class will be added.
        if (e.target.nodeName === 'INPUT'){
            e.target.classList.add('input-hover')
        }

        // This event will be fired, every time the user hovers over a button, the button-form-hover class will be added.
        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.add('button-form-hover')
        }

       // This event will be fired, every time the user hovers over fa-plus icon, the fa-plus-hover class will be added.
       if (e.target.classList.contains('fa-plus')){
            e.target.classList.add('fa-plus-hover')
        }

       // This event will be fired, every time the user hovers over fa-trash icon, the fa-trash-hover class will be added.
       if (e.target.classList.contains('fa-trash')){
            e.target.classList.add('fa-trash-hover')
        }

       // This event will be fired, every time the user hovers over fa-edit icon, the fa-edit-hover class will be added.
       if (e.target.classList.contains('fa-edit')){
            e.target.classList.add('fa-edit-hover')
        }

       // This event will be fired, every time the user hovers over fa-filter icon, the fa-filter-hover class will be added.
        if (e.target.classList.contains('fa-filter')){
            e.target.classList.add('fa-filter-hover')
        }


        })

    // Wrapper Mouseout Events
    wrapper.addEventListener('mouseout', (e) => {
      /* This event will be fired every time a hover occurs in the icons or a td cell, this will change many style
         properties from the row and removed tr-hover and td-hover class*/
      if (e.target.nodeName === 'TD' || ((e.target.classList.contains('fa-trash') || e.target.classList.contains('fa-edit')))){
        let row
        e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = ''
            row.style.color = ''
      }

        // This event will be fired, every time the user hovers out over an input, the input-hover class will removed.
        if (e.target.nodeName === 'INPUT'){
            e.target.classList.remove('input-hover')
        }

        // This event will be fired, every time the user hovers out a button, the button-form-hover class will be removed.
        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.remove('button-form-hover')
        }

       // This event will be fired, every time the user hovers out a fa-plus icon, the fa-plus-hover class will be removed.
       if (e.target.classList.contains('fa-plus')){
            e.target.classList.remove('fa-plus-hover')
        }

       // This event will be fired, every time the user hovers out a fa-trash icon, the fa-trash-hover class will be removed.
       if (e.target.classList.contains('fa-trash')){
            e.target.classList.remove('fa-trash-hover')
        }

       // This event will be fired, every time the user hovers out a fa-edit icon, the fa-edit-hover class will be removed.
       if (e.target.classList.contains('fa-edit')){
            e.target.classList.remove('fa-edit-hover')
        }

       // This event will be fired, every time the user hovers out a fa-filter icon, the fa-filter-hover class will be removed.
        if (e.target.classList.contains('fa-filter')){
            e.target.classList.remove('fa-filter-hover')
        }

     })

    // Wrapper Click Events
    wrapper.addEventListener('click', (e) => {

        // This event will be fired if the target is the modal, it will remove the class 'modal-show' from the modal.
        if (e.target === modal){
            modal.classList.remove('modal-show')
        }

        /* This event will be fired if the target is a button and contains the 'no' textContent or 'ok',
           it will remove the class 'modal-show' from the modal.*/
        if (e.target.value === 'no' || e.target.textContent === 'Ok'){
            e.stopPropagation()
            e.preventDefault()
            modal.classList.remove('modal-show')
        }

        /* This event will be fired if the target is a fa-filter icon, and depending if the filter form contains the
           show-form class or not, will add or remove this class.*/
        if (e.target.classList.contains('fa-filter')){
            warningPopup.classList.remove('popup-show')
            warningPopup.style.top = ''
            !form.classList.contains('show-form') ? form.classList.add('show-form') : form.classList.remove('show-form')
        }

    })

    // Wrapper Submit Events
    wrapper.addEventListener('submit', (e) => {
        const form = document.querySelector('#modal-form')
        const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
        /*This event will be fired every time the target is a form, it will collect some data from the target, as the
          action attribute value and the csrfmiddlwaretoken, it will make a request using the submitFormAW and depending
          if the form used was filter, it will insert that data inside the backedUpContent variable inside the wrapper,
          else the new data retrieved will be added to the wrapper.*/
        if (e.target === form){
            e.preventDefault()
            submitFormAW(form, csrfmiddlewaretoken)
            .then(data => {
                if (data.hasOwnProperty('patients')){
                    modalContent.innerHTML = data['html']
                    tbody.innerHTML = data['patients']
                }else{
                    modalContent.innerHTML = data['html']
                }
            })
        }

    })

    wrapper.addEventListener('input', (e) => {
        /*This event will be fired every time the target is an input, it will collect some data from the target, as the
          action attribute value, the csrfmiddlwaretoken, the input value, the method, and will create a new FormData
          obj, it will make a request using the filterResultsAW and retrieve the information from the server to insert it
          to the wrapper inner HTML, if the value is empty, it will insert the content inside the backedUpContent variable
          to the wrapper innerHTML.*/
        if (e.target.nodeName === 'INPUT'){
            const url = form.action
            const method = form.method
            const query = e.target.value
            filterResults(url, method, query)
            .then(data => {
                tbody.innerHTML = data['html']
            })
        }

    })

}