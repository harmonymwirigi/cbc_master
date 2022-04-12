//add student popup
document.querySelector("#add").addEventListener("click",function(){
document.querySelector(".add").classList.add("active");
});
document.querySelector("#add").addEventListener("click",function(){
document.querySelector("#overlay").classList.add("active");
});
document.querySelector(".add .close-btn").addEventListener("click",function(){
document.querySelector(".add").classList.remove("active");
});
document.querySelector(".add .close-btn").addEventListener("click",function(){
document.querySelector("#overlay").classList.remove("active");
});

function openContainer(containerName) {
  var i;
  var x = document.getElementsByClassName("container1");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  document.getElementById(containerName).style.display = "block";
}

function side(sidebar){
document.getElementById(sidebar).style.right = "0px";
}
document.querySelector("#side").addEventListener('click', function(){
document.querySelector(".sidebar").classList.add("active");
});
document.querySelector("#side").addEventListener('dblclick', function(){
document.querySelector(".sidebar").classList.remove("active");
});

