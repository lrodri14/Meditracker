var a = document.querySelectorAll('a')
var li = document.querySelectorAll('li')
var logo = document.querySelector('img')

if (li.length === a.length){
  for (var i = 0; i < li.length; i++) {
    li[i].addEventListener('mouseover', function(){
        this.style.cssText = 'background-color: #3e5278;';
        this.style.transition = '0.5s';
        this.firstElementChild.style.color = 'cyan';

})
    li[i].addEventListener('mouseout', function(){
            this.style.cssText = '';
            this.style.transition = '0.5s';
            this.firstElementChild.style.color = '';

    })
}
}

logo.addEventListener('mouseover', function(){
    this.style.cssText = 'width: 150px; height: 150px;'
    this.style.transition = '0.5s';
})

logo.addEventListener('mouseout', function(){
    this.style.cssText = 'width: 100px; height: 100px;'
    this.style.transition = '0.5s';
})

