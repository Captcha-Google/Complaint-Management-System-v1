$(function () {
  'use strict'

  var ticksStyle = {
    fontColor: '#495057',
    fontStyle: 'bold'
  }

  var mode = 'index'
  var intersect = true
  var backgroundColors = []

  var $complaintChart = $('#complaint_chart')

  $.ajax({
    url: $complaintChart.data('url'),
    success:function(response){
     for(var i = 0; i < response.amount.length; i++){
      if(response.amount[i] < 10){
        backgroundColors.push('#28a745')
      }else if(response.amount[i] >= 10){
        backgroundColors.push('#ffc107')
      }else if(response.amount[i] >= 50){
        backgroundColors.push('#dc3545')
      }
     }

      var complaintChart = new Chart($complaintChart, {
        type: 'bar',
        data: {
          labels: response.month,
          datasets: [
            {
              label: 'Complaint/s',
              backgroundColor: backgroundColors,
              borderColor: backgroundColors,
              data: response.amount
            }
          ]
        },
        options: {
          maintainAspectRatio: false,
          tooltips: {
            mode: mode,
            intersect: intersect
          },
          hover: {
            mode: mode,
            intersect: intersect
          },
          legend: {
            display: true
          },
          scales: {
            yAxes: [{
              // display: false,
              gridLines: {
                display: true,
                lineWidth: '4px',
                color: 'rgba(0, 0, 0, .2)',
                zeroLineColor: 'transparent'
              },
              ticks: $.extend({
                beginAtZero: true,
              }, ticksStyle)
            }],
            xAxes: [{
              display: true,
              gridLines: {
                display: true
              },
              ticks: ticksStyle
            }]
          }
        }
      })

    }
  })

  var $PurokChart = $('#purok_chart')

  $.ajax({
    url: $PurokChart.data('url'),
    success: function(response){
      var PurokChart = new Chart($PurokChart, {
        data: {
          labels: response.purok_name,
          datasets: [{
            label: '# of Complaint/s',
            type: 'line',
            data: response.no_complaints,
            backgroundColor: 'transparent',
            borderColor: '#28a745',
            pointBorderColor: '#28a745',
            pointBackgroundColor: '#28a745',
            fill: false,
          }
        ]
        },
        options: {
          maintainAspectRatio: false,
          tooltips: {
            mode: mode,
            intersect: intersect
          },
          hover: {
            mode: mode,
            intersect: intersect
          },
          legend: {
            display: true
          },
          scales: {
            yAxes: [{
              display: true,
              gridLines: {
                display: true,
                lineWidth: '4px',
                color: 'rgba(0, 0, 0, .2)',
                zeroLineColor: 'transparent'
              },
              ticks: $.extend({
                beginAtZero: true,
                suggestedMax: false
              }, ticksStyle)
            }],
            xAxes: [{
              display: true,
              gridLines: {
                display: true
              },
              ticks: ticksStyle
            }]
          }
        }
      })
    }
  })

})
