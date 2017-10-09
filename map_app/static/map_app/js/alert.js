'use strict';

var displayAlert = function displayAlert(message) {
    var tag = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : "info";

    if (tag === 'error') {
        tag = 'danger';
    }
    var alertDiv = '<div class="alert alert-' + tag + '" id="page-alert" style="display: none;">' + message + '</div>';
    $(alertDiv).appendTo($('.nav-alert')).slideUp(200);
    addAlertHandler(undefined);
};

var renderAlerts = function renderAlerts(messages) {
    var _iteratorNormalCompletion = true;
    var _didIteratorError = false;
    var _iteratorError = undefined;

    try {
        for (var _iterator = messages[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
            var message = _step.value;

            displayAlert(message.message, message.level_tag);
        }
    } catch (err) {
        _didIteratorError = true;
        _iteratorError = err;
    } finally {
        try {
            if (!_iteratorNormalCompletion && _iterator.return) {
                _iterator.return();
            }
        } finally {
            if (_didIteratorError) {
                throw _iteratorError;
            }
        }
    }
};

var removeAlert = function removeAlert(e) {
    $(e.target).fadeTo(500, 0).slideUp(300, function () {
        return $(e.target).remove();
    });
};

var addAlertHandler = function addAlertHandler() {
    var target = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '.alert';

    $(target).bind('click', removeAlert);
};

$('#addresses_table').on('saved-address', addAlertHandler);

$(document).ready(function () {
    return addAlertHandler();
});
