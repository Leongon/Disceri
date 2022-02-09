axios({
    method: "get",
    url: "/inicio",
   
    
  })
    .then(function (response) {
      //handle success
      console.log(response.data.urlvideo[0])
      
    })
    .catch(function (response) {
      //handle error
      console.log(response);
    });