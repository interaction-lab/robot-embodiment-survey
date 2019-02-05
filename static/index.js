$('.abstractionSlider').slider({
    formatter: function (value) {
        return 'Current value: ' + value;
    }
});

console.log("index");

$().ready(() => {
    console.log("ready");
});

$("#submit").click(function (e) {
    console.log(e);
    console.log("submit");
    let data = {
        assignmentId: ASSIGNMENT_ID,
    };
    $("input").each(function () {
        let txt = this;
        let o = $(txt);
        let name = o.data("robot-name");
        let dataType = o.data("type");
        if (!(name in data)) {
            data[name] = {}
        }
        data[name][dataType] = o.val();
    });
    console.log(JSON.stringify(data));
    console.log(SUBMISSION_URL);

    $.ajax({
        type: "POST",
        url: SUBMISSION_URL,
        data: data
    }, function (e) {
        console.log(e);
        console.log("success");
    });
});