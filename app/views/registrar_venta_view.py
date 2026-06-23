from flask import render_template, request, redirect, url_for, jsonify
from flask_appbuilder import BaseView, expose
from flask_login import login_required, current_user
from app.extensions import db
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta
from app.models.ticket import Ticket
from app.models.menu import Menu
from app.models.cliente import Cliente


class RegistrarVentaView(BaseView):
    route_base = "/registrar-venta"
    default_view = "registrar"

    @expose("/")
    @login_required
    def registrar(self):
        return self.render_template("registrar_venta.html")

    @expose("/api/menu", methods=["GET"])
    @login_required
    def get_menu(self):
        from app.models.categoria import Categoria
        categorias = db.session.query(Categoria).all()
        data = {}
        for cat in categorias:
            items = [m for m in cat.menus if m.estado == 1]
            if items:
                data[cat.nombre] = [
                    {'id': m.id, 'nombre': m.nombre, 'precio': float(m.precio)}
                    for m in items
                ]
        return jsonify(data)

    @expose("/api/guardar-venta", methods=["POST"])
    @login_required
    def guardar_venta(self):
        try:
            data = request.get_json()

            # --- Resolver/crear cliente si viene con datos ---
            cliente_id = None
            cliente_data = data.get('cliente')
            if cliente_data and cliente_data.get('nombre'):
                cedula  = cliente_data.get('cedula', '').strip() or None
                celular = cliente_data.get('celular', '').strip() or None
                nombre  = cliente_data.get('nombre', '').strip()

                # Buscar por cédula o celular para no duplicar
                cliente = None
                if cedula:
                    cliente = db.session.query(Cliente).filter_by(documento=cedula).first()
                if not cliente and celular:
                    cliente = db.session.query(Cliente).filter_by(celular=celular).first()

                if not cliente:
                    cliente = Cliente(nombre=nombre, documento=cedula, celular=celular)
                    db.session.add(cliente)
                    db.session.flush()
                else:
                    # Actualizar nombre si cambió
                    cliente.nombre = nombre
                    db.session.flush()

                cliente_id = cliente.id

            # --- Venta ---
            venta = Venta()
            venta.usuario_id = current_user.id
            venta.total_venta = data.get('total_venta', 0)
            db.session.add(venta)
            db.session.flush()

            # --- Detalles ---
            for det in data.get('detalles', []):
                dv = DetalleVenta()
                dv.venta_id  = venta.id
                dv.menu_id   = det['menu_id']
                dv.cantidad  = det['cantidad']
                dv.subtotal  = det['subtotal']
                db.session.add(dv)

            # --- Ticket ---
            ticket = Ticket()
            ticket.venta_id         = venta.id
            ticket.cliente_id       = cliente_id
            ticket.numero_pedido    = data.get('numero_pedido')
            ticket.descuento        = data.get('descuento', 0)
            ticket.total            = data.get('total_venta', 0)
            ticket.efectivo_recibido = data.get('efectivo_recibido', 0)
            ticket.cambio           = data.get('cambio', 0)
            ticket.emitido_por      = current_user.id
            db.session.add(ticket)

            db.session.commit()

            return jsonify({'success': True, 'venta_id': venta.id, 'ticket_id': ticket.id})

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 400