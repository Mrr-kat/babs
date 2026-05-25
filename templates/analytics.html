{% extends "base.html" %}
{% block title %}Analitica{% endblock %}
{% block page_title %}Analitica e Inteligencia{% endblock %}

{% block head %}
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
{% endblock %}

{% block content %}
<!-- Tab nav -->
<div style="display:flex;gap:4px;margin-bottom:24px;background:var(--bg-2);border:1px solid var(--border);border-radius:var(--radius);padding:4px;width:fit-content">
  <button class="tab-btn active" onclick="showTab('ventas')" id="tab-ventas">Analisis de Ventas</button>
  <button class="tab-btn" onclick="showTab('predicciones')" id="tab-predicciones">Prediccion de Stock</button>
  <button class="tab-btn" onclick="showTab('recomendaciones')" id="tab-recomendaciones">Reabastecimiento</button>
</div>

<!-- TAB: Ventas -->
<div id="tabVentas">
  <div class="grid-2" style="margin-bottom:20px">
    <div class="card">
      <div class="card-header"><div class="card-title">Ventas Diarias — 30 dias</div></div>
      <div class="chart-container" style="height:240px"><canvas id="chartVentasDia"></canvas></div>
    </div>
    <div class="card">
      <div class="card-header"><div class="card-title">Ventas por Dia de Semana</div></div>
      <div class="chart-container" style="height:240px"><canvas id="chartSemana"></canvas></div>
    </div>
  </div>
  <div class="grid-2" style="margin-bottom:20px">
    <div class="card">
      <div class="card-header"><div class="card-title">Ingresos por Categoria</div></div>
      <div class="chart-container" style="height:240px"><canvas id="chartCatBar"></canvas></div>
    </div>
    <div class="card">
      <div class="card-header"><div class="card-title">Metodos de Pago</div></div>
      <div class="chart-container" style="height:240px;display:flex;align-items:center;justify-content:center"><canvas id="chartPago" style="max-height:220px"></canvas></div>
    </div>
  </div>
  <div class="card">
    <div class="card-header"><div class="card-title">Top 10 Productos — Ultimos 30 dias</div></div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>#</th><th>Producto</th><th>Unidades Vendidas</th><th>Ingresos</th><th>Ganancias</th><th>Margen</th><th>Stock Actual</th></tr></thead>
        <tbody id="topProdTable"></tbody>
      </table>
    </div>
  </div>
</div>

<!-- TAB: Predicciones -->
<div id="tabPredicciones" style="display:none">
  <div class="card" style="margin-bottom:20px">
    <div class="card-header">
      <div>
        <div class="card-title">Prediccion de Agotamiento de Stock</div>
        <div class="card-sub">Basado en promedio ponderado de ventas de los ultimos 30 dias</div>
      </div>
      <div class="search-bar">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        <input type="text" id="predSearch" placeholder="Buscar producto..." oninput="filterPred()">
      </div>
    </div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Producto</th>
            <th>Categoria</th>
            <th>Stock</th>
            <th>Venta Diaria</th>
            <th>Dias Restantes</th>
            <th>Fecha Estimada</th>
            <th>Confianza</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody id="predTable"><tr><td colspan="8"><div class="loading"><div class="spinner"></div> Calculando predicciones...</div></td></tr></tbody>
      </table>
    </div>
  </div>
</div>

<!-- TAB: Recomendaciones -->
<div id="tabRecomendaciones" style="display:none">
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:20px" id="recStats">
    <div class="stat-card red"><div class="stat-label">Urgencia Alta</div><div class="stat-value" id="rec-alta">—</div></div>
    <div class="stat-card accent"><div class="stat-label">Urgencia Media</div><div class="stat-value" id="rec-media">—</div></div>
    <div class="stat-card blue"><div class="stat-label">Inversion Sugerida</div><div class="stat-value small" id="rec-inv">—</div></div>
  </div>
  <div id="recList"><div class="loading"><div class="spinner"></div> Calculando...</div></div>
</div>
{% endblock %}

{% block scripts %}
<style>
.tab-btn {
  padding: 7px 16px;
  border-radius: 6px;
  border: none;
  background: transparent;
  color: var(--text-3);
  font-family: var(--font);
  font-size: 0.84rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}
.tab-btn.active { background: var(--bg-3); color: var(--text); font-weight: 600; }
.tab-btn:hover:not(.active) { color: var(--text-2); }
</style>
<script>
Chart.defaults.color = 'rgba(160,171,190,0.7)';
Chart.defaults.borderColor = '#2a3348';
Chart.defaults.font.family = "'DM Sans', sans-serif";

