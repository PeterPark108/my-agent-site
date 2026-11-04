/* Trang chủ cosmos. Cờ: data-fx-cosmos|orbit|pin|glow-m và MYAGENT_CONFIG.home*.
   GSAP 3.15.1 chỉ tải khi được phép ghim thẻ trên máy tính có chuột và hiệu năng ổn.
   Giấy phép: js/vendor/gsap/NOTICE.txt */
(function(){
  var d=document.documentElement,C=window.MYAGENT_CONFIG||{};
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches||C.motionEnabled===false;
  function flag(attr,key){
    if(d.getAttribute('data-fx-'+attr)==='off')return false;
    if(C[key]===false)return false;
    return true;
  }
  var stage=document.querySelector('.hero-stage');
  if(stage&&'IntersectionObserver' in window){
    new IntersectionObserver(function(es){stage.classList.toggle('is-paused',!es[0].isIntersecting);}).observe(stage);
  }
  var desk=matchMedia('(min-width:1050px) and (hover:hover) and (pointer:fine)');
  function strong(){
    if(!desk.matches)return false;
    var c=navigator.connection;if(c&&c.saveData)return false;
    var cores=navigator.hardwareConcurrency||8;if(cores<4)return false;
    var mem=navigator.deviceMemory;if(mem&&mem<4)return false;
    return true;
  }
  function ambience(){
    var ok=!reduce&&strong();
    d.classList.toggle('fx-orbit',ok&&flag('orbit','homeOrbit'));
    d.classList.toggle('fx-glow',ok&&flag('glow-m','homeGlowM'));
    d.classList.toggle('fx-cosmos-live',ok&&flag('cosmos','homeCosmos'));
  }
  ambience();
  if(desk.addEventListener)desk.addEventListener('change',ambience);
  if(!flag('cosmos','homeCosmos'))d.classList.add('fx-cosmos-off');
  var started=false;
  function pin(){
    if(started||reduce||!flag('pin','homePin')||!strong())return;
    if(!document.querySelector('.hx-stack'))return;
    started=true;
    function load(src){return new Promise(function(ok,bad){var s=document.createElement('script');s.src=src;s.onload=ok;s.onerror=function(){started=false;bad();};document.body.appendChild(s);});}
    load('js/vendor/gsap/gsap.min.js?v=0.9.39').then(function(){return load('js/vendor/gsap/ScrollTrigger.min.js?v=0.9.39');}).then(function(){
      var g=window.gsap,ST=window.ScrollTrigger;if(!g||!ST)return;
      g.registerPlugin(ST);
      var mm=g.matchMedia();
      mm.add('(min-width:1050px) and (hover:hover) and (pointer:fine) and (prefers-reduced-motion:no-preference)',function(){
        var cards=g.utils.toArray('.hx-card');
        var stack=document.querySelector('.hx-stack');
        if(!stack||cards.length<2)return;
        g.set(stack,{height:function(){return Math.max(420,Math.min(window.innerHeight*0.62,560));}});
        g.set(cards,{position:'absolute',left:0,right:0,top:0,minHeight:0});
        cards.forEach(function(card,i){g.set(card,{zIndex:i+1});});
        g.set(cards.slice(1),{yPercent:105,autoAlpha:0});
        d.classList.add('fx-pin');
        var tl=g.timeline({scrollTrigger:{trigger:'.hx-pin-zone',start:'top 96px',end:'bottom bottom',scrub:0.65,invalidateOnRefresh:true}});
        cards.slice(1).forEach(function(card){
          tl.to(card,{yPercent:0,autoAlpha:1,duration:1,ease:'power2.inOut'})
            .to('.hx-edge',{opacity:1,duration:0.08},'-=0.12')
            .to('.hx-edge',{opacity:0,duration:0.22})
            .to({}, {duration:0.2});
        });
        return function(){d.classList.remove('fx-pin');};
      });
      addEventListener('load',function(){ST.refresh();},{once:true});
    }).catch(function(){});
  }
  pin();
  if(desk.addEventListener)desk.addEventListener('change',pin);
})();
