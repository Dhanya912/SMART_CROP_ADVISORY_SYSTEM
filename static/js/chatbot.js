(function(){
const btn=document.getElementById('chatToggleBtn');const icon=document.getElementById('chatToggleIcon');
const win=document.getElementById('chatWindow');const closeBtn=document.getElementById('chatCloseBtn');
const msgs=document.getElementById('chatMessages');const chipsEl=document.getElementById('chatChips');
const form=document.getElementById('chatForm');const input=document.getElementById('chatInput');
const langSel=document.getElementById('chatLangSelect');
if(!btn) return; // not on this page

let opened=false,greeted=false;

function open(){win.classList.remove('hidden','closing');icon.textContent='✕';opened=true;
  if(!greeted){greeted=true;greet();loadChips();} input.focus();}
function close(){win.classList.add('closing');setTimeout(()=>win.classList.add('hidden'),200);icon.textContent='💬';opened=false;}
btn.addEventListener('click',()=>opened?close():open());
closeBtn.addEventListener('click',close);

function bubble(text,who){const b=document.createElement('div');b.className=`chat-bubble ${who}`;b.textContent=text;msgs.appendChild(b);msgs.scrollTop=msgs.scrollHeight;return b;}
function typing(){const b=document.createElement('div');b.className='chat-bubble bot typing';b.innerHTML='<span></span><span></span><span></span>';msgs.appendChild(b);msgs.scrollTop=msgs.scrollHeight;return b;}

async function greet(){
  const t=typing();
  try{
    const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:'',lang:langSel.value})});
    const d=await r.json();t.remove();bubble(d.reply||"Hi! Ask me anything about your crop advisory.",'bot');
  }catch(e){t.remove();bubble("Hi! I'm here to help with your crop advisory questions.",'bot');}
}

async function loadChips(){
  try{
    const r=await fetch(`/api/chat/chips?lang=${langSel.value}`);const d=await r.json();
    chipsEl.innerHTML='';
    (d.chips||[]).forEach(c=>{
      const b=document.createElement('button');b.type='button';b.className='chat-chip';b.textContent=c.label;
      b.addEventListener('click',()=>send(c.label,c.intent));chipsEl.appendChild(b);
    });
  }catch(e){}
}

async function send(text,intent){
  if(!text||!text.trim()) return;
  bubble(text,'user');input.value='';
  const t=typing();
  try{
    const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({message:text,intent:intent||null,lang:langSel.value})});
    const d=await r.json();t.remove();bubble(d.reply||'Sorry, please try again.','bot');
  }catch(e){t.remove();bubble('Connection issue — please try again.','bot');}
}

form.addEventListener('submit',e=>{e.preventDefault();send(input.value);});
langSel.addEventListener('change',()=>{if(opened){msgs.innerHTML='';greeted=false;greet();greeted=true;loadChips();}});
})();
