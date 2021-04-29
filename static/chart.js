var colors = [];
for (var i=0; i < labels.length; i++) {
  colors.push('#' + (Math.random().toString(16) + '0000000').slice(2, 8));
}
const data = {
  labels: labels,
  datasets: [
    {
      label: 'USD',
      data: usdsx,
      backgroundColor: colors,
    }
  ]
};
const config = {
  type: 'doughnut',
  data: data,
  options: {
    responsive: false,
    plugins: {
      legend: {
        position: 'right',
        display: false,
      },
      title: {
        display: true,
        text: 'DeFi Projects Valuations'
      },
      tooltip: {
        callbacks: {
          label: function(tooltipItem) {
            var total = 0;
            for (var i = 0; i < tooltipItem.dataset.data.length; ++i) {
              total = total + tooltipItem.dataset.data[i];
            }
            var current = tooltipItem.parsed;
            var percentage = parseFloat(((current / total) * 100).toFixed(3));
            //console.log(percentage);
            return tooltipItem.label + " : " + percentage + "%";
          }
        }
      }
    }
  }
};
var ctx = document.getElementById("myChart").getContext("2d");
var myChart = new Chart(ctx, config);
