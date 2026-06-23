(function () {
  'use strict';

  const URLS = window.REGISTRAR_VENTA_URLS || {};

  let pedido = {}; 
  let tmpProd = null;
  let snap = {};

  document.addEventListener('DOMContentLoaded', () => {
    fetch(URLS.getMenu)
      .then(r => r.json())
      .then(renderMenu)
      .catch(() => {
        document.getElementById('cols-menu').innerHTML =
          '<div style="color:#ef5350;padding:20px;">Error cargando el menú</div>';
      });
  });

  function renderMenu(data) {
    const root = document.getElementById('cols-menu');
    root.innerHTML = '';
    const cats = Object.entries(data);
    if (!cats.length) { root.innerHTML = '<div style="padding:20px;color:#666;">No hay productos</div>'; return; }

    document.documentElement.style.setProperty('--num-categorias', cats.length);

    cats.forEach(([cat, prods]) => {
      const col = document.createElement('div');
      col.className = 'col-cat';

      let html = `<div class="col-cat-header">${escapeHtml(cat)}</div><div class="col-cat-body">`;
      prods.forEach(p => {
        html += `<button class="btn-prod" data-id="${p.id}" data-nombre="${escapeHtml(p.nombre)}" data-precio="${p.precio}">
          <span class="prod-nombre">${escapeHtml(p.nombre)}</span>
          <span class="prod-precio">${p.precio.toFixed(2)} Bs.</span>
        </button>`;
      });
      html += '</div>';
      col.innerHTML = html;
      root.appendChild(col);
    });

    root.querySelectorAll('.btn-prod').forEach(btn => {
      btn.addEventListener('click', () => {
        abrirQty(
          parseInt(btn.dataset.id, 10),
          btn.dataset.nombre,
          parseFloat(btn.dataset.precio)
        );
      });
    });
  }

  function escapeHtml(str) {
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }

  function abrirQty(id, nombre, precio) {
    tmpProd = { id, nombre, precio };
    document.getElementById('m-nombre').textContent = nombre;
    document.getElementById('m-precio').textContent = precio.toFixed(2) + ' Bs.';
    document.getElementById('qty').value = 1;
    document.getElementById('ov-qty').classList.add('open');
    document.getElementById('qty').focus();
  }
  function cQty() { document.getElementById('ov-qty').classList.remove('open'); tmpProd = null; }
  function dQty(d) {
    const i = document.getElementById('qty');
    i.value = Math.max(1, parseInt(i.value || 1) + d);
  }
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { cQty(); cTicket(); }
    if (e.key === 'Enter' && document.getElementById('ov-qty').classList.contains('open')) okQty();
  });
  function okQty() {
    const c = Math.max(1, parseInt(document.getElementById('qty').value) || 1);
    if (!tmpProd) return;
    const { id, nombre, precio } = tmpProd;
    if (pedido[id]) {
      pedido[id].cantidad += c;
      pedido[id].subtotal = pedido[id].cantidad * precio;
    } else {
      pedido[id] = { nombre, precio, cantidad: c, subtotal: c * precio };
    }
    cQty();
    renderPedido();
    calcTotal();
  }

  function renderPedido() {
    const area = document.getElementById('pedido-area');
    const vacio = document.getElementById('pedido-vacio');
    const keys = Object.keys(pedido);
    document.getElementById('pedido-cnt').textContent = keys.length;

    area.querySelectorAll('.pedido-fila').forEach(r => r.remove());

    if (!keys.length) {
      if (!vacio) {
        const d = document.createElement('div');
        d.className = 'pedido-vacio';
        d.id = 'pedido-vacio';
        d.textContent = 'Sin productos aún';
        area.appendChild(d);
      } else {
        vacio.style.display = 'block';
      }
      return;
    }
    if (vacio) vacio.style.display = 'none';

    keys.forEach(id => {
      const p = pedido[id];
      const row = document.createElement('div');
      row.className = 'pedido-fila';
      row.innerHTML = `
        <span class="pf-nombre">${escapeHtml(p.nombre)}</span>
        <input type="number" class="pf-qty" min="1" value="${p.cantidad}" data-id="${id}">
        <span class="pf-sub">${p.subtotal.toFixed(2)} Bs.</span>
        <button class="pf-del" data-id="${id}">✕</button>`;
      area.appendChild(row);
    });

    // Delegación de eventos para cantidad y borrar
    area.querySelectorAll('.pf-qty').forEach(inp => {
      inp.addEventListener('change', () => cambQty(parseInt(inp.dataset.id, 10), inp.value));
    });
    area.querySelectorAll('.pf-del').forEach(btn => {
      btn.addEventListener('click', () => delItem(parseInt(btn.dataset.id, 10)));
    });
  }

  function cambQty(id, v) {
    const c = parseInt(v, 10);
    if (c > 0 && pedido[id]) {
      pedido[id].cantidad = c;
      pedido[id].subtotal = c * pedido[id].precio;
      renderPedido();
      calcTotal();
    }
  }
  function delItem(id) { delete pedido[id]; renderPedido(); calcTotal(); }

  function calcTotal() {
    const sub = Object.values(pedido).reduce((s, p) => s + p.subtotal, 0);
    const desc = parseFloat(document.getElementById('v-desc').value) || 0;
    const tot = Math.max(0, sub - desc);
    document.getElementById('v-subtotal').textContent = sub.toFixed(2) + ' Bs.';
    document.getElementById('v-total').textContent = tot.toFixed(2) + ' Bs.';
    calcCambio();
  }
  function calcCambio() {
    const tot = parseFloat(document.getElementById('v-total').textContent) || 0;
    const efec = parseFloat(document.getElementById('v-efec').value) || 0;
    const cambio = efec - tot;
    document.getElementById('v-cambio').textContent = (cambio >= 0 ? cambio : 0).toFixed(2) + ' Bs.';
    const box = document.getElementById('cambio-box');
    box.className = 'cambio-box' + (cambio < 0 ? ' negativo' : '');
  }

  function limpiarFormulario() {
    pedido = {};
    ['cli-nombre', 'cli-cedula', 'cli-celular'].forEach(id => {
      document.getElementById(id).value = '';
    });
    document.getElementById('v-desc').value = 0;
    document.getElementById('v-efec').value = 0;
    renderPedido();
    calcTotal();
  }

  function cancelarVenta() {
    if (!Object.keys(pedido).length) {
      limpiarFormulario();
      return;
    }
    if (confirm('¿Cancelar la venta actual?')) {
      limpiarFormulario();
    }
  }

  function finalizarVenta() {
    if (!Object.keys(pedido).length) { alert('Agrega al menos un producto.'); return; }
    const tot = parseFloat(document.getElementById('v-total').textContent) || 0;
    const efec = parseFloat(document.getElementById('v-efec').value) || 0;
    if (efec < tot) { alert('El efectivo recibido debe ser igual o mayor al total.'); return; }

    snap = JSON.parse(JSON.stringify(pedido));   // guardar snapshot antes de limpiar

    const desc = parseFloat(document.getElementById('v-desc').value) || 0;
    const cambio = efec - tot;
    const cliente = {
      nombre: document.getElementById('cli-nombre').value.trim(),
      cedula: document.getElementById('cli-cedula').value.trim(),
      celular: document.getElementById('cli-celular').value.trim(),
    };
    const payload = {
      detalles: Object.entries(pedido).map(([id, p]) => ({
        menu_id: parseInt(id, 10), cantidad: p.cantidad, subtotal: p.subtotal
      })),
      total_venta: tot,
      descuento: desc,
      efectivo_recibido: efec,
      cambio,
      cliente: cliente.nombre ? cliente : null,
    };

    fetch(URLS.guardarVenta, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(r => r.json())
      .then(res => {
        if (res.success) {
          mostrarTicket(res, payload, cliente);
          limpiarFormulario();
        } else {
          alert('Error: ' + res.error);
        }
      })
      .catch(e => alert('Error de conexión: ' + e));
  }

  function mostrarTicket(res, payload, cliente) {
    const fecha = new Date().toLocaleString('es-BO');
    const items = Object.values(snap).map(p =>
      `<div class="tr"><span>${escapeHtml(String(p.cantidad))}x ${escapeHtml(p.nombre)}</span><span>${p.subtotal.toFixed(2)} Bs.</span></div>`
    ).join('');
    const cliHtml = cliente.nombre
      ? `<div class="tr"><span>Cliente:</span><span>${escapeHtml(cliente.nombre)}</span></div>
         ${cliente.cedula ? `<div class="tr tm"><span>CI:</span><span>${escapeHtml(cliente.cedula)}</span></div>` : ''}
         ${cliente.celular ? `<div class="tr tm"><span>Cel:</span><span>${escapeHtml(cliente.celular)}</span></div>` : ''}`
      : `<div class="tr tm"><span>Cliente:</span><span>Consumidor final</span></div>`;

    document.getElementById('ticket-papel').innerHTML = `
      <div class="tc tb" style="font-size:16px;letter-spacing:2px;">CHICKEN LINDO</div>
      <div class="tc tm">${fecha}</div>
      <div class="td"></div>
      ${cliHtml}
      <div class="td"></div>
      <div class="tr tb"><span>PRODUCTO</span><span>TOTAL</span></div>
      ${items}
      <div class="td"></div>
      <div class="tr"><span>Subtotal:</span><span>${(payload.total_venta + payload.descuento).toFixed(2)} Bs.</span></div>
      ${payload.descuento > 0 ? `<div class="tr"><span>Descuento:</span><span>-${payload.descuento.toFixed(2)} Bs.</span></div>` : ''}
      <div class="tr tb" style="font-size:14px;"><span>TOTAL:</span><span>${payload.total_venta.toFixed(2)} Bs.</span></div>
      <div class="tr"><span>Efectivo:</span><span>${payload.efectivo_recibido.toFixed(2)} Bs.</span></div>
      <div class="tr"><span>Cambio:</span><span>${payload.cambio.toFixed(2)} Bs.</span></div>
      <div class="td"></div>
      <div class="tc tm">Ticket #${res.ticket_id} — Venta #${res.venta_id}</div>
      <div class="tc" style="margin-top:8px;">¡Gracias por su preferencia!</div>`;
    document.getElementById('ov-ticket').classList.add('open');
  }
  function cTicket() { document.getElementById('ov-ticket').classList.remove('open'); }
  function printTicket() {
    const html = document.getElementById('ticket-papel').innerHTML;
    const w = window.open('', '_blank', 'width=380,height=600');
    w.document.write(`<!DOCTYPE html><html><head><title>Ticket</title>
    <style>body{font-family:'Courier New',monospace;font-size:12px;padding:16px;width:280px;margin:0 auto;}
    .tc{text-align:center}.tb{font-weight:900}.td{border-top:1px dashed #bbb;margin:5px 0;}
    .tr{display:flex;justify-content:space-between;margin:2px 0;}.tm{color:#666;font-size:11px;}
    </style></head><body>${html}</body></html>`);
    w.document.close();
    w.focus();
    setTimeout(() => { w.print(); w.close(); }, 300);
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('qty-btn-menos').addEventListener('click', () => dQty(-1));
    document.getElementById('qty-btn-mas').addEventListener('click', () => dQty(1));
    document.getElementById('qty-cancelar').addEventListener('click', cQty);
    document.getElementById('qty-agregar').addEventListener('click', okQty);
    document.getElementById('btn-aplicar-desc').addEventListener('click', calcTotal);
    document.getElementById('v-efec').addEventListener('input', calcCambio);
    document.getElementById('btn-finalizar-venta').addEventListener('click', finalizarVenta);
    document.getElementById('btn-cancelar-venta').addEventListener('click', cancelarVenta);
    document.getElementById('ticket-cerrar-1').addEventListener('click', cTicket);
    document.getElementById('ticket-cerrar-2').addEventListener('click', cTicket);
    document.getElementById('ticket-imprimir').addEventListener('click', printTicket);
  });

})();
