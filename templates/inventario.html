{% extends "base.html" %}
{% block title %}Inventario{% endblock %}
{% block page_title %}Inventario{% endblock %}

{% block content %}
<div class="stats-grid" id="invStats">
  <div class="stat-card blue"><div class="stat-label">Total Productos</div><div class="stat-value" id="si-total">—</div></div>
  <div class="stat-card red"><div class="stat-label">Stock Critico</div><div class="stat-value" id="si-critico">—</div></div>
  <div class="stat-card accent"><div class="stat-label">Stock Bajo</div><div class="stat-value" id="si-bajo">—</div></div>
  <div class="stat-card green"><div class="stat-label">Valor Inventario</div><div class="stat-value small" id="si-valor">—</div></div>
</div>

<div class="card">
  <div class="toolbar">
    <div class="search-bar">
      <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
      <input type="text" id="searchInput" placeholder="Buscar por nombre o codigo...">
    </div>
    <select class="form-control" id="filterCat" style="width:160px">
      <option value="">Todas las categorias</option>
    </select>
    <select class="form-control" id="filterEstado" style="width:140px">
      <option value="">Todos los estados</option>
      <option value="critico">Critico</option>
      <option value="bajo">Bajo</option>
      <option value="normal">Normal</option>
    </select>
    <button class="btn btn-primary" onclick="openModal()">
      <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
      Nuevo Producto
    </button>
  </div>

  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Codigo</th>
          <th>Producto</th>
          <th>Categoria</th>
          <th>Stock</th>
          <th>Estado</th>
          <th>P. Compra</th>
          <th>P. Venta</th>
          <th>Margen</th>
          <th>Proveedor</th>
          <th></th>
        </tr>
      </thead>
      <tbody id="productTable">
        <tr><td colspan="10"><div class="loading"><div class="spinner"></div> Cargando...</div></td></tr>
      </tbody>
    </table>
  </div>
</div>

<!-- Modal Product -->
<div class="modal-overlay" id="productModal">
  <div class="modal">
    <div class="modal-header">
      <div class="modal-title" id="modalTitle">Nuevo Producto</div>
      <button class="btn btn-secondary btn-icon" onclick="closeModal()">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
      </button>
    </div>
    <div class="modal-body">
      <input type="hidden" id="prodId">
      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Nombre</label>
          <input class="form-control" id="pNombre" placeholder="Ej: Martillo 16oz">
        </div>
        <div class="form-group">
          <label class="form-label">Codigo</label>
          <input class="form-control" id="pCodigo" placeholder="Ej: HM-001">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Categoria</label>
          <select class="form-control" id="pCategoria"></select>
        </div>
        <div class="form-group">
          <label class="form-label">Proveedor</label>
          <input class="form-control" id="pProveedor" placeholder="Nombre del proveedor">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Precio Compra ($)</label>
          <input class="form-control" id="pPrecioCompra" type="number" min="0">
        </div>
        <div class="form-group">
          <label class="form-label">Precio Venta ($)</label>
          <input class="form-control" id="pPrecioVenta" type="number" min="0">
        </div>
      </div>
      <div class="form-row-3">
        <div class="form-group">
          <label class="form-label">Stock Actual</label>
          <input class="form-control" id="pStock" type="number" min="0" value="0">
        </div>
        <div class="form-group">
          <label class="form-label">Stock Minimo</label>
          <input class="form-control" id="pStockMin" type="number" min="0" value="5">
        </div>
        <div class="form-group">
          <label class="form-label">Stock Maximo</label>
          <input class="form-control" id="pStockMax" type="number" min="0" value="100">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label class="form-label">Unidad</label>
          <select class="form-control" id="pUnidad">
            <option>unidad</option><option>caja</option><option>rollo</option>
            <option>kg</option><option>litro</option><option>galon</option>
            <option>bulto</option><option>par</option><option>juego</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Descripcion</label>
          <input class="form-control" id="pDesc" placeholder="Opcional">
        </div>
      </div>
      <!-- Image upload -->
      <div class="form-group" style="margin-top:4px">
        <label class="form-label">Imagen del Producto</label>
        <div id="imgUploadArea" onclick="document.getElementById('pImagen').click()" style="border:2px dashed var(--border);border-radius:var(--radius-sm);padding:16px;cursor:pointer;text-align:center;transition:border-color 0.2s;position:relative;min-height:90px;display:flex;align-items:center;justify-content:center;gap:12px;">
          <img id="imgPreview" src="" alt="" style="display:none;max-height:70px;max-width:100px;object-fit:contain;border-radius:6px;border:1px solid var(--border);">
          <div id="imgPlaceholder" style="color:var(--text-3);font-size:0.82rem">
            <svg width="28" height="28" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" style="display:block;margin:0 auto 6px;opacity:0.4"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
            Haz clic para subir imagen (JPG, PNG, WEBP)
          </div>
          <div id="imgName" style="display:none;font-size:0.78rem;color:var(--text-3);margin-top:4px"></div>
        </div>
        <input type="file" id="pImagen" accept="image/*" style="display:none" onchange="previewImg(this)">
        <input type="hidden" id="pImagenB64">
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Cancelar</button>
      <button class="btn btn-primary" onclick="saveProduct()">Guardar</button>
    </div>
  </div>
