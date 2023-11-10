var imgFile = document.getElementById('imgFile');
var imgView = document.getElementById('imgView');
var imgBtn = document.getElementById('imgBtn');



imgBtn.addEventListener('click',()=>{
    imgFile.click()
})

imgFile.addEventListener('change',(e)=>{
    var img = e.target.files[0];
    var imgSrc = URL.createObjectURL(img);

    imgView.setAttribute('src',imgSrc);
})