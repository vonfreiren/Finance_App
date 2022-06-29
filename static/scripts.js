$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

function loading4() {
    var assets = 0;
    var inputs = document.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].name.indexOf('asset') == 0) {
            if (inputs[i].value != "") {
                assets = assets + 1;
            }
        }
    }
    if (assets > 0) {
        $(".btn-sm .fa-spinner").show();
        $(".btn-sm .btn-text").html("Loading");
    } else {
        alert("At least 2 assets must be provided")
        event.preventDefault()

        return false
    }

}

function loading3() {
    var assets = 0;
    var inputs = document.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].name.indexOf('asset') == 0) {
            if (inputs[i].value != "") {
                assets = assets + 1;
            }
        }
    }
    if (assets > 1) {
        $(".btn-sm .fa-spinner").show();
        $(".btn-sm .btn-text").html("Loading");
    } else {
        alert("At least 2 assets must be provided")
        event.preventDefault()

        return false
    }

}

function loading2() {
    var assets = 0;
    let initialValue = document.forms["form_opti"]["initialValue2"].value;
    value = parseInt(initialValue)
    var inputs = document.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].name.indexOf('asset') == 0) {
            if (inputs[i].value != "") {
                assets = assets + 1;
            }
        }
    }
    if (assets > 1 && value > 0) {
        $(".btn-sm .fa-spinner").show();
        $(".btn-sm .btn-text").html("Loading");
    } else {
        alert("The initial value and at least 2 assets must be provided")
        event.preventDefault()

        return false
    }

}

function loading() {
    var total = 0;
    let stock = document.forms["form"]["asset"].value;
    var inputs = document.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].name.indexOf('weight') == 0) {
            weight = parseInt(inputs[i].value)
            total = total + weight
        }
    }
    if (total != 100 && stock == "") {
        alert("The Single  Asset must be filled or.\n The Multiple Assets and the total weights must equal 100")
        event.preventDefault()
        return false
    } else {
        $(".btn-sm .fa-spinner").show();
        $(".btn-sm .btn-text").html("Loading");
    }
}



$(document).ready(function () {
    $(".btn-sm .fa-spinner").hide();

});