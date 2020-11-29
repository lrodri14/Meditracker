/* This JS File contains all the variable declarations, async  and sync functions, and event listeners needed to show a
   particular patient's details, the variable section is divided into 4 divisions: backedUpData, imgPreview, titles and
   containers, the function section is divided into two divisions, sync functions and async functions, it contains a total
   of 6 functions, 5 of them sync and one left async.*/

// ##################################################### Variables #####################################################

let body = document.querySelector('body')

// Containers
let generalInfo = document.querySelector('.general-info')
let extras = document.querySelector('.extras')
let appointments = document.querySelector('.appointments')
let exams = document.querySelector('.exams')
let charges = document.querySelector('.charges')
let title = document.querySelector('#title')

// Back Up Content
let appointmentsBackUp = document.querySelector('.appointments').innerHTML
let examsBackUp = document.querySelector('.exams').innerHTML
let chargesBackUp = document.querySelector('.charges').innerHTML

// Image Preview
let previewImg = document.querySelector('.image-preview')
let image = document.querySelector('.previewed-image')

// Title
let titleOriginalContent = title.innerText

// ##################################################### Functions #####################################################

/* This functions will be used to perform the smooth automatic scrolling every time we click on a navigation tab*/
// Sync Functions
function generalScroll(){
    /*This function will scroll the window object left to 0 in a smooth behavior.*/
    window.scrollTo({
        left: 0,
        behavior: 'smooth'
    })
}

function backgroundScroll(){
    /*This function will scroll the window object left the width of the window screen in a smooth behavior.*/
    window.scrollTo({
        left: window.screen.availWidth,
        behavior: 'smooth'
    })
}

function appointmentsScroll(){
    /*This function will scroll the window object left the width of the window screen * 2 in a smooth behavior.*/
    window.scrollTo({
        left: window.screen.availWidth * 2,
        behavior: 'smooth'
    })
}

function examsScroll(){
    /*This function will scroll the window object left the width of the window screen * 3 in a smooth behavior.*/
    window.scrollTo({
        left: window.screen.availWidth * 3,
        behavior: 'smooth'
    })
}

function chargesScroll(){
    /*This function will scroll the window object left the width of the window screen * 4 in a smooth behavior.*/
    window.scrollTo({
        left: window.screen.availWidth * 4,
        behavior: 'smooth'
    })
}

// Async Functions
async function filterResultsAW(url, method,type, csrfmiddlewaretoken, formData){
    /* This function will be used to perform the filtering functionality for every data related to the specific patient,
       it requites 4 parameters we will grab to make the POST request successfully: 'url', required to make the POST
       request to this address, 'method' is the method used for the request, 'csrfmiddlewaretoken' we grab from the form
       hidden input and lastly the 'formData', we create a new FormData object using the information in the inputs of the
       form, we send this information and the response we return it in JSON Format.*/
    const result = await fetch(url, {'method':method, headers: {'X-CSRFToken':csrfmiddlewaretoken, 'FilterType': type}, body:formData})
    const data = await result.json()
    return data
}


// ##################################################### Event Listeners ###############################################

