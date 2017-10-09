"use strict";

var $progress = $("#progress");

var stopProgress = function stopProgress() {
    return $progress.addClass("done");
};

var errorProgress = function errorProgress() {
    return $progress.toggleClass("success").addClass("error");
};

var startProgress = function startProgress() {
    var color = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : "";
    var duration = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 4000;

    return $({ property: 0 }).animate({ property: 105 }, {
        duration: duration,
        step: function step() {
            var _percent = Math.round(this.property);
            $progress.removeClass("done").addClass("success").removeClass("error");
            $progress.css('width', _percent + "%");
            if (_percent == 105) {
                stopProgress();
            }
        }
        // complete: function() {
        //     alert('complete');
        // }
    });
};
