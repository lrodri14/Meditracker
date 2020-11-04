//Checked
var download = document.querySelector('.fa-print')
var exams = document.querySelectorAll('.exams a')
var examsModal = document.querySelector('.exam-preview')
var examImg = document.querySelector('#exam-image')

download.addEventListener('mouseover', function(){
    this.classList.add('fa-print-hover')
})

download.addEventListener('mouseout', function(){
    this.classList.remove('fa-print-hover')
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


