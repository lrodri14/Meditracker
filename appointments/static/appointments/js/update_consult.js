/* This update_consult.js file contains all the variables definitions, async and sync functions, assignments,
as well as event listeners need for the Consult Update View to work properly in the Appointments App, this file is
composed of 5 async functions, and 1 sync function.*/

/*#################################################### Variables #####################################################*/

// General

var form = document.querySelector('form')
var formInputs = document.querySelectorAll('input:not([type=checkbox]):not([type=hidden]):not([type=file]):not(#id_name), textarea')
var button = document.querySelectorAll('button')
var navigation = document.querySelector('.navigation')
var prevSlide = document.querySelector('.fa-angle-left')
var nextSlide = document.querySelector('.fa-angle-right')
var controllers = [prevSlide, nextSlide]

// Consult Information

var generalInfo = document.querySelector('.general-info')
var patientInfo = document.querySelector('#patient-info')
var patientInfoPopUp = document.querySelector('.patient-info-popup')
var exams = document.querySelector('.fa-file-medical-alt')
var medicalBook = document.querySelector('.fa-book-medical')
var padlock = document.querySelector('.fa-lock')
var lock = document.querySelector('.lock')
var lockInput = document.querySelector('#id_lock')
var lockPopUp = document.querySelector('.popup')

// Diagnose

var diagnose = document.querySelector('.diagnose')
var medicineText = document.querySelector('#id_indications')
var actions = document.querySelector('#id_actions')

// Exams

var examsModal = document.querySelector('.exams-modal')
var examsData = document.querySelector('.exams-data')
var previewImg = document.querySelector('.preview-image')
var image = document.querySelector('.previewed-image')
var addForm = document.querySelector('.add-form')
var remExam = document.querySelector('.fa-trash')

// Drugs

var drugCategoryFilter = document.querySelector('#id_category')
var drugList = document.querySelector('#drugs')
var addDrug = document.querySelector('.add-drug')
var addDrugModal = document.querySelector('.add-drug-modal')
var addDrugModalContent = document.querySelector('.add-drug-modal-content')
var addDrugForm = document.querySelector('.add-drug-modal-content form')

// Modals

var modal = document.querySelector('.modal')
var recordsModal = document.querySelector('.records-modal')
var recordsTable = document.querySelector('.records-table')
var recordsSummary = document.querySelector('.records-general-information')
var prescriptionModal = document.querySelector('.prescription-modal')
var prescriptionModalContent = document.querySelector('.prescription-modal-content')

// Navigator
navigation.innerHTML = '<li></li>'.repeat(document.querySelectorAll('.diagnose > div').length)
navigation.childNodes[0].classList.add('navigator-active')

/*#################################################### Functions #####################################################*/

// Async Functions

async function addDrugAsync(url, method, formData, csrfmiddlewaretoken){
    /*This addDrugAsync function is used to drugs asynchronously to the server, this function takes 4 paramaters we collect
    from the form that fires the submit event, we need to collect the 'url' to where we make our POST request, we also
    need to collect 'method' from the form.method attribute and 'csrfmiddlewaretoken' from the form's hidden input, finally
    we collect the formData from the form and send it in our request, the response will be converted to JSON Format and
    returned for further processing.*/
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken':csrfmiddlewaretoken}, body:formData})
    const data = await result.json()
    return data
}

async function retrieveDrugsFilterAsync(url){
    /* This retrieveDrugsFilterAsync function is used to filter the drugs options in the drugs select element, this
    function only takes one argument, the url containing the parameters for the GET request, the response will be
    converted into JSON Format and finally, displayed in the select box. It takes a single argument, the 'url' to make
    the GET request.*/
    const result = await fetch(url)
    const data = await result.json()
    return data
}

async function requestRecords(url){
    /* This requestRecords function is used to display the records filled of this current patient, this data will be
     displayed in the records modal as a table, the response will be converted into JSON Format and finally, displayed
     in the modal. It takes a single argument, the 'url' to make the GET request.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function consultSummaryAW(url){
    /* This consultSummaryAW function is used to display a summary of the most important things from a consult in the
        consult summary section, This function only takes one single argument, the 'url' with the primary key of that
        consult.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function submitConsultAW(url, method, csrfmiddlewaretoken, formData){
    /* This submitConsultAW function is used to submit the consult to the server, once the consult has been sent to the
    server, if the response contains a prescription, then the prescription modal will be displayed containing the prescription
    in PDF Format, if not, the user will be redirected to the consults main page, (This is not part of the async func
    functionality but it makes part of this process), The function takes 4 arguments, the 'url' to make the POST request,
    the 'method' which we collect from the form.method attribute, the 'csrfmiddlewaretoken' we collect from the forms hidden
    input and finally the formData we collect from the form and create a new FormData object, the response is converted into
    JSON Format for future use.*/
    const result = await fetch(url, {method: method, headers:{'X-CSRFToken': csrfmiddlewaretoken}, body: formData})
    const data = result.json()
    return data
}