</div>

<!-- Modal Abastecer -->
<div class="modal-overlay" id="abastecerModal">
  <div class="modal" style="max-width:380px">
    <div class="modal-header">
      <div class="modal-title">Reabastecer Producto</div>
      <button class="btn btn-secondary btn-icon" onclick="closeAbastecer()">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
      </button>
    </div>
    <div class="modal-body">
      <div style="margin-bottom:16px;padding:12px;background:var(--bg-3);border-radius:var(--radius-sm)">
        <div id="abProdName" style="font-weight:600;color:var(--text)"></div>
        <div id="abStockInfo" style="font-size:0.82rem;color:var(--text-3);margin-top:4px"></div>
      </div>
      <input type="hidden" id="abProdId">
      <div class="form-group">
        <label class="form-label">Cantidad a agregar</label>
        <input class="form-control" id="abCantidad" type="number" min="1" value="10">
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeAbastecer()">Cancelar</button>
      <button class="btn btn-primary" onclick="doAbastecer()">Confirmar</button>
    </div>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script>
let categorias = [];
let editId = null;

async function loadStats(){
  const s = await fetch('/api/inventario/stats').then(r=>r.json());
  document.getElementById('si-total').textContent = s.total_productos;
  document.getElementById('si-critico').textContent = s.stock_critico;
  document.getElementById('si-bajo').textContent = s.stock_bajo;
  document.getElementById('si-valor').textContent = fmt(s.valor_inventario);
}

async function loadCategorias(){
  categorias = await fetch('/api/inventario/categorias').then(r=>r.json());
  const sel = document.getElementById('filterCat');
  categorias.forEach(c => sel.innerHTML += `<option value="${c.id}">${c.nombre}</option>`);
  const pSel = document.getElementById('pCategoria');
  pSel.innerHTML = '<option value="">Sin categoria</option>' + categorias.map(c=>`<option value="${c.id}">${c.nombre}</option>`).join('');
}