function showTab(tab){
  ['ventas','predicciones','recomendaciones'].forEach(t=>{
    document.getElementById('tab'+t.charAt(0).toUpperCase()+t.slice(1)).style.display = t===tab?'':'none';
    document.getElementById('tab-'+t).classList.toggle('active', t===tab);
  });
}

let predData = [];

async function loadAnalytics(){
  const [dash, semana] = await Promise.all([
    fetch('/api/analytics/dashboard').then(r=>r.json()),
    fetch('/api/analytics/ventas-semana').then(r=>r.json())
  ]);

  const dias = dash.ventas_diarias;
  const colors = ['#e8a838','#5b9cf6','#4ecb8d','#e85555','#a78bfa','#f472b6','#fb923c','#34d399'];

  new Chart(document.getElementById('chartVentasDia'),{
    type:'bar',
    data:{
      labels: dias.map(d=>d.dia.slice(5)),
      datasets:[
        {label:'Ingresos',data:dias.map(d=>d.total),backgroundColor:'rgba(91,156,246,0.25)',borderColor:'#5b9cf6',borderWidth:1.5,borderRadius:3},
        {label:'Ganancia',data:dias.map(d=>d.ganancia),type:'line',backgroundColor:'rgba(78,203,141,0.1)',borderColor:'#4ecb8d',borderWidth:2,tension:0.4,fill:true,pointRadius:2}
      ]
    },
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{boxWidth:10,font:{size:11}}}},scales:{y:{beginAtZero:true,ticks:{callback:v=>'$'+(v/1000).toFixed(0)+'k',font:{size:10}}},x:{ticks:{font:{size:10},maxRotation:0}}}}
  });

  new Chart(document.getElementById('chartSemana'),{
    type:'bar',
    data:{
      labels:semana.map(d=>d.dia),
      datasets:[{label:'Ventas',data:semana.map(d=>d.total),backgroundColor:colors,borderRadius:4}]
    },
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,ticks:{callback:v=>'$'+(v/1000).toFixed(0)+'k',font:{size:10}}}}}
  });

  const cats = dash.por_categoria;
  new Chart(document.getElementById('chartCatBar'),{
    type:'bar',
    data:{labels:cats.map(c=>c.nombre.length>14?c.nombre.slice(0,13)+'...':c.nombre),datasets:[{label:'Ingresos',data:cats.map(c=>c.total),backgroundColor:colors.map(c=>c+'55'),borderColor:colors,borderWidth:1.5,borderRadius:4}]},
    options:{responsive:true,maintainAspectRatio:false,indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:{callback:v=>'$'+(v/1000).toFixed(0)+'k',font:{size:10}}},y:{ticks:{font:{size:11}}}}}
  });

  const metodos = dash.metodos_pago;
  new Chart(document.getElementById('chartPago'),{
    type:'doughnut',
    data:{labels:metodos.map(m=>m.metodo_pago),datasets:[{data:metodos.map(m=>m.total),backgroundColor:['#e8a838','#5b9cf6','#4ecb8d'],borderWidth:0}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'right',labels:{boxWidth:10,font:{size:11}}}},cutout:'60%'}
  });

  // Top products table
  document.getElementById('topProdTable').innerHTML = dash.top_productos.map((p,i)=>`
    <tr>
      <td style="font-weight:700;color:var(--text-3);font-size:0.8rem">${i+1}</td>
      <td class="primary">${p.nombre}</td>
      <td style="font-weight:600">${fmtNum(p.total_vendido||0)}</td>
      <td>${fmt(p.ingresos||0)}</td>
      <td class="text-green">${fmt(p.ganancias||0)}</td>
      <td><span style="color:${(p.margen_promedio||0)>=30?'var(--green)':(p.margen_promedio||0)>=15?'var(--accent)':'var(--red)'}">${p.margen_promedio||0}%</span></td>
      <td>${p.stock_actual}</td>
    </tr>`).join('');
}

async function loadPredicciones(){
  predData = await fetch('/api/analytics/predicciones').then(r=>r.json());
  renderPred(predData);
}

