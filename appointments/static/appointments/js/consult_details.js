//Checked
var download = document.querySelector('.fa-print')
var prescriptionModal = document.querySelector('.prescription-modal')
var prescriptionModalContent = document.querySelector('.prescription-modal-content')
var exams = document.querySelectorAll('.exams a')
var examsModal = document.querySelector('.exam-preview')
var examImg = document.querySelector('#exam-image')

download.addEventListener('mouseover', function(){
    this.classList.add('fa-print-hover')
})

download.addEventListener('mouseout', function(){
    this.classList.remove('fa-print-hover')
})

download.addEventListener('click', (e) => {
    let pdfPath = e.target.getAttribute('data-pdf')
    prescriptionModal.classList.add('prescription-modal-show')
    PDFObject.embed(pdfPath, prescriptionModalContent)
})

prescriptionModal.addEventListener('click', (e) => {
    if (e.target === prescriptionModal){
        prescriptionModal.classList.remove('prescription-modal-show')
    }
})

for (let i = 0; i<exams.length; i++){

    exams[i].addEventListener('click', (e) =>{
        e.preventDefault()
        e.stopPropagation()
    })

    exams[i].addEventListener('mouseover', () => {
        examsModal.classList.add('exam-preview-show')
        examImg.src = exams[i].href
    })

    exams[i].addEventListener('mouseout', () => {
        examsModal.classList.remove('exam-preview-show')
    })

}


