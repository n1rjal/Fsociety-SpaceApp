let nameplate=document.getElementById("member-name");
let names=["Nirjal Paudel","Sushan Poudyal","Bipin Bhandari","Prabesh Pudasaini","Thinam Tamang"];
var i=0;
setInterval(()=>{
    
    console.log(i)
    nameplate.innerText=names[i];
    i++;
    if (i===names.length){
        i=0;
        
    }
    
},2000);