async function loadProducts(){
  const s = document.getElementById('searchInput').value;
  const cat = document.getElementById('filterCat').value;
  const est = document.getElementById('filterEstado').value;
  const params = new URLSearchParams();
  if(s) params.set('search', s);
  if(cat) params.set('categoria', cat);
  if(est) params.set('estado', est);

  const products = await fetch('/api/inventario/productos?' + params).then(r=>r.json());
  const tbody = document.getElementById('productTable');

  if(!products.length){
    tbody.innerHTML = '<tr><td colspan="10"><div class="empty-state"><p>No se encontraron productos</p></div></td></tr>';
    return;
  }

  tbody.innerHTML = products.map(p => {
    const pct = Math.min((p.stock_actual / p.stock_maximo) * 100, 100);
    const barColor = p.estado_stock === 'critico' ? 'red' : p.estado_stock === 'bajo' ? 'yellow' : 'green';
    const badge = p.estado_stock === 'critico'
      ? '<span class="badge badge-red">Critico</span>'
      : p.estado_stock === 'bajo'
      ? '<span class="badge badge-yellow">Bajo</span>'
      : '<span class="badge badge-green">Normal</span>';
    return `<tr>
      <td style="font-size:0.75rem;color:var(--text-3);font-family:monospace">${p.codigo}</td>
      <td class="primary">${p.nombre}</td>
      <td style="font-size:0.8rem">${p.categoria_nombre||'—'}</td>
      <td>
        <div style="display:flex;align-items:center;gap:8px">
          <span style="font-weight:600;min-width:28px">${p.stock_actual}</span>
          <div class="stock-bar"><div class="stock-bar-fill ${barColor}" style="width:${pct}%"></div></div>
          <span style="font-size:0.72rem;color:var(--text-3)">${p.unidad}</span>
        </div>
      </td>
      <td>${badge}</td>
      <td>${fmt(p.precio_compra)}</td>
      <td style="color:var(--accent);font-weight:550">${fmt(p.precio_venta)}</td>
      <td><span style="color:${p.margen>=30?'var(--green)':p.margen>=15?'var(--accent)':'var(--red)'}">${p.margen}%</span></td>
      <td style="font-size:0.8rem;color:var(--text-3)">${p.proveedor||'—'}</td>
      <td>
        <div style="display:flex;gap:4px">
          <button class="btn btn-secondary btn-sm btn-icon" onclick="openAbastecer(${p.id},'${p.nombre.replace(/'/g,"\\'")}',${p.stock_actual},${p.stock_minimo},${p.stock_maximo})" title="Reabastecer">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" style="width:13px;height:13px"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
          </button>
          <button class="btn btn-secondary btn-sm btn-icon" onclick="editProduct(${p.id})" title="Editar">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" style="width:13px;height:13px"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
          </button>
          <button class="btn btn-danger btn-sm btn-icon" onclick="deleteProduct(${p.id},'${p.nombre.replace(/'/g,"\\'")}')">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" style="width:13px;height:13px"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </button>
        </div>
      </td>
    </tr>`;
  }).join('');
}

function previewImg(input){
  const file = input.files[0];
  if(!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    document.getElementById('pImagenB64').value = e.target.result;
    const preview = document.getElementById('imgPreview');
    preview.src = e.target.result;
    preview.style.display = 'block';
    document.getElementById('imgPlaceholder').style.display = 'none';
    document.getElementById('imgName').textContent = file.name;
    document.getElementById('imgName').style.display = 'block';
  };
  reader.readAsDataURL(file);
}

function openModal(){ editId=null; document.getElementById('modalTitle').textContent='Nuevo Producto'; document.getElementById('productModal').classList.add('open'); }
function closeModal(){ document.getElementById('productModal').classList.remove('open'); resetForm(); }
function resetForm(){
  ['pNombre','pCodigo','pProveedor','pDesc'].forEach(id=>document.getElementById(id).value='');
  document.getElementById('pStock').value=0; document.getElementById('pStockMin').value=5;
  document.getElementById('pStockMax').value=100; document.getElementById('pPrecioCompra').value='';
  document.getElementById('pPrecioVenta').value=''; document.getElementById('pImagenB64').value='';
  document.getElementById('pImagen').value='';
  document.getElementById('imgPreview').style.display='none'; document.getElementById('imgPreview').src='';
  document.getElementById('imgPlaceholder').style.display='block'; document.getElementById('imgName').style.display='none';
}

