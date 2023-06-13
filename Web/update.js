
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
		const game_state = JSON.parse(o);
		//const test = JSON.parse('{"a": 13, "b": 5}')
		document.getElementById('kack').value = game_state.card_on_top;
		//alert(game_state.current_player)
		//alert("Test")
	});
}

function initState(){
	//const test = JSON.parse('{"a": 13, "b": 5, "c": 10}')
	//document.getElementById('kack').value = test.c;
	$.ajax({
		type: "POST",
		url: "update.php",
//		data: {
			val: document.getElementById('state').value//,
//			b: 'zack'
//		}
	}).done(function(o) {
		const game_state = JSON.parse(o);
		//const test = JSON.parse('{"a": 13, "b": 5}')
		document.getElementById('state').value = game_state.current_player;
		//alert(game_state.current_player)
		//alert("Test")
	});
}

