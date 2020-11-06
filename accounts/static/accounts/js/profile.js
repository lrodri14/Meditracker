//Checked
var profilePic = document.querySelector('img')
var edit = document.querySelectorAll('a')
var controllers = document.querySelectorAll('.fa-angle-left, .fa-angle-right')
var generalInfo = document.querySelector('.first')
var generalInfoBackUp = document.querySelector('.first').innerHTML


//Async Functions
async function changePasswordFormAW(url){
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function changePasswordAW(url, method, csrfmiddlewaretoken, body){
    const result = await fetch(url, {method: method, headers: {'X-CSRFToken': csrfmiddlewaretoken}, body:body})
    const data = result.json()
    return data
}


//General Info
if (generalInfo){

    generalInfo.addEventListener('click', (e) => {
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
    })

    generalInfo.addEventListener('mouseover', (e) => {
        if (e.target.classList.contains('fa-times')){
            e.target.classList.add('fa-times-hover')
        }

        if (e.target.nodeName === 'A'){
            e.target.classList.add('link-hover')
        }

        if (e.target.classList.contains('fa-angle-left') || e.target.classList.contains('fa-angle-right')){
            e.target.classList.add('controller-hover')
        }

        if (e.target.nodeName === 'IMG'){
            e.target.classList.add('image-hover')
        }

        if (e.target.classList.contains('fa-check')){
            e.target.classList.add('fa-check-hover')
        }
    })


    generalInfo.addEventListener('mouseout', (e) => {

        if (e.target.classList.contains('fa-times')){
            e.target.classList.remove('fa-times-hover')
        }

        if (e.target.nodeName === 'A'){
            e.target.classList.remove('link-hover')
        }

        if (e.target.classList.contains('fa-angle-left') || e.target.classList.contains('fa-angle-right')){
            e.target.classList.remove('controller-hover')
        }

        if (e.target.nodeName === 'IMG'){
            e.target.classList.remove('image-hover')
        }

        if (e.target.classList.contains('fa-check')){
            e.target.classList.remove('fa-check-hover')
        }

    })

    generalInfo.addEventListener('submit', (e) => {
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

