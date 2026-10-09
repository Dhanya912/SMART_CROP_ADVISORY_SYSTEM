/* main.js — Advisory Form + Report Renderer + PDF Download */
let _lastReport = null;

document.getElementById('imgInput')?.addEventListener('change', function () {
  const prev = document.getElementById('imgPreview');
  const ph   = document.getElementById('uploadPH');
  if (this.files[0]) {
    prev.src = URL.createObjectURL(this.files[0]);
    prev.style.display = 'block'; ph.style.display = 'none';
  }
});

document.getElementById('advisoryForm')?.addEventListener('submit', async function (e) {
  e.preventDefault();
  const btn     = document.getElementById('submitBtn');
  const loading = document.getElementById('loading');
  const result  = document.getElementById('result');
  const fab     = document.getElementById('pdfFab');
  btn.disabled  = true; btn.textContent = '⏳ Running AI Agents…';
  loading.style.display = 'block'; result.style.display = 'none';
  if (fab) fab.style.display = 'none';

  const AGENTS = ['🌾 Crop Recommendation Agent','⛅ Weather Analysis Agent','📈 Market Intelligence Agent',
                  '🔬 Disease Detection Agent','🪨 Soil Health Agent','📜 Policy Advisory Agent','📋 Report Generation Agent'];
  const prog = document.getElementById('agentProgress');
  prog.innerHTML = AGENTS.map((a,i) => `<div class="prog-item" id="prog-${i}">${a}</div>`).join('');
  document.getElementById('loadingText').textContent = 'Initialising agent pipeline…';

  for (let i = 0; i < AGENTS.length; i++) {
    const el = document.getElementById(`prog-${i}`);
    el.classList.add('running');
    document.getElementById('loadingText').textContent = `Running: ${AGENTS[i]}`;
    await new Promise(r => setTimeout(r, 500));
    el.classList.remove('running'); el.classList.add('done');
  }
  document.getElementById('loadingText').textContent = 'Compiling advisory report…';

  try {
    const fd  = new FormData(e.target);
    const res = await fetch('/api/full-advisory', { method: 'POST', body: fd, credentials: 'include' });
    const json = await res.json();
    loading.style.display = 'none';
    if (json.success) {
      _lastReport = json.data;
      renderReport(json.data);
      if (fab) fab.style.display = 'block';
    } else {
      result.innerHTML = `<div class="error-box">❌ ${json.error || 'Unknown error'}</div>`;
      result.style.display = 'block';
    }
  } catch (err) {
    loading.style.display = 'none';
    result.innerHTML = `<div class="error-box">❌ Network error: ${err.message}</div>`;
    result.style.display = 'block';
  } finally {
    btn.disabled = false; btn.textContent = '🚀 Generate Full Advisory Report';
    document.getElementById('result').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
});

async function downloadPDF() {
  if (!_lastReport) { alert('No report yet. Generate advisory first.'); return; }
  const btn = document.getElementById('pdfFab');
  btn.textContent = '⏳ Generating PDF…'; btn.disabled = true;
  try {
    const aid = _lastReport.advisory_id;
    const url = aid ? `/api/download-pdf/${aid}` : '/api/download-latest-pdf';
    const opts = aid
      ? { credentials: 'include' }
      : { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'include', body: JSON.stringify({ report: _lastReport }) };
    const res  = await fetch(url, opts);
    if (!res.ok) throw new Error('Server error');
    const blob = await res.blob();
    const a    = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `CropAI_Advisory_${new Date().toISOString().slice(0,10)}.pdf`;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(a.href);
    btn.textContent = '✅ Downloaded!';
    setTimeout(() => { btn.textContent = '📄 Download PDF'; btn.disabled = false; }, 3000);
  } catch (err) {
    btn.textContent = '❌ Failed — Retry'; btn.disabled = false;
  }
}

/* ── REPORT RENDERER ──────────────────────────────────────────────────── */
function renderReport(data) {
  const secs = data.sections || {};
  const el   = document.getElementById('result');
  el.style.display = 'block';
  el.innerHTML = `
    <div class="report-wrap">
      <div class="report-header">
        <div class="report-title">📋 ${data.title || 'Smart Crop Advisory Report'}</div>
        <div class="report-meta">📍 ${data.location || ''} &nbsp;|&nbsp; 📅 ${data.generated_at || ''} &nbsp;|&nbsp; ⏱ ${data.processing_time_s}s</div>
      </div>
      <div class="exec-summary">${data.executive_summary || ''}</div>
      <div class="pdf-bar">
        <div class="pdf-bar-left"><span class="pdf-icon">📄</span>
          <div><strong>Your advisory report is ready</strong>
            <span>Save it as a PDF to read offline or share with your agronomist</span></div></div>
        <button class="pdf-btn" id="pdfBarBtn" onclick="downloadPDF()">⬇ Download PDF Report</button>
      </div>
      <div class="report-grid">
        ${renderCropCard(secs.crop_recommendation)}
        ${renderDiseaseCard(secs.disease_detection)}
        ${renderWeatherCard(secs.weather_analysis)}
        ${renderSoilCard(secs.soil_health)}
        ${renderMarketCard(secs.market_intelligence)}
        ${renderPolicyCard(secs.policy_advisory)}
      </div>
      ${renderCharts()}
      ${renderActionPlan(data.action_plan)}
      ${data.tamil_summary ? renderTamil(data.tamil_summary) : ''}
    </div>`;
  drawCharts(data);
}

function renderCharts(){
  return `<div class="report-wrap" style="margin-top:22px">
    <div class="report-header"><div class="report-title">\u{1F4CA} Visual Analysis</div></div>
    <div class="chart-grid">
      <div class="chart-box"><h4>Crop Suitability</h4><canvas id="chCrop"></canvas></div>
      <div class="chart-box"><h4>Disease Likelihood</h4><canvas id="chDis"></canvas></div>
      <div class="chart-box"><h4>Soil Nutrients (N-P-K)</h4><canvas id="chSoil"></canvas></div>
      <div class="chart-box"><h4>Soil Health Score</h4><canvas id="chScore"></canvas></div>
      <div class="chart-box"><h4>Weather Snapshot</h4><canvas id="chWx"></canvas></div>
      <div class="chart-box"><h4>Leaf Colour Evidence</h4><canvas id="chLeaf"></canvas></div>
    </div></div>`;
}

let _charts=[];
function mk(id,cfg){const c=document.getElementById(id);if(!c)return;_charts.push(new Chart(c,cfg));}
function drawCharts(data){
  if(typeof Chart==='undefined')return;
  _charts.forEach(c=>{try{c.destroy()}catch(e){}});_charts=[];
  const s=data.sections||{},G='#2d6a4f',R='#e63946',B='#1b4965',Y='#e9c46a';
  const base={responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}}};
  const crops=(s.crop_recommendation&&s.crop_recommendation.all_crops||[]).slice(0,5);
  mk('chCrop',{type:'bar',data:{labels:crops.map(c=>c.crop_display||c.crop),
    datasets:[{data:crops.map(c=>Math.round(c.confidence<=1?c.confidence*100:c.confidence)),backgroundColor:G,borderRadius:6}]},
    options:Object.assign({},base,{scales:{y:{beginAtZero:true,max:100}}})});
  const t3=(s.disease_detection&&s.disease_detection.top3)||[];
  mk('chDis',{type:'doughnut',data:{labels:t3.map(t=>t.disease),
    datasets:[{data:t3.map(t=>t.confidence),backgroundColor:[R,Y,B]}]},
    options:Object.assign({},base,{plugins:{legend:{display:true,position:'bottom',labels:{boxWidth:12,font:{size:10}}}}})});
  const so=s.soil_health||{};
  mk('chSoil',{type:'bar',data:{labels:['N','P','K','pH x10'],
    datasets:[{data:[so.nitrogen||0,so.phosphorus||0,so.potassium||0,(so.ph||0)*10],
      backgroundColor:['#40916c','#b8860b','#1b4965','#6b4226'],borderRadius:6}]},options:base});
  const sc=so.health_score||0;
  mk('chScore',{type:'doughnut',data:{labels:['Score','Gap'],
    datasets:[{data:[sc,100-sc],backgroundColor:[scoreCol(sc),'#e5eae5'],cutout:'72%'}]},options:base});
  const w=s.weather_analysis||{};
  const num=v=>parseFloat(String(v==null?'':v).replace(/[^0-9.\-]/g,''))||0;
  mk('chWx',{type:'radar',data:{labels:['Temp C','Humidity %','Wind km/h','Rain mm','Irrigation mm'],
    datasets:[{data:[num(w.temperature),num(w.humidity),num(w.wind_speed),num(w.rainfall_mm),num(w.irrigation&&w.irrigation.net_irrigation)],
      backgroundColor:'rgba(27,73,101,.2)',borderColor:B,pointBackgroundColor:B}]},options:base});
  const f=(s.disease_detection&&s.disease_detection.image_features)||{};
  mk('chLeaf',{type:'bar',data:{labels:['Green','Yellow','Brown','Rust','Dark'],
    datasets:[{data:[f.green,f.yellow,f.brown,f.red,f.dark].map(v=>Math.round((v||0)*100)),
      backgroundColor:['#2d6a4f','#e9c46a','#6b4226','#e76f51','#333'],borderRadius:6}]},
    options:Object.assign({},base,{scales:{y:{beginAtZero:true,max:100}}})});
}

