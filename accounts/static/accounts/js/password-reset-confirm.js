// Checked
if ( document.querySelectorAll('input') !== 'undefined' && document.querySelectorAll('input') !== 'null'
    && document.querySelectorAll('button') !== 'undefined' && document.querySelectorAll('input') !== 'null'){
        var inputs = document.querySelectorAll('input')
        var reset = document.querySelector('button')
    }
if (document.querySelector('a') !== 'undefined' && document.querySelector('a') !== 'null'){
    var invalidLink = document.querySelector('a')
}

// Inputs
if (inputs){
    for (let i = 0; i<inputs.length; i++){
    inputs[i].addEventListener('mouseover', function(){
        this.classList.add('input-hover')
    })

    inputs[i].addEventListener('mouseout', function(){
        this.classList.remove('input-hover')
    })
}
}

// Reset

if (reset){
    reset.addEventListener('mouseover', function(){
        this.classList.add('button-hover')
    })

    reset.addEventListener('mouseout', function(){
        this.classList.remove('button-hover')
})
}



// Invalid Link
if (invalidLink){
    invalidLink.addEventListener('mouseover', function(){
        this.classList.add('link-hover')
    })

    invalidLink.addEventListener('mouseout', function(){
        this.classList.remove('link-hover')
    })
}