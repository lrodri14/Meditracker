var body = document.querySelector('body')
var content = document.querySelector('.content')
var img = document.querySelector('img')
var edit = document.querySelector('.edit-profile-picture-modal')
var profile = document.querySelector('.profile-picture')
var modal = document.querySelector('.modal')
var modalContent = document.querySelector('.modal-content')

// Async Functions

async function editFormAW(url){
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function editProfileAW(url, method, csrfmiddlewaretoken, formData){
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken': csrfmiddlewaretoken}, body:formData})
    const data = result.json()
    return data
}

if (body){

    body.addEventListener('mouseover', (e) => {
        if (e.target === img || e.target === edit || e.target.classList.contains('fa-pen')){
            edit.classList.add('edit-profile-picture-modal-show')
        }

        if (e.target.classList.contains('fa-edit')){
            e.target.classList.add('fa-edit-hover')
        }

        if (e.target.classList.contains('fa-camera')){
            e.target.classList.add('fa-camera-hover')
        }

        if (e.target.classList.contains('fa-pen')){
            e.target.classList.add('fa-pen-hover')
        }

        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.add('button-hover')
        }

    })

    body.addEventListener('mouseout', (e) => {
        if (e.target === img || e.target === edit){
            edit.classList.remove('edit-profile-picture-modal-show')
        }

        if (e.target.classList.contains('fa-edit')){
            e.target.classList.remove('fa-edit-hover')
        }

        if (e.target.classList.contains('fa-camera')){
            e.target.classList.remove('fa-camera-hover')
        }

        if (e.target.classList.contains('fa-pen')){
            e.target.classList.remove('fa-pen-hover')
        }

        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.remove('button-hover')
        }

    })

    body.addEventListener('click', (e) => {

        if (e.target.classList.contains('fa-edit') || e.target.classList.contains('fa-pen') || e.target.classList.contains('fa-camera')){
            modal.classList.add('modal-show')
            edit.classList.remove('edit-profile-picture-modal-show')
            let url = e.target.getAttribute('data-url')
            let type = e.target.getAttribute('data-type')
            editFormAW(url, type)
            .then(data => {
                modalContent.innerHTML = data['html']
            })
        }

        if (e.target.classList.contains('modal')){
            modal.classList.remove('modal-show')
        }

    })


}

if (modal){
    modal.addEventListener('submit', (e) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.target.nodeName === 'FORM'){
            let form = e.target
            let url = form.action
            let method = form.method
            let csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value
            let formData = new FormData(form)
            editProfileAW(url, method, csrfmiddlewaretoken, formData)
            .then(data => {
                if (data['success']){
                    modalContent.innerHTML = ''
                    modal.classList.remove('modal-show')
                    content.innerHTML = data['success']
                    img = document.querySelector('img')
                    edit = document.querySelector('.edit-profile-picture-modal')
                    profile = document.querySelector('.profile-picture')
                }else{
                    modalContent.innerHTML = data['html']
                }
            })
        }
    })
}