// Functions

function diagnoseScroll(elScrollLeft, elScrollWidth, distance, element, eTarget, navigation){

    /* The diagnoseScroll function is used to scroll the diagnose section and activating a navigator dot based on the
       scroll distance of that element. This function takes 6 arguments, 'elScrollLeft' which is the distance that
       exists from the left which is 0 to the current position scrolled of that element, 'elScrollWidth' expects
       the whole width of that element, in this case the '.diagnose' element, 'distance' is the distance that the element
       will be scrolled, 'element' is the element that will be scrolled, in all the cases of this file, it will be the
       '.diagnose' element, 'eTarget' is the controller that was clicked either a 'fa-angle-left' or 'fa-angle-right'
       element, and based on the element clicked is the direction in which the section will be scrolled, 'navigation'
       is the set of navigator dots in the navigator section. Now with all this data, the function will decide where to
       scroll based on the arrow that was clicked, making use of the scrollTo function.*/

    let activeElement = Math.round((elScrollLeft / distance))

    if (eTarget.classList.contains('fa-angle-left') && elScrollLeft !== 0){
        element.scrollTo({
            left: elScrollLeft - distance,
            behavior: 'smooth'
        })
    }

    if (eTarget.classList.contains('fa-angle-right') && elScrollLeft !== elScrollWidth){
        element.scrollTo({
            left: elScrollLeft + distance,
            behavior: 'smooth'
        })
    }
}

/*#################################################### Assignments ###################################################*/


// Asignments

// This assignment is made to ensure that every time a consult is opened, it is locked, no matter if it was left opened in the last opening.

lockInput.value = 'True'


/*#################################################### Event Listeners ###############################################*/

//Wrapper
if (form){
    form.addEventListener('submit', (e) => {
        e.preventDefault()
        e.stopPropagation()
        let unfilledInputs = 0
        for (let i = 0; i<formInputs.length; i++){
            if (formInputs[i].value !== ''){
                continue
            }else{
                unfilledInputs++
            }
        }

        if (unfilledInputs === 0){
            let url = e.target.action
            let method = e.target.method
            let csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            let formData = new FormData(e.target)
            submitConsultAW(url, method, csrfmiddlewaretoken, formData)
            .then(data => {
                if (data['prescription_path']){
                    prescriptionModalContent.setAttribute('data-pdf', data['prescription_path'])
                    pdfPath = prescriptionModalContent.getAttribute('data-pdf')
                    PDFObject.embed(pdfPath, prescriptionModalContent)
                    prescriptionModal.classList.add('prescription-modal-show')
                }
            })
        } else{
            modal.classList.add('modal-show')
        }
    })
}

if (patientInfo){
    patientInfo.addEventListener('mouseover', () => {
        patientInfoPopUp.classList.add('popup-show')
    })

    patientInfo.addEventListener('mouseout', () => {
        patientInfoPopUp.classList.remove('popup-show')
    })
}


medicalBook.addEventListener('mouseover', function(){
    this.classList.add('fa-book-medical-hover')
})

medicalBook.addEventListener('mouseout', function(){
    this.classList.remove('fa-book-medical-hover')
})

medicalBook.addEventListener('click', () => {
    let url = medicalBook.getAttribute('data-url')
    requestRecords(url)
    .then(data => {
        recordsTable.innerHTML = data['html']
        if (document.querySelector('#no-records')){
            recordsSummary.classList.add('records-general-information-hide')
        }
    })
    recordsModal.classList.add('records-modal-show')
})

for (let i = 0; i<button.length; i++){
    button[i].addEventListener('mouseover', function(){
        this.classList.add('button-hover')
    })

    button[i].addEventListener('mouseout', function(){
        this.classList.remove('button-hover')
    })
}

exams.addEventListener('mouseover', function(){
    this.classList.add('fa-file-medical-alt-hover')
})

