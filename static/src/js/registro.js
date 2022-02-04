const formregistro=document.getElementById("formregistro");
const error=document.getElementById("error");
    

formregistro.addEventListener('submit',function(e){
    e.preventDefault();
    
    const datos=new FormData(formregistro);

    const datoJson={"usuario":datos.get("username"),"pass":datos.get("password")};
   
    console.log(datoJson);
})