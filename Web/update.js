
function update(){
	$.ajax({
		type: "POST",
		url: "update.php",
//		data: {
			val: document.getElementById('state').value//,
//			b: 'zack'
//		}
	}).done(function(o) {
		const game_state = JSON.parse(o);
		document.getElementById('kack').value = game_state.card_on_top;
	});
}

function initState(){
	const test = JSON.parse('{"a": 13, "b": 5, "c": 10}')
	document.getElementById('kack').value = test.c;
}

