//Checked
//var generalInfo = document.querySelector('.first')
//var generalInfoBackUp = document.querySelector('.first').innerHTML
//var wrapper = document.querySelector('.wrapper')
//var profileBackUp = document.querySelector('.wrapper').innerHTML
//var editProfileForm = document.querySelector('form')
//var body = document.querySelector('body')
//var

//Async Functions
//async function changePasswordFormAW(url){
//    const result = await fetch(url)
//    const data = result.json()
//    return data
//}
//
//async function editProfileFormAW(url){
//    const result = await fetch(url)
//    const data = result.json()
//    return data
//}
//
//async function editProfileAW(url, method, csrfmiddlewaretoken, formData){
//    const result = await fetch(url, {method:method, headers:{'X-CSRFToken': csrfmiddlewaretoken}, body:formData})
//    const data = result.json()
//    return data
//}
//
//async function changePasswordAW(url, method, csrfmiddlewaretoken, body){
//    const result = await fetch(url, {method: method, headers: {'X-CSRFToken': csrfmiddlewaretoken}, body:body})
//    const data = result.json()
//    return data
//}
//
//
////General Info
//if (body){
//
//    body.addEventListener('click', (e) => {
//        if (e.target.classList.contains('fa-times')){
//            generalInfo.innerHTML = generalInfoBackUp
//        }
//
//        if (e.target.classList.contains('change-password')){
//            e.preventDefault()
//            e.stopPropagation()
//            let url = e.target.href
//            changePasswordFormAW(url)
//            .then(data => {
//                generalInfo.innerHTML = data['html']
//        })
//       }
//
//       if (e.target.classList.contains('edit-profile')){
//            e.preventDefault()
//            e.stopPropagation()
//            let url = e.target.href
//            editProfileFormAW(url)
//            .then(data => {
//                wrapper.innerHTML = data['html']
//        })
//       }
//    })
//
//
//    body.addEventListener('mouseover', (e) => {
//        if (e.target.classList.contains('fa-times')){
//            e.target.classList.add('fa-times-hover')
//        }
//
//        if (e.target.nodeName === 'A'){
//            e.target.classList.add('link-hover')
//        }
//
//        if (e.target.classList.contains('profile-picture')){
//            e.target.classList.add('image-hover')
//        }
//
//        if (e.target.classList.contains('edit-profile-picture')){
//            e.target.classList.add('img-edit-hover')
//        }
//
//        if (e.target.classList.contains('fa-check')){
//            e.target.classList.add('fa-check-hover')
//        }
//    })
//
//
//    body.addEventListener('mouseout', (e) => {
//
//        if (e.target.classList.contains('fa-times')){
//            e.target.classList.remove('fa-times-hover')
//        }
//
//        if (e.target.nodeName === 'A'){
//            e.target.classList.remove('link-hover')
//        }
//
//        if (e.target.classList.contains('profile-picture')){
//            e.target.classList.remove('image-hover')
//        }
//
//        if (e.target.classList.contains('edit-profile-picture')){
//            e.target.classList.remove('img-edit-hover')
//        }
//
//        if (e.target.classList.contains('fa-check')){
//            e.target.classList.remove('fa-check-hover')
//        }
//
//    })
//
//    body.addEventListener('submit', (e) => {
//        e.preventDefault()
//        e.stopPropagation()
//        if (e.target.nodeName === 'FORM' && e.target.classList.contains('password-form')){
//            let url = e.target.action
//            let method = e.target.method
//            let csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
//            let body = new FormData(e.target)
//            changePasswordAW(url, method, csrfmiddlewaretoken, body)
//            .then(data => {
//                if (data['html']){
//                    generalInfo.innerHTML = data['html']
//                }else{
//                    generalInfo.innerHTML = generalInfoBackUp
//                }
//            })
//        }else{
//            let form = editProfileForm
//            let url = form.action
//            let method = form.method
//            let csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
//            let formData = new FormData(form)
//            editProfileAW(url, method, csrfmiddlewaretoken, formData)
//            .then(data => {
//                if (data['success']){
//                    wrapper.innerHTML = data['success']
//                    generalInfo = document.querySelector('.first')
//                    generalInfoBackUp = document.querySelector('.first').innerHTML
//                    wrapper = document.querySelector('.wrapper')
//                    profileBackUp = document.querySelector('.wrapper').innerHTML
//                }else{
//                    editProfileForm.innerHTML = data['html']
//                }
//            })
//        }
//    })
//
//}

var img = document.querySelector('img')
var edit = document.querySelector('.edit-profile-picture-modal')
var profile = document.querySelector('.profile-picture')
profile.addEventListener('mouseover', (e) =>{
    if (e.target === img || e.target === edit || e.target.classList.contains('fa-pen')){
        edit.classList.add('edit-profile-picture-modal-show')
    }
})

profile.addEventListener('mouseout', (e) =>{
    if (e.target === img || e.target === edit){
        edit.classList.remove('edit-profile-picture-modal-show')
    }
})