function renderPred(data){
  const tbody = document.getElementById('predTable');
  if(!data.length){ tbody.innerHTML='<tr><td colspan="8"><div class="empty-state"><p>Sin datos</p></div></td></tr>'; return; }
  tbody.innerHTML = data.map(p=>{
    const pred = p.prediccion;
    const dias = pred ? Math.round(pred.dias_restantes) : null;
    const diaColor = dias===null ? '' : dias<=3 ? 'var(--red)' : dias<=7 ? 'var(--accent)' : dias<=15 ? 'var(--blue)' : 'var(--green)';
    const confBadge = pred ? (pred.confianza==='alta'?'badge-green':pred.confianza==='media'?'badge-yellow':'badge-gray') : '';
    const badge = p.estado==='critico'?'<span class="badge badge-red">Critico</span>':p.estado==='bajo'?'<span class="badge badge-yellow">Bajo</span>':'<span class="badge badge-green">Normal</span>';
    return `<tr>
      <td class="primary">${p.nombre}</td>
      <td style="font-size:0.8rem">${p.categoria}</td>
      <td style="font-weight:600">${p.stock_actual} <span style="font-size:0.72rem;color:var(--text-3)">/ min ${p.stock_minimo}</span></td>
      <td>${pred ? pred.venta_diaria_promedio : '—'} uds/dia</td>
      <td style="font-weight:700;color:${diaColor}">${dias !== null ? dias + ' dias' : 'Sin ventas'}</td>
      <td style="font-size:0.82rem">${pred ? pred.fecha_estimada : '—'}</td>
      <td>${pred ? `<span class="badge ${confBadge}">${pred.confianza}</span>` : '—'}</td>
      <td>${badge}</td>
    </tr>`;
  }).join('');
}

function filterPred(){
  const q = document.getElementById('predSearch').value.toLowerCase();
  renderPred(predData.filter(p=>p.nombre.toLowerCase().includes(q)||p.categoria.toLowerCase().includes(q)));
}

async function loadRecomendaciones(){
  const recs = await fetch('/api/analytics/recomendaciones-reabastecimiento').then(r=>r.json());
  const alta = recs.filter(r=>r.urgencia==='alta');
  const media = recs.filter(r=>r.urgencia==='media');
  const inv = recs.reduce((s,r)=>s+r.costo_estimado,0);
  document.getElementById('rec-alta').textContent = alta.length;
  document.getElementById('rec-media').textContent = media.length;
  document.getElementById('rec-inv').textContent = fmt(inv);

  document.getElementById('recList').innerHTML = recs.length===0
    ? '<div class="empty-state"><p>No hay recomendaciones de reabastecimiento en este momento</p></div>'
    : recs.map(r=>{
      const urgColor = r.urgencia==='alta'?'var(--red)':r.urgencia==='media'?'var(--accent)':'var(--blue)';
      const urgLabel = r.urgencia==='alta'?'Urgente':r.urgencia==='media'?'Pronto':'Normal';
      return `<div class="card" style="margin-bottom:12px">
        <div style="display:flex;align-items:flex-start;gap:16px;flex-wrap:wrap">
          <div style="flex:1;min-width:200px">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
              <span style="width:8px;height:8px;border-radius:50%;background:${urgColor};box-shadow:0 0 6px ${urgColor};flex-shrink:0"></span>
              <span style="font-weight:650;color:var(--text)">${r.nombre}</span>
              <span style="font-size:0.7rem;font-weight:600;padding:2px 7px;border-radius:20px;background:${urgColor}22;color:${urgColor}">${urgLabel}</span>
            </div>
            <div style="font-size:0.8rem;color:var(--text-3);margin-bottom:6px">${r.categoria} — ${r.proveedor||'Sin proveedor'}</div>
            <div style="font-size:0.82rem;color:var(--text-2)">${r.motivo}</div>
          </div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;min-width:360px">
            <div style="text-align:center;padding:10px;background:var(--bg-3);border-radius:var(--radius-sm)">
              <div style="font-size:0.7rem;color:var(--text-3);text-transform:uppercase;letter-spacing:0.05em">Cantidad</div>
              <div style="font-size:1.2rem;font-weight:700;color:var(--text)">${fmtNum(r.cantidad_recomendada)}</div>
              <div style="font-size:0.72rem;color:var(--text-3)">unidades</div>
            </div>
            <div style="text-align:center;padding:10px;background:var(--bg-3);border-radius:var(--radius-sm)">
              <div style="font-size:0.7rem;color:var(--text-3);text-transform:uppercase;letter-spacing:0.05em">Inversion</div>
              <div style="font-size:1.1rem;font-weight:700;color:var(--red)">${fmt(r.costo_estimado)}</div>
            </div>
            <div style="text-align:center;padding:10px;background:var(--bg-3);border-radius:var(--radius-sm)">
              <div style="font-size:0.7rem;color:var(--text-3);text-transform:uppercase;letter-spacing:0.05em">Ganancia</div>
              <div style="font-size:1.1rem;font-weight:700;color:var(--green)">${fmt(r.ganancia_potencial)}</div>
            </div>
          </div>
        </div>
      </div>`;
    }).join('');
}

loadAnalytics();
loadPredicciones();
loadRecomendaciones();
</script>
{% endblock %}