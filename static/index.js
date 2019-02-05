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
        robots: {}
    };
    $("input").each(function () {
        let txt = this;
        let o = $(txt);
        let name = o.data("robot-name");
        let dataType = o.data("type");
        if (!(name in data['robots'])) {
            data['robots'][name] = {}
        }
        data['robots'][name][dataType] = o.val();
    });
    console.log(JSON.stringify(data));


    $.ajax({
        type: "POST",
        url: SERVER_SUBMISSION,
        data: JSON.stringify(data),
        contentType: 'application/json'
    }, function () {
        console.log("server submit success, doing mturk submission");
        $.ajax({
            type: "POST",
            url: MTURK_SUBMISSION_URL,
            data: data
        }, function (e) {
            console.log(e);
            console.log("success");
        });
    });
});