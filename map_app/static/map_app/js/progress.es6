
const $progress = $("#progress");

const stopProgress = () => $progress.addClass("done");

const errorProgress = () => $progress.toggleClass("success").addClass("error");

const startProgress = (color = "", duration = 4000) => {
    return $({property: 0}).animate({property: 105}, {
                duration: duration,
                step: function() {
                    let _percent = Math.round(this.property);
                    $progress.removeClass("done").addClass("success"
                    ).removeClass("error");
                    $progress.css('width',  _percent+"%");
                    if(_percent == 105) {
                        stopProgress();
                    }
                },
                // complete: function() {
                //     alert('complete');
                // }
            });
};
