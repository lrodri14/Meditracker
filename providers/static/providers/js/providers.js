/* This JS File contains all the code to make the Providers App Work, it contains all the variable declarations for code
use, the definition of Asynchronous Functions and Synchronous functions, as well as all the Event Listeners needed to
execute these functions. The variable declarations contains two sections "Available Data", which contains all the
variable declarations needed when data is present and retrieved from the server side, and "Modal", this contains all
the variable declarations for Modal Functionality. The Functions Section contains two sections as well "Async Funcs"
which contains all the Async functions, it consists of 11 async function declarations, and the "Sync Funcs" which
contains the only Sync functions all over the file. The Event Listeners Section is composed of 3, the navigation bar
events listener sections, the wrapper event listeners section and the modal event listeners section.*/

////////////////////////////////////////////////////Variables///////////////////////////////////////////////////////////

// Available Data
if (document.querySelector('.wrapper') !== 'undefined' && document.querySelector('.wrapper') !== 'null'){
    var wrapper = document.querySelector('.wrapper')
    var navigation = document.querySelector('.navigation')
    var tabs = document.querySelectorAll('.tab')
}

// Modal
let modal = document.querySelector('.modal');
let modalContent = document.querySelector('.modal-content');


////////////////////////////////////////////////////Functions///////////////////////////////////////////////////////////


// Async Functions
async function addProvidersFormAW(url, formType){
    /*Function used to display provider's form dynamically, it accepts two
      parameters, the 'url' for the "GET" request, and the 'formType', which
      we grab from the data-provider-type attribute in our target. This
      function will return the data from the request in JSON Format.*/
    const result = await fetch(url, {headers:{'FORM-TYPE': formType}})
    const data = result.json()
    return data
}

async function addVisitorsFormAW(url){
    /*Function used to display visitor's form, it accepts one parameter,
      the 'url' for the "GET" request, This function will return the data
      from the request in JSON Format.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function updateProvidersFormAW(url){
    /*Function used to display the update provider form, it accepts one parameter,
      the 'url' for the "GET" request, This function will return the data
      from the request in JSON Format.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function deleteProvidersFormAW(url){
    /*Function used to display the delete provider form, it accepts one parameter,
      the 'url' for the "GET" request, This function will return the data
      from the request in JSON Format.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function addProvidersAW(url, method, csrfmiddlewaretoken, formData){
    /*Function used to add providers to the database, this functions takes
      four parameters, the 'url' for the "POST" request, the 'method' which
      we collect from the form's method attribute, the 'csrfmiddlewaretoken'
      parameter, which receives the value from the csrfmiddlewaretoken attribute
      in every form's hidden input, and lastly the 'formData' the collection of
      all the data values in the form inputs. This function will return the
      result in JSON Format.*/
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken': csrfmiddlewaretoken}, body:formData})
    const data = result.json()
    return data
}

async function deleteProvidersAW(url, method, csrfmiddlewaretoken){
    /*Function used to add providers to the database, this functions takes
      three parameters, the 'url' for the "POST" request, the 'method' which
      we collect from the form's method attribute, the 'csrfmiddlewaretoken'
      parameter, which receives the value from the csrfmiddlewaretoken attribute
      in every form's hidden input. This function will return the
      result in JSON Format.*/
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken': csrfmiddlewaretoken}})
    const data = result.json()
    return data
}

async function requestProvidersAW(url, providerType){
    /*This function is used to request the providers from the server side every time we
      click on a tab in the navigation bar, it receives two parameters, 'url' for the
      "GET" request, and the 'providerType' which is sent as a header requesting that
      specific type of provider. This function will return it's result in JSON Format.*/
    const result = await fetch(url, {headers:{'PROVIDER-TYPE': providerType}})
    const data = result.json()
    return data
}

