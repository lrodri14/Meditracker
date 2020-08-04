// Checked


var li = document.querySelectorAll('li')
var logo = document.querySelector('img')

// Links
for (let i = 0; i < li.length; i++) {
    li[i].addEventListener('mouseover', function(){
        this.classList.add('hover-over')
})
    li[i].addEventListener('mouseout', function(){
        this.classList.remove('hover-over')
    })
  }

// Logo
logo.addEventListener('mouseover', function(){
    this.style.cssText = 'width: 150px; height: 150px; transition: 0.5s;'
})

logo.addEventListener('mouseout', function(){
    this.style.cssText = 'width: 100px; height: 100px; transition: 0.5s;'
})