async function editProduct(id){
  const p = await fetch('/api/inventario/productos/'+id).then(r=>r.json());
  editId = id;
  document.getElementById('modalTitle').textContent = 'Editar Producto';
  document.getElementById('pNombre').value = p.nombre;
  document.getElementById('pCodigo').value = p.codigo;
  document.getElementById('pProveedor').value = p.proveedor||'';
  document.getElementById('pDesc').value = p.descripcion||'';
  document.getElementById('pStock').value = p.stock_actual;
  document.getElementById('pStockMin').value = p.stock_minimo;
  document.getElementById('pStockMax').value = p.stock_maximo;
  document.getElementById('pPrecioCompra').value = p.precio_compra;
  document.getElementById('pPrecioVenta').value = p.precio_venta;
  document.getElementById('pCategoria').value = p.categoria_id||'';
  document.getElementById('pUnidad').value = p.unidad;
  // Load existing image
  if(p.imagen){
    document.getElementById('pImagenB64').value = p.imagen;
    const preview = document.getElementById('imgPreview');
    preview.src = p.imagen; preview.style.display='block';
    document.getElementById('imgPlaceholder').style.display='none';
    document.getElementById('imgName').textContent='Imagen actual'; document.getElementById('imgName').style.display='block';
  }
  document.getElementById('productModal').classList.add('open');
}

async function saveProduct(){
  const data = {
    nombre: document.getElementById('pNombre').value.trim(),
    codigo: document.getElementById('pCodigo').value.trim(),
    categoria_id: document.getElementById('pCategoria').value||null,
    proveedor: document.getElementById('pProveedor').value.trim(),
    descripcion: document.getElementById('pDesc').value.trim(),
    precio_compra: parseFloat(document.getElementById('pPrecioCompra').value)||0,
    precio_venta: parseFloat(document.getElementById('pPrecioVenta').value)||0,
    stock_actual: parseInt(document.getElementById('pStock').value)||0,
    stock_minimo: parseInt(document.getElementById('pStockMin').value)||5,
    stock_maximo: parseInt(document.getElementById('pStockMax').value)||100,
    unidad: document.getElementById('pUnidad').value,
    imagen: document.getElementById('pImagenB64').value || null
  };
  if(!data.nombre||!data.codigo){ showToast('Nombre y codigo son requeridos','error'); return; }

  const url = editId ? '/api/inventario/productos/'+editId : '/api/inventario/productos';
  const method = editId ? 'PUT' : 'POST';
  const res = await fetch(url,{method,headers:{'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json());
  if(res.success){ showToast(editId?'Producto actualizado':'Producto creado','success'); closeModal(); loadProducts(); loadStats(); }
  else showToast(res.error||'Error','error');
}

async function deleteProduct(id, nombre){
  if(!confirm(`Eliminar "${nombre}"?`)) return;
  const res = await fetch('/api/inventario/productos/'+id,{method:'DELETE'}).then(r=>r.json());
  if(res.success){ showToast('Producto eliminado','success'); loadProducts(); loadStats(); }
}

function openAbastecer(id, nombre, stock, min, max){
  document.getElementById('abProdId').value = id;
  document.getElementById('abProdName').textContent = nombre;
  document.getElementById('abStockInfo').textContent = `Stock actual: ${stock} | Minimo: ${min} | Maximo: ${max}`;
  document.getElementById('abCantidad').value = max - stock;
  document.getElementById('abastecerModal').classList.add('open');
}
function closeAbastecer(){ document.getElementById('abastecerModal').classList.remove('open'); }
async function doAbastecer(){
  const id = document.getElementById('abProdId').value;
  const qty = parseInt(document.getElementById('abCantidad').value);
  const res = await fetch('/api/inventario/abastecer/'+id,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({cantidad:qty})}).then(r=>r.json());
  if(res.success){ showToast(`Stock actualizado. Nuevo stock: ${res.nuevo_stock}`,'success'); closeAbastecer(); loadProducts(); loadStats(); }
  else showToast(res.error||'Error','error');
}

// Debounce search
let searchTimer;
document.getElementById('searchInput').addEventListener('input', ()=>{ clearTimeout(searchTimer); searchTimer=setTimeout(loadProducts,300); });
document.getElementById('filterCat').addEventListener('change', loadProducts);
document.getElementById('filterEstado').addEventListener('change', loadProducts);

loadStats(); loadCategorias(); loadProducts();
</script>
{% endblock %}