<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Top users - Select a Date Range</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script src="//code.jquery.com/jquery-1.10.2.js"></script>
  <script src="//code.jquery.com/ui/1.11.2/jquery-ui.js"></script>
  <script>
	  google.load('visualization', '1', {packages:['table']});
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
	      	var selected_customer = $( "#customer option:selected" ).text();
	        from =  $("#from").datepicker().val()
	        to=$("#to").datepicker().val()  
			$.get(
				'top_users',
				{"from_date": from, "to_date": to, 'customer': selected_customer},
				function(responsejson){
					var json_table = new google.visualization.Table(document.getElementById('orgchart'));
	      			var json_data = new google.visualization.DataTable(responsejson, 0.6);
	      			json_table.draw(json_data, {showRowNumber: true});
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
<label for="speed">Customer</label>
<select name="customer" id="customer">
%for customer in customers:
<option>${customer}</option>
%endfor
</select>
<input type="submit" value="Search">
<div id="orgchart"></div>
 
 
</body>
</html>