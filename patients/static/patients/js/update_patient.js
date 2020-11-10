//Checked
var form = document.querySelector('form')
var allergiesTotalForms = document.querySelector('.allergies_management_form > #id_allergies-TOTAL_FORMS')
var antecedentsTotalForms = document.querySelector('.antecedents_management_form > #id_antecedents-TOTAL_FORMS')
var generalInfoInputs = document.querySelectorAll('.general-info input, .general-info select')
var inputs = document.querySelectorAll('input')
var button = document.querySelectorAll('button')
var extraInfo = document.querySelector('.extra-info')
var allergySelection
var insuranceSelection = document.querySelector('.insurance-form select')
var allergiesFormBlueprint = document.querySelectorAll('.allergies-form .form-container')[document.querySelectorAll('.allergies-form .form-container').length - 1].cloneNode(true)
var antecedentsFormBlueprint = document.querySelectorAll('.antecedents-form .form-container')[document.querySelectorAll('.antecedents-form .form-container').length - 1].cloneNode(true)
var allergiesFormsContainer = document.querySelector('.allergies-form tbody')
var antecedentsFormsContainer = document.querySelector('.antecedents-form tbody')
var modal = document.querySelector('.modal')
var modalContent = document.querySelector('.modal-content')
var saveConfirmationModal = document.querySelector('.save-confirmation-modal')
// Async Functions

async function elementAdditionFormAsync(url){
    const result = await fetch(url)
    const data = await result.json()
    return data
}

async function addElementAsync(url, method, csrfmiddlewaretoken, formData){
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken':csrfmiddlewaretoken}, body:formData})
    const data = await result.json()
    return data
}

form.addEventListener('submit', (e) => {
    e.preventDefault()
    e.stopPropagation()
    unfilledInputs = 0
    for (let i = 0; i<generalInfoInputs.length; i++){
        if (generalInfoInputs[i].value !== ''){
            continue
        }else{
            unfilledInputs++
        }
    }
    unfilledInputs === 0 ? form.submit() : saveConfirmationModal.classList.add('save-confirmation-modal-show')
})


// Button
for (let i = 0; i<button.length; i++){
    button[i].addEventListener('mouseover', function(){
        this.classList.add('button-hover')
    })

    button[i].addEventListener('mouseout', function(){
        this.classList.remove('button-hover')
    })
}


// Inputs
for (var i = 0; i<inputs.length; i++){
    inputs[i].addEventListener('mouseover', function(){
        this.classList.add('input-hover')
    })

    inputs[i].addEventListener('mouseout', function(){
        this.classList.remove('input-hover')
    })
}


