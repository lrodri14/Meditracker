//Checked
function generalScroll(){
    window.scrollTo({
        left: 0,
        behavior: 'smooth'
    })
}

function backgroundScroll(){
    window.scrollTo({
        left: window.screen.availWidth,
        behavior: 'smooth'
    })
}

function appointmentsScroll(){
    window.scrollTo({
        left: window.screen.availWidth * 2,
        behavior: 'smooth'
    })
}

function examsScroll(){
    window.scrollTo({
        left: window.screen.availWidth * 3,
        behavior: 'smooth'
    })
}

function chargesScroll(){
    window.scrollTo({
        left: window.screen.availWidth * 4,
        behavior: 'smooth'
    })
}

// Async Functions
async function filterResultsAW(url, method,type, csrfmiddlewaretoken, formData){
    const result = await fetch(url, {'method':method, headers: {'X-CSRFToken':csrfmiddlewaretoken, 'FilterType': type}, body:formData})
    const data = await result.json()
    return data
}

let body = document.querySelector('body')
let generalInfo = document.querySelector('.general-info')
let extras = document.querySelector('.extras')
let appointments = document.querySelector('.appointments')
let exams = document.querySelector('.exams')
let charges = document.querySelector('.charges')
let title = document.querySelector('#title')
let previewImg = document.querySelector('.image-preview')
let image = document.querySelector('.previewed-image')
let titleOriginalContent = title.innerText
let appointmentsBackUp = document.querySelector('.appointments').innerHTML
let examsBackUp = document.querySelector('.exams').innerHTML
let chargesBackUp = document.querySelector('.charges').innerHTML

// List of wrappers
let wrappers = [generalInfo, extras, appointments, exams, charges]

body.addEventListener('mouseover', (e) => {

    if (e.target.nodeName === 'TD' || ((e.target.classList.contains('fa-trash') || e.target.classList.contains('fa-edit')))){
        let row
        e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
        row.style.backgroundColor = '#0ff5fc'
        row.classList.add('tr-hover')
        for (let i = 0; i<row.childNodes.length; i++){
            if (row.childNodes[i].nodeName === 'TD'){
                row.childNodes[i].classList.add('td-hover')
            }
        }
    }

    if (e.target.classList.contains('info-tab') || e.target.parentNode.classList.contains('info-tab')){
        let tab = e.target.classList.contains('info-tab') ? e.target : e.target.parentNode
        tab.classList.add('tab-hover')
    }

    if (e.target.classList.contains('fa-filter')){
        e.target.classList.add('fa-filter-hover')
    }

    if (e.target.classList.contains('fa-sync-alt')){
        e.target.classList.add('fa-sync-alt-hover')
    }

    if (e.target.nodeName === 'BUTTON'){
        const button = e.target
        button.classList.add('button-form-hover')
    }

})

