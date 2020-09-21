//Checked
var download = document.querySelector('.fa-print')

download.addEventListener('mouseover', function(){
    this.classList.add('fa-print-hover')
})

download.addEventListener('mouseout', function(){
    this.classList.remove('fa-print-hover')
})
