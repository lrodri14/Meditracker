//Checked
var download = document.querySelector('.fa-download')

download.addEventListener('mouseover', function(){
    this.classList.add('fa-download-hover')
})

download.addEventListener('mouseout', function(){
    this.classList.remove('fa-download-hover')
})
