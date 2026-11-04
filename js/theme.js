/* GĐ1 — nút sáng/tối. Cờ: html[data-fx-theme=off] hoặc MYAGENT_CONFIG.themeEnabled===false. */
(function(){var d=document.documentElement,C=window.MYAGENT_CONFIG||{};
if(d.getAttribute("data-fx-theme")==="off"||C.themeEnabled===false){d.removeAttribute("data-theme");d.style.colorScheme="";var b0=document.querySelector(".theme-btn");if(b0)b0.hidden=true;return}
var K="ma-theme";
function cur(){return d.getAttribute("data-theme")==="light"?"light":"dark"}
function sync(t){var b=document.querySelector(".theme-btn"),dark=t!=="light";
if(b){b.setAttribute("aria-pressed",dark?"true":"false");b.setAttribute("aria-label",dark?"Chuyển sang giao diện sáng":"Chuyển sang giao diện tối");var s=b.querySelector(".theme-lbl");if(s)s.textContent=dark?"Giao diện tối":"Giao diện sáng"}
var m=document.querySelector('meta[name="theme-color"]');if(m)m.setAttribute("content",dark?"#05070F":"#F4F7FB");
var i3=document.getElementById("i3d");if(i3)i3.classList.toggle("light",!dark);
try{document.dispatchEvent(new CustomEvent("ma-theme",{detail:t}))}catch(e){}}
function apply(t){d.setAttribute("data-theme",t);d.style.colorScheme=t;try{localStorage.setItem(K,t)}catch(e){}sync(t)}
function go(t,x,y){var reduce=matchMedia("(prefers-reduced-motion: reduce)").matches,off=d.getAttribute("data-fx-theme-anim")==="off";
if(reduce||off||!document.startViewTransition){apply(t);return}
var end=Math.hypot(Math.max(x,innerWidth-x),Math.max(y,innerHeight-y));
var tr=document.startViewTransition(function(){apply(t)});
tr.ready.then(function(){d.animate({clipPath:["circle(0px at "+x+"px "+y+"px)","circle("+end+"px at "+x+"px "+y+"px)"]},{duration:480,easing:"ease-in-out",pseudoElement:"::view-transition-new(root)"})}).catch(function(){})}
var btn=document.querySelector(".theme-btn");
sync(cur());
if(btn)btn.addEventListener("click",function(){var r=btn.getBoundingClientRect();go(cur()==="dark"?"light":"dark",r.left+r.width/2,r.top+r.height/2)});
window.MYAGENT_THEME={toggle:function(el){var r=el&&el.getBoundingClientRect?el.getBoundingClientRect():null;go(cur()==="dark"?"light":"dark",r?r.left+r.width/2:innerWidth/2,r?r.top+r.height/2:0)},set:apply}})();
