document.addEventListener('DOMContentLoaded', function () {

  /* ---- Mobile sidebar toggle (hook up to base.html's existing hamburger if present) ---- */
  var sidebar = document.getElementById('dashSidebar');
  var toggleBtn = document.getElementById('sidebarToggle'); // expected id on hamburger button in base.html
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', function () {
      sidebar.classList.toggle('is-open');
    });
  }

  /* ---- Sales overview chart ---- */
  var canvas = document.getElementById('saleChart');
  if (canvas && window.Chart) {
    var ctx = canvas.getContext('2d');

    var gradient = ctx.createLinearGradient(0, 0, 0, 260);
    gradient.addColorStop(0, 'rgba(212, 175, 55, 0.28)');
    gradient.addColorStop(1, 'rgba(212, 175, 55, 0)');

    var dataEl = document.getElementById('salesChartData');
    var labels = ['May 18', 'May 19', 'May 20', 'May 21', 'May 22', 'May 23', 'May 24'];
    var values = [21000, 27500, 39500, 31000, 33500, 23500, 36500];

    if (dataEl) {
      try {
        var parsed = JSON.parse(dataEl.textContent);
        if (parsed.labels) labels = parsed.labels;
        if (parsed.values) values = parsed.values;
      } catch (e) { /* fall back to defaults */ }
    }

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Revenue (KSh)',
          data: values,
          borderColor: '#D4AF37',
          backgroundColor: gradient,
          borderWidth: 2,
          pointBackgroundColor: '#0a0a0a',
          pointBorderColor: '#D4AF37',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
          tension: 0.35,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              usePointStyle: true,
              pointStyle: 'circle',
              color: '#6c757d',
              font: { family: 'Montserrat', size: 12 }
            }
          },
          tooltip: {
            backgroundColor: '#0a0a0a',
            titleFont: { family: 'Montserrat', weight: '600' },
            bodyFont: { family: 'Montserrat' },
            padding: 10,
            cornerRadius: 8,
            displayColors: false,
            callbacks: {
              label: function (item) {
                return 'KSh ' + item.parsed.y.toLocaleString();
              }
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: '#6c757d', font: { family: 'Montserrat', size: 11 } }
          },
          y: {
            beginAtZero: true,
            grid: { color: '#e7e3d8' },
            ticks: {
              color: '#6c757d',
              font: { family: 'Montserrat', size: 11 },
              callback: function (val) {
                return val >= 1000 ? (val / 1000) + 'K' : val;
              }
            }
          }
        }
      }
    });
  }
  const salesChart = document.getElementById(
      "salesChart"
  );


  if (salesChart) {


      new Chart(
          salesChart,
          {


          type: "line",


          data: {


              labels: salesLabels,


              datasets: [{

                  label: "Revenue (KSh)",


                  data: salesValues,


                  tension: 0.4,


                  fill: true

              }]


          },


          options: {


              responsive: true,


              plugins: {


                  legend: {


                      display: true


                  }


              }


          }


      });

  }
  /* ---- Sales range selector re-renders chart (placeholder hook for AJAX) ---- */
  var rangeSelect = document.getElementById('salesRangeSelect');
  if (rangeSelect) {
    rangeSelect.addEventListener('change', function () {
      // Hook point: fetch new dataset for this range via fetch() and update chart.data
      console.log('Sales range changed to:', rangeSelect.value);
    });
  }

});