exams.addEventListener('mouseout', function(){
    this.classList.remove('fa-file-medical-alt-hover')
})

exams.addEventListener('click', function(){
    examsModal.classList.add('exams-modal-show')
})

if (recordsTable){
    recordsTable.addEventListener('mouseover', (e) => {
        if (e.target.nodeName === 'TD'){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = '#C7E8F3'
            row.style.color = '#496897'

        let url = row.getAttribute('data-url')
        consultSummaryAW(url)
        .then(data => {
            recordsSummary.innerHTML = data['html']
        })
        }
    })

    recordsTable.addEventListener('mouseout', (e) => {

          if (e.target.nodeName === 'TD'){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = ''
            row.style.color = ''

          }

    })
}

lock.addEventListener('click', (e) => {

    if (e.target.classList.contains('lock') || e.target.classList.contains('lock-switch')){
        lock.classList.contains('lock-active') ? lock.classList.remove('lock-active') : lock.classList.add('lock-active')
        lockInput.value === 'True' ? lockInput.value = 'False' : lockInput.value = 'True'
        if (padlock.classList.contains('fa-lock')){
            padlock.classList.remove('fa-lock')
            padlock.classList.add('fa-unlock')
        }else{
            padlock.classList.remove('fa-unlock')
            padlock.classList.add('fa-lock')
        }
    }

})

lock.addEventListener('mouseover', () => {
    lockPopUp.classList.add('popup-show')
})

lock.addEventListener('mouseout', () => {
    lockPopUp.classList.remove('popup-show')
})

if (examsModal){

    examsModal.addEventListener('click', function(e){
        if (e.target.classList.contains('exams-modal') || e.target.innerText === 'Save'){
            this.classList.remove('exams-modal-show')
        }

        if (e.target.classList.contains('fa-trash')){
            let parentNode = e.target.parentNode.parentNode
            for (let i = 0; i<parentNode.childNodes.length; i++){
                if (parentNode.childNodes[i].firstChild){
                    if (parentNode.childNodes[i].firstChild.type === 'checkbox'){
                        parentNode.childNodes[i].firstChild.checked = true
                    }
                }
            }
            parentNode.classList.add('form-hide')
        }

        if (e.target.classList.contains('fa-eye')){
            examsData.classList.contains('exams-data-preview-set') ? examsData.classList.remove('exams-data-preview-set') : examsData.classList.add('exams-data-preview-set')
            previewImg.classList.contains('preview-image-display') ? previewImg.classList.remove('preview-image-display') : previewImg.classList.add('preview-image-display')
        }

    })

    examsModal.addEventListener('change', function(e){

        if (e.target.nodeName === 'INPUT' && e.target.type === 'file'){
            var parent = e.target.parentNode.parentNode
            var filenameSpace
            for (let i = 0; i<parent.childNodes.length; i++){
                if (parent.childNodes[i].classList){
                    if (parent.childNodes[i].classList.contains('filename')){
                        filenameSpace = parent.childNodes[i]
                    }
                }
            }
            filenameSpace.innerText = e.target.files[0]['name']
        }

    })

    examsModal.addEventListener('mouseover', function(e){

        if (e.target.classList.contains('add-exam')){
            e.target.classList.add('add-exam-hover')
        }

        if (e.target.classList.contains('fa-plus')){
            e.target.classList.add('fa-plus-hover')
        }

        if (e.target.classList.contains('fa-trash')){
            e.target.classList.add('fa-trash-hover')
        }

        if (e.target.classList.contains('fa-eye')){
            e.target.classList.add('fa-eye-hover')
        }

        if (e.target.classList.contains('filename') && e.target.innerText !== '' && examsModal.classList.contains('exams-modal-show')){
            let imagePreview = document.querySelector('.previewed-image')
            let file
            for (let i = 0; i<e.target.parentNode.childNodes.length; i++){
                if (e.target.parentNode.childNodes[i].firstChild && e.target.parentNode.childNodes[i].firstChild.type === 'file'){
                    file = e.target.parentNode.childNodes[i].firstChild.files[0]
                }
            }
            let reader = new FileReader()
            reader.addEventListener('load', (e) => {
                imagePreview.src = e.target.result
                if (imagePreview.parentNode.classList.contains('preview-image-display')){
                    imagePreview.classList.add('previewed-image-show')
                }
            })
            reader.readAsDataURL(file);
        }

    })

    examsModal.addEventListener('mouseout', function(e){
        if (e.target.classList.contains('add-exam')){
            e.target.classList.remove('add-exam-hover')
        }

        if (e.target.classList.contains('fa-plus')){
            e.target.classList.remove('fa-plus-hover')
        }

        if (e.target.classList.contains('fa-trash')){
            e.target.classList.remove('fa-trash-hover')
        }

        if (e.target.classList.contains('fa-eye')){
            e.target.classList.remove('fa-eye-hover')
        }

         if (e.target.classList.contains('filename') && e.target.innerText !== ''){
            let imagePreview = document.querySelector('.previewed-image')
            imagePreview.classList.remove('previewed-image-show')
            imagePreview.src = ''
        }
    })

}

