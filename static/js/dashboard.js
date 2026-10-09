/* dashboard.js — Individual agent testers */
async function postJSON(url,body){
  try{const res=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),credentials:'include'});
  const json=await res.json();if(!json.success){console.error(json.error);return null;}return json;}
  catch(err){console.error(err);return null;}}
function setLoad(id){const d=document.getElementById(id);d.className='agent-result visible';d.innerHTML='<div style="text-align:center;padding:12px"><div style="width:26px;height:26px;border:3px solid #ccc;border-top-color:var(--leaf);border-radius:50%;animation:spin .8s linear infinite;margin:0 auto 8px"></div><span style="color:var(--leaf);font-size:.85rem">Running agent…</span></div>';}
function showErr(id,msg){const d=document.getElementById(id);d.className='agent-result visible';d.innerHTML=`<p style="color:var(--alert)">❌ ${msg}</p>`;}
function cap(s){return s?s.charAt(0).toUpperCase()+s.slice(1):s;}
function scoreCol(s){return s>=80?'var(--leaf)':s>=60?'#b8860b':s>=40?'var(--sun)':'var(--alert)';}
function trendIcon(t){return{rising:'📈',falling:'📉',stable:'➡️',volatile:'⚡',seasonal:'🔄'}[(t||'').toLowerCase()]||'➡️';}

