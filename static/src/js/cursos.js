const idcurso=1 

videos(idcurso);
function videos(videoid){
    const videos=document.getElementById("conte");
    const listvideo=document.getElementById("clases-videos");

    

    datos={"idcurso":videoid}
    axios({
        method: "post",
        url: "/get_videos",
        data:datos
        
    })
        .then(function (response) {
            
            //handle success
            
            videos.innerHTML="";
            listvideo.innerHTML="";
            i=0
            for(x of response.data.msj){
                i=i+1
            videos.innerHTML+=`<a href="${x.url}" value="${i}" data-video="${x.idmodulo}" id="video${i}" class="circulo btn material ">${i}</a> `;
            listvideo.innerHTML+=`<li class="list-group-item "> <a href="${x.url}" data-video="${x.idmodulo}" value="${i}" class="material"> Video${i}</a>
            
            </li>`
            }
            //donde se quiere que empiece el video ya sea vide 1 video 2 o 3
            inicio=1;
            cargariniciovideo(inicio)
            
            function cargariniciovideo(numerovideo){
                seleccionvideo="#video"+numerovideo;
                
                URLactual=$(seleccionvideo).attr("href");
                $(".cambio-video").attr("src", URLactual)
                idvimate=$(seleccionvideo).attr("data-video");
                materialvideo(idvimate)
            }
        
            barra_progreso();

            $('.cursoss').click(function(){
            $('.curso-activar').click();
            })
            
            function barra_progreso(){
                $(".activar").click();
                $(".radio-izquierda").prop('disabled',true);
                
                contador=0
                
                var circulos = document.getElementsByClassName("circulo").length;
                
                $(".material").click(function(e){
                e.preventDefault();
                URLactual=$(this).attr("href");

                $(".cambio-video").attr("src", URLactual)

                contador=($(this).attr('value'))-1
                
                cargar(contador)

                
                idvimate=$(this).attr("data-video");
                materialvideo(idvimate)
                
                })
                $(".radio-derecha").click(function(){
                contador++
                
                if (contador>(circulos-1)){
        
                    contador=(circulos-1);
                    
                }
                cargar(contador);
                console.log(contador)
                seleccionvideo="#video"+(contador+1);
                URLactual=$(seleccionvideo).attr("href");
                $(".cambio-video").attr("src", URLactual)

                idvimate=$(seleccionvideo).attr("data-video");
                materialvideo(idvimate)
                
                })
        
                $(".radio-izquierda").click(function(){
        
                contador--
                if(contador<0){
                    contador=0
                }
                cargar(contador);
                console.log(contador)
                seleccionvideo="#video"+(contador+1)
                URLactual=$(seleccionvideo).attr("href");
                console.log(URLactual)
                $(".cambio-video").attr("src", URLactual)

                $(".cambio-video").attr("src", URLactual)
                idvimate=$(seleccionvideo).attr("data-video");
                materialvideo(idvimate)
                
                })
                
        
                $(".circulo").click(function(){
                contador=($(this).attr('value'))-1
                
                cargar(contador)
                })
                //video
                contador=inicio-1
                cargar(contador);
                function cargar(contador) {
                    
                progreso=(100/(circulos-1));
        
                total=progreso * contador
        
                $(".progreso").css('width',total  +'%');
        
                if(contador==0){
                    
                    $(".radio-izquierda").prop('disabled',true);
                    $(".radio-derecha").removeAttr('disabled');
                }
                else if (contador==(circulos-1)) 
                {
                    $(".radio-derecha").prop('disabled',true);
                    $(".radio-izquierda").removeAttr('disabled');
                } 
                else {
                    $(".radio-derecha").removeAttr('disabled');
                    $(".radio-izquierda").removeAttr('disabled');
                }
        
                }
            }
        


        })
        .catch(function (response) {
            //handle error
            console.log(response);
        });
}


function materialvideo(materialvideoid){
    const materialevideo=document.getElementById("materiales-videos");
    datos={"idvideo":materialvideoid}
    axios({
        method: "post",
        url: "/get_archivos",
        data:datos  
    })
        .then(function (response) {
          console.log(response.data.msj);
          materialevideo.innerHTML="";
          for(x of response.data.msj){
              materialevideo.innerHTML+=`<li class="list-group-item " id="materiales-videos">
              <a href="${x.url}"  class="material"> ${x.url}</a>
             </li>`
          }
        })
        .catch(function (response) {
            //handle error
            console.log(response);
        });
}