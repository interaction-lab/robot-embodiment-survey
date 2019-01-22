$('.abstractionSlider').slider({
	formatter: function(value) {
		return 'Current value: ' + value;
	}
});

console.log("index");

$().ready(() => {
	console.log("ready");
});