async function runCropAgent(){
  setLoad('crop-result');
  const data=await postJSON('/api/recommend-crop',{nitrogen:+document.getElementById('cr-n').value,phosphorus:+document.getElementById('cr-p').value,potassium:+document.getElementById('cr-k').value,ph:+document.getElementById('cr-ph').value,temperature:+document.getElementById('cr-temp').value,humidity:70,rainfall:+document.getElementById('cr-rain').value});
  if(!data){showErr('crop-result','Agent failed.');return;}
  const d=data.data;const d2=document.getElementById('crop-result');d2.className='agent-result visible';
  d2.innerHTML=`<div class="res-row"><span class="res-k">Top Crop</span><span class="res-v" style="color:var(--leaf)">⭐ ${cap(d.top_crop)}</span></div>
    <div class="res-row"><span class="res-k">Confidence</span><span class="res-v">${Math.round(d.confidence*100)}%</span></div>
    ${(d.all_crops||[]).slice(1).map((r,i)=>`<div class="res-row"><span class="res-k">#${i+2}</span><span class="res-v">${cap(r.crop)} (${Math.round(r.confidence*100)}%)</span></div>`).join('')}
    <div style="margin-top:8px;font-size:.78rem;color:#666">Top factors: ${Object.entries(d.feature_importance||{}).sort((a,b)=>b[1]-a[1]).slice(0,3).map(([k,v])=>`${k}: <b>${v}%</b>`).join(' | ')}</div>`;}

async function runWeatherAgent(){
  setLoad('weather-result');
  const data=await postJSON('/api/weather',{location:document.getElementById('wx-loc').value});
  if(!data){showErr('weather-result','Agent failed.');return;}
  const d=data.data;const el=document.getElementById('weather-result');el.className='agent-result visible';
  el.innerHTML=`<div class="res-row"><span class="res-k">Condition</span><span class="res-v">⛅ ${d.condition}</span></div>
    <div class="res-row"><span class="res-k">Temperature</span><span class="res-v">${d.temperature}°C</span></div>
    <div class="res-row"><span class="res-k">Humidity</span><span class="res-v">${d.humidity}%</span></div>
    <div class="res-row"><span class="res-k">Wind</span><span class="res-v">${d.wind_speed} km/h</span></div>
    <div class="res-row"><span class="res-k">Rainfall</span><span class="res-v">${d.rainfall_mm} mm</span></div>
    <div style="margin-top:8px;font-size:.82rem;color:var(--leaf);font-weight:600">${(d.advisory||[])[0]||'No advisory.'}</div>`;}

async function runSoilAgent(){
  setLoad('soil-result');
  const data=await postJSON('/api/soil-health',{nitrogen:+document.getElementById('sh-n').value,phosphorus:+document.getElementById('sh-p').value,potassium:+document.getElementById('sh-k').value,ph:+document.getElementById('sh-ph').value,crop:document.getElementById('sh-crop').value});
  if(!data){showErr('soil-result','Agent failed.');return;}
  const d=data.data;const el=document.getElementById('soil-result');el.className='agent-result visible';
  el.innerHTML=`<div class="res-row"><span class="res-k">Health Score</span><span class="res-v" style="color:${scoreCol(d.health_score)}">${d.health_score}/100 — ${d.overall_health}</span></div>
    <div class="res-row"><span class="res-k">Nitrogen</span><span class="res-v">${d.nitrogen} kg/ha <small>(${d.nitrogen_status})</small></span></div>
    <div class="res-row"><span class="res-k">Phosphorus</span><span class="res-v">${d.phosphorus} kg/ha <small>(${d.phosphorus_status})</small></span></div>
    <div class="res-row"><span class="res-k">Potassium</span><span class="res-v">${d.potassium} kg/ha <small>(${d.potassium_status})</small></span></div>
    <div class="res-row"><span class="res-k">pH</span><span class="res-v">${d.ph} <small>(${d.ph_status})</small></span></div>
    <div style="margin-top:8px;font-size:.82rem;color:#555">${(d.amendments||[])[0]||''}</div>`;}

async function runMarketAgent(){
  setLoad('market-result');
  const data=await postJSON('/api/market-prices',{crop:document.getElementById('mk-crop').value,location:document.getElementById('mk-loc').value,area:1});
  if(!data){showErr('market-result','Agent failed.');return;}
  const d=data.data;const el=document.getElementById('market-result');el.className='agent-result visible';
  el.innerHTML=`<div class="res-row"><span class="res-k">Avg Price</span><span class="res-v">₹${d.avg_price_quintal}/quintal</span></div>
    <div class="res-row"><span class="res-k">Range</span><span class="res-v">₹${d.min_price_quintal}–₹${d.max_price_quintal}</span></div>
    <div class="res-row"><span class="res-k">Trend</span><span class="res-v">${trendIcon(d.price_trend)} ${d.price_trend}</span></div>
    <div class="res-row"><span class="res-k">Best Market</span><span class="res-v">${d.best_market}</span></div>
    <div class="res-row"><span class="res-k">Net Income (1ha)</span><span class="res-v" style="color:var(--leaf)">₹${(d.net_income_inr||0).toLocaleString()}</span></div>
    <div style="margin-top:8px;font-size:.82rem;color:#555">${(d.advisory||[])[0]||''}</div>`;}

async function runPolicyAgent(){
  setLoad('policy-result');
  const data=await postJSON('/api/policy',{crop:document.getElementById('po-crop').value,state:document.getElementById('po-state').value});
  if(!data){showErr('policy-result','Agent failed.');return;}
  const d=data.data;const el=document.getElementById('policy-result');el.className='agent-result visible';
  const msp=d.msp||{};
  el.innerHTML=`${msp.msp?`<div class="res-row"><span class="res-k">MSP ${msp.year}</span><span class="res-v">₹${msp.msp}/${msp.unit||'quintal'}</span></div>`:''}
    <div class="res-row"><span class="res-k">Schemes</span><span class="res-v">${(d.schemes||[]).length} schemes found</span></div>
    ${(d.schemes||[]).slice(0,3).map(s=>`<div style="margin-top:6px"><div style="font-size:.82rem;font-weight:700;color:var(--leaf)">✅ ${s.name}</div><div style="font-size:.78rem;color:#555;margin-top:2px">${s.benefit}</div></div>`).join('')}
    <div style="margin-top:10px;font-size:.8rem;color:var(--leaf);font-weight:700">📞 ${d.helpline||'1800-180-1551'}</div>`;}

async function runDiseaseAgent(){
  const file=document.getElementById('dd-image').files[0];
  if(!file){showErr('disease-result','Please select a leaf image first.');return;}
  setLoad('disease-result');
  const fd=new FormData();fd.append('image',file);fd.append('crop_type',document.getElementById('dd-crop').value);
  try{const res=await fetch('/api/detect-disease',{method:'POST',body:fd,credentials:'include'});
  const json=await res.json();if(!json.success){showErr('disease-result',json.error);return;}
  const d=json.data;const healthy=d.status==='healthy';
  const el=document.getElementById('disease-result');el.className='agent-result visible';
  el.innerHTML=`<div class="res-row"><span class="res-k">Disease</span><span class="res-v" style="color:${healthy?'var(--leaf)':'var(--alert)'}">${d.disease_name}</span></div>
    <div class="res-row"><span class="res-k">Severity</span><span class="res-v">${d.severity}</span></div>
    <div class="res-row"><span class="res-k">Confidence</span><span class="res-v">${Math.round(d.confidence*100)}%</span></div>
    <div class="res-row"><span class="res-k">Cause</span><span class="res-v" style="font-size:.78rem">${d.cause}</span></div>
    ${!healthy&&(d.treatment||[]).length?`<div style="margin-top:8px;font-size:.82rem"><b>Treatment:</b><br/>${d.treatment.slice(0,2).join('<br/>')}</div>`:''}`;
  }catch(err){showErr('disease-result',err.message);}
}

document.getElementById('dd-image')?.addEventListener('change',function(){
  const prev=document.getElementById('dd-preview'),ph=document.getElementById('dd-ph');
  if(this.files[0]){prev.src=URL.createObjectURL(this.files[0]);prev.style.display='block';if(ph)ph.style.display='none';}});
