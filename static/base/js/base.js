var loaderModal = document.querySelector('.loader-modal')

if (document.querySelector('.navigator') !== 'undefined' || document.querySelector('.navigator') !== 'null'){
    var bars = document.querySelector('.fa-bars')
    var globalNavigator = document.querySelector('.global-navigator')
}

if (document.querySelector('.social-section') !== 'undefined' && document.querySelector('.social-section') !== 'null'){
    var contacts = document.querySelector('.fa-users')
    var socialSection = document.querySelector('.social-section')
    var socialSectionSearch = document.querySelector('.social-section-search')
    var socialSectionData = document.querySelector('.social-section-data')
    var socialSectionTabs = document.querySelectorAll('.social-section-tab')
    var closeSocialSection = document.querySelector('.close-social-section')
}

async function displayContactsAW(url){
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function displayRequestsAW(url){
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function requestResponseAW(url){
    const result = await fetch(url)
    const data = result.json()
    return data
}

if (bars){

    bars.addEventListener('click', () => {
       globalNavigator.classList.add('global-navigator-show')
    })

}

if (contacts){

    contacts.addEventListener('click', (e) => {
       socialSectionTabs[0].classList.add('social-section-tab-active')
       let url = e.target.getAttribute('data-url') + '?query=' + socialSectionSearch.value
        displayContactsAW(url)
        .then(data => {
            socialSectionData.innerHTML = data['html']
        })
       socialSection.classList.add('social-section-show')
    })

}


if (globalNavigator){

    globalNavigator.addEventListener('mouseover', (e) => {

        if (e.target.classList.contains('global-navigator-tab') || e.target.classList.contains('fas') && !e.target.classList.contains('fa-times')){
            let tab = e.target.classList.contains('global-navigator-tab') ? e.target : e.target.parentNode.parentNode
            tab.classList.add('global-navigator-tab-hover')
        }

    })

    globalNavigator.addEventListener('mouseout', (e) => {

        if (e.target.classList.contains('global-navigator-tab') || e.target.classList.contains('fas') && !e.target.classList.contains('fa-times')){
            let tab = e.target.classList.contains('global-navigator-tab') ? e.target : e.target.parentNode.parentNode
            tab.classList.remove('global-navigator-tab-hover')
        }

    })

    globalNavigator.addEventListener('click', (e) => {

        if (e.target.parentNode.classList.contains('close-global-navigator')){
           globalNavigator.classList.remove('global-navigator-show')
        }

    })

}

if (socialSection){

    socialSection.addEventListener('mouseover', (e) => {

        /*This event will be fired every time a mouseover occurs over a 'TD' or the target contains 'fa-edit'
        class in it's classList, This will make changes inside this row.*/
        if (e.target.nodeName === 'TD' ||  e.target.classList.contains('delete-contact') ||  e.target.classList.contains('accept-contact-request') || e.target.classList.contains('deny-contact-request')){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = '#C7E8F3'
            row.style.color = '#496897'
        }

         if (e.target.classList.contains('social-section-tab')){

            e.target.classList.add('social-section-tab-hover')

         }

        // This event will be fired, every time the user hovers out a fa-trash icon, the fa-trash-hover class will be removed.
        if (e.target.classList.contains('delete-contact')){
            e.target.classList.add('delete-contact-hover')
        }

        // This event will be fired, every time the user hovers out a fa-trash icon, the fa-trash-hover class will be removed.
        if (e.target.classList.contains('accept-contact-request')){
            e.target.classList.add('accept-contact-request-hover')
        }

        // This event will be fired, every time the user hovers out a fa-trash icon, the fa-trash-hover class will be removed.
        if (e.target.classList.contains('deny-contact-request')){
            e.target.classList.add('deny-contact-request-hover')
        }

    })

    socialSection.addEventListener('mouseout', (e) => {

        /*This event will be fired every time a mouse out occurs from a 'TD' or the target contains 'fa-edit'
        class in it's classList, This will make changes inside this row.*/
          if (e.target.nodeName === 'TD' || e.target.classList.contains('delete-contact') ||  e.target.classList.contains('accept-contact-request') || e.target.classList.contains('deny-contact-request')){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = ''
            row.style.color = ''
          }

          if (e.target.classList.contains('social-section-tab')){

            e.target.classList.remove('social-section-tab-hover')

          }

        // This event will be fired, every time the user hovers outa fa-trash icon, the fa-trash-hover class will be removed.
        if (e.target.classList.contains('delete-contact')){
            e.target.classList.remove('delete-contact-hover')
        }

        // This event will be fired, every time the user hovers out a fa-trash icon, the fa-trash-hover class will be removed.
        if (e.target.classList.contains('accept-contact-request')){
            e.target.classList.remove('accept-contact-request-hover')
        }

        // This event will be fired, every time the user hovers out a fa-trash icon, the fa-trash-hover class will be removed.
        if (e.target.classList.contains('deny-contact-request')){
            e.target.classList.remove('deny-contact-request-hover')
        }


    })

    socialSection.addEventListener('click', (e) => {

        if (e.target.classList.contains('close-social-section')){
            socialSection.classList.remove('social-section-show')
            for (let i = 0; i<socialSectionTabs.length; i++){
                socialSectionTabs[i].classList.remove('social-section-tab-active')
            }
       }

        if (e.target.classList.contains('social-section-tab')){

            for (let i = 0; i<socialSectionTabs.length; i++){
                socialSectionTabs[i].classList.remove('social-section-tab-active')
            }
            e.target.classList.add('social-section-tab-active')
            let url = e.target.getAttribute('data-url') + '?query=' + socialSectionSearch.value
            displayContactsAW(url)
            .then(data => {
                socialSectionData.innerHTML = data['html']
            })
        }

        if (e.target.classList.contains('fa-check') || e.target.classList.contains('fa-times') && !e.target.classList.contains('close-social-section')){
            let url = e.target.getAttribute('data-url') + '?response=' + e.target.getAttribute('data-response')
            requestResponseAW(url)
            .then(data => {
                socialSectionData.innerHTML = data['html']
            })
        }

    })
}


window.addEventListener('DOMContentLoaded', () => {
    loaderModal.classList.add('loader-modal-hide')
})
