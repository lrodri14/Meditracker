var body = document.querySelector('body')
var medicalBook = document.querySelector('.fa-book-medical')
var button = document.querySelectorAll('button')
var diagnose = document.querySelector('.diagnose')
var navigation = document.querySelector('.navigation')
var exams = document.querySelector('.fa-file-medical-alt')
var examsModal = document.querySelector('.exams-modal')
var examsData = document.querySelector('.exams-data')
var previewImg = document.querySelector('.preview-image')
var addForm = document.querySelector('.fa-plus')
var remExam = document.querySelector('.fa-trash')
var prevSlide = document.querySelector('.fa-angle-left')
var nextSlide = document.querySelector('.fa-angle-right')
var controllers = [prevSlide, nextSlide]

navigation.innerHTML = '<li></li>'.repeat(document.querySelectorAll('.diagnose > div').length)
navigation.childNodes[0].classList.add('navigator-active')

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


body.addEventListener('submit', (e) => {

})

medicalBook.addEventListener('mouseover', function(){
    this.classList.add('fa-book-medical-hover')
})

medicalBook.addEventListener('mouseout', function(){
    this.classList.remove('fa-book-medical-hover')
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


if (examsModal){

    examsModal.addEventListener('click', function(e){
        if (e.target.classList.contains('exams-modal') || e.target.innerText === 'Save'){
            this.classList.remove('exams-modal-show')
            if (examsData.classList.contains('exams-data-preview-set') && previewImg.classList.contains('preview-image-display')){
                examsData.classList.remove('exams-data-preview-set')
                previewImg.classList.remove('preview-image-display')
            }
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

        if (e.target.classList.contains('filename') && e.target.innerText !== ''){
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
                imagePreview.classList.add('previewed-image-show')
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