function renderCropCard(c) {
  if (!c) return '';
  const rows = (c.all_crops || []).map((r,i) => `
    <div class="stat-row"><span class="stat-label">${i===0?'⭐ ':'#'+(i+1)+' '}${r.crop_display||cap(r.crop)}</span>
      <div class="conf-bar-wrap"><div class="conf-bar" style="width:${Math.round(r.confidence<=1?r.confidence*100:r.confidence)}px"></div>
        <span class="conf-num">${Math.round(r.confidence<=1?r.confidence*100:r.confidence)}%</span></div></div>`).join('');
  return card('#2d6a4f','🌱 Crop Recommendation',`
    <p class="top-crop-name">${c.top_crop||'—'}</p>${rows}
    <p class="card-note">🤖 ${c.method||''}</p>
    <p class="key-insight">${c.key_insight||''}</p>`);
}

function renderDiseaseCard(d) {
  if (!d) return '';
  if (d.status==='No image submitted') return card('#e63946','🔬 Disease Detection',`
    <p class="key-insight">${d.key_insight||'No image provided.'}</p>
    <p class="card-note">Upload a leaf photo on the advisory form to enable disease detection.</p>`);
  const healthy = d.status==='healthy';
  const txList  = (d.treatment||[]).map(t=>`<li>${t}</li>`).join('');
  return card(healthy?'#2d6a4f':'#e63946','🔬 Disease Detection',`
    <div class="stat-row"><span class="stat-label">Disease</span>
      <span class="stat-value ${healthy?'text-green':'text-red'}">${d.disease||'N/A'}</span></div>
    <div class="stat-row"><span class="stat-label">Severity</span>
      <span class="stat-badge ${sevClass(d.severity)}">${d.severity}</span></div>
    <div class="stat-row"><span class="stat-label">Confidence</span>
      <span class="stat-value">${d.confidence}</span></div>
    <div class="stat-row"><span class="stat-label">Cause</span>
      <span class="stat-value" style="font-size:.8rem">${d.cause||''}</span></div>
    ${!healthy&&txList?`<p class="card-sub-header">Treatment:</p><ul class="bullet-list">${txList}</ul>`:''}
    <p class="key-insight">${d.key_insight||''}</p>`);
}