async function requestVisitorsAW(url){
    /*This function is used to request the providers from the server side every time we
      click on a tab in the navigation bar, it receives one parameter, 'url' for the
      "GET" request, This function will return it's result in JSON Format.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function filterProvidersAW(url, query, type){
    /*This function is used retrieve specific providers from the server side
      depending on a query sent by a "GET" request and a type. This function takes
      three parameters, 'url' for the "GET" request, the 'query' which we collect from
      the input in the form and the type, which we collect from the classlist of the form.
      This function will return it's result in JSON Format.*/
    provider_type = (type === 'laboratories-filter-form') ? 'LP' : 'MP'
    const result = await fetch(url, {headers:{'QUERY':query, 'PROVIDER-TYPE':provider_type}})
    const data = result.json()
    return data
}

async function filterVisitorsAW(url, query){
    /*This function is used retrieve specific visitors from the server side
      depending on a query sent by a "GET" request. This function takes
      two parameters, 'url' for the "GET" request, the 'query' which we collect from
      the input in the form. This function will return it's result in JSON Format.*/
    const result = await fetch(url, {headers:{'QUERY':query}})
    const data = result.json()
    return data
}

async function providerDetailsAW(url){
    /*This function is used to display the provider or visitor details
      in our page, it takes one parameter, the 'url' for the "GET"
      request. This function will return it's result in JSON Format.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

// Sync Functions

function addIconLevitate(addProvidersIcon){
    /*This function is used to perform the levitation effect in the
      .fa-plus icon every time there is no data available, it takes
      one parameter, 'addProvidersIcon' is the icon itself. it will
      execute a setInterval function every 0.5 seconds, which just
      changes the style of the 'top' attribute in our element.*/
    setInterval(function(){
        if (addProvidersIcon.style.top == '90%'){
            addProvidersIcon.style.top = '88%'
        } else {
            addProvidersIcon.style.top = '90%'
        }
    },500)
}


////////////////////////////////////////////////////Event Listeners/////////////////////////////////////////////////////

/////////////////////////////////
// Navigation Bar Event Listeners
if (navigation){

    // Click Events
    navigation.addEventListener('click', (e) => {

        /*This event will be fired every time a navigation bar is clicked, it will remove
          the 'tab-active' class from the all the tabs and add it to the target, so we can
          create an 'active' effect, it will pickup the following values 'url' and 'providerType
          these will be used in the async function called depeding on the tab clicked, if the
          visitors tab is clicked, the providerType variable will be useless. Once the function
          is executed, the JSON Format data will be added to the Wrapper inner HTML.'*/
        if (e.target.classList.contains('tab')){
            for (let i = 0; i<tabs.length; i++){
                tabs[i].classList.remove('tab-active')
            }
            e.target.classList.add('tab-active')
            let url = e.target.getAttribute('data-url')
            let providerType = e.target.getAttribute('data-provider-type')
            if (providerType){
                requestProvidersAW(url, providerType)
                .then(data => {
                    wrapper.innerHTML = data['html']
                    if (document.querySelector('.add-providers')){
                        addProvidersIcon = document.querySelector('.add-providers')
                        addIconLevitate(addProvidersIcon)
                    }
                })
            }else{
                requestVisitorsAW(url)
                .then(data => {
                    wrapper.innerHTML = data['html']
                    if (document.querySelector('.add-providers')){
                        addProvidersIcon = document.querySelector('.add-providers')
                        addIconLevitate(addProvidersIcon)
                    }
                })
            }
        }


    })

    /*This event will add the 'tab-hover' class to the target
      to create a hovering effect.*/
    navigation.addEventListener('mouseover', (e) => {
        if (e.target.classList.contains('tab')){
            e.target.classList.add('tab-hover')
        }
    })

    /*This event will remove the 'tab-hover' class from the target
      to create a hover off effect.*/
    navigation.addEventListener('mouseout', (e) => {
        if (e.target.classList.contains('tab')){
            e.target.classList.remove('tab-hover')
        }
    })
}

