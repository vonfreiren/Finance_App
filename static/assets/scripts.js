$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

/*!
* Start Bootstrap - Clean Blog v5.1.0 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
(function ($) {
    "use strict"; // Start of use strict

    // Floating label headings for the contact form
    $("body").on("input propertychange", ".floating-label-form-group", function (e) {
        $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
    }).on("focus", ".floating-label-form-group", function () {
        $(this).addClass("floating-label-form-group-with-focus");
    }).on("blur", ".floating-label-form-group", function () {
        $(this).removeClass("floating-label-form-group-with-focus");
    });

    // Show the navbar when the page is scrolled up
    var MQL = 992;

    //primary navigation slide-in effect
    if ($(window).width() > MQL) {
        var headerHeight = $('#mainNav').height();
        $(window).on('scroll', {
                previousTop: 0
            },
            function () {
                var currentTop = $(window).scrollTop();
                //check if user is scrolling up
                if (currentTop < this.previousTop) {
                    //if scrolling up...
                    if (currentTop > 0 && $('#mainNav').hasClass('is-fixed')) {
                        $('#mainNav').addClass('is-visible');
                    } else {
                        $('#mainNav').removeClass('is-visible is-fixed');
                    }
                } else if (currentTop > this.previousTop) {
                    //if scrolling down...
                    $('#mainNav').removeClass('is-visible');
                    if (currentTop > headerHeight && !$('#mainNav').hasClass('is-fixed')) $('#mainNav').addClass('is-fixed');
                }
                this.previousTop = currentTop;
            });
    }


})(jQuery); // End of use strict


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