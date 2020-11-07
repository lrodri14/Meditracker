//Checked
var profilePic = document.querySelector('img')
var controllers = document.querySelectorAll('.fa-angle-left, .fa-angle-right')
var generalInfo = document.querySelector('.first')
var generalInfoBackUp = document.querySelector('.first').innerHTML
var wrapper = document.querySelector('.wrapper')
var profileBackUp = document.querySelector('.wrapper').innerHTML
var editProfileForm = document.querySelector('form')


//Async Functions
async function changePasswordFormAW(url){
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function editProfileFormAW(url){
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function editProfileAW(url, method, csrfmiddlewaretoken, formData){
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken': csrfmiddlewaretoken}, body:formData})
    const data = result.json()
    return data
}

async function changePasswordAW(url, method, csrfmiddlewaretoken, body){
    const result = await fetch(url, {method: method, headers: {'X-CSRFToken': csrfmiddlewaretoken}, body:body})
    const data = result.json()
    return data
}


//General Info
if (wrapper){

    wrapper.addEventListener('click', (e) => {
        if (e.target.classList.contains('fa-times')){
            generalInfo.innerHTML = generalInfoBackUp
        }

        if (e.target.classList.contains('change-password')){
            e.preventDefault()
            e.stopPropagation()
            let url = e.target.href
            changePasswordFormAW(url)
            .then(data => {
                generalInfo.innerHTML = data['html']
        })
       }

       if (e.target.classList.contains('edit-profile')){
            e.preventDefault()
            e.stopPropagation()
            let url = e.target.href
            editProfileFormAW(url)
            .then(data => {
                wrapper.innerHTML = data['html']
        })
       }
    })


    wrapper.addEventListener('mouseover', (e) => {
        if (e.target.classList.contains('fa-times')){
            e.target.classList.add('fa-times-hover')
        }

        if (e.target.nodeName === 'A'){
            e.target.classList.add('link-hover')
        }

        if (e.target.classList.contains('fa-angle-left') || e.target.classList.contains('fa-angle-right')){
            e.target.classList.add('controller-hover')
        }

        if (e.target.classList.contains('profile-picture')){
            e.target.classList.add('image-hover')
        }

        if (e.target.classList.contains('edit-profile-picture')){
            e.target.classList.add('img-edit-hover')
        }

        if (e.target.classList.contains('fa-check')){
            e.target.classList.add('fa-check-hover')
        }
    })


    wrapper.addEventListener('mouseout', (e) => {

        if (e.target.classList.contains('fa-times')){
            e.target.classList.remove('fa-times-hover')
        }

        if (e.target.nodeName === 'A'){
            e.target.classList.remove('link-hover')
        }

        if (e.target.classList.contains('fa-angle-left') || e.target.classList.contains('fa-angle-right')){
            e.target.classList.remove('controller-hover')
        }

        if (e.target.classList.contains('profile-picture')){
            e.target.classList.remove('image-hover')
        }

        if (e.target.classList.contains('edit-profile-picture')){
            e.target.classList.remove('img-edit-hover')
        }

        if (e.target.classList.contains('fa-check')){
            e.target.classList.remove('fa-check-hover')
        }

    })

    wrapper.addEventListener('submit', (e) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.target.nodeName === 'FORM'){
            let url = e.target.action
            let method = e.target.method
            let csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            let body = new FormData(e.target)
            changePasswordAW(url, method, csrfmiddlewaretoken, body)
            .then(data => {
                if (data['html']){
                    generalInfo.innerHTML = data['html']
                }else{
                    generalInfo.innerHTML = generalInfoBackUp
                }
            })
        }
    })
}

// Form
editProfileForm.addEventListener('submit', (e) => {
    e.preventDefault()
    e.stopPropagation()
    let form = editProfileForm
    let url = form.action
    let method = form.method
    let csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    let formData = new FormData(form)
    editProfileAW(url, method, csrfmiddlewaretoken, formData)
    .then(data => {
        if (data['success']){
            wrapper.innerHTML = data['success']
        }else{
            editProfileForm.innerHTML = data['html']
        }
    })
})

