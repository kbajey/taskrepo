<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Top customers for a Date Range</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script src="//code.jquery.com/jquery-1.10.2.js"></script>
  <script src="//code.jquery.com/ui/1.11.2/jquery-ui.js"></script>
  <script>
	  google.load('visualization', '1', {packages:['table', 'corechart']});
	  $(function() {
	  $( "#from" ).datepicker({
	      dateFormat: "yy-mm-dd",
	    });
	  $( "#to" ).datepicker({
	      dateFormat: "yy-mm-dd",
	    });
	  });
	  $(function() {
	    $( "input[type=submit]" )
	      .button()
	      .click(function( event ) {
	        var selected_size = $( "#size option:selected" ).text();
	        from =  $("#from").datepicker().val()
	        to=$("#to").datepicker().val()  
			$.get(
				'top_customers',
				{"from_date": from, "to_date": to, 'size': selected_size},
				function(responsejson){
					var json_table = new google.visualization.Table(document.getElementById('orgchart'));
	      			var json_data = new google.visualization.DataTable(responsejson, 0.6);
	      			json_table.draw(json_data, {showRowNumber: true});
	      			
	      			var options = {
         				 title: 'Customers Search Distribution',
         				 is3D: true
        			};

        			var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        			chart.draw(json_data, options);
        			
        			var options = {
          title: 'Customers Search Numbers'
        };

        //var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
        var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
        chart.draw(json_data, options);
	      			
				},
				"json"
			);
	      });
	  });
  </script>
</head>
<body>
 
<label for="from">From</label>
<input type="text" id="from" name="from">
<label for="to">to</label>
<input type="text" id="to" name="to">
<label for="speed">Size</label>
<select name="size" id="size">
%for size in sizes:
<option>${size}</option>
%endfor
</select>
<input type="submit" value="Search">
<div id="orgchart"></div>
<div id="piechart" style="width: 900px; height: 500px;"></div>
<div id="chart_div" style="width: 900px; height: 500px;"></div>
 
 
</body>
</html>