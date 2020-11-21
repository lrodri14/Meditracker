/*This JS file contains all the variables and event listeners needed for the deletion error modal to work properly,
  it is composed of two sections, the variables section and event listeners section.*/

// #############################################Variables###############################################################

var button = document.querySelector('button')

// #############################################Event Listeners#########################################################

// This event occurs every time the target is the element itself, it adds the button-hover class to the target.
button.addEventListener('mouseover', function(){
    this.classList.add('button-hover')
})

    // This event occurs every time the target is the element itself, it removes the button-hover class to the target.
button.addEventListener('mouseout', function(){
    this.classList.remove('button-hover')
})