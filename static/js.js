document.addEventListener("DOMContentLoaded", function(){
        document.querySelector('#PW').onchecked= function(){
            var x=document.querySelector("login-pw");
            if (x.type="password"){
                x.type="text";
            }
        };
});

document.addEventListener("DOMCOntentLoaded", ()=>{
    document.querySelector('.signup').onclick = function(){
        email=document.querySelector('.signup').value;
        name=document.querySelector('.signup').value;
        if (email <=0){
            alert("eneter a email address");
        }
        if (name.lrnght<=0){
            alert("enter a name");
        }
    };

});