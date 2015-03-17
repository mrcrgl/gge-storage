function createCookie(name, value, days) {
    var expires;

    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toGMTString();
    } else {
        expires = "";
    }
    document.cookie = escape(name) + "=" + escape(value) + expires + "; path=/";
}

function readCookie(name) {
    var nameEQ = escape(name) + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return unescape(c.substring(nameEQ.length, c.length));
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name, "", -1);
}


$(function () {

    $.extend($.tablesorter.themes.bootstrap, {
        // these classes are added to the table. To see other table classes available,
        // look here: http://twitter.github.com/bootstrap/base-css.html#tables
        table: 'table table-bordered',
        caption: 'caption',
        header: 'bootstrap-header', // give the header a gradient background
        footerRow: '',
        footerCells: '',
        icons: '', // add "icon-white" to make them white; this icon class is added to the <i> in the header
        sortNone: 'bootstrap-icon-unsorted',
        sortAsc: 'icon-chevron-up glyphicon glyphicon-chevron-up',     // includes classes for Bootstrap v2 & v3
        sortDesc: 'icon-chevron-down glyphicon glyphicon-chevron-down', // includes classes for Bootstrap v2 & v3
        active: '', // applied when column is sorted
        hover: '', // use custom css here - bootstrap class may not override it
        filterRow: '', // filter row class
        even: '', // odd row zebra striping
        odd: ''  // even row zebra striping
    });

    // call the tablesorter plugin and apply the uitheme widget
    if ($("table.tablesorter").length) {
        $("table.tablesorter").tablesorter({
            // this will apply the bootstrap theme if "uitheme" widget is included
            // the widgetOptions.uitheme is no longer required to be set
            theme: "bootstrap",

            widthFixed: true,

            headerTemplate: '{content} {icon}', // new in v2.7. Needed to add the bootstrap icon!

            // widget code contained in the jquery.tablesorter.widgets.js file
            // use the zebra stripe widget if you plan on hiding any rows (filter widget)
            widgets: [ "uitheme", "filter", "zebra" ],

            widgetOptions: {
                // using the default zebra striping class name, so it actually isn't included in the theme variable above
                // this is ONLY needed for bootstrap theming if you are using the filter widget, because rows are hidden
                zebra: ["even", "odd"],

                // reset filters button
                filter_reset: ".reset"

                // set the uitheme widget to use the bootstrap theme class names
                // this is no longer required, if theme is set
                // ,uitheme : "bootstrap"

            }
        })
            .tablesorterPager({

                // target the pager markup - see the HTML block below
                container: $(".ts-pager"),

                // target the pager page select dropdown - choose a page
                cssGoto: ".pagenum",

                // remove rows from the table to speed up the sort of large tables.
                // setting this to false, only hides the non-visible rows; needed if you plan to add/remove rows with the pager enabled.
                removeRows: false,

                // output string - default is '{page}/{totalPages}';
                // possible variables: {page}, {totalPages}, {filteredPages}, {startRow}, {endRow}, {filteredRows} and {totalRows}
                output: '{startRow} - {endRow} / {filteredRows} ({totalRows})'

            });
    }

    $(document).ready(function () {
        var step = 30 * 60 * 1000; // 30min

        function walk(time, cb) {
            $.post(
                $("#data-url").val(),
                {
                    from: parseInt(time / 1000),
                    to: parseInt((time + step) / 1000),
                    kingdom: $("#kingdom").val(),
                    csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
                },
                function (data, textStatus) {
                    console.log("Response: ", textStatus);
                    console.dir(data.castle_list.length);

                    $(".map-y.matches").removeClass("matches").addClass("prev-matches");

                    if (data.castle_list.length > 0) {
                        var dt = new Date(time);
                        $(".log-window").append($("<p>").html(dt.toString() + " " + data.castle_list.length + " Neu"))
                        for (var i = 0; i < data.castle_list.length; ++i) {
                            var castle = data.castle_list[i];
                            var pos_x = Math.floor(castle.pos_x / 10);
                            var pos_y = Math.floor(castle.pos_y / 10);
                            $(".map-y.x" + pos_x + "0.y" + pos_y + "0").not(".matches").addClass("matches");
                        }
                    }

                    cb();
                },
                'json'
            )
        }


        $("#btn-start-drop-map").click(function () {
            var start = Date.now() - 24 * 60 * 60 * 1000;

            var walk_to = function (start) {
                console.log("walk: ", start);
                if (start < Date.now()) {
                    var dt = new Date(start);
                    $("#current-time").val(dt.toString());
                    walk(start, function () {
                        setTimeout(function () {
                            walk_to(start + step);
                        }, 2500);
                    });
                } else {
                    $("#current-time").val("Fertig!");
                }
            };

            walk_to(start);
        });


        if ($('.attack-time-calculator').length) {
            $('form.attack-time-calculator').submit(function (e) {
                e.preventDefault();

                var arrivalHour = parseInt($("[name=arrival-hour]").val());
                var arrivalMinute = parseInt($("select[name=arrival-minute]").val());

                var durationHours = parseInt($("select[name=duration-hours]").val());
                var durationMinutes = parseInt($("select[name=duration-minutes]").val());
                var durationSeconds = parseInt($("select[name=duration-seconds]").val());

                var departure = $("input[name=departure]");

                var now = new Date();
                var arrival = new Date(now.getFullYear(), now.getMonth(), now.getDay(), arrivalHour, arrivalMinute);
                var arrivalTime = arrival.getTime() + 60 * 60 * 24 * 1000;  // Force next day, should be ok in 99%

                var departureTime = arrivalTime - (60 * 60 * 1000 * durationHours) - (60 * 1000 * durationMinutes) - (1000 * durationSeconds);
                var dep = new Date(departureTime);

                departure.val((dep.getHours() < 10 ? "0" : "") + dep.getHours() + ":" + (dep.getMinutes() < 10 ? "0" : "") + dep.getMinutes() + ":" + (dep.getSeconds() < 10 ? "0" : "") + dep.getSeconds());

            });

            $('form.attack-time-calculator').find("select, input").change(function () {
                $(this).closest("form").submit();
            });
        }
    });

    $(document).ready(function () {
        $("body").tooltip({ selector: '[data-toggle=tooltip]' });
    });


    /**
     * Typeahead
     */
    var castleAjaxMatcher = function () {
        return function findMatches(q, cb) {
            var matches, substringRegex;

            // an array that will be populated with substring matches
            matches = [];

            var typeFilter = "&type__in=TYPE_WITH_WARRIORS"

            $.getJSON('/intern/rest/gge_proxy_manager/castle/' + $('[name=castle]').val(), function (pre_data) {
                if (pre_data && pre_data.length) {
                    var fromCastle = pre_data.shift();
                    typeFilter += '&kingdom_id=' + fromCastle.fields.kingdom;
                }

                $.getJSON('/intern/rest/gge_proxy_manager/castle/?name__icontains=' + q + typeFilter, function (data) {
                    $.each(data, function(key, row) {
                        matches.push({
                            "id": row.pk,
                            "value": row.fields.name + ' / ' + row.fields.pos_x + ':' + row.fields.pos_y + ' [' + row.pk + ']'
                        });
                    });
                    cb(matches);
                });
            });
        };
    };

    $('.typeahead').typeahead({
            hint: true,
            highlight: true,
            minLength: 1
        },
        {
            name: 'id',
            displayKey: 'value',
            source: castleAjaxMatcher()
        });
    console.log("loaded.")

    if ($('.form.logistic-job').length) {
        var castleInput = $('.form.logistic-job').find('[name=castle]');
        var receiverInput = $('.form.logistic-job').find('[name=receiver_name]');
        if ($(castleInput).val()) {
            receiverInput.attr('disabled', false);
        } else {
            receiverInput.attr('disabled', true);
        }

        castleInput.change(function() {
            if ($(this).val()) {
                receiverInput.attr('disabled', false);
            } else {
                receiverInput.attr('disabled', true);
            }
        });
    }

    $('input#checkall').click(function(){
        //alert('dwedwq');
        var check = $('input#checkall')[0].checked;
        $('tbody input[type=checkbox]').each(function(){
            this.checked = check;
        });
    });

    $('tbody input[type=checkbox]').click(function() {
        var checked = 0;
        var unchecked = 0;

        for (var i=0;i<$('tbody input[type=checkbox]').length;i++) {
            if ($('tbody input[type=checkbox]')[i].checked) {
                checked++;
            } else {
                unchecked++;
            }
        }

        if (checked == 0) {
            $('input#checkall')[0].checked = false;
        } else if (unchecked == 0) {
            $('input#checkall')[0].checked = true;
        } else {
            $('input#checkall')[0].checked = false;
        }
    });

    $(".neighborhood > .castle").mouseenter(function() {
        var player_id = $(this).attr("player");
        $(".neighborhood > .castle[player="+player_id+"]").addClass("highlight");
    });
    $(".neighborhood > .castle").mouseleave(function() {
        $(".neighborhood > .castle").removeClass("highlight");
    });

    function changeMapZoom(zoom) {
        var mapWidth = 1400;
        var mapHeight = 1400;

        // .ruler.ruler-top -> width
        // .ruler-top > ul > li -> width 1:1
        // .neighborhood -> width + height, background-size: 25px 25px;
        // .ruler-left > ul > li -> height 1:1

        var newWidth = (zoom/100*mapWidth);
        var newHeight = (zoom/100*mapHeight);
        var backgroundSize = (zoom/100*25);

        $(".ruler.ruler-top").css("width", newWidth+"px");
        $(".ruler.ruler-top > ul > li").css("width", (zoom)+"px");


        $(".ruler.ruler-left > ul > li").css("height", (zoom)+"px");
        $(".neighborhood")
            .css("width", newWidth+"px")
            .css("height", newHeight+"px")
            .css("backgroundSize", backgroundSize+"px "+backgroundSize+"px");

        $(".neighborhood .castle").each(function() {
            var castle = $(this);
            var width = castle.width();
            var height = castle.height();

            if (!castle.data("pos-x")) {
                castle.data("pos-x", parseInt(castle.css("left")) + (width/2));
            }
            if (!castle.data("pos-y")) {
                castle.data("pos-y", parseInt(castle.css("top")) + (height/2));
            }

            castle.css("left", (zoom/100*parseInt(castle.data("pos-x")))+(width/2) + "px");
            castle.css("top", (zoom/100*parseInt(castle.data("pos-y")))+(height/2) + "px");
        });
    }

    if ($("#map-zoom").length) {
        $("#map-zoom").change(function() {
            var value = $("#map-zoom").val();
            changeMapZoom(parseInt(value));
            eraseCookie("zoom-faktor");
            createCookie("zoom-faktor", value);
        });

        var savedZoom = readCookie("zoom-faktor");
        if (savedZoom) {
            changeMapZoom(parseInt(savedZoom) || 100);
        }

        $("#map-zoom").val(savedZoom+"");
    }

    if ($("form#empire_login_form").length) {
        $("form#empire_login_form").submit(function(e) {
            var form = $("form#empire_login_form");

            form.find('button').attr('disabled', true);

            function onSuccess(data) {
                if (data.status == "ok") {
                    alert("Login erfolgreich!");
                    ga('send', 'event', 'BotLogin', 'succeed', document.getElementById('id_bot_playername').value);
                } else {
                    alert("Login fehlgeschlagen!");
                    ga('send', 'event', 'BotLogin', 'failed', document.getElementById('id_bot_playername').value);
                }
                form.find('button').attr('disabled', false);
            }

            function onError() {
                alert("Er trat ein Fehler auf!");
                ga('send', 'event', 'BotLogin', 'error', document.getElementById('id_bot_playername').value);
                form.find('button').attr('disabled', false);
            }

            $.post(form.attr('action'), form.serialize()).success(onSuccess).error(onError);

            return false;
        });
    }

});