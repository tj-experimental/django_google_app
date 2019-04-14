const resetAddresses = () => {
    window.startProgress();
    window.successProgress();
    $.ajax(
        window.resetUrl,
        {'method': "DELETE"}
    ).done(function (data, textStatus, jqXHR) {
        let message = "Successfully reset addresses";
        renderAlerts([{message: message, level_tag: 'success'}]);
        return true;
    }).fail(function (jqXHR, textStatus, err) {
        window.errorProgress();
        let message = "Error resetting addresses";
        renderAlerts([{message: message, level_tag: 'error'}]);
        console.log(textStatus);
        return true;
    }).always(function(){
        location.reload();
        window.stopProgress();
    })
};
$('#reset-button').data("callable", resetAddresses);