body.addEventListener('mouseout', (e) => {

  if (e.target.nodeName === 'TD' || ((e.target.classList.contains('fa-trash') || e.target.classList.contains('fa-edit')))){
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

  if (e.target.classList.contains('info-tab') || e.target.parentNode.classList.contains('info-tab')){
        let tab = e.target.classList.contains('info-tab') ? e.target : e.target.parentNode
        tab.classList.remove('tab-hover')
    }

    if (e.target.classList.contains('fa-filter')){
        e.target.classList.remove('fa-filter-hover')
    }

    if (e.target.classList.contains('fa-sync-alt')){
        e.target.classList.remove('fa-sync-alt-hover')
    }

    if (e.target.nodeName === 'BUTTON'){
        const button = e.target
        button.classList.remove('button-form-hover')
    }

})

body.addEventListener('click', (e) => {

    if (e.target.classList.contains('info-tab') || e.target.parentNode.classList.contains('info-tab')){
        let tab = e.target.classList.contains('info-tab') ? e.target : e.target.parentNode
        let tabs = document.querySelectorAll('.info-tab')
        for (let i = 0; i<tabs.length; i++){
            if (tabs[i].classList.contains('tab-active') && tabs[i] !== tab){
                tabs[i].classList.remove('tab-active')
            }
            if (wrappers[i].classList.contains('wrapper-show')){
                wrappers[i].classList.remove('wrapper-show')
            }

        }

        tab.classList.add('tab-active')
        if (tab.innerText === 'General'){
            generalScroll()
            title.innerText = titleOriginalContent
            generalInfo.classList.add('wrapper-show')
        } else if (tab.innerText === 'Background'){
            backgroundScroll()
            title.innerText = 'Background'
            extras.classList.add('wrapper-show')
        }else if (tab.innerText === 'Appointments'){
            appointmentsScroll()
            title.innerText = 'Appointments'
            appointments.classList.add('wrapper-show')
        }else if (tab.innerText === 'Exams'){
            examsScroll()
            title.innerText = 'Exams'
            exams.classList.add('wrapper-show')
        }else{
            chargesScroll()
            title.innerText = 'Charges'
            charges.classList.add('wrapper-show')
        }
    }

    if (e.target.classList.contains('fa-filter') && e.target.classList.contains('appointments-filter')){
        let form = document.querySelector('.appointments-form')
        if (form.classList.contains('show-form')){
            form.classList.remove('show-form')
            appointmentsBackUp = document.querySelector('.appointments').innerHTML

        }else{
            form.classList.add('show-form')
            appointmentsBackUp = document.querySelector('.appointments').innerHTML
        }
    } else if (e.target.classList.contains('fa-filter') && e.target.classList.contains('exams-filter')){
        let form = document.querySelector('.exams-form')
        if (form.classList.contains('show-form')){
            form.classList.remove('show-form')
            examsBackUp = document.querySelector('.exams').innerHTML
        }else{
            form.classList.add('show-form')
            examsBackUp = document.querySelector('.exams').innerHTML
        }
    } else if (e.target.classList.contains('fa-filter') && e.target.classList.contains('charges-filter')){
        let form = document.querySelector('.charges-form')
        if (form.classList.contains('show-form')){
            form.classList.remove('show-form')
            chargesBackUp = document.querySelector('.charges').innerHTML
        }else{
            form.classList.add('show-form')
            chargesBackUp = document.querySelector('.charges').innerHTML
        }
    }

    if (e.target.classList.contains('fa-sync-alt') && e.target.classList.contains('appointments-reload')){
        appointments.innerHTML = appointmentsBackUp
        document.querySelector('.appointments-filter').classList.remove('fa-filter-hover')
    } else if (e.target.classList.contains('fa-sync-alt') && e.target.classList.contains('exams-reload')){
        exams.innerHTML = examsBackUp
        document.querySelector('.exams-filter').classList.remove('fa-filter-hover')
    }else if (e.target.classList.contains('fa-sync-alt') && e.target.classList.contains('charges-reload')){
        charges.innerHTML = chargesBackUp
        document.querySelector('.charges-filter').classList.remove('fa-filter-hover')
    }


})

body.addEventListener('submit', (e) => {
        e.preventDefault()
        e.stopPropagation()
        let wrapper
    if (e.target.classList.contains('appointments-form')){
        wrapper = document.querySelector('.appointments')
        const url = e.target.action
        const method = e.target.method
        const type = 'appointments'
        const csrfmiddlewaretoken = document.querySelector('.appointments-form > [name=csrfmiddlewaretoken]').value
        const formData = new FormData(e.target)
        filterResultsAW(url, method, type, csrfmiddlewaretoken, formData)
        .then(data => {
            wrapper.innerHTML = data['html']
            document.querySelector('.appointments-form').classList.add('show-form')
        })
    } else if (e.target.classList.contains('exams-form')){
        wrapper = document.querySelector('.exams')
        const url = e.target.action
        const method = e.target.method
        const type = 'exams'
        const csrfmiddlewaretoken = document.querySelector('.exams-form > [name=csrfmiddlewaretoken]').value
        const formData = new FormData(e.target)
        filterResultsAW(url, method, type, csrfmiddlewaretoken, formData)
        .then(data => {
            wrapper.innerHTML = data['html']
            document.querySelector('.exams-form').classList.add('show-form')
        })
    } else{
        wrapper = document.querySelector('.charges')
        const url = e.target.action
        const method = e.target.method
        const type = 'charges'
        const csrfmiddlewaretoken = document.querySelector('.charges-form > [name=csrfmiddlewaretoken]').value
        const formData = new FormData(e.target)
        filterResultsAW(url, method, type, csrfmiddlewaretoken, formData)
        .then(data => {
            wrapper.innerHTML = data['html']
            document.querySelector('.charges-form').classList.add('show-form')
        })
    }
})

// Exams
if (exams){
    exams.addEventListener('mouseover', (e) => {
        if (e.target.classList.contains('exam-filename')){
            previewImg.classList.add('image-preview-show')
            image.src = e.target.getAttribute('data-img-src')
            document.querySelector('.exams-form').classList.remove('show-form')
        }
    })

    exams.addEventListener('mouseout', (e) => {
        if (e.target.classList.contains('exam-filename')){
            previewImg.classList.remove('image-preview-show')
            image.src = ''
        }
    })
}

window.addEventListener('scroll', (e) => {
    if(window.scrollX > 1440){
        body.classList.add('body-color-change')
    }else if (window.scrollX < 2880){
        body.classList.remove('body-color-change')
    }

})

window.addEventListener('load', (e) => {
    generalScroll()
})