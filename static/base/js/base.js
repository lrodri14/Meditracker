var loaderModal = document.querySelector('.loader-modal')

if (document.querySelector('.fa-bars') !== 'null' && document.querySelector('.fa-bars') !== 'undefined'){
    var bars = document.querySelector('.fa-bars')
    var menu = document.querySelector('.menu')
    var close = document.querySelector('.close')
}

if (bars){

    bars.addEventListener('click', () => {
        bars.classList.add('fa-bars-hide')
        menu.classList.add('menu-show')
    })

    close.addEventListener('click', () => {
        bars.classList.remove('fa-bars-hide')
        menu.classList.remove('menu-show')
    })

}

window.addEventListener('DOMContentLoaded', () => {
    loaderModal.classList.add('loader-modal-hide')
})