// Body Event Listeners
// Body Mouseover events
body.addEventListener('mouseover', (e) => {

    /* This event will be fired every time a hover occurs in the icons or a td cell, this will change many style
       properties from the row and add tr-hover and td-hover class*/
    if (e.target.nodeName === 'TD' || ((e.target.classList.contains('fa-trash') || e.target.classList.contains('fa-edit')))){
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

    /* This event will be fired every time a hover occurs over the target and the target or parentNode contains the
       info-tab class, and will add the tab-hover class*/
    if (e.target.classList.contains('info-tab') || e.target.parentNode.classList.contains('info-tab')){
        let tab = e.target.classList.contains('info-tab') ? e.target : e.target.parentNode
        tab.classList.add('tab-hover')
    }

    /*This event will be fired every time a hover occurs over the fa-filter icon and the fa-filter-hover class will be added*/
    if (e.target.classList.contains('fa-filter')){
        e.target.classList.add('fa-filter-hover')
    }

    /*This event will be fired every time a hover occurs over the fa-sync-alt icon and the fa-sync-alt-hover class will be added*/
    if (e.target.classList.contains('fa-sync-alt')){
        e.target.classList.add('fa-sync-alt-hover')
    }

    /*This event will be fired every time a hover occurs over a button and the button-form--hover class will be added*/
    if (e.target.nodeName === 'BUTTON'){
        const button = e.target
        button.classList.add('button-form-hover')
    }

})

// Body Mouseout Events
body.addEventListener('mouseout', (e) => {

  /* This event will be fired every time a hover occurs in the icons or a td cell, this will change many style
     properties from the row and removed tr-hover and td-hover class*/
  if (e.target.nodeName === 'TD' || ((e.target.classList.contains('fa-trash') || e.target.classList.contains('fa-edit')))){
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

/* This event will be fired every time a mouseout occurs off a target and the target or parentNode contains the
   info-tab class, and the tab-hover class will be removed*/
  if (e.target.classList.contains('info-tab') || e.target.parentNode.classList.contains('info-tab')){
        let tab = e.target.classList.contains('info-tab') ? e.target : e.target.parentNode
        tab.classList.remove('tab-hover')
    }

    /*This event will be fired every time a mouseout occurs off the fa-filter icon and the fa-filter-hover class will be removed*/
    if (e.target.classList.contains('fa-filter')){
        e.target.classList.remove('fa-filter-hover')
    }

    /*This event will be fired every time a mouseout occurs off a fa-sync-alt icon and the fa-sync-alt-hover class will be removed*/
    if (e.target.classList.contains('fa-sync-alt')){
        e.target.classList.remove('fa-sync-alt-hover')
    }

    /*This event will be fired every time a mouseout occurs off a button and the button-hover class will be removed*/
    if (e.target.nodeName === 'BUTTON'){
        const button = e.target
        button.classList.remove('button-form-hover')
    }

})

body.addEventListener('click', (e) => {

    /* This event will be fired every time a click occurs over the target and the target or parentNode contains the
       info-tab class, and will add the tab-hover class, the function will grab the tab clicked, and all the exiting
       tabs, will remove the tab-active class from all the tabs and finally add it to the tab clicked, afterwards, it
       will read the tab clicked innerText and depending of this value will set the title.innerText to the tab's inner text,
       call the corresponding sync function for the scrolling functionality.*/
    if (e.target.classList.contains('info-tab') || e.target.parentNode.classList.contains('info-tab')){
        let tab = e.target.classList.contains('info-tab') ? e.target : e.target.parentNode
        let tabs = document.querySelectorAll('.info-tab')
        for (let i = 0; i<tabs.length; i++){
            tabs[i].classList.remove('tab-active')
        }
        tab.classList.add('tab-active')

        if (tab.innerText === 'General'){
            generalScroll()
            title.innerText = titleOriginalContent
        } else if (tab.innerText === 'Background'){
            backgroundScroll()
            title.innerText = tab.innerText
        }else if (tab.innerText === 'Appointments'){
            appointmentsScroll()
            title.innerText = tab.innerText
        }else if (tab.innerText === 'Exams'){
            examsScroll()
            title.innerText = tab.innerText
        }else{
            chargesScroll()
            title.innerText = tab.innerText
        }
    }

    /* These event listeners are used to show and hide the filtering form, as well as creating a backup of the data that
       is present in the container at the time the form is showed, to every time we reload the results, the backedUpData
       will be displayed.*/
    if (e.target.classList.contains('fa-filter') && e.target.classList.contains('appointments-filter')){

        let form = document.querySelector('.appointments-form')
        form.classList.contains('show-form') ? form.classList.remove('show-form') : form.classList.add('show-form')
        appointmentsBackUp = document.querySelector('.appointments').innerHTML

    } else if (e.target.classList.contains('fa-filter') && e.target.classList.contains('exams-filter')){

        let form = document.querySelector('.exams-form')
        form.classList.contains('show-form') ? form.classList.remove('show-form') : form.classList.add('show-form')
        examsBackUp = document.querySelector('.exams').innerHTML

    } else if (e.target.classList.contains('fa-filter') && e.target.classList.contains('charges-filter')){

        let form = document.querySelector('.charges-form')
        form.classList.contains('show-form') ? form.classList.remove('show-form') : form.classList.add('show-form')
        chargesBackUp = document.querySelector('.charges').innerHTML

    }

    /* These event listeners are used to reload the backedUpData and display it in the container, the backed up data
       display, will depend on the icon clicked and the classes it contains in it's classlist.*/
    if (e.target.classList.contains('fa-sync-alt') && e.target.classList.contains('appointments-reload')){

        appointments.innerHTML = appointmentsBackUp
        document.querySelector('.appointments-filter').classList.remove('fa-filter-hover')

    } else if (e.target.classList.contains('fa-sync-alt') && e.target.classList.contains('exams-reload')){

        exams.innerHTML = examsBackUp
        document.querySelector('.exams-filter').classList.remove('fa-filter-hover')

    }else if (e.target.classList.contains('fa-sync-alt') && e.target.classList.contains('charges-reload')){

        charges.innerHTML = chargesBackUp
        document.querySelector('.charges-filter').classList.remove('fa-filter-hover')

    }


})

// Body Submit event Listeners

/* All these event listeners will be fired every time a filtering is done to request data from the BackEnd through a query,
   depending on the class the target contains a specific data will be retrieved. This function will collect some data from
   the target as the 'url' which we will retrieve from the action attribute in the target, the 'method' we retrieve from the
   method attribute from the target, the 'type' of data we will retrieve, the 'csrfmiddlewaretoken', data that we collect
   from the hidden input in our form, and lastly our data, we create a new FormData obj with the content inside our form,
   we also set the wrapper variable to the actual container active, and the data received from the backend will be set to
   the container active.*/

body.addEventListener('submit', (e) => {
        e.preventDefault()
        e.stopPropagation()
        let container
    if (e.target.classList.contains('appointments-form')){
        container = document.querySelector('.appointments')
        const url = e.target.action
        const method = e.target.method
        const type = 'appointments'
        const csrfmiddlewaretoken = document.querySelector('.appointments-form > [name=csrfmiddlewaretoken]').value
        const formData = new FormData(e.target)
        filterResultsAW(url, method, type, csrfmiddlewaretoken, formData)
        .then(data => {
            container.innerHTML = data['html']
            document.querySelector('.appointments-form').classList.add('show-form')
        })
    } else if (e.target.classList.contains('exams-form')){
        container = document.querySelector('.exams')
        const url = e.target.action
        const method = e.target.method
        const type = 'exams'
        const csrfmiddlewaretoken = document.querySelector('.exams-form > [name=csrfmiddlewaretoken]').value
        const formData = new FormData(e.target)
        filterResultsAW(url, method, type, csrfmiddlewaretoken, formData)
        .then(data => {
            container.innerHTML = data['html']
            document.querySelector('.exams-form').classList.add('show-form')
        })
    } else{
        container = document.querySelector('.charges')
        const url = e.target.action
        const method = e.target.method
        const type = 'charges'
        const csrfmiddlewaretoken = document.querySelector('.charges-form > [name=csrfmiddlewaretoken]').value
        const formData = new FormData(e.target)
        filterResultsAW(url, method, type, csrfmiddlewaretoken, formData)
        .then(data => {
            container.innerHTML = data['html']
            document.querySelector('.charges-form').classList.add('show-form')
        })
    }
})

// Exams Event Listeners
if (exams){

    // Exams Mouseouver events

    exams.addEventListener('mouseover', (e) => {

        /* This event will be fired every time the target contains the exam-filename class in it's classlist, it will add
           the previewImg element the image-preview-show class to make visible the container where the image will be
           displayed, and we will remove the form if it's shown. Also we will set the src attribute to the data-img-src
           attribute of the target*/

        if (e.target.classList.contains('exam-filename')){
            previewImg.classList.add('image-preview-show')
            image.src = e.target.getAttribute('data-img-src')
            document.querySelector('.exams-form').classList.remove('show-form')
        }
    })

    // Exams mouseout events

    exams.addEventListener('mouseout', (e) => {

        /* This event will be fired every time the target contains the exam-filename class in it's classlist and the
           previewImg element will be hidden by removing the image-preview-show class, also the src attribute from the
           image will be removed.*/

        if (e.target.classList.contains('exam-filename')){
            previewImg.classList.remove('image-preview-show')
            image.src = ''
        }
    })
}

/* This event listener will be fired every time the page is loaded and will set the window scroll 0 to the left. */
window.addEventListener('load', (e) => {
    generalScroll()
})