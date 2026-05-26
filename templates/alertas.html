{% extends "base.html" %}
{% block title %}Alertas{% endblock %}
{% block page_title %}Alertas y Recomendaciones{% endblock %}

{% block content %}

<!-- Summary stats -->
<div class="stats-grid" style="margin-bottom:24px" id="alertStats">
  <div class="stat-card red">
    <div class="stat-label">Stock Critico</div>
    <div class="stat-value" id="a-critico">—</div>
    <div class="stat-sub">Reabastecimiento inmediato</div>
  </div>
  <div class="stat-card accent">
    <div class="stat-label">Stock Bajo</div>
    <div class="stat-value" id="a-advertencia">—</div>
    <div class="stat-sub">Programar pedido pronto</div>
  </div>
  <div class="stat-card blue">
    <div class="stat-label">Predicciones</div>
    <div class="stat-value" id="a-prediccion">—</div>
    <div class="stat-sub">Se agotaran en 7 dias</div>
  </div>
  <div class="stat-card green">
    <div class="stat-label">Oportunidades</div>
    <div class="stat-value" id="a-oportunidad">—</div>
    <div class="stat-sub">Alto margen, bajo stock</div>
  </div>
</div>

<!-- Filter tabs -->
<div style="display:flex;gap:4px;margin-bottom:20px;background:var(--bg-2);border:1px solid var(--border);border-radius:var(--radius);padding:4px;width:fit-content">
  <button class="tab-btn active" onclick="filterAlerts('todos')" id="ftab-todos">Todas</button>
  <button class="tab-btn" onclick="filterAlerts('critico')" id="ftab-critico">Criticas</button>
  <button class="tab-btn" onclick="filterAlerts('advertencia')" id="ftab-advertencia">Advertencias</button>
  <button class="tab-btn" onclick="filterAlerts('prediccion')" id="ftab-prediccion">Predicciones</button>
  <button class="tab-btn" onclick="filterAlerts('oportunidad')" id="ftab-oportunidad">Oportunidades</button>
</div>

<!-- Alerts list -->
<div id="alertsList">
  <div class="loading"><div class="spinner"></div> Cargando alertas...</div>
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

.alert-card {
  background: var(--bg-2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 10px;
  display: flex;
  gap: 16px;
  align-items: flex-start;
  transition: transform 0.15s, box-shadow 0.15s;
}
.alert-card:hover { transform: translateX(4px); box-shadow: var(--shadow-sm); }
.alert-card.critico    { border-left: 3px solid var(--red);   background: linear-gradient(90deg, rgba(232,85,85,0.05) 0%, transparent 50%); }
.alert-card.advertencia{ border-left: 3px solid var(--accent); background: linear-gradient(90deg, rgba(232,168,56,0.05) 0%, transparent 50%); }
.alert-card.prediccion { border-left: 3px solid var(--blue);  background: linear-gradient(90deg, rgba(91,156,246,0.05) 0%, transparent 50%); }
.alert-card.oportunidad{ border-left: 3px solid var(--green); background: linear-gradient(90deg, rgba(78,203,141,0.05) 0%, transparent 50%); }

.alert-icon {
  width: 38px; height: 38px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
}
.critico    .alert-icon { background: var(--red-dim);   color: var(--red); }
.advertencia .alert-icon { background: var(--accent-dim); color: var(--accent); }
.prediccion .alert-icon { background: var(--blue-dim);  color: var(--blue); }
.oportunidad .alert-icon { background: var(--green-dim); color: var(--green); }

.alert-body { flex: 1; min-width: 0; }
.alert-header { display: flex; align-items: center; gap: 8px; margin-bottom: 5px; flex-wrap: wrap; }
.alert-type-label {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  padding: 2px 8px;
  border-radius: 20px;
}
.critico    .alert-type-label { background: var(--red-dim);   color: var(--red); }
.advertencia .alert-type-label { background: var(--accent-dim); color: var(--accent); }
.prediccion .alert-type-label { background: var(--blue-dim);  color: var(--blue); }
.oportunidad .alert-type-label { background: var(--green-dim); color: var(--green); }

.alert-product-name { font-size: 0.95rem; font-weight: 650; color: var(--text); }
.alert-cat { font-size: 0.76rem; color: var(--text-3); margin-left: auto; }
.alert-message { font-size: 0.84rem; color: var(--text-2); line-height: 1.5; margin-bottom: 10px; }
.alert-action-box {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.78rem;
  color: var(--text-3);
  background: var(--bg-3);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 6px 12px;
}
.alert-action-box svg { flex-shrink: 0; opacity: 0.6; }

.no-alerts {
  text-align: center;
  padding: 64px 20px;
  color: var(--text-3);
}
.no-alerts-icon {
  width: 56px; height: 56px;
  border-radius: 50%;
  background: var(--bg-3);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 16px;
  opacity: 0.5;
}
</style>

<script>
let allAlerts = [];
let currentFilter = 'todos';

const iconMap = {
  critico: `<svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`,
  advertencia: `<svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`,
  prediccion: `<svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>`,
  oportunidad: `<svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>`
};

const labelMap = {
  critico: 'Critico',
  advertencia: 'Advertencia',
  prediccion: 'Prediccion',
  oportunidad: 'Oportunidad'
};

async function loadAlerts() {
  const data = await fetch('/api/alertas').then(r => r.json());
  allAlerts = data.alertas || [];
  const res = data.resumen || {};

  document.getElementById('a-critico').textContent    = res.criticos      || 0;
  document.getElementById('a-advertencia').textContent = res.advertencias  || 0;
  document.getElementById('a-prediccion').textContent  = res.predicciones  || 0;
  document.getElementById('a-oportunidad').textContent = res.oportunidades || 0;

  renderAlerts(allAlerts);
}

function filterAlerts(tipo) {
  currentFilter = tipo;
  ['todos','critico','advertencia','prediccion','oportunidad'].forEach(t => {
    document.getElementById('ftab-' + t).classList.toggle('active', t === tipo);
  });
  const filtered = tipo === 'todos' ? allAlerts : allAlerts.filter(a => a.tipo === tipo);
  renderAlerts(filtered);
}

function renderAlerts(list) {
  const container = document.getElementById('alertsList');
  if (!list.length) {
    container.innerHTML = `
      <div class="no-alerts">
        <div class="no-alerts-icon">
          <svg width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <p style="font-size:0.95rem;font-weight:500;color:var(--text-2);margin-bottom:4px">Sin alertas en esta categoria</p>
        <p style="font-size:0.82rem">El inventario se encuentra en buen estado</p>
      </div>`;
    return;
  }

  container.innerHTML = list.map(a => `
    <div class="alert-card ${a.tipo}">
      <div class="alert-icon">${iconMap[a.tipo] || ''}</div>
      <div class="alert-body">
        <div class="alert-header">
          <span class="alert-type-label">${labelMap[a.tipo] || a.tipo}</span>
          <span class="alert-product-name">${a.producto}</span>
          ${a.categoria ? `<span class="alert-cat">${a.categoria}</span>` : ''}
        </div>
        <div class="alert-message">${a.mensaje}</div>
        <div class="alert-action-box">
          <svg width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
          </svg>
          ${a.accion}
        </div>
      </div>
    </div>
  `).join('');
}

loadAlerts();
</script>
{% endblock %}
