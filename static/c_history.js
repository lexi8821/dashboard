function CreateHistoryChart(chartElement, labelsSet, dataset) {
  const data = {
    labels: labelsSet,
    datasets: [{
      label: "Total Value Locked (USD)",
      data: dataset,
      fill: false,
      borderColor: "rgba(255, 99, 132, 0.6)",
      tension: 0.1
    }]
  };

  const config = {
    type: 'line',
    data: data,
  };

  var ctx = document.getElementById(chartElement).getContext("2d");
  var myChart = new Chart(ctx, config);
}
