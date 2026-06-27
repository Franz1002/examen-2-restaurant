from flask import render_template, request
from flask_appbuilder import BaseView, expose
from flask_login import login_required
from app.extensions import db
from app.models.detalle_venta import DetalleVenta
from app.models.menu import Menu
from app.models.categoria import Categoria
from app.models.cliente import Cliente
from app.models.ticket import Ticket
from app.models.venta import Venta
from app.services.gemini_service import pronostico_productos, pronostico_clientes, pronostico_ventas, pronostico_ventas_futuras
from sqlalchemy import func
from datetime import datetime, timedelta


class ReportesView(BaseView):
    route_base = "/reportes"
    default_view = "productos_vendidos"

    @expose("/productos-vendidos")
    @login_required
    def productos_vendidos(self):
        reporte = db.session.query(
            Menu.nombre,
            Menu.id,
            Categoria.nombre.label('categoria'),
            func.sum(DetalleVenta.cantidad).label('cantidad_total'),
            func.sum(DetalleVenta.subtotal).label('ingresos_total'),
            func.count(DetalleVenta.id).label('veces_vendido')
        ).join(
            DetalleVenta, Menu.id == DetalleVenta.menu_id
        ).join(
            Categoria, Menu.categoria_id == Categoria.id
        ).group_by(
            Menu.id, Menu.nombre, Categoria.nombre
        ).order_by(
            func.sum(DetalleVenta.subtotal).desc()
        ).all()

        datos_ia = [
            {"producto": r.nombre, "cantidad": int(r.cantidad_total), "ingresos_bs": float(r.ingresos_total)}
            for r in reporte
        ]
        pronostico = pronostico_productos(datos_ia)

        return self.render_template(
            "reportes/productos_vendidos.html",
            reporte=reporte,
            pronostico=pronostico
        )

    @expose("/clientes-compras")
    @login_required
    def clientes_compras(self):
        reporte = db.session.query(
            Cliente.nombre,
            Cliente.id,
            Cliente.celular,
            func.count(Ticket.id).label('num_tickets'),
            func.sum(Ticket.total).label('total_gastado'),
            func.avg(Ticket.total).label('ticket_promedio')
        ).outerjoin(
            Ticket, Cliente.id == Ticket.cliente_id
        ).group_by(
            Cliente.id, Cliente.nombre, Cliente.celular
        ).order_by(
            func.sum(Ticket.total).desc()
        ).all()

        datos_ia = [
            {"cliente": r.nombre or "Consumidor Final", "tickets": int(r.num_tickets or 0), "total_gastado_bs": float(r.total_gastado or 0)}
            for r in reporte
        ]
        pronostico = pronostico_clientes(datos_ia)

        return self.render_template(
            "reportes/clientes_compras.html",
            reporte=reporte,
            pronostico=pronostico
        )

    @expose("/ventas-por-fecha")
    @login_required
    def ventas_por_fecha(self):
        fecha_inicio_str = request.args.get('fecha_inicio')
        fecha_fin_str = request.args.get('fecha_fin')

        fecha_fin = datetime.now()
        fecha_inicio = fecha_fin - timedelta(days=30)

        if fecha_fin_str:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d')
        if fecha_inicio_str:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')

        venta_data = db.session.query(
            func.sum(Venta.total_venta).label('total_vendido'),
            func.sum(Ticket.descuento).label('total_descuentos'),
            func.sum(Ticket.efectivo_recibido).label('efectivo_recibido'),
            func.sum(Ticket.cambio).label('cambio_entregado'),
            func.count(Ticket.id).label('num_tickets')
        ).join(
            Ticket, Venta.id == Ticket.venta_id
        ).filter(
            Venta.fecha_venta >= fecha_inicio,
            Venta.fecha_venta <= fecha_fin
        ).first()

        reporte_diario = db.session.query(
            func.date(Venta.fecha_venta).label('fecha'),
            func.sum(Venta.total_venta).label('total_dia'),
            func.count(Ticket.id).label('tickets_dia'),
            func.sum(Ticket.descuento).label('desc_dia')
        ).join(
            Ticket, Venta.id == Ticket.venta_id
        ).filter(
            Venta.fecha_venta >= fecha_inicio,
            Venta.fecha_venta <= fecha_fin
        ).group_by(
            func.date(Venta.fecha_venta)
        ).order_by(
            func.date(Venta.fecha_venta).desc()
        ).all()

        datos_ia = [
            {"fecha": str(r.fecha), "total_bs": float(r.total_dia or 0), "tickets": int(r.tickets_dia or 0)}
            for r in reporte_diario
        ]
        pronostico = pronostico_ventas(datos_ia)
        pronostico_futuro = pronostico_ventas_futuras(datos_ia)

        return self.render_template(
            "reportes/ventas_por_fecha.html",
            venta_data=venta_data,
            reporte_diario=reporte_diario,
            fecha_inicio=fecha_inicio.strftime('%Y-%m-%d'),
            fecha_fin=fecha_fin.strftime('%Y-%m-%d'),
            pronostico=pronostico,
            pronostico_futuro=pronostico_futuro
            
        )

    @expose("/dashboard")
    @login_required
    def dashboard(self):
        hoy = datetime.now().date()

        arqueo = db.session.query(
            func.sum(Venta.total_venta).label('total_vendido'),
            func.sum(Ticket.descuento).label('total_descuentos'),
            func.sum(Ticket.efectivo_recibido).label('efectivo_recibido'),
            func.sum(Ticket.cambio).label('cambio_entregado'),
            func.count(Ticket.id).label('num_tickets')
        ).join(
            Ticket, Venta.id == Ticket.venta_id
        ).filter(
            func.date(Venta.fecha_venta) == hoy
        ).first()

        return self.render_template(
            "dashboard.html",
            arqueo=arqueo
        )