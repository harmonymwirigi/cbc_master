const menu =  document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar__menu');

// display mobile menu
const mobileMenu = () => {
menu.classList.toggle('is-active');
menuLinks.classList.toggle('active');
};
menu.addEventListener("click", mobileMenu);

// login popup
document.querySelector("#login").addEventListener("click",function(){
document.querySelector(".popup").classList.add("active");
});
document.querySelector("#login").addEventListener("click",function(){
document.querySelector("#overlay").classList.add("active");
});
document.querySelector(".popup .close-btn").addEventListener("click",function(){
document.querySelector(".popup").classList.remove("active");
});
document.querySelector(".popup .close-btn").addEventListener("click",function(){
document.querySelector("#overlay").classList.remove("active");
});
function remove_student(id_std){
//let id_student=id_std.value;
      // login popup

document.querySelector(".popup").classList.add("active");

document.querySelector("#3844").addEventListener("click",function(){
document.querySelector("#overlay").classList.add("active");
});

}


document.querySelector("#signup").addEventListener("click",function(){
document.querySelector(".choose").classList.add("active");
});
document.querySelector("#signup").addEventListener("click",function(){
document.querySelector("#overlay").classList.add("active");
});
document.querySelector(".choose .close-btn").addEventListener("click",function(){
document.querySelector(".choose").classList.remove("active");
});
document.querySelector(".choose .close-btn").addEventListener("click",function(){
document.querySelector("#overlay").classList.remove("active");
});

document.querySelector("#teacher").addEventListener("click",function(){
document.querySelector(".container").classList.add("active");
document.querySelector(".choose").classList.remove("active");
});
document.querySelector("#teacher").addEventListener("click",function(){
document.querySelector("#overlay").classList.add("active");
});
document.querySelector(".container .close-signup-btn").addEventListener("click",function(){
document.querySelector(".container").classList.remove("active");
});




const slidePage = document.querySelector(".slidepage");
const firtNextBtn = document.querySelector(".nextBtn");
const prevBtnSec = document.querySelector(".prev-1");
const nextBtnSec = document.querySelector(".next-1");
const prevBtnThird = document.querySelector(".prev-2");
const nextBtnThird = document.querySelector(".next-2");
const prevBtnFourth = document.querySelector(".prev-3");
const submitBtn = document.querySelector(".Submit");
const pregressText = document.querySelectorAll(".step p");
const pregressCheck = document.querySelectorAll(".step .check");
const bullet = document.querySelectorAll(".step .bullet");

let max =4;
let current =1;

firtNextBtn.addEventListener('click',function(){
const activediv = document.querySelector(".slidepage");
const field = activediv.getElementsByClassName("field");
let inputFirst = field[0].children[1];
let inputLast = field[1].children[1];

if (inputFirst.value != '' && inputLast.value != ''){
slidePage.style.marginLeft = "-25%";
bullet[current -1].classList.add("active");
pregressText[current -1].classList.add("active");
pregressCheck[current -1].classList.add("active");
current +=1;
}
if (inputFirst.value == ''){
hide(inputFirst);
}
if (inputLast.value == ''){
hide(inputLast);
}
});
nextBtnSec.addEventListener('click',function(){
const activediv = document.querySelector(".page2");
const field = activediv.getElementsByClassName("field");
let inputFirst = field[0].children[1];
let inputLast = field[1].children[1];

if (inputFirst.value != '' && inputLast.value != ''){
slidePage.style.marginLeft = "-50%";
bullet[current -1].classList.add("active");
pregressText[current -1].classList.add("active");
pregressCheck[current -1].classList.add("active");
current +=1;
}
if (inputFirst.value == ''){
hide(inputFirst);
}
if (inputLast.value == ''){
hide(inputLast);
}
});
nextBtnThird.addEventListener('click',function(){
const activediv = document.querySelector(".page3");
const field = activediv.getElementsByClassName("field");
let inputFirst = field[0].children[1];
let inputLast = field[1].children[1];

if (inputFirst.value != '' && inputLast.value != ''){
slidePage.style.marginLeft = "-75%";
bullet[current -1].classList.add("active");
pregressText[current -1].classList.add("active");
pregressCheck[current -1].classList.add("active");
current +=1;
}
if (inputFirst.value == ''){
hide(inputFirst);
}
if (inputLast.value == ''){
hide(inputLast);
}
});
submitBtn.addEventListener('click',function(){
const activediv = document.querySelector(".page4");
const field = activediv.getElementsByClassName("field");
let inputFirst = field[0].children[1];
let inputLast = field[1].children[1];

if (inputFirst.value != '' && inputLast.value != ''){
if (inputLast.value == inputFirst.value){
bullet[current -1].classList.add("active");
pregressText[current -1].classList.add("active");
pregressCheck[current -1].classList.add("active");
current +=1;
setTimeout(function(){
alert("You are successfully created your account");
location.reload();
},800);
}
}
if (inputFirst.value == ''){
hide(inputFirst);
}
if (inputLast.value == ''){
hide(inputLast);
}
});

prevBtnSec.addEventListener('click',function(){
slidePage.style.marginLeft = "0%";
bullet[current -2].classList.remove("active");
pregressText[current -2].classList.remove("active");
pregressCheck[current -2].classList.remove("active");
current -=1;
});
prevBtnThird.addEventListener('click',function(){
slidePage.style.marginLeft = "-25%";
bullet[current -2].classList.remove("active");
pregressText[current -2].classList.remove("active");
pregressCheck[current -2].classList.remove("active");
current -=1;
});
prevBtnFourth.addEventListener('click',function(){
slidePage.style.marginLeft = "-50%";
bullet[current -2].classList.remove("active");
pregressText[current -2].classList.remove("active");
pregressCheck[current -2].classList.remove("active");
current -=1;
});

function hide(input){
input.nextElementSibling.textContent = "This field is empty";
setTimeout(()=>{input.nextElementSibling.textContent = '';},2000);
}