addForm.addEventListener('click', function(){
    let formAmount = document.querySelectorAll('.form-container')
    let totalAmountFormManagement = document.querySelector('#id_form-TOTAL_FORMS')
    let clonedForm = formAmount[0].cloneNode(true)
    let formContainers = document.querySelector('tbody')
    for (let i = 0; i<clonedForm.childNodes.length; i++){
        if (clonedForm.childNodes[i].firstChild){
            if (clonedForm.childNodes[i].firstChild.nodeName === 'INPUT' && clonedForm.childNodes[i].firstChild.type === 'file'){
                clonedForm.childNodes[i].childNodes[0].value = null
                clonedForm.childNodes[i].childNodes[1].htmlFor = 'id_form-' + formAmount.length + '-image'
                clonedForm.childNodes[i].childNodes[0].name = 'form-' + formAmount.length + '-image'
                clonedForm.childNodes[i].childNodes[0].id = 'id_form-' + formAmount.length + '-image'
            }else if (clonedForm.childNodes[i].firstChild.nodeName === 'INPUT' && clonedForm.childNodes[i].firstChild.type === 'checkbox'){
                clonedForm.childNodes[i].childNodes[0].name = 'form-' + formAmount.length + '-DELETE'
                clonedForm.childNodes[i].childNodes[0].id = 'id_form-' + formAmount.length + '-DELETE'
            }else if (clonedForm.childNodes[i].firstChild.nodeName === 'SELECT'){
                clonedForm.childNodes[i].childNodes[0].value = null
                clonedForm.childNodes[i].childNodes[0].name = 'form-' + formAmount.length + '-type'
                clonedForm.childNodes[i].childNodes[0].id = 'id_form-' + formAmount.length + '-type'
            }
        }

        if (clonedForm.childNodes[i].classList){
            if (clonedForm.childNodes[i].classList.contains('filename')){
                clonedForm.childNodes[i].innerText = ''
            }
        }

    }
    totalAmountFormManagement.value = formAmount.length + 1
    clonedForm.classList.remove('form-hide')
    formContainers.appendChild(clonedForm)
})


for (let i = 0; i<controllers.length; i++){

    controllers[i].addEventListener('mouseover', function(){
        this.classList.add('angle-active')
    })

    controllers[i].addEventListener('mouseout', function(){
        this.classList.remove('angle-active')
    })

    controllers[i].addEventListener('click', function(e){
        diagnoseScroll(diagnose.scrollLeft, diagnose.scrollWidth, diagnose.scrollWidth/navigation.childNodes.length, diagnose, e.target, navigation)
    })

}

diagnose.addEventListener('scroll', function(){

    let navigationDots = navigation.childNodes
    let distance = diagnose.scrollWidth/navigationDots.length
    let activeElement = Math.round(diagnose.scrollLeft/distance)
    for (let i = 0; i<navigationDots.length; i++){
        if (navigationDots[i] !== navigationDots[activeElement]){
            navigationDots[i].classList.remove('navigator-active')
        }
        navigationDots[activeElement].classList.add('navigator-active')
    }

})

// Check for a better way to improve this code.
// Better way to take control of the already checked checkboxes
let drugsPrescribed = []
let checkedDrugs = []
drugList.addEventListener('change', function(e){

    medicineText.value = ''
    let drugPrescribed = e.target.parentNode.innerText
    if (drugsPrescribed.indexOf(drugPrescribed + ' -') === -1){
        drugsPrescribed.push(drugPrescribed + ' -')
        checkedDrugs.push(e.target)
    }else{
        drugsPrescribed.splice(drugsPrescribed.indexOf(drugPrescribed + ' -'), 1)
        checkedDrugs.splice(checkedDrugs.indexOf(e.target), 1)
    }
    for (let i = 0; i<drugsPrescribed.length; i++){
        if (medicineText.value.split('\n').indexOf(drugsPrescribed[i]) === -1){
            medicineText.value += drugsPrescribed[i] + '\n'
        }
    }

})

