// Core JavaScript helper functions
'use strict';
$(document).ready(function() {
    $('#update-button').click(function() {
        $.ajax({
            url: '/update_data/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $('#updated-data').html(data.updated_data);
            }
        });
    });
});

const filterInput = document.getElementById('filter-input');
const servicesList = document.getElementById('services-list').getElementsByTagName('li');

filterInput.addEventListener('input', function() {
  const filterValue = filterInput.value.toLowerCase();

  // Показать или скрыть элементы списка на основе фильтра
  Array.from(servicesList).forEach(function(item) {
    const serviceName = item.firstElementChild.textContent.toLowerCase();
    const display = serviceName.includes(filterValue) ? 'block' : 'none';
    item.style.display = display;
  });
});
$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
// quickElement(tagType, parentReference [, textInChildNode, attribute, attributeValue ...]);
function quickElement() {
    const obj = document.createElement(arguments[0]);
    if (arguments[2]) {
        const textNode = document.createTextNode(arguments[2]);
        obj.appendChild(textNode);
    }
    const len = arguments.length;
    for (let i = 3; i < len; i += 2) {
        obj.setAttribute(arguments[i], arguments[i + 1]);
    }
    arguments[1].appendChild(obj);
    return obj;
}

// "a" is reference to an object
function removeChildren(a) {
    while (a.hasChildNodes()) {
        a.removeChild(a.lastChild);
    }
}

// ----------------------------------------------------------------------------
// Find-position functions by PPK
// See https://www.quirksmode.org/js/findpos.html
// ----------------------------------------------------------------------------
function findPosX(obj) {
    let curleft = 0;
    if (obj.offsetParent) {
        while (obj.offsetParent) {
            curleft += obj.offsetLeft - obj.scrollLeft;
            obj = obj.offsetParent;
        }
    } else if (obj.x) {
        curleft += obj.x;
    }
    return curleft;
}

function findPosY(obj) {
    let curtop = 0;
    if (obj.offsetParent) {
        while (obj.offsetParent) {
            curtop += obj.offsetTop - obj.scrollTop;
            obj = obj.offsetParent;
        }
    } else if (obj.y) {
        curtop += obj.y;
    }
    return curtop;
}

//-----------------------------------------------------------------------------
// Date object extensions
// ----------------------------------------------------------------------------
{
    Date.prototype.getTwelveHours = function() {
        return this.getHours() % 12 || 12;
    };

    Date.prototype.getTwoDigitMonth = function() {
        return (this.getMonth() < 9) ? '0' + (this.getMonth() + 1) : (this.getMonth() + 1);
    };

    Date.prototype.getTwoDigitDate = function() {
        return (this.getDate() < 10) ? '0' + this.getDate() : this.getDate();
    };

    Date.prototype.getTwoDigitTwelveHour = function() {
        return (this.getTwelveHours() < 10) ? '0' + this.getTwelveHours() : this.getTwelveHours();
    };

    Date.prototype.getTwoDigitHour = function() {
        return (this.getHours() < 10) ? '0' + this.getHours() : this.getHours();
    };

    Date.prototype.getTwoDigitMinute = function() {
        return (this.getMinutes() < 10) ? '0' + this.getMinutes() : this.getMinutes();
    };

    Date.prototype.getTwoDigitSecond = function() {
        return (this.getSeconds() < 10) ? '0' + this.getSeconds() : this.getSeconds();
    };

    Date.prototype.getAbbrevMonthName = function() {
        return typeof window.CalendarNamespace === "undefined"
            ? this.getTwoDigitMonth()
            : window.CalendarNamespace.monthsOfYearAbbrev[this.getMonth()];
    };

    Date.prototype.getFullMonthName = function() {
        return typeof window.CalendarNamespace === "undefined"
            ? this.getTwoDigitMonth()
            : window.CalendarNamespace.monthsOfYear[this.getMonth()];
    };

    Date.prototype.strftime = function(format) {
        const fields = {
            b: this.getAbbrevMonthName(),
            B: this.getFullMonthName(),
            c: this.toString(),
            d: this.getTwoDigitDate(),
            H: this.getTwoDigitHour(),
            I: this.getTwoDigitTwelveHour(),
            m: this.getTwoDigitMonth(),
            M: this.getTwoDigitMinute(),
            p: (this.getHours() >= 12) ? 'PM' : 'AM',
            S: this.getTwoDigitSecond(),
            w: '0' + this.getDay(),
            x: this.toLocaleDateString(),
            X: this.toLocaleTimeString(),
            y: ('' + this.getFullYear()).substr(2, 4),
            Y: '' + this.getFullYear(),
            '%': '%'
        };
        let result = '', i = 0;
        while (i < format.length) {
            if (format.charAt(i) === '%') {
                result += fields[format.charAt(i + 1)];
                ++i;
            }
            else {
                result += format.charAt(i);
            }
            ++i;
        }
        return result;
    };

    // ----------------------------------------------------------------------------
    // String object extensions
    // ----------------------------------------------------------------------------
    String.prototype.strptime = function(format) {
        const split_format = format.split(/[.\-/]/);
        const date = this.split(/[.\-/]/);
        let i = 0;
        let day, month, year;
        while (i < split_format.length) {
            switch (split_format[i]) {
            case "%d":
                day = date[i];
                break;
            case "%m":
                month = date[i] - 1;
                break;
            case "%Y":
                year = date[i];
                break;
            case "%y":
                // A %y value in the range of [00, 68] is in the current
                // century, while [69, 99] is in the previous century,
                // according to the Open Group Specification.
                if (parseInt(date[i], 10) >= 69) {
                    year = date[i];
                } else {
                    year = (new Date(Date.UTC(date[i], 0))).getUTCFullYear() + 100;
                }
                break;
            }
            ++i;
        }
        // Create Date object from UTC since the parsed value is supposed to be
        // in UTC, not local time. Also, the calendar uses UTC functions for
        // date extraction.
        return new Date(Date.UTC(year, month, day));
    };
}
