(function() {
  'use strict';

  document.addEventListener('DOMContentLoaded', initCharts);

  function initCharts() {
    if (!window.REPORTES_DATA || window.REPORTES_DATA.length === 0) return;

    window.REPORTES_DATA.forEach(chartConfig => {
      const canvasEl = document.getElementById(chartConfig.canvasId);
      if (!canvasEl) return;

      const ctx = canvasEl.getContext('2d');
      renderChart(ctx, chartConfig);
    });
  }

  function renderChart(ctx, config) {
    const { tipo, labels, data, title, options = {} } = config;

    let chartType = 'bar';
    let chartOptions = {
      plugins: {
        legend: { display: true },
        title: { display: true, text: title || '', font: { size: 16 }, padding: { bottom: 20 } }
      },
      scales: { y: { beginAtZero: true } }
    };

    if (tipo === 'barras_h') {
      chartType = 'bar';
      chartOptions.indexAxis = 'y';
      chartOptions.plugins.legend = { display: false };
    } else if (tipo === 'dona') {
      chartType = 'doughnut';
      delete chartOptions.scales;
      chartOptions.plugins.legend = { position: 'right' };
    } else if (tipo === 'linea') {
      chartType = 'line';
      chartOptions.plugins.legend = { display: true };
    }

    chartOptions = { ...chartOptions, ...options };

    new Chart(ctx, {
      type: chartType,
      data: { labels: labels, datasets: data },
      options: chartOptions
    });
  }
})();