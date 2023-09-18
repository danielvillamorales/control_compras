function mostrar_foto(foto){
    console.log(foto);
    var imagen = document.getElementById("img_"+foto);
    if (imagen.style.display === "none") {
        imagen.style.display = "block";
      } else {
        imagen.style.display = "none";
      }
};