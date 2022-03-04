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

