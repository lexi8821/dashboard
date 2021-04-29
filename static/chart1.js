function createChart(chartElement, labelsSet, dataset, selection) {
  const data = {
    labels: labelsSet,
    datasets: [
      {
        label: selection,
        data: dataset,
        backgroundColor: "rgba(255, 99, 132, 0.6)",
      }
    ]
  };

  const config = {
    type: 'bar',
    data: data,
    options: {
      responsive: false,
      plugins: {
        legend: {
          position: 'top',
          display: false,
        },
        title: {
          display: false,
          text: 'DeFi Projects Valuations'
        },
      }
    }
  };

  var ctx = document.getElementById(chartElement).getContext("2d");
  var myChart = new Chart(ctx, config);
}
