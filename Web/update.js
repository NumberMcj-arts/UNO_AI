
function update(){
//	$.ajax({
//		url: "update.php",
//		success: function(state){
//			var nr = state;
//			document.getElementById('state').value = nr;
//		};
//	})
	
	$.ajax({
		type: "POST",
		url: "update.php",
//		data: {
			val: document.getElementById('state').value//,
//			b: 'zack'
//		}
	}).done(function(o) {
		document.getElementById('state').value = o;
	});
}

function initState(){
	document.getElementById('state').value = 'zack';
}

