# Chicken Lindo — Sistema de Gestión de Restaurante

**Materia:** Taller de Aplicaciones en Internet  
**Docente:** Ing. Ximena Añaguaya  
**Gestión:** 2026 — Examen 2do Parcial  
**Estudiante:** Franz Erik Cori Copaly  
**Universidad:** Universidad Adventista de Bolivia (UAB)

---

## Descripción del Sistema

**Chicken Lindo** es un sistema web de gestión para restaurantes desarrollado con Flask-AppBuilder, SQLAlchemy y MySQL. El sistema permite administrar el catálogo de productos, registrar ventas, emitir tickets y generar reportes con gráficas estadísticas.

El sistema está orientado al restaurante **"Chicken Lindo a la Leña"**, ubicado en Shinahota, Chapare, y cubre el flujo completo de una venta: desde la selección de productos hasta la emisión del ticket de cobro.

---

## Funcionalidades Principales

### Catálogo
- Gestión de **categorías** de productos (Platos, Bebidas, Combos, etc.)
- Gestión de **menú** con nombre, precio, descripción e imagen por categoría

### Registro de Ventas (POS)
- Pantalla interactiva estilo punto de venta (POS)
- Selección de productos por categoría con cantidad configurable
- Cálculo automático de subtotal, descuento, total y cambio
- Emisión e impresión de **ticket** al finalizar la venta
- Registro opcional del cliente en cada venta

### Gestión de Clientes
- Registro de clientes con nombre, celular y documento de identidad
- Fecha de registro automática

### Reportes con Gráficas
| Reporte | Descripción | Gráfica |
|---|---|---|
| Productos más vendidos | Muestra qué productos generan más ingresos y cantidad vendida | Barras horizontales |
| Historial por cliente | Total gastado, número de tickets y ticket promedio por cliente | Dona |
| Corte de caja | Ventas por rango de fechas con detalle diario | Línea con área |

### Dashboard (Arqueo Diario)
- Página principal al loguearse
- Muestra en tiempo real: total vendido hoy, tickets emitidos, descuentos, efectivo recibido y cambio entregado

### Roles y Permisos
| Rol | Acceso |
|---|---|
| Admin | Acceso total al sistema |
| Cajera | Registrar ventas, agregar clientes, emitir tickets |
| Supervisor | Solo lectura — ver reportes y estadísticas |

---

## Tecnologías Utilizadas

- **Backend:** Python 3, Flask, Flask-AppBuilder 5.2.1
- **Base de datos:** MySQL + SQLAlchemy
- **Frontend:** Bootstrap 5, Chart.js, JavaScript (ES6)
- **Control de versiones:** Git + GitHub (flujo por ramas con Pull Requests)

---

## Estructura de la Base de Datos

```
categoria ──< menu ──< detalle_venta >── venta >── ticket
                                                      │
cliente ──────────────────────────────────────────────┘
```

6 tablas propias + tablas de autenticación de Flask-AppBuilder (ab_user, ab_role, etc.)

---

## Flujo de Ramas (Git)

```
main
 └── develop
      ├── feature/catalogo          → Categoria, Menu
      ├── feature/clientes-ventas   → Cliente, Venta, DetalleVenta, Ticket
      ├── feature/roles-auth        → Admin, Cajera, Supervisor
      ├── feature/registrar-venta   → POS interactivo + emisión de tickets
      ├── feature/reportes          → 3 reportes funcionales
      ├── feature/graficas          → 3 gráficas con Chart.js
      └── feature/dashboard         → Arqueo diario como página principal
```

Cada rama fue mergeada a `develop` mediante Pull Request. Al finalizar, `develop` fue mergeado a `main` como versión final de entrega.

---

## Repositorio

🔗 [https://github.com/Franz1002/examen-2-restaurant](https://github.com/Franz1002/examen-2-restaurant)
