document.addEventListener('DOMContentLoaded', function() {
  const hoy = new Date();
  const opciones = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  const fechaFormato = hoy.toLocaleDateString('es-BO', opciones);
  const el = document.getElementById('fecha-actual');
  if (el) el.textContent = 'Hoy: ' + fechaFormato;
});