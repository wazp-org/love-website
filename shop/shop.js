/* Love and Beauty — Website Shop.
   Browse, search, filter, product view, basket (kept in this browser) and checkout.
   Card payments: when LB_CONF.gateway.live is true, checkout hands the order to
   LB_PAY (Barclaycard gateway hook, below). Until then customers place the order
   by email and pay the exact total by PayPal. */
(function(){
  var ITEMS=window.LB_ITEMS||[], CONF=window.LB_CONF||{}, CATS=window.LB_CATS||{};
  var GW=CONF.gateway||{}, LIVE=!!GW.live, ND=Number(CONF.nextDay||4.99);
  var PAGE=40, $=function(id){return document.getElementById(id);};
  var byId={}; ITEMS.forEach(function(x){byId[x.i]=x;});
  var st={q:'',c:'',b:'',max:0,sort:'',shown:PAGE};
  function money(v){return '£'+Number(v).toFixed(2);}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function img(x,s){return x.m?'/images/shop/'+x.m:'https://i.ebayimg.com/images/g/'+x.g+'/s-l'+(s||500)+'.jpg';}
  function store(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k)||'null');localStorage.setItem(k,JSON.stringify(v));}catch(e){}}

  /* age gate */
  var gate=$('age-gate'); if(!store('lb_age')) gate.hidden=false;
  $('gate-enter').onclick=function(){gate.hidden=true;store('lb_age',1);};

  /* ---------- browsing ---------- */
  var words=function(s){return s.toLowerCase().replace(/[^a-z0-9£.]+/g,' ').trim().split(' ').filter(Boolean);};
  ITEMS.forEach(function(x){x._s=(x.t+' '+x.b+' '+(CATS[x.c]||'')).toLowerCase();});
  function list(){
    var w=words(st.q), r=ITEMS.filter(function(x){
      if(st.c&&x.c!==st.c) return false;
      if(st.b&&x.b!==st.b) return false;
      if(st.max&&x.p>st.max) return false;
      for(var i=0;i<w.length;i++) if(x._s.indexOf(w[i])<0) return false;
      return true;});
    if(st.sort==='low') r.sort(function(a,b){return a.p-b.p;});
    else if(st.sort==='high') r.sort(function(a,b){return b.p-a.p;});
    else if(st.sort==='az') r.sort(function(a,b){return a.t.localeCompare(b.t);});
    r.sort(function(a,b){return (a.o?1:0)-(b.o?1:0);});
    return r;
  }
  function card(x){
    var off=x.p<x.w, tag=x.o?'<span class="c-tag out">Sold out</span>':(off?'<span class="c-tag">15% OFF</span>':'');
    return '<article class="card" data-id="'+x.i+'"><div class="c-img" data-open>'+tag+'<img src="'+img(x)+'" alt="'+esc(x.t)+'" loading="lazy" width="500" height="500"></div>'+
      '<div class="c-body"><div class="c-brand">'+esc(x.b||CATS[x.c]||'')+'</div><h3 class="c-t" data-open>'+esc(x.t)+'</h3>'+
      '<div class="c-p"><b>'+money(x.p)+'</b>'+(off?'<s>'+money(x.w)+'</s>':'')+'</div>'+
      (x.o?'<button class="c-add" disabled>Sold out</button>':'<button class="c-add" data-add>Add to basket</button>')+'</div></article>';
  }
  var GRID=$('grid');
  function render(keep){
    if(!GRID) return;
    var r=list(); if(!keep) st.shown=PAGE;
    $('grid').innerHTML=r.slice(0,st.shown).map(card).join('');
    $('count').textContent=r.length; $('count-l').textContent=r.length===1?'product':'products';
    $('empty').hidden=r.length>0; $('more').hidden=r.length<=st.shown;
    $('more').textContent='Show more ('+(r.length-st.shown)+' left)';
    [].forEach.call(document.querySelectorAll('.tile'),function(t){t.setAttribute('aria-pressed',t.dataset.c===st.c?'true':'false');});
    var a=[]; if(st.c) a.push(['c',CATS[st.c]]); if(st.b) a.push(['b',st.b]); if(st.max) a.push(['max','Under '+money(st.max)]); if(st.q) a.push(['q','“'+st.q+'”']);
    $('active').innerHTML=a.map(function(f){return '<button class="chip" data-clear="'+f[0]+'">'+esc(f[1])+' <span>×</span></button>';}).join('')+(a.length>1?'<button class="lnk" data-clear="all">Clear all</button>':'');
    try{var u=new URL(location.href);['c','b','q'].forEach(function(k){st[k]?u.searchParams.set(k,st[k]):u.searchParams.delete(k);});history.replaceState(null,'',u.pathname+u.search+location.hash);}catch(e){}
  }
  function toTop(){var b=$('bar'); if(b.getBoundingClientRect().top<0) window.scrollTo({top:b.offsetTop-70,behavior:'smooth'});}
  if(!GRID){ $('q').addEventListener('keydown',function(e){if(e.key==='Enter'&&this.value.trim()){location.href='/shop/?q='+encodeURIComponent(this.value.trim());}}); }
  if(GRID){
  var tq; $('q').addEventListener('input',function(){ $('q-x').hidden=!this.value; clearTimeout(tq); var v=this.value; tq=setTimeout(function(){st.q=v.trim();render();},160);});
  $('q').addEventListener('keydown',function(e){if(e.key==='Enter'){this.blur();toTop();}});
  $('q-x').onclick=function(){$('q').value='';this.hidden=true;st.q='';render();};
  $('sort').onchange=function(){st.sort=this.value;render();};
  $('more').onclick=function(){st.shown+=PAGE;render(true);};
  $('reset').onclick=function(){clearAll();};
  function clearAll(){st.q='';st.c='';st.b='';st.max=0;$('q').value='';$('q-x').hidden=true;render();}
  document.querySelector('.tiles').addEventListener('click',function(e){var t=e.target.closest('.tile');if(!t)return;st.c=(st.c===t.dataset.c?'':t.dataset.c);render();toTop();});
  $('active').addEventListener('click',function(e){var c=e.target.closest('[data-clear]');if(!c)return;var k=c.dataset.clear;if(k==='all')return clearAll();if(k==='q'){$('q').value='';$('q-x').hidden=true;}st[k]=k==='max'?0:'';render();});

  /* filter sheet (brand + price) */
  $('filter-open').onclick=function(){
    var pool=ITEMS.filter(function(x){return !st.c||x.c===st.c;}), bc={};
    pool.forEach(function(x){if(x.b)bc[x.b]=(bc[x.b]||0)+1;});
    var brands=Object.keys(bc).sort(function(a,b){return bc[b]-bc[a];});
    var ov=document.createElement('div'); ov.className='ov'; ov.id='flt';
    ov.innerHTML='<div class="sheet co" role="dialog" aria-modal="true" aria-label="Filter"><button class="x" data-close aria-label="Close">×</button><h2>Filter</h2>'+
      '<p class="small" style="margin:6px 0 8px;font-weight:700;color:#1b1320">Price</p><div class="row" id="f-price">'+[0,15,25,50,100].map(function(v){return '<button class="b b-sm '+(st.max===v?'b-gold':'b-line')+'" data-max="'+v+'">'+(v?'Under £'+v:'Any')+'</button>';}).join('')+'</div>'+
      '<p class="small" style="margin:16px 0 8px;font-weight:700;color:#1b1320">Brand</p><div class="row" id="f-brand" style="flex-wrap:wrap">'+
      '<button class="b b-sm '+(!st.b?'b-gold':'b-line')+'" data-b="" style="flex:0 0 auto">All brands</button>'+brands.map(function(b){return '<button class="b b-sm '+(st.b===b?'b-gold':'b-line')+'" data-b="'+esc(b)+'" style="flex:0 0 auto">'+esc(b)+' ('+bc[b]+')</button>';}).join('')+'</div>'+
      '<button class="b b-gold b-big" data-close style="margin-top:20px">Show results</button></div>';
    document.body.appendChild(ov); lock(true);
    ov.addEventListener('click',function(e){
      var m=e.target.closest('[data-max]'), b=e.target.closest('[data-b]');
      if(m){st.max=Number(m.dataset.max);[].forEach.call(ov.querySelectorAll('[data-max]'),function(x){x.className='b b-sm '+(x===m?'b-gold':'b-line');});render();}
      if(b){st.b=b.dataset.b;[].forEach.call(ov.querySelectorAll('[data-b]'),function(x){x.className='b b-sm '+(x===b?'b-gold':'b-line');});render();}
      if(e.target===ov||e.target.closest('[data-close]')){ov.remove();lock(false);toTop();}
    });
  };

  }

  /* rails (The Unseen): rows of cards from window.LB_RAILS */
  function railCard(x,badge){
    var h=card(x); var b=[];
    if(badge) b.push('<span class="u-badge">'+esc(badge)+'</span>');
    if(x.q===1) b.push('<span class="u-badge u-last">Only 1 left</span>');
    else if(x.q&&x.q<=3) b.push('<span class="u-badge u-last">Only '+x.q+' left</span>');
    return h.replace(/<span class="c-tag">15% OFF<\/span>/,'').replace('<div class="c-img" data-open>','<div class="c-img" data-open><div class="u-badges">'+b.join('')+'</div>');
  }
  [].forEach.call(document.querySelectorAll('[data-rail]'),function(el){
    var R=(window.LB_RAILS||{})[el.dataset.rail]; if(!R) return;
    el.innerHTML=R.ids.map(function(i){return byId[i]?railCard(byId[i],R.badge):'';}).join('');
  });
  [].forEach.call(document.querySelectorAll('[data-scroll]'),function(b){b.onclick=function(){var r=document.querySelector('[data-rail="'+b.dataset.scroll+'"]');r.scrollBy({left:(b.dataset.dir==='l'?-1:1)*r.clientWidth*0.85,behavior:'smooth'});};});

  /* ---------- product view ---------- */
  var cur=null, pq=1;
  function lock(on){document.body.style.overflow=on?'hidden':'';}
  function openP(id){
    var x=byId[id]; if(!x) return; cur=x; pq=1;
    $('pv-img').src=x.m?img(x):img(x,1600); $('pv-img').alt=x.t;
    $('pv-b').textContent=x.b||CATS[x.c]||''; $('pv-t').textContent=x.t;
    $('pv-p').textContent=money(x.p); var off=x.p<x.w;
    $('pv-w').textContent=off?money(x.w):''; $('pv-s').textContent=off?'Save '+money(x.w-x.p):''; $('pv-s').hidden=!off;
    $('pv-q').textContent='1'; $('pv-opt').value='';
    $('pv-opt-l').hidden=!/\b(s|m|l|xl|xxl|[2-4]xl|s-xl|s\/m|m\/l|l\/xl|one size|size|colou?r|black|pink|purple|red|blue)\b/i.test(x.t);
    $('pv-add').disabled=!!x.o; $('pv-add').textContent=x.o?'Sold out':'Add to basket · '+money(x.p);
    $('pv-ebay').href='https://www.ebay.co.uk/itm/'+x.i;
    $('pv').hidden=false; lock(true);
    try{history.replaceState(null,'','#p'+x.i);}catch(e){}
  }
  function closeOv(ov){ov.hidden=true;lock(false); if(ov.id==='pv'){try{history.replaceState(null,'',location.pathname+location.search);}catch(e){}}}
  document.addEventListener('click',function(e){
    var c=e.target.closest&&e.target.closest('.card'); if(!c||c.closest('.ov')) return;
    if(e.target.closest('[data-add]')){ add(c.dataset.id,1,''); var b=e.target.closest('[data-add]'); b.textContent='Added ✓'; b.classList.add('done'); setTimeout(function(){b.textContent='Add to basket';b.classList.remove('done');},1600); return; }
    if(e.target.closest('[data-open]')) openP(c.dataset.id);
  });
  $('pv').addEventListener('click',function(e){var q=e.target.closest('[data-q]'); if(q){pq=Math.max(1,Math.min(9,pq+Number(q.dataset.q)));$('pv-q').textContent=pq;$('pv-add').textContent='Add to basket · '+money(cur.p*pq);}});
  $('pv-add').onclick=function(){ if(!cur||cur.o) return; add(cur.i,pq,$('pv-opt').value.trim()); closeOv($('pv')); };

  /* ---------- basket ---------- */
  var bag=store('lb_bag')||[];
  bag=bag.filter(function(l){return byId[l.i]&&!byId[l.i].o;});
  function save(){store('lb_bag',bag); var n=bag.reduce(function(s,l){return s+l.q;},0); var el=$('bag-n'); el.hidden=!n; el.textContent=n; el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop');}
  function add(id,q,opt){
    var l=bag.filter(function(l){return l.i===id&&l.o===opt;})[0];
    if(l) l.q=Math.min(9,l.q+q); else bag.push({i:id,q:q,o:opt});
    save(); toast(byId[id].t.slice(0,38)+(byId[id].t.length>38?'…':'')+' added');
  }
  function ship(){var r=document.querySelector('input[name=ship]:checked');return r&&r.value==='nd'?ND:0;}
  function sub(){return bag.reduce(function(s,l){return s+byId[l.i].p*l.q;},0);}
  function drawBag(){
    if(!bag.length){$('bag-list').innerHTML='<div class="side-empty"><p><b>Your basket is empty</b></p><p class="small">Tap “Add to basket” on anything you like.</p></div>';$('bag-f').hidden=true;return;}
    $('bag-f').hidden=false;
    $('bag-list').innerHTML=bag.map(function(l,k){var x=byId[l.i];return '<div class="li"><img src="'+img(x,300)+'" alt=""><div><div class="li-t">'+esc(x.t)+'</div>'+(l.o?'<div class="li-o">'+esc(l.o)+'</div>':'')+
      '<div class="qty"><button data-k="'+k+'" data-d="-1" aria-label="Less">−</button><span>'+l.q+'</span><button data-k="'+k+'" data-d="1" aria-label="More">+</button></div></div>'+
      '<div class="li-r">'+money(x.p*l.q)+'<button data-rm="'+k+'">Remove</button></div></div>';}).join('');
    $('bag-tot').textContent=money(sub()+ship());
  }
  function openBag(){drawBag();$('bag').hidden=false;lock(true);}
  $('bag-open').onclick=openBag;
  $('bag-list').addEventListener('click',function(e){
    var d=e.target.closest('[data-d]'), r=e.target.closest('[data-rm]');
    if(d){var l=bag[d.dataset.k]; l.q=Math.max(0,Math.min(9,l.q+Number(d.dataset.d))); if(!l.q) bag.splice(d.dataset.k,1);}
    if(r) bag.splice(r.dataset.rm,1);
    if(d||r){save();drawBag();}
  });
  [].forEach.call(document.querySelectorAll('input[name=ship]'),function(r){r.onchange=drawBag;});

  /* ---------- checkout ---------- */
  var ref='';
  function orderText(f){
    var L=bag.map(function(l){var x=byId[l.i];return l.q+' × '+x.t+(l.o?' ('+l.o+')':'')+' – '+money(x.p*l.q)+'  [ref '+x.i+']';});
    return 'Order '+ref+'\n\n'+L.join('\n')+'\n\nDelivery: '+(ship()?'Evri Next Day '+money(ND):'Evri Tracked (free)')+'\nTOTAL: '+money(sub()+ship())+
      '\n\nName: '+f.first.value+' '+f.last.value+'\nEmail: '+f.email.value+'\nPhone: '+f.phone.value+'\nAddress: '+[f.addr1.value,f.addr2.value,f.town.value,f.postcode.value].filter(Boolean).join(', ')+'\n\nI confirm I am 18 or over.';
  }
  $('go-checkout').onclick=function(){
    ref='LB'+Date.now().toString(36).toUpperCase().slice(-6);
    $('bag').hidden=true;
    $('co-sum').innerHTML=bag.map(function(l){var x=byId[l.i];return '<div class="tl"><span>'+l.q+' × '+esc(x.t)+'</span><b>'+money(x.p*l.q)+'</b></div>';}).join('')+
      '<div class="tl"><span>Delivery: '+(ship()?'Evri Next Day':'Evri Tracked')+'</span><b>'+(ship()?money(ND):'FREE')+'</b></div><div class="tl gt"><span>Total</span><b>'+money(sub()+ship())+'</b></div>';
    $('express').hidden=!LIVE; $('co-alt').hidden=LIVE;
    $('co-pay').textContent=LIVE?'Pay '+money(sub()+ship())+' securely':'Place order · '+money(sub()+ship());
    var saved=store('lb_addr'); if(saved){var f=$('co-form');Object.keys(saved).forEach(function(k){if(f[k]&&f[k].type!=='checkbox')f[k].value=saved[k];});}
    $('co').hidden=false; lock(true);
  };
  $('co-form').addEventListener('submit',function(e){
    e.preventDefault(); var f=this, keep={};
    ['first','last','email','phone','addr1','addr2','town','postcode'].forEach(function(k){keep[k]=f[k].value;}); store('lb_addr',keep);
    var order={ref:ref,items:bag.map(function(l){var x=byId[l.i];return {id:x.i,title:x.t,option:l.o,qty:l.q,price:x.p};}),delivery:ship()?'evri-next-day':'evri-tracked',deliveryCost:ship(),total:Math.round((sub()+ship())*100)/100,customer:keep};
    if(LIVE&&window.LB_PAY){ window.LB_PAY(order,'card'); return; }
    var mail='mailto:'+CONF.email+'?subject='+encodeURIComponent('Website order '+ref+' – '+money(order.total))+'&body='+encodeURIComponent(orderText(f));
    location.href=mail; showDone(order);
  });
  $('express').addEventListener('click',function(e){var p=e.target.closest('[data-pay]'); if(p&&window.LB_PAY){var f=$('co-form'); if(!f.reportValidity())return; f.requestSubmit?0:0; window.LB_PAY({ref:ref,total:Math.round((sub()+ship())*100)/100},p.dataset.pay);}});
  function showDone(o){
    var pp=CONF.paypal?'https://www.paypal.com/paypalme/'+encodeURIComponent(CONF.paypal)+'/'+o.total.toFixed(2)+'GBP':'';
    $('co-form').innerHTML='<div class="done-msg"><h3>Nearly done!</h3><p>Your order <b>'+o.ref+'</b> has opened in your email app – just press send.</p>'+
      (pp?'<p style="margin:14px 0">Then pay the total of <b>'+money(o.total)+'</b>:</p><a class="b b-gold b-big" href="'+pp+'" target="_blank" rel="noopener">Pay '+money(o.total)+' with PayPal</a><p class="small" style="margin-top:8px">Put <b>'+o.ref+'</b> in the PayPal note.</p>':'<p>We\'ll reply with a payment link.</p>')+
      '<p class="small" style="margin-top:14px">Email didn\'t open? Send your order to <a href="mailto:'+CONF.email+'">'+CONF.email+'</a>.</p></div>';
    bag=[]; save();
  }

  /* close buttons, Esc, toast */
  document.addEventListener('click',function(e){
    var ov=e.target.classList&&e.target.classList.contains('ov')?e.target:null;
    var c=e.target.closest&&e.target.closest('[data-close]');
    if(c&&!c.closest('#flt')) ov=c.closest('.ov');
    if(ov&&ov.id!=='flt') closeOv(ov);
  });
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){[].forEach.call(document.querySelectorAll('.ov'),function(o){if(o.id==='flt'){o.remove();lock(false);}else if(!o.hidden)closeOv(o);});}});
  var tt; function toast(m){var t=$('toast');t.innerHTML='<span>'+esc(m)+'</span> <button type="button">View basket</button>';t.hidden=false;t.querySelector('button').onclick=function(){t.hidden=true;openBag();};clearTimeout(tt);tt=setTimeout(function(){t.hidden=true;},2600);}

  /* start */
  try{var u=new URL(location.href);st.c=CATS[u.searchParams.get('c')]?u.searchParams.get('c'):'';st.b=u.searchParams.get('b')||u.searchParams.get('brand')||'';st.q=u.searchParams.get('q')||'';if(st.q){$('q').value=st.q;$('q-x').hidden=false;}}catch(e){}
  if(st.b&&!ITEMS.some(function(x){return x.b===st.b;})){var m=ITEMS.filter(function(x){return x.b&&x.b.toLowerCase().replace(/[^a-z0-9]+/g,'-')===st.b;})[0];st.b=m?m.b:'';}
  save(); render();
  var h=location.hash.match(/^#p(\d+)/); if(h) openP(h[1]);
})();