function renderWeatherCard(w) {
  if (!w) return '';
  const adv = (w.advisory||[]).map(a=>`<li>${a}</li>`).join('');
  const irr = w.irrigation||{};
  return card('#1b4965','⛅ Weather Analysis',`
    <div class="weather-banner">${w.condition||'—'}</div>
    <div class="stat-row"><span class="stat-label">Temperature</span><span class="stat-value">${w.temperature}</span></div>
    <div class="stat-row"><span class="stat-label">Humidity</span><span class="stat-value">${w.humidity}</span></div>
    <div class="stat-row"><span class="stat-label">Wind Speed</span><span class="stat-value">${w.wind_speed} km/h</span></div>
    <div class="stat-row"><span class="stat-label">Rainfall</span><span class="stat-value">${w.rainfall_mm} mm</span></div>
    <div class="stat-row"><span class="stat-label">Irrigation Need</span><span class="stat-value">${irr.net_irrigation||0} mm/day</span></div>
    ${adv?`<p class="card-sub-header">Advisory:</p><ul class="bullet-list">${adv}</ul>`:''}`);
}

function renderSoilCard(s) {
  if (!s) return '';
  const score = s.health_score||0;
  const amend = (s.amendments||[]).map(a=>`<li>${a}</li>`).join('');
  return card('#6b4226','🪨 Soil Health Analysis',`
    <div class="score-circle-wrap">
      <div class="score-circle" style="border-color:${scoreCol(score)}">
        <span class="score-num" style="color:${scoreCol(score)}">${score}</span>
        <span class="score-sub">/ 100</span></div>
      <span class="score-label">${s.overall_health||''}</span></div>
    ${nuRow('Nitrogen (N)',s.nitrogen,s.nitrogen_status)}
    ${nuRow('Phosphorus (P)',s.phosphorus,s.phosphorus_status)}
    ${nuRow('Potassium (K)',s.potassium,s.potassium_status)}
    ${nuRow('pH',s.ph,s.ph_status)}
    <div class="stat-row"><span class="stat-label">Soil Type</span><span class="stat-value">${s.soil_type||'—'}</span></div>
    ${amend?`<p class="card-sub-header">Fertiliser Plan:</p><ul class="bullet-list">${amend}</ul>`:''}
    <p class="key-insight">${s.key_insight||''}</p>`);
}