drugCategoryFilter.addEventListener('change', function(e){
    const data = e.target.options[e.target.selectedIndex].value
    const url = e.target.parentNode.getAttribute('data-url') + '?category=' + data
    retrieveDrugsFilterAsync(url)
    .then(data => {
        document.querySelector('#id_drugs').innerHTML = data['updated_drugs']
        // Better way to take control of the already checked checkboxes
        let checkboxes = document.querySelectorAll('input[type=checkbox]')
        for (let i = 0; i<checkedDrugs.length; i++){
            let checkedDrug = checkedDrugs[i]
            for (let j = 0; j<checkboxes.length; j++){
                if (checkedDrug.value === checkboxes[j].value){
                    checkboxes[j].checked = true
                }
            }
        }
    })
})

if (addDrug){

    addDrug.addEventListener('mouseover', function(e){
        this.classList.add('add-drug-hover')
    })

    addDrug.addEventListener('mouseout', function(e){
        this.classList.remove('add-drug-hover')
    })

    addDrug.addEventListener('click', function(e){
        addDrugModal.classList.add('modal-show')
    })

}

if (addDrugModal){

    addDrugModal.addEventListener('click', function(e){
        if (e.target.classList.contains('add-drug-modal')){
            document.querySelector('#error').innerText = ''
            addDrugForm.reset()
            this.classList.remove('modal-show')
        }
    })

    addDrugModal.addEventListener('mouseover', function(e){
        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.add('button-hover')
        }
    })

    addDrugModal.addEventListener('mouseout', function(e){
        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.remove('button-hover')
        }
    })

    addDrugModal.addEventListener('submit', function(e){
        e.preventDefault()
        e.stopPropagation()
        const url = addDrugForm.action
        const method = addDrugForm.method
        const data = new FormData(addDrugForm)
        const csrfmiddlewaretoken = document.querySelector('.add-drug-form > [name=csrfmiddlewaretoken]').value
        addDrugAsync(url, method, data, csrfmiddlewaretoken)
        .then(data => {
            if (data['html']){
                const error = document.querySelector('#error')
                error.innerText = 'This drug is already listed.'
            }else{
                addDrugModal.classList.remove('modal-show')
                document.querySelector('#error').innerText = ''
                addDrugForm.reset()
                document.querySelector('#id_drugs').innerHTML = data['updated_drugs_list']
                // Better way to take control of the already checked checkboxes
                let checkboxes = document.querySelectorAll('input[type=checkbox]')
                for (let i = 0; i<checkedDrugs.length; i++){
                    let checkedDrug = checkedDrugs[i]
                    for (let j = 0; j<checkboxes.length; j++){
                        if (checkedDrug.value === checkboxes[j].value){
                            checkboxes[j].checked = true
                        }
                    }
                }
            }
        })
    })

}

// Modal
if (modal){
    modal.addEventListener('click', (e) => {
        if (e.target === modal || (e.target.nodeName === 'BUTTON' && e.target.textContent === 'No')){
            modal.classList.remove('modal-show')
        }

        if (e.target.nodeName === 'BUTTON' && e.target.textContent === 'Yes'){
            let url = form.action
            let method = form.method
            let csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            let formData = new FormData(form)
            if (medicineText.value || actions.value){
                submitConsultAW(url, method, csrfmiddlewaretoken, formData)
                .then(data => {
                    if (data['prescription_path']){
                        prescriptionModalContent.setAttribute('data-pdf', data['prescription_path'])
                        pdfPath = prescriptionModalContent.getAttribute('data-pdf')
                        PDFObject.embed(pdfPath, prescriptionModalContent)
                        prescriptionModal.classList.add('prescription-modal-show')
                        modal.classList.remove('modal-show')
                    }
                })
            }else{
                form.submit()
            }
    }
   })
}


if (recordsModal){
    recordsModal.addEventListener('click', (e) => {
        if (e.target === recordsModal){
            recordsModal.classList.remove('records-modal-show')
        }
    })
}

prescriptionModal.addEventListener('click', (e) => {
    if (e.target.textContent === 'Save Consult'){
        window.location.href = e.target.getAttribute('data-url')
    }
})