//////////////////////////
// Wrapper Event Listeners
if (wrapper){

    // Wrapper Click Events
    wrapper.addEventListener('click', (e) => {

        /*This click event will be fired every time the 'fa-plus' icon is clicked,
          it will collect the following data form the target: 'url' form the data-url
          attribute and the 'providerType' from the data-provider-type attribute, and will
          execute an async function depending if the data-provider-type was localized. It will
          open the modal and display the JSON Formatted data in the modal content section,
          it returns a form.*/
        if (e.target.classList.contains('fa-plus')){
            let url = e.target.getAttribute('data-url')
            let providerType = e.target.getAttribute('data-provider-type')
            if (providerType){
                addProvidersFormAW(url, providerType)
                .then(data => {
                    modalContent.innerHTML = data['html']
                    modal.classList.add('modal-show')
                })
            }else{
                addVisitorsFormAW(url)
                .then(data => {
                    modalContent.innerHTML = data['html']
                    modal.classList.add('modal-show')
                })
            }
        }

        /*This click event will be fired every time a table row is clicked,
          it will collect the following data form the target: 'url' form the data-url
          attribute, it will execute an async function for this process which will display
          the details of the element the user clicked. it will open the modal and display the
          JSON Formatted data in the modal content section, it returns a card-like template.*/
        if (e.target.parentNode.nodeName === 'TR'){
            let url = e.target.parentNode.getAttribute('data-url')
            providerDetailsAW(url)
            .then(data => {
                modalContent.innerHTML = data['html']
                modal.classList.add('modal-show')
            })
        }

        /*This click event will be fired every time a 'fa-filter' icon is clicked,
          it won't collect any data, it will just add or remove the 'filter-form-show'
          class from the filter which resides at the right side of the wrapper, it will
          show up a filtering form.*/
        if (e.target.classList.contains('fa-filter')){
            var filterForm = document.querySelector('.filter-form')
            filterForm.classList.contains('filter-form-show') ? filterForm.classList.remove('filter-form-show') : filterForm.classList.add('filter-form-show')
        }

        /*This click event will be fired every time a 'fa-edit' icon is clicked,
        it will collect the following data from the target: 'url' from the data-url
        attribute in the target, it will execute an async function, will open up the modal
        and show up the JSON Formatted data in the modal content section, it returns a form*/
        if (e.target.classList.contains('fa-edit')){
            let url = e.target.getAttribute('data-url')
            updateProvidersFormAW(url)
            .then(data => {
                modalContent.innerHTML = data['html']
                modal.classList.add('modal-show')
            })
        }

        /*This click event will be fired every time a 'fa-trash' icon is clicked,
        it will collect the following data from the target: 'url' from the data-url
        attribute in the target, it will execute an async function, will open up the modal
        and show up the JSON Formatted data in the modal content section, it returns a form*/
        if (e.target.classList.contains('fa-trash')){
            let url = e.target.getAttribute('data-url')
            deleteProvidersFormAW(url)
            .then(data => {
                modalContent.innerHTML = data['html']
                modal.classList.add('modal-show')
            })
        }

    })

    // Wrapper Mouseover Events
    wrapper.addEventListener('mouseover', (e) => {

        /*This mouseover event is fired every time a hover occurs in a 'fa-plus' icon
          it will add the 'fa-plus-hover' class to the target*/
        if (e.target.classList.contains('fa-plus')){
            e.target.classList.add('fa-plus-hover')
        }

        /*This mouseover event is fired every time a hover occurs in a 'fa-edit' icon
          it will add the 'fa-edit-hover' class to the target*/
        if (e.target.classList.contains('fa-edit')){
            e.target.classList.add('fa-edit-hover')
        }

        /*This mouseover event is fired every time a hover occurs in a 'fa-trash' icon
          it will add the 'fa-trash-hover' class to the target*/
        if (e.target.classList.contains('fa-trash')){
            e.target.classList.add('fa-trash-hover')
        }

        /*This mouseover event is fired every time a hover occurs in a 'fa-envelope' icon
          it will add the 'fa-envelope-hover' class to the target*/
        if (e.target.classList.contains('fa-envelope')){
            e.target.classList.add('fa-envelope-hover')
        }

        /*This mouseover event is fired every time a hover occurs in a 'fa-filter' icon
          it will add the 'fa-filter-hover' class to the target*/
        if (e.target.classList.contains('fa-filter')){
            e.target.classList.add('fa-filter-hover')
        }

        /*This mouseover event is fired every time a hover occurs in a table row, this event
          must be fired by it's children since it's impossible to hover over a tr element*/
        if (e.target.nodeName === 'TD' ||  ((e.target.classList.contains('fa-trash') || e.target.classList.contains('fa-edit') || e.target.classList.contains('fa-envelope')))){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = '#0ff5fc'
            row.classList.add('tr-hover')
            for (let i = 0; i<row.childNodes.length; i++){
                if (row.childNodes[i].nodeName === 'TD'){
                    row.childNodes[i].classList.add('td-hover')
                }
            }
        }

    })

    // Wrapper Mouseout Events
    wrapper.addEventListener('mouseout', (e) => {

        /*This mouseout event is fired every time a mouseout event occurs in a 'fa-plus' icon,
          it will remove the 'fa-plus-hover' class to the target*/
        if (e.target.classList.contains('fa-plus')){
            e.target.classList.remove('fa-plus-hover')
        }

        /*This mouseout event is fired every time a mouseout event occurs in a 'fa-edit' icon,
          it will remove the 'fa-edit-hover' class to the target*/
        if (e.target.classList.contains('fa-edit')){
            e.target.classList.remove('fa-edit-hover')
        }

        /*This mouseout event is fired every time a mouseout event occurs in a 'fa-trash' icon,
          it will remove the 'fa-trash-hover' class to the target*/
        if (e.target.classList.contains('fa-trash')){
            e.target.classList.remove('fa-trash-hover')
        }

        /*This mouseout event is fired every time a mouseout event occurs in a 'fa-envelope' icon,
          it will remove the 'fa-envelope-hover' class to the target*/
        if (e.target.classList.contains('fa-envelope')){
            e.target.classList.remove('fa-envelope-hover')
        }

        /*This mouseout event is fired every time a mouseout event occurs in a 'fa-filter' icon,
          it will remove the 'fa-filter-hover' class to the target*/
        if (e.target.classList.contains('fa-filter')){
            e.target.classList.remove('fa-filter-hover')
        }

        /*This mouseover event is fired every time a hover occurs in a table row, this event
          must be fired by it's children since it's impossible to hover over a tr element*/
        if (e.target.nodeName === 'TD' ||  ((e.target.classList.contains('fa-trash') || e.target.classList.contains('fa-edit') || e.target.classList.contains('fa-envelope')))){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = ''
            row.classList.remove('tr-hover')
            for (let i = 0; i<row.childNodes.length; i++){
                if (row.childNodes[i].nodeName === 'TD'){
                    row.childNodes[i].classList.remove('td-hover')
                }
            }
          }

    })

    // Wrapper Input Events
    wrapper.addEventListener('input', (e) => {

        /*This event is fired every time the filter form receives an input, for each
        character this event will be fired. It will collect the following data from the
        target: 'url' form the action attribute in the form, 'query' which is collected
        from the input, 'type' which is collected from the classlist of the target. it will
        call an async func depending if the type attribute is present in the classlist
        the data returned in JSON Format is added to the innerHTML from the tbody element.*/
        if (e.target.nodeName === 'INPUT'){
            let form = e.target.parentNode.parentNode
            let url = form.action
            let query = e.target.value
            let type = form.classList[1]
            if (type){
                filterProvidersAW(url, query, type)
                .then(data => {
                    document.querySelector('tbody').innerHTML = data['html']
                })
            }else{
                filterVisitorsAW(url, query)
                .then(data => {
                    document.querySelector('tbody').innerHTML = data['html']
                })
            }
        }
    })

}