function renderMarketCard(m) {
  if (!m) return '';
  const adv = (m.advisory||[]).map(a=>`<li>${a}</li>`).join('');
  return card('#b8860b','📈 Market Intelligence',`
    <div class="stat-row"><span class="stat-label">Crop</span><span class="stat-value">${m.crop||'—'}</span></div>
    <div class="stat-row"><span class="stat-label">Avg Price</span><span class="stat-value">${m.avg_price||'—'}</span></div>
    <div class="stat-row"><span class="stat-label">Trend</span><span class="stat-value">${trendIcon(m.price_trend)} ${m.price_trend}</span></div>
    <div class="stat-row"><span class="stat-label">Best Market</span><span class="stat-value">${m.best_market||'APMC'}</span></div>
    <div class="stat-row"><span class="stat-label">Yield Estimate</span><span class="stat-value">${m.yield_estimate||'—'}</span></div>
    <div class="stat-row"><span class="stat-label">Net Income</span><span class="stat-value text-green">${m.net_income||'—'}</span></div>
    ${adv?`<ul class="bullet-list" style="margin-top:10px">${adv}</ul>`:''}`);
}

function renderPolicyCard(p) {
  if (!p) return '';
  const msp = p.msp||{};
  const sch = (p.schemes||[]).slice(0,5).map(s=>`
    <div class="scheme-row"><span class="scheme-name">✅ ${s.name}</span>
      <span class="scheme-benefit">${s.benefit}</span></div>`).join('');
  return card('#2d6a4f','📜 Policy & Govt Schemes',`
    ${msp.msp?`<div class="msp-badge">MSP ${msp.year}: ₹${msp.msp}/${msp.unit||'quintal'}</div>`:''}
    <p class="card-sub-header">Applicable Schemes:</p>${sch}
    <p class="key-insight">${p.key_insight||''}</p>
    <p class="helpline">📞 ${p.helpline||'1800-180-1551'}</p>`);
}

function renderActionPlan(plan) {
  if (!plan||!plan.length) return '';
  return `<div class="action-plan"><h3>📋 Priority Action Plan</h3>
    ${plan.map(a=>`<div class="action-item">
      <div class="action-num">${a.priority}</div>
      <div class="action-text"><strong>${a.action}</strong><small>⏰ ${a.timeline}</small></div>
    </div>`).join('')}</div>`;
}

function renderTamil(s) {
  return `<div class="tamil-section"><h4>🇮🇳 Tamil Advisory (தமிழில் ஆலோசனை)</h4><p>${s}</p></div>`;
}

/* helpers */
function card(color,title,body){return`<div class="report-card"><div class="report-card-header" style="background:${color}">${title}</div><div class="report-card-body">${body}</div></div>`;}
function nuRow(label,val,status){return`<div class="stat-row"><span class="stat-label">${label}</span><span style="display:flex;gap:8px;align-items:center"><span class="stat-value">${val??'N/A'}</span>${status?`<span class="stat-badge ${stClass(status)}">${status}</span>`:''}</span></div>`;}
function stClass(s){if(!s)return'';const sl=s.toLowerCase();if(sl.includes('low'))return'badge-low';if(sl.includes('high'))return'badge-high';return'badge-ok';}
function sevClass(s){if(!s)return'badge-ok';const sl=s.toLowerCase();if(sl==='none')return'badge-ok';if(sl==='moderate')return'badge-medium';if(sl==='high'||sl==='very high')return'badge-low';return'badge-ok';}
function scoreCol(s){return s>=80?'#2d6a4f':s>=60?'#b8860b':s>=40?'#f4a261':'#e63946';}
function trendIcon(t){return{rising:'📈',falling:'📉',stable:'➡️',volatile:'⚡',seasonal:'🔄'}[(t||'').toLowerCase()]||'➡️';}
function cap(s){return s?s.charAt(0).toUpperCase()+s.slice(1):s;}
