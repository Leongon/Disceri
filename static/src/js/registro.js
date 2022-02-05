const formregistro = document.getElementById("formregistro");


formregistro.addEventListener('submit', function (e) {
    e.preventDefault();

    const datos = new FormData(formregistro);

    registrar(datos.get("Nombre"), datos.get("Apellido"), datos.get("username"), datos.get("password"), datos.get("phone"), datos.get("Correo"),datos.get("Rpassword"))

});


function registrar(nombre, apellido, usuario, password, telefono, correo,Rpassword) {

    if(password==Rpassword){
        if (!((usuario && telefono && correo && password && nombre && apellido) == "")) {
            const datoJson = {
                "usuario": usuario,
                "password": password,
                "nombres": nombre,
                "apellidos": apellido,
                "correo": correo,
                "telefono": telefono,
            };

            axios({
                method: "post",
                url: "/registrar_usuario",
                data: datoJson
            })

                .then(function (response) {


                    if ((response.data.ingreso == true)) {
                        error.innerHTML = `
                                <div class="alert alert-success" role="alert">
                                Registro correcto<br/>
                                </div>
                        `;
                        formregistro.reset();
                    } else {
                        console.log("error al registrar");
                        if (response.data.dato[0].duplicado == true) {
                            error.innerHTML = `
                                <div class="alert alert-danger" role="alert">
                                - ${response.data.dato[0].msj}<br/>
                                </div>
                        `;
                        }
                        if (response.data.dato[1].duplicado == true) {
                            error.innerHTML = `
                                <div class="alert alert-danger" role="alert">
                                
                                --    ${response.data.dato[1].msj}<br/>
                                
                                </div>
                        `;
                        }
                        if (response.data.dato[2].duplicado == true) {
                            error.innerHTML = `
                                <div class="alert alert-danger" role="alert">
                                ---   ${response.data.dato[2].msj}<br/>
                                </div>
                        `;
                        }

                    }


                    




                })
                .catch(function (response) {
                    //handle error
                    console.log(response);
                });
        } else {
            error.innerHTML = `
                <div class="alert alert-danger" role="alert">
                        Llene todos los campos
                        </div>
                `;
        }
    }else{
        error.innerHTML = `
                <div class="alert alert-danger" role="alert">
                        Las contraseñas no coinciden
                        </div>
                `;
    }
}
