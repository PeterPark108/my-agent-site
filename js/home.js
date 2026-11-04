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
  /* Concept: repo gốc pin + scrub 0.65, end = 2.8 lần chiều cao màn hình, không snap.
     Một nấc (khóa 700ms) đổi một khung trong 0.62s. Hết khung thì không chặn cuộn. */
  var snapMq=matchMedia('(min-width:1050px) and (hover:hover) and (pointer:fine)');
  function snapWanted(){
    if(d.getAttribute('data-fx-snap')==='off'||C.homeSnap===false)return false;
    if(reduce||!snapMq.matches)return false;
    return !!document.querySelector('.hx-stack');
  }
  var snapBound=false,snapIndex=0,lockUntil=0,wheelAcc=0;
  function paintSnap(i){
    var cards=[].slice.call(document.querySelectorAll('.hx-card'));
    snapIndex=Math.max(0,Math.min(cards.length-1,i));
    cards.forEach(function(card,n){
      card.classList.toggle('is-on',n===snapIndex);
      card.classList.toggle('is-prev',n<snapIndex);
      card.classList.toggle('is-next',n>snapIndex);
    });
    var zone=document.getElementById('hx-pin');
    if(zone)zone.dataset.step=String(snapIndex);
    [].slice.call(document.querySelectorAll('.hx-dot')).forEach(function(a,n){
      var on=n===snapIndex;a.setAttribute('aria-selected',on?'true':'false');if(on)a.setAttribute('tabindex','0');else a.setAttribute('tabindex','-1');
    });
    var live=document.querySelector('.hx-step-live');
    if(live)live.textContent='Đang xem concept '+(snapIndex+1)+' trên '+cards.length;
  }
  function flashEdge(){
    var edge=document.querySelector('.hx-edge');if(!edge)return;
    edge.classList.remove('is-flash');void edge.offsetWidth;edge.classList.add('is-flash');
  }
  function goSnap(i){
    var cards=document.querySelectorAll('.hx-card');
    var n=Math.max(0,Math.min(cards.length-1,i));
    if(n===snapIndex)return;
    paintSnap(n);flashEdge();
  }
  function snapEngaged(){
    var zone=document.getElementById('hx-pin');if(!zone)return false;
    var r=zone.getBoundingClientRect();
    var head=document.querySelector('body.home > header');
    var line=head?head.getBoundingClientRect().height:72;
    return r.top<=line+40&&r.bottom>=window.innerHeight*0.5;
  }
  function onWheel(e){
    if(!d.classList.contains('fx-snap'))return;
    if(e.ctrlKey)return;
    var dy=e.deltaY;
    if(e.deltaMode===1)dy*=16;else if(e.deltaMode===2)dy*=window.innerHeight||800;
    if(!dy||Math.abs(e.deltaX)>Math.abs(dy))return;
    if(!snapEngaged()){wheelAcc=0;return;}
    var now=performance.now();
    if(now<lockUntil){e.preventDefault();return;}
    var cards=document.querySelectorAll('.hx-card');
    var last=cards.length-1;
    var dir=dy>0?1:-1;
    if((dir>0&&snapIndex>=last)||(dir<0&&snapIndex<=0)){wheelAcc=0;return;}
    e.preventDefault();
    wheelAcc+=dy;
    if(Math.abs(wheelAcc)<40)return;
    wheelAcc=0;
    goSnap(snapIndex+dir);
    lockUntil=now+700;
  }
  function bindSnap(){
    var on=snapWanted();
    d.classList.toggle('fx-snap',on);
    if(on)paintSnap(snapIndex);
    if(on&&!snapBound){window.addEventListener('wheel',onWheel,{passive:false,capture:true});snapBound=true;}
    if(!on&&snapBound){window.removeEventListener('wheel',onWheel,{capture:true});snapBound=false;}
  }
  [].slice.call(document.querySelectorAll('.hx-dot')).forEach(function(a){
    a.addEventListener('click',function(e){
      if(!d.classList.contains('fx-snap'))return;
      e.preventDefault();
      var i=parseInt(a.getAttribute('data-hx-step')||'0',10);
      goSnap(i);lockUntil=performance.now()+700;wheelAcc=0;
    });
    a.addEventListener('keydown',function(e){
      if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft')return;
      var dots=[].slice.call(document.querySelectorAll('.hx-dot'));
      var i=dots.indexOf(a);if(i<0)return;
      var n=e.key==='ArrowRight'?Math.min(dots.length-1,i+1):Math.max(0,i-1);
      if(n===i)return;
      e.preventDefault();
      if(d.classList.contains('fx-snap')){goSnap(n);lockUntil=performance.now()+700;}
      dots[n].focus();
    });
  });
  bindSnap();
  if(snapMq.addEventListener)snapMq.addEventListener('change',bindSnap);

  var track=document.querySelector('.nw-track');
  if(track){
    var box=track.parentElement;
    if(box)box.classList.add('nw-carousel-ready');
    var prev=document.querySelector('.nw-prev'),next=document.querySelector('.nw-next');
    function pageStep(){
      return Math.max(1, track.clientWidth);
    }
    function syncNav(){
      var max=track.scrollWidth-track.clientWidth;
      var idle=max<=4;
      if(prev){prev.disabled=idle||track.scrollLeft<=4;prev.hidden=idle;}
      if(next){next.disabled=idle||track.scrollLeft>=max-4;next.hidden=idle;}
    }
    function goNews(dir){
      var left=track.scrollLeft+dir*pageStep();
      if(reduce){track.scrollTo({left:left,behavior:'auto'});return;}
      track.style.scrollSnapType='none';
      track.scrollTo({left:left,behavior:'smooth'});
      var restored=false;
      var restore=function(){if(restored)return;restored=true;track.style.scrollSnapType='';track.removeEventListener('scrollend',restore);};
      track.addEventListener('scrollend',restore);
      setTimeout(restore,900);
    }
    if(prev)prev.addEventListener('click',function(){goNews(-1);});
    if(next)next.addEventListener('click',function(){goNews(1);});
    track.addEventListener('scroll',syncNav,{passive:true});
    track.addEventListener('keydown',function(e){
      if(e.key==='ArrowRight'){e.preventDefault();goNews(1);}
      else if(e.key==='ArrowLeft'){e.preventDefault();goNews(-1);}
    });
    addEventListener('resize',syncNav);
    addEventListener('load',syncNav);
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(syncNav);
    if(window.ResizeObserver)new ResizeObserver(syncNav).observe(track);
    syncNav();
  }

  var hud=document.querySelector('.hx-hud');
  if(hud&&'IntersectionObserver' in window){
    var video=hud.querySelector('video');
    var conn=navigator.connection;
    var save=conn&&(conn.saveData||conn.effectiveType==='slow-2g'||conn.effectiveType==='2g');
    var narrow=matchMedia('(max-width:700px)').matches;
    var canPlay=video&&!reduce&&!save&&!narrow;
    if(canPlay){
      new IntersectionObserver(function(es){
        var on=es[0].isIntersecting;
        if(on){
          if(!video.getAttribute('src')&&!video.querySelector('source')){
            var w=document.createElement('source');w.src=video.getAttribute('data-webm');w.type='video/webm';
            var m=document.createElement('source');m.src=video.getAttribute('data-mp4');m.type='video/mp4';
            video.appendChild(w);video.appendChild(m);video.load();
          }
          var p=video.play();
          if(p&&p.then)p.then(function(){hud.classList.add('is-playing');}).catch(function(){});
        }else{video.pause();}
      },{rootMargin:'120px 0px'}).observe(hud);
    }
  }

  var started=false;
  function pin(){
    if(d.classList.contains('fx-snap'))return;
    if(started||reduce||!flag('pin','homePin')||!strong())return;
    if(!document.querySelector('.hx-stack'))return;
    started=true;
    function load(src){return new Promise(function(ok,bad){var s=document.createElement('script');s.src=src;s.onload=ok;s.onerror=function(){started=false;bad();};document.body.appendChild(s);});}
    load('js/vendor/gsap/gsap.min.js?v=0.9.41').then(function(){return load('js/vendor/gsap/ScrollTrigger.min.js?v=0.9.41');}).then(function(){
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
