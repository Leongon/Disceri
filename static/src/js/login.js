const formlogin=document.getElementById("formlogin");
const error=document.getElementById("error");


formlogin.addEventListener('submit',function(e){
    e.preventDefault();
    
    const datos=new FormData(formlogin);
    
    const datoJson={"usuario":datos.get("username"),"pass":datos.get("password")};
    
    axios({
        method: "post",
        url: "/login",
        data: datoJson,
        
      })
        .then(function (response) {
          //handle success
          
          if(response.data.acceso==false){
            
            error.innerHTML=`
            <div class="alert alert-danger" role="alert">
						Contraseña o usuario incorrecto!
					  </div>
            `;
            
          }
          if(response.data.acceso==true){
            console.log("Bienvenido");
            window.location.href = "/inicio";
            console.log(datoJson);
          }
        })
        .catch(function (response) {
          //handle error
          console.log(response);
        });
})