////////////////////////
// Modal Event Listeners
if (modal){

    // Modal Click Events
    modal.addEventListener('click', (e) => {

        /*This click event is fired every time the modal or the modal content
        is clicked, it will remove the 'modal-show' class from the modal*/
        if (e.target === modal || e.target === modalContent){
            modal.classList.remove('modal-show')
        }

        /*This click event is fired every time the button inside the modal
        or the modal content is clicked and it's text content contains the
        'No' word, it will remove the 'modal-show' class from the modal.*/
        if (e.target.textContent === 'No'){
            e.preventDefault()
            e.stopPropagation()
            modal.classList.remove('modal-show')
        }

    })

    // Modal Mouseover Events
    modal.addEventListener('mouseover', (e) => {
        /*This event will be fired every time a hover occurs over a
          button, and will add the 'button-hover' class to the target.*/
        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.add('button-hover')
        }

    })

    // Modal Mouseout Events
    modal.addEventListener('mouseout', (e) => {
        /*This event will be fired every time a hover out occurs over a
          button, and will remove the 'button-hover' class to the target.*/
        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.remove('button-hover')
        }

    })

    // Modal Submit Events
    modal.addEventListener('submit', (e) => {
        e.preventDefault()
        e.stopPropagation()

        /*This submit event will be fired every time a form is submitted, and the form
          contains an id attribute with the 'delete-operation' value, it will collect
          the following data from the target: 'url' which is used to do the "POST" request,
          the 'method' which it collects from the method attribute in the form, the 'csrfmiddlewaretoke',
          used to protect the request against Cross-Site Request Forgeries attacks and collected from the
          '[name=csrfmiddlewaretoken]' hidden input value, the data received in JSON Format will be added
          to the wrapper InnerHTML, it will also make a check in if the '.add-providers' element is present,
          if it is, it will call the addIconLevitate function.*/
        if (e.target.id === 'delete-operation'){
            let form = e.target
            let url = form.action
            let method = form.method
            let csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            deleteProvidersAW(url, method, csrfmiddlewaretoken)
            .then(data => {
                if (data['updated_html']){
                    modal.classList.remove('modal-show')
                    wrapper.innerHTML = data['updated_html']
                    if (document.querySelector('.add-providers')){
                        addProvidersIcon = document.querySelector('.add-providers')
                        addIconLevitate(addProvidersIcon)
                    }
                }
            }
          )
        }

        /*This submit event will be fired every time a form is submitted, it will collect
          the following data from the target: 'url' which is used to do the "POST" request,
          the 'method' which it collects from the method attribute in the form, the 'csrfmiddlewaretoke',
          used to protect the request against Cross-Site Request Forgeries attacks and collected from the
          '[name=csrfmiddlewaretoken]' hidden input value, the data received in JSON Format will be added
          to the wrapper InnerHTML, it will also make a check in if the'.add-providers' element is present
          , if it is, it will call the addIconLevitate function.*/
        if (e.target.nodeName === 'FORM' && !e.target.id){
            let form = e.target
            let url = form.action
            let method = form.method
            let csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            let formData = new FormData(form)
            addProvidersAW(url, method, csrfmiddlewaretoken, formData)
            .then(data => {
                console.log('data')
                if (data['html']){
                    modalContent.innerHTML = data['html']
                }else{
                    modal.classList.remove('modal-show')
                    wrapper.innerHTML = data['updated_html']
                    if (document.querySelector('.add-providers')){
                        addProvidersIcon = document.querySelector('.add-providers')
                        addIconLevitate(addProvidersIcon)
                    }
                }
            }
          )
        }

    })
}