if (extraInfo){
    extraInfo.addEventListener('mouseover', (e) =>{
        if (e.target.classList.contains('fa-plus')){
            e.target.classList.add('fa-plus-hover')
        }

        if (e.target.classList.contains('fa-trash')){
            e.target.classList.add('fa-trash-hover')
        }
    })

    extraInfo.addEventListener('mouseout', (e) =>{
        if (e.target.classList.contains('fa-plus')){
            e.target.classList.remove('fa-plus-hover')
        }

        if (e.target.classList.contains('fa-trash')){
            e.target.classList.remove('fa-trash-hover')
        }
    })

    extraInfo.addEventListener('click', (e) =>{
        if (e.target.classList.contains('add-allergy')){
            const url = e.target.getAttribute('data-url')
            allergySelection = e.target.parentNode.firstChild
            elementAdditionFormAsync(url)
            .then(data => {
                modal.classList.add('modal-show')
                modalContent.innerHTML = data['html']
            })
        }

        if (e.target.classList.contains('add-insurance')){
            const url = e.target.getAttribute('data-url')
            elementAdditionFormAsync(url)
            .then(data => {
                modal.classList.add('modal-show')
                modalContent.innerHTML = data['html']
            })
        }

        if (e.target.classList.contains('add-allergy-form')){
            let formAmount = document.querySelectorAll('.allergies-form .form-container')
            let allergyTotalForms = document.querySelector('.allergies_management_form #id_allergies-TOTAL_FORMS')
            let clonedNode = allergiesFormBlueprint.cloneNode(true)
            for (let i = 0; i<clonedNode.childNodes.length; i++){
                if (clonedNode.childNodes[i].firstChild){
                    if (clonedNode.childNodes[i].childNodes[0].nodeName === 'SELECT'){
                        clonedNode.childNodes[i].childNodes[0].name = 'form-' + formAmount.length + '-allergy_type'
                        clonedNode.childNodes[i].childNodes[0].id = 'id_form-' + formAmount.length + '-allergy_type'
                    }else if (clonedNode.childNodes[i].childNodes[0].nodeName === 'TEXTAREA'){
                        clonedNode.childNodes[i].childNodes[0].name = 'form-' + formAmount.length + '-about'
                        clonedNode.childNodes[i].childNodes[0].id = 'id_form-' + formAmount.length + '-about'
                    }else if (clonedNode.childNodes[i].childNodes[0].nodeName === 'INPUT' && clonedNode.childNodes[i].childNodes[0].type === 'checkbox'){
                        clonedNode.childNodes[i].childNodes[0].name = 'form-' + formAmount.length + '-DELETE'
                        clonedNode.childNodes[i].childNodes[0].id = 'id_form-' + formAmount.length + '-DELETE'
                    }
                }
            }
            allergyTotalForms.value = formAmount.length + 1
            allergiesFormsContainer.appendChild(clonedNode)
        }

        if (e.target.classList.contains('delete-allergy-form')){
            let formContainer = e.target.parentNode.parentNode
            for (let i = 0; i<formContainer.childNodes.length; i++){
                if (formContainer.childNodes[i].firstChild){
                    if (formContainer.childNodes[i].firstChild.type === 'checkbox'){
                        formContainer.childNodes[i].firstChild.checked = true
                    }
                }
            }
            formContainer.classList.add('form-hide')
        }

        if (e.target.classList.contains('add-antecedent-form')){
            let formAmount = document.querySelectorAll('.antecedents-form .form-container')
            let antecedentsTotalForms = document.querySelector('.antecedents_management_form #id_antecedents-TOTAL_FORMS')
            let clonedNode = antecedentsFormBlueprint.cloneNode(true)
            for (let i = 0; i<clonedNode.childNodes.length; i++){
                if (clonedNode.childNodes[i].firstChild){
                    if (clonedNode.childNodes[i].childNodes[0].nodeName === 'INPUT' && clonedNode.childNodes[i].childNodes[0].type === 'text'){
                        clonedNode.childNodes[i].childNodes[0].name = 'form-' + formAmount.length + '-antecedent'
                        clonedNode.childNodes[i].childNodes[0].id = 'id_form-' + formAmount.length + '-antecedent'
                    }else if (clonedNode.childNodes[i].childNodes[0].nodeName === 'TEXTAREA'){
                        clonedNode.childNodes[i].childNodes[0].name = 'form-' + formAmount.length + '-info'
                        clonedNode.childNodes[i].childNodes[0].id = 'id_form-' + formAmount.length + '-info'
                    }else if (clonedNode.childNodes[i].childNodes[0].nodeName === 'INPUT' && clonedNode.childNodes[i].childNodes[0].type === 'checkbox'){
                        clonedNode.childNodes[i].childNodes[0].name = 'form-' + formAmount.length + '-DELETE'
                        clonedNode.childNodes[i].childNodes[0].id = 'id_form-' + formAmount.length + '-DELETE'
                    }
                }
            }
            antecedentsTotalForms.value = formAmount.length + 1
            antecedentsFormsContainer.appendChild(clonedNode)
        }

        if (e.target.classList.contains('delete-antecedent-form')){
            let formContainer = e.target.parentNode.parentNode
            for (let i = 0; i<formContainer.childNodes.length; i++){
                if (formContainer.childNodes[i].firstChild){
                    if (formContainer.childNodes[i].firstChild.type === 'checkbox'){
                        formContainer.childNodes[i].firstChild.checked = true
                    }
                }
            }
            formContainer.classList.add('form-hide')
        }

    })
}


if (modal){
    modal.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')){
            e.target.classList.remove('modal-show')
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
        e.preventDefault()
        e.stopPropagation()
        const form = e.target
        const url = form.action
        const method = form.method
        const csrfmiddlewaretoken = e.target.childNodes[0].value
        const formData = new FormData(form)
        if (e.target.id = 'add-allergy'){
            addElementAsync(url, method, csrfmiddlewaretoken, formData)
            .then(data => {
                if (data['html']){
                    modalContent.innerHTML = data['html']
                }else{
                    allergySelection.innerHTML = data['updated_selections']
                    modal.classList.remove('modal-show')
                }
            })
        }else{
            addElementAsync(url, method, csrfmiddlewaretoken, formData)
            .then(data => {
                if (data['html']){
                    modalContent.innerHTML = data['html']
                }else{
                    for (let i = 0; i<insuranceSelection.length; i++){
                        insuranceSelection[i].innerHTML = data['updated_selections']
                    }
                    modal.classList.remove('modal-show')
                }
            })
        }
    })
}

// Confirmation Modal

if (saveConfirmationModal){
    saveConfirmationModal.addEventListener('click', (e) => {
        if (e.target === saveConfirmationModal || (e.target.nodeName === 'BUTTON' && e.target.textContent === 'No')){
            saveConfirmationModal.classList.remove('save-confirmation-modal-show')
        }

        if (e.target.nodeName === 'BUTTON' && e.target.textContent === 'Yes'){
            form.submit()
        }
    })
}