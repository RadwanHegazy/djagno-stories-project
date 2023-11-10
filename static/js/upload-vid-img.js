var btns = document.querySelectorAll('.upload button');
var media = document.getElementById('media')
var file = document.getElementById('file');
var doneBtn = document.getElementById('done');

let element;
var form = new FormData();

btns.forEach(btn => {

    btn.addEventListener('click',()=>{
        file.click()
        element = btn.id
    })

})


file.addEventListener('change',(e)=>{
    var f = e.target.files[0];
    form.append(element,f,f.name)
    var path = URL.createObjectURL(f);
    let content ;
    
    if ( element == 'img' ){
        content = document.createElement('img');
    }else{
        content = document.createElement('video');
    }

    content.setAttribute('src',path)

    media.appendChild(content)
})




doneBtn.addEventListener('click',()=>{
    $.ajax({
        url:".",
        type:"POST",
        data:form,
        contentType:false,
        processData:false,
        cache:false,
        success:function(done){
            window.location.href = "/status/" + done
        }
    })



})
