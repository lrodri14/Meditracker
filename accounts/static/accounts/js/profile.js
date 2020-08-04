//Checked
var profilePic = document.querySelector('img')
var edit = document.querySelectorAll('a')

//Profile Picture
profilePic.addEventListener('mouseover', function(){
    this.classList.add('image-hover')
})

profilePic.addEventListener('mouseout', function(){
    this.classList.remove('image-hover')
})

// Edit Links
for (let i = 0; i<edit.length; i++){
    edit[i].addEventListener('mouseover', function(){
        edit[i].classList.add('link-hover')
    })

    edit[i].addEventListener('mouseout', function(){
        edit[i].classList.remove('link-hover')
    })
}

