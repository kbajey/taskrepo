<html>
  <head>
    <title>Response Chart till ${date_from}</title>
    <%! import json %>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable(${json.dumps(data1) | n});
        var options = {
          title: 'Init.JS Response Time'
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_init'));

        chart.draw(data, options);
      }
    </script>
<script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable(${json.dumps(data2) | n});

        var options = {
          title: 'Recommendation Response Time'
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_rcd'));

        chart.draw(data, options);
      }
    </script>
<script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable(${json.dumps(data3) | n});

        var options = {
          title: 'Search Response Time'
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_srch'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="chart_init" style="width: 500px; height: 300px; float: left"></div>
    <div id="chart_rcd" style="width: 500px; height: 300px; float: right"></div>
    <div id="chart_srch" style="width: 500px; height: 300px; top: 350"></div>
  </body>
</html>