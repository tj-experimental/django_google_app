
const $progress = $("#progress");

const stopProgress = () => $progress.addClass("done");

const errorProgress = () => $progress.removeClass("success").addClass("error");

const successProgress = () => $progress.addClass("success").removeClass("error");

const startProgress = (status = "", duration = 4000) => {
    return $({property: 0}).animate({property: 105}, {
                duration: duration,
                step: function() {
                    let _percent = Math.round(this.property);
                    $progress.removeClass("done");
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
