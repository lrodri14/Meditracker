var form = document.querySelector('form')
var formInputs = document.querySelectorAll('input:not([type=checkbox]):not([type=hidden]):not([type=file]):not(#id_name), textarea')
var patientInfo = document.querySelector('#patient-info')
var patientInfoPopUp = document.querySelector('.patient-info-popup')
var medicalBook = document.querySelector('.fa-book-medical')
var button = document.querySelectorAll('button')
var generalInfo = document.querySelector('.general-info')
var lock = document.querySelector('.lock')
var padlock = document.querySelector('.fa-lock')
var lockInput = document.querySelector('#id_lock')
var lockPopUp = document.querySelector('.popup')
var diagnose = document.querySelector('.diagnose')
var navigation = document.querySelector('.navigation')
var exams = document.querySelector('.fa-file-medical-alt')
var examsModal = document.querySelector('.exams-modal')
var examsData = document.querySelector('.exams-data')
var previewImg = document.querySelector('.preview-image')
var image = document.querySelector('.previewed-image')
var addForm = document.querySelector('.add-form')
var remExam = document.querySelector('.fa-trash')
var drugCategoryFilter = document.querySelector('#id_category')
var drugList = document.querySelector('#drugs')
var addDrug = document.querySelector('.add-drug')
var addDrugModal = document.querySelector('.add-drug-modal')
var addDrugModalContent = document.querySelector('.add-drug-modal-content')
var addDrugForm = document.querySelector('.add-drug-modal-content form')
var medicineText = document.querySelector('#id_medicine')
var prevSlide = document.querySelector('.fa-angle-left')
var nextSlide = document.querySelector('.fa-angle-right')
var controllers = [prevSlide, nextSlide]
var modal = document.querySelector('.modal')
var recordsModal = document.querySelector('.records-modal')
var recordsTable = document.querySelector('.records-table')
var recordsSummary = document.querySelector('.records-general-information')
var prescriptionModal = document.querySelector('.prescription-modal')
var prescriptionModalContent = document.querySelector('.prescription-modal-content')

navigation.innerHTML = '<li></li>'.repeat(document.querySelectorAll('.diagnose > div').length)
navigation.childNodes[0].classList.add('navigator-active')

// Async Functions
async function addDrugAsync(url, method, formData, csrfmiddlewaretoken){
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken':csrfmiddlewaretoken}, body:formData})
    const data = await result.json()
    return data
}

async function retrieveDrugsFilterAsync(url){
    const result = await fetch(url)
    const data = await result.json()
    return data
}

async function requestRecords(url){
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function consultSummaryAW(url){
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function submitConsultAW(url, method, csrfmiddlewaretoken, formData){
    const result = await fetch(url, {method: method, headers:{'X-CSRFToken': csrfmiddlewaretoken}, body: formData})
    const data = result.json()
    return data
}
// Functions
function diagnoseScroll(elScrollLeft, elScrollWidth, distance, element, eTarget, navigation){

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

// Asignments
lockInput.value = 'True'


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
                    console.log(data['prescription_path'])
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
            row.style.backgroundColor = '#0ff5fc'
            row.classList.add('tr-hover')
            for (let i = 0; i<row.childNodes.length; i++){
                if (row.childNodes[i].nodeName === 'TD'){
                    row.childNodes[i].classList.add('td-hover')
                }
            }
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
            row.classList.remove('tr-hover')
            for (let i = 0; i<row.childNodes.length; i++){
                if (row.childNodes[i].nodeName === 'TD'){
                    row.childNodes[i].classList.remove('td-hover')
                }
            }

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

