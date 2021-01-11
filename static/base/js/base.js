var loaderModal = document.querySelector('.loader-modal')

if (document.querySelector('.fa-bars') !== 'null' && document.querySelector('.fa-bars') !== 'undefined'){
    var bars = document.querySelector('.fa-bars')
    var closeNavigator = document.querySelector('#close-navigator')
}

if (document.querySelector('.fa-users') !== 'null' && document.querySelector('.fa-users') !== 'undefined'){
    var contacts = document.querySelector('.fa-users')
    var socialContent = document.querySelector('.social-content')
    var socialContentTabs = document.querySelectorAll('.social-content-tab')
    var closeSocialContent = document.querySelector('#close-social-content')
}

if (bars){

    bars.addEventListener('click', () => {
        document.querySelector('.navigator').classList.add('navigator-show')
    })

    closeNavigator.addEventListener('click', () => {
        document.querySelector('.navigator').classList.remove('navigator-show')
    })

}

if (contacts){

    contacts.addEventListener('click', (e) => {
        socialContent.classList.add('social-content-show')
    })

    closeSocialContent.addEventListener('click', (e) => {
        socialContent.classList.remove('social-content-show')
    })

}

if (socialContentTabs){

    for (let i = 0; i<socialContentTabs.length; i++){

        socialContentTabs[i].addEventListener('mouseover', (e) => {
            socialContentTabs[i].classList.add('social-content-tab-hover')
        })

        socialContentTabs[i].addEventListener('mouseout', (e) => {
            socialContentTabs[i].classList.remove('social-content-tab-hover')
        })

        socialContentTabs[i].addEventListener('click', (e) => {
            for (let i = 0; i<socialContentTabs.length; i++){
                socialContentTabs[i].classList.remove('social-content-tab-active')
            }
            e.target.classList.add('social-content-tab-active')
        })

    }

}

window.addEventListener('DOMContentLoaded', () => {
    loaderModal.classList.add('loader-modal-hide')
})
