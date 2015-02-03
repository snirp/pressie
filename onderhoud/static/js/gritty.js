// numeral.js language definition
!function () {
    var a = {delimiters: {thousands: ".", decimal: ","}, abbreviations: {thousand: "k", million: "mln", billion: "mrd", trillion: "bln"}, ordinal: function (a) {
        var b = a % 100;
        return 0 !== a && 1 >= b || 8 === b || b >= 20 ? "ste" : "de"
    }, currency: {symbol: "€ "}};
    "undefined" != typeof module && module.exports && (module.exports = a), "undefined" != typeof window && this.numeral && this.numeral.language && this.numeral.language("nl-nl", a)
}();
numeral.language('nl-nl');



// Set up the filters
// polluting the global namespace here...
var smallerFilter = {
    text: 'Kleiner dan',
    passThrough: function(value, comparison){
        return parseFloat(value) < parseFloat(comparison);
    },
    multi: false  // More than one argument makes no logical sense
};

var greaterFilter = {
    text: 'Groter dan',
    passThrough: function(value, comparison){
        return parseFloat(value) > parseFloat(comparison);
    },
    multi: false
};

var smallerEqualFilter = {
    text: 'Kleiner of gelijk',
    passThrough: function(value, comparison){
        return parseFloat(value) <= parseFloat(comparison);
    },
    // Does it even make logical sense to have more than one argument?
    multi: false
};

var greaterEqualFilter = {
    text: 'Groter of gelijk',
    passThrough: function(value, comparison){
        return parseFloat(value) >= parseFloat(comparison);
    },
    multi: false
};

var containsFilter = {
    text: 'Bevat',
    passThrough: function(value, comparison){
        return (value.indexOf(comparison) !== -1);
    },
    multi: true
};

var startsFilter = {
    text: 'Begint met',
    passThrough: function(value, comparison){
        return value.lastIndexOf(comparison, 0) === 0;
    },
    multi: true
};

var endsFilter = {
    text: 'Eindigt met',
    passThrough: function(value, comparison){
        return value.indexOf(comparison, value.length - comparison.length) !== -1;
    },
    multi: true
};

var notContainsFilter = {
    text: 'Bevat niet',
    passThrough: function(value, comparison){
        return (value.indexOf(comparison) === -1);
    },
    multi: false
};

var equalFilter = {
    // TODO make provisions to handle [empty] and [nonempty]
    text: "Gelijk",
    passThrough: function(value, comparison){
        return value === comparison;
    },
    multi: true
};

var notEqualFilter = {
    text: "Niet gelijk",
    passThrough: function(value, comparison){
        return value !== comparison;
    },
    multi: false
};

// Shortcut filter lists
var numberFilters = [greaterFilter, smallerFilter, greaterEqualFilter, smallerEqualFilter, equalFilter, notEqualFilter];
var textFilters = [containsFilter, notContainsFilter, startsFilter, endsFilter, equalFilter, notEqualFilter];


var Column = function (obj) {
    this.cellKey = '';         // References the properties/keys of the row objects
    this.thText = '';          // Text to display as table header
    this.contentType = 'text';   // 'text', 'number', ?'date'?
    this.formatString = '';    // Apply string formatting in numeral.js style
    this.width = 50;           // Default column width
    this.total = false;        // Calculate and display totals for column
    this.totalSum = 0;
    this.hidden = false;
    // Filter stuff
    this.allowFilter = true;
    this.filterOptions = textFilters;
    this.activeFilters = [];
    // Formatting classes for the TH and TD elements in thead, tbody or tfoot
    this.headClasses = [];
    this.bodyClasses = [];
    this.footClasses = [];

    // Overrride property values with custom supplied values
    for ( var prop in obj ) {
        if ( obj.hasOwnProperty(prop) ) {
            this[prop] = obj[prop];
        }
    }
    var _this = this;

    this.renderTdFilter = function () {
        var tdHTML = document.createElement('td');
        return tdHTML;
    };

    this.renderTheadTh = function () {
        /* Return DOM object for TH element */
        var thHTML = document.createElement('th');
        thHTML.appendChild(document.createTextNode(_this.thText));
        for (var i = 0; i < _this.headClasses.length; i++) {
            thHTML.classList.add(_this.headClasses[i]);
        }
        thHTML.classList.add('draggable');
        return thHTML;
    };

    this.renderTbodyTd = function (row) {
        /* Return DOM object for TD element in TBODY */
        var tdHTML = document.createElement('td');
        var text = '';
        if (_this.formatString) {
            text = numeral(row[_this.cellKey]).format(_this.formatString);
        } else {
            text = row[_this.cellKey];
        }
        tdHTML.appendChild(document.createTextNode(text));
        for (var i = 0; i < _this.bodyClasses.length; i++) {
            tdHTML.classList.add(_this.bodyClasses[i]);
        }
        return tdHTML;
    };

    this.renderTfootTd = function () {
        /* Return DOM object for TD element in TFOOT */
        var tdHTML = document.createElement('td');
        var text = '';
        if (_this.total) {
            if (_this.formatString) {
                text = numeral(_this.totalSum).format(_this.formatString);
            } else {
                text = _this.totalSum;
            }
            tdHTML.appendChild(document.createTextNode(text));
        }
        for (var i = 0; i < _this.footClasses.length; i++) {
            tdHTML.classList.add(_this.footClasses[i]);
        }
        return tdHTML;
    };
};

var Gritty = function () {
    var _this = this;
    _this.rows = [];                // Ordered row objects
    _this.columns = [];             // Ordered column objects
    _this.grouping = [];            // Columns used for row grouping (sub-tables)
    _this.sorting = [];             // Columns and sorting options used
    _this.hideGrouped = true;       // Show or hide the columns which are used for grouping
    _this.renderTarget = undefined; // The object to render the grid to

    _this.showGrouping = true;
    _this.showFiltering = true;
    _this.showHiding = false;
    var filtering = true;
    var filterChanged = true;
    var filtrate = [];               // Caches the current filtrate
    // Overrride property values with custom supplied values
    for (var n in arguments[0]) {
        _this[n] = arguments[0][n];
    }

    // Set both rows and filtrate
    _this.set_rows = function(rowsInput){
        _this.rows = rowsInput;
        filtrate = rowsInput;
    };

    /* Update the grouping and re-render the grid
     * Calling the function without a `position` equals
     * deleting the column from the grouping. */
    _this.updateGrouping = function (columnKey, position) {
        // Make sure the column is removed from the sorting array
        _this.removeSort(columnKey);
        // Remove column from current grouping
        var index = _this.grouping.indexOf(columnKey);
        if (index !== -1) {
            _this.grouping.splice(index, 1);
        }
        // ... and add to the new position
        if (typeof position !== 'undefined') {
            _this.grouping.splice(position, 0, columnKey);
        }
        // Rerender the grid
        _this.renderGrid()
    };

    // For existing sort column: reverse the value
    // otherwise add the column to the sorting array
    _this.updateSort = function (colnr) {
        var exists = false;
        for (var i = 0; i < _this.sorting.length; i++) {
            if (colnr === Math.abs(_this.sorting[i])) {
                _this.sorting[i] = -(_this.sorting[i]);
                exists = true;
            }
        }
        if (!exists) {
            _this.sorting.push(colnr);
        }
        _this.renderGrid();
    };

    // For a given column: check whether it is sorted (+ or -)
    // Remove the column from sorting
    _this.removeSort = function (colnr) {
        var index = Math.max(_this.sorting.indexOf(colnr), _this.sorting.indexOf(-(colnr)));
        if (index !== -1) {
            _this.sorting.splice(index, 1);
        }
        _this.renderGrid();
    };

    _this.sortRows = function () {
        var sortArray = [];
        // Order by grouping
        var ordering = _this.grouping.concat(_this.sorting);
        for (var i = 0; i < ordering.length; i++) {
            // Compare for negative, including `-0`
            if ((1 / ordering[i]) > 0) {
                sortArray.push(_this.columns[ordering[i]].cellKey)
            } else {
                sortArray.push("-" + _this.columns[-(ordering[i])].cellKey)
            }
        }
        _this.rows.sort(_this.dynamicSortMultiple(sortArray));
        filtrate.sort(_this.dynamicSortMultiple(sortArray));
    };

    _this.renderGrid = function () {
        // Only if sorting has changed
        _this.renderTarget.innerHTML = '';
        _this.sortRows();
        _this.renderControls();
        _this.renderHideControl();
        _this.renderGroupControl();
        _this.renderTable();
    };

    _this.bindEvent = function (element, type, handler) {
        if (element.addEventListener) {
            element.addEventListener(type, handler, false);
        } else {
            element.attachEvent('on' + type, handler);
        }
    };

    _this.changeOption = function (ev) {
        //
        ev.target.parentNode.setAttribute('data-filter-option', ev.target.value);
        // TODO clear inputs??
    };

    var removeFilter = function(colId, filterId){
        _this.columns[colId].activeFilters.splice(filterId, 1);
        filterChanged = true;
        _this.renderGrid();
    };

    var removeFilterItem = function(colId, filterId, itemId){
        _this.columns[colId].activeFilters[filterId][1].splice(itemId, 1);
        filterChanged = true;
        _this.renderGrid();
    };

    var filterRows = function () {
        filtrate = [];
        for (var i = 0; i < _this.rows.length; i++) {
            var pushRow = true;
        columnloop:
            for (var j = 0; j < _this.columns.length; j++){
                for (var k = 0; k < _this.columns[j].activeFilters.length; k++) {
                    var filter = _this.columns[j].activeFilters[k];
                    var inFilter = false;
                    for (var l = 0; l < filter[1].length; l++) {
                        if (filter[0].passThrough(_this.rows[i][_this.columns[j].cellKey], filter[1][l])){
                            // Filter array is 'OR' type -> break on first positive hit
                            inFilter = true;
                            break
                        }
                    }
                    if (!inFilter) {
                        // Filters are 'AND' type -> break if any individual one is negative
                        pushRow = false;
                        break columnloop;
                    }
                }
            }
            if (pushRow) {
                filtrate.push(_this.rows[i]);
            }
        }
    };

    var addFilter = function (ev, i, filterOption) {
        var filterValue = ev.target.value ;
        if (_this.columns[i].contentType === 'number') {
            filterValue = parseFloat(filterValue)
        }
        var added = false;
        for (var j = 0; j < _this.columns[i].activeFilters.length; j++) {
            if (_this.columns[i].activeFilters[j][0] === filterOption) {
                _this.columns[i].activeFilters[j][1].push(filterValue);
                added = true;
                break
            }
        }
        // We were unable to attach to an existing filter. Let's make a new one.
        if (!added) {
            var filterAddition = [ filterOption ];
            filterAddition.push([ filterValue ]);
            _this.columns[i].activeFilters.push( filterAddition )
        }
        _this.renderGrid();
    };

    var renderFilterInput = function (event, i, div) {
        var filterOption = _this.columns[i].filterOptions[event.target.selectedIndex-1];
        // Delete previous input
        if (div.getElementsByTagName('input')[0]) {
            div.removeChild(div.getElementsByTagName('input')[0]);
        }
        var input = document.createElement('input');
        div.appendChild(input);
        input.focus();

        _this.bindEvent( input, 'change', (function (i, filterOption) {
                    return function (ev) {
                        addFilter(ev, i, filterOption);
                    };
                }(i, filterOption)));
    };


    _this.renderTable = function () {
        // Handle filtering
        if (filtering && filterChanged) {
            filterRows();
        }

        var tableHTML = document.createElement('table');
        var theadHTML = document.createElement('thead');
        var tbodyHTML = document.createElement('tbody');
        var tfootHTML = document.createElement('tfoot');
        tableHTML.classList.add('gritty-table', 'resizable');
        if (_this.hideGrouped) {
            tableHTML.classList.add('hide-grouped');
        }

        // Render colgroup for widths and resizing
        var colgrp = document.createElement('colgroup');
        for (var i = 0; i < _this.columns.length; i++) {
            var col = document.createElement('col');
            col.style.width = _this.columns[i].width + '%';
            if (_this.grouping.indexOf(i) !== -1) {
                col.classList.add('grouped');
            }
            if (_this.columns[i].hidden) {
                col.classList.add('hidden');
            }
            colgrp.appendChild(col);
        }
        tableHTML.appendChild(colgrp);

        // Render filter controls
        if (_this.showFiltering) {
            var trFilterHTML = document.createElement('tr');
            for (var i = 0; i < _this.columns.length; i++) {
                var col = _this.columns[i];
                var tdHTML = col.renderTdFilter();

                // Create div for new filtergroup
                // TODO only if filtering is allowed on column
                var div = document.createElement('div');
                div.classList.add('filter-add');
                var select = document.createElement('select');
                var option = document.createElement('option');
                option.selected = true;
                option.disabled = true;
                option.appendChild(document.createTextNode('kies filter...'));
                select.appendChild(option);
                for (var j = 0; j < col.filterOptions.length; j++) {
                    var option = document.createElement('option');
                    option.value = [j];
                    option.appendChild(document.createTextNode(col.filterOptions[j].text));
                    select.appendChild(option);
                    }
                div.appendChild(select);
                _this.bindEvent(select, 'change', (function (i, div) {
                    // - try to delete current input box
                    // - create new input box
                    return function (ev) {
                        renderFilterInput(ev, i, div);
                    };
                }(i, div)));

                tdHTML.appendChild(div);

                // Create lists for each current filtergroup and their input arrays
                var ulGroep = document.createElement('ul');
                ulGroep.classList.add('filter-group');

                for (var j = 0; j < col.activeFilters.length; j++) {
                    var liGroep = document.createElement('li');
                    liGroep.appendChild(document.createTextNode(col.activeFilters[j][0].text)); //delete button?
                    var delSpan = document.createElement('span');
                    delSpan.classList.add('float-right', 'cursor-pointer');
                    delSpan.appendChild(document.createTextNode('x'));
                    _this.bindEvent(delSpan, 'click', (function (i, j) {
                        return function (ev) {
                            removeFilter(i, j);
                        }
                    }(i, j)));
                    liGroep.appendChild(delSpan);

                    // Attach the current filter array
                    var ulItem = document.createElement('ul');
                    for (var k = 0; k < col.activeFilters[j][1].length; k++) {
                        var liItem = document.createElement('li');
                        liItem.appendChild(document.createTextNode(col.activeFilters[j][1][k]));
                        // Add individual delete buttons if more than one item
                        if (col.activeFilters[j][1].length > 1) {
                            var delSpan = document.createElement('span');
                            delSpan.classList.add('float-right', 'cursor-pointer');
                            delSpan.appendChild(document.createTextNode('x'));
                            _this.bindEvent(delSpan, 'click', (function (i, j, k) {
                                return function (ev) {
                                    removeFilterItem(i, j, k);
                                }
                            }(i, j, k)));

                            liItem.appendChild(delSpan);
                        }
                        ulItem.appendChild(liItem);
                    }
                    //if multi filter -> input field here
                    liGroep.appendChild(ulItem);
                    ulGroep.appendChild(liGroep);
                }
                tdHTML.appendChild(ulGroep);



                if (_this.grouping.indexOf(i) !== -1) {
                    tdHTML.classList.add('grouped');
                }
                if (_this.columns[i].hidden) {
                    tdHTML.classList.add('hidden');
                }
                trFilterHTML.appendChild(tdHTML);
            }
            theadHTML.appendChild(trFilterHTML);
        }

        // Render th titels
        var theadTrHTML = document.createElement('tr');
        for (var i = 0; i < _this.columns.length; i++) {
            // reset total sum here
            _this.columns[i].totalSum = 0;
            var thHTML = _this.columns[i].renderTheadTh();
            if (_this.grouping.indexOf(i) !== -1) {
                thHTML.classList.add('grouped');
            }
            if (_this.columns[i].hidden) {
                thHTML.classList.add('hidden');
            }
            // Sorting status
            var spanControls = document.createElement('span');
            var iconStatus = document.createElement('i');
            iconStatus.classList.add('fa', 'cursor-pointer');
            // Current sorting status: asc, desc or none
            var sorted = true;
            if (_this.sorting.indexOf(+([i])) !== -1) {
                iconStatus.classList.add('fa-sort-asc');
            } else if (_this.sorting.indexOf(-([i])) !== -1) {
                iconStatus.classList.add('fa-sort-desc');
            } else {
                iconStatus.classList.add('fa-unsorted');
                sorted = false;
            }
            spanControls.appendChild(iconStatus);
            spanControls.classList.add('float-right', 'filter-control-th');
            _this.bindEvent(iconStatus, 'click', (function (i) {
                return function (ev) {
                    _this.updateSort(i);
                }
            }(i)));
            thHTML.appendChild(spanControls);

            // Add a remove button if currently sorted
            if (sorted) {
                var iconRemove = document.createElement('i');
                iconRemove.classList.add('fa', 'fa-close', 'cursor-pointer');
                _this.bindEvent(iconRemove, 'click', (function (i) {
                    return function (ev) {
                        _this.removeSort(i);
                    }
                }(i)));
                spanControls.appendChild(iconRemove);
            }

            // Make resizable

            $(thHTML).resizable({
                handles: "e",
                helper: "resizable-helper",
                stop: function (event, ui) {
                    var table = ui.element.closest("table"),
                        // gaat deze selector werken???
                        cols = table.find(">colgroup>col"),
                        col = cols.filter(":eq(" + ui.element.index() + ")"),
                        colWidth = Math.floor(ui.size.width * 100 / table.width()),
                        oriColWidth = parseInt(col.css("width"), 10),
                        diff = colWidth - oriColWidth;
                    // Set the width (%) in all the columns.
                    cols.each(function(index) {

                        if (index == ui.element.index()) {
                            // prevent from being 0 -> strange things happen in layout
                            if (colWidth < 1){
                                colWidth = 1;
                            }
                            $(this).css("width", colWidth + "%");
                            // save widths to object
                            _this.columns[index].width = colWidth;
                        }else {
                            var width = Math.floor(parseInt($(this).css("width"), 10) - (diff / (cols.length - 1)));
                            // prevent from being 0 -> strange things happen in layout
                            if (width < 1){
                                width = 1;
                            }
                            $(this).css("width", width + "%");
                            // save widths to object
                            _this.columns[index].width = width;
                        }
                    });
                    // Remove any inline style created by the resizable feature.
                    ui.element.removeAttr("style");
                    // Callback action:: Save colWidth in database using id => col.attr("id")
                }
            });



            theadTrHTML.appendChild(thHTML);
        }
        theadHTML.appendChild(theadTrHTML);


        // Render tbody
        // Do progressive rendering???
        var subGrouping;
        for (var i = 0; i < filtrate.length; i++) {
            // Add grouping rows
            subGrouping = false;
            for (var j = 0; j < _this.grouping.length; j++) {
                // TODO cache previous row data
                if (i === 0 || subGrouping || filtrate[i][_this.columns[_this.grouping[j]].cellKey] !== filtrate[i - 1][_this.columns[_this.grouping[j]].cellKey]) {
                    var trHTML = document.createElement('tr');
                    trHTML.classList.add('grouphead', 'grouplevel-' + j);
                    tdHTML = document.createElement('td');
                    tdHTML.colSpan = _this.columns.length;
                    tdHTML.appendChild(document.createTextNode(filtrate[i][_this.columns[_this.grouping[j]].cellKey]));
                    trHTML.appendChild(tdHTML);
                    tbodyHTML.appendChild(trHTML);
                    // make certain the groupings next-in-line are also activated
                    subGrouping = true;
                }
            }
            // Add content rows
            var trHTML = document.createElement('tr');
            for (var j = 0; j < _this.columns.length; j++) {
                // Add cell value to total if no previous render and if total is calculated
                if (_this.columns[j].total) {
                    _this.columns[j].totalSum += filtrate[i][_this.columns[j].cellKey];
                }
                var tdHTML = _this.columns[j].renderTbodyTd(filtrate[i]);
                if (_this.grouping.indexOf(j) !== -1) {
                    tdHTML.classList.add('grouped');
                }
                if (_this.columns[j].hidden) {
                    tdHTML.classList.add('hidden');
                }
                trHTML.appendChild(tdHTML);
            }
            tbodyHTML.appendChild(trHTML);
        }

        // Render tfoot
        var trHTML = document.createElement('tr');
        for (var i = 0; i < _this.columns.length; i++) {
            tdHTML = _this.columns[i].renderTfootTd();
            trHTML.appendChild(tdHTML);
            if (_this.grouping.indexOf(i) !== -1) {
                tdHTML.classList.add('grouped');
            }
            if (_this.columns[i].hidden) {
                tdHTML.classList.add('hidden');
            }

        }
        tfootHTML.appendChild(trHTML);

        // Compose the table
        tableHTML.appendChild(theadHTML);
        tableHTML.appendChild(tbodyHTML);
        tableHTML.appendChild(tfootHTML);
        // Prevent recalculation of totals for redraw

        // Delete potential existing table and add new table
        //_this.renderTarget.removeChild(document.getElementsByClassName('gritty-table')[0]);
        _this.renderTarget.appendChild(tableHTML);


        $(".draggable").draggable({
            connectToSortable: '.sortable',
            helper: function (event, ui) {
                return $(_this.renderControlItem(this.cellIndex));
            },
            revert: 'invalid'
        });

    };

    _this.renderControlItem = function (columnKey, handler) {
        // Render the <li> items for the individual controls
        var li = document.createElement('li');
        li.classList.add('cursor-move');
        li.setAttribute('data-column-key', columnKey);
        var text = document.createTextNode(_this.columns[columnKey].thText);
        li.appendChild(text);
        var span = document.createElement('span');
        span.classList.add('close-handle', 'cursor-pointer', 'float-right');
        var iconClose = document.createElement('i');
        iconClose.classList.add('fa', 'fa-close');
        span.appendChild(iconClose);
        li.appendChild(span);
        // Invoke closeGroupHandler on click
        _this.bindEvent(iconClose, 'click', handler);
        return li
    };

    _this.closeHideHandler = function (ev) {
        var colKey = ev.target.parentNode.parentNode.getAttribute('data-column-key');
        _this.columns[colKey].hidden = false;
        _this.renderGrid();
    };

    _this.updateHiding = function(colKey){
        _this.columns[colKey].hidden = true;
        _this.renderGrid();
    };

    _this.closeGroupHandler = function (ev) {
        /* Get the ColumnKey from the parent element and call
         * updateGrouping to remove the column */
        //TODO is chaining parentNode even supported beyond chrome???
        var el = ev.target.parentNode.parentNode;
        _this.updateGrouping(parseInt(el.getAttribute('data-column-key')));
    };

    _this.renderToggle = function (label, toggleTarget) {
        // Render a toggle control with label and switch
        var toggleControl = document.createElement('li');
        toggleControl.appendChild(document.createTextNode(label));
        if (_this[toggleTarget]) {
            toggleControl.classList.add('toggle-on')
        } else {
            toggleControl.classList.remove('toggle-on')
        }

        _this.bindEvent(toggleControl, 'click', function(){
            _this[toggleTarget] = !_this[toggleTarget];
            _this.renderGrid();
        });
        return toggleControl;
    };

    _this.renderControls = function(){
        var controls = document.createElement('ul');
        controls.classList.add('grid-controls');
        controls.appendChild(_this.renderToggle('Verborgen', 'showHiding'));
        controls.appendChild(_this.renderToggle('Groepering', 'showGrouping'));
        controls.appendChild(_this.renderToggle('Filters', 'showFiltering'));
        _this.renderTarget.appendChild(controls);
    };

    _this.renderHideControl = function(){
        if (_this.showHiding) {
            var controlbar = document.createElement('div');
            controlbar.classList.add('controlbar');
            var controlName = document.createElement('span');
            controlName.appendChild(document.createTextNode('verborgen'));
            controlbar.appendChild(controlName);
            var hideControl = document.createElement('ol');
            hideControl.classList.add('sortable');
            for (var i = 0; i < _this.columns.length; i++) {
                if (_this.columns[i].hidden) {
                    hideControl.appendChild(_this.renderControlItem(i, _this.closeHideHandler));
                }
            }

            controlbar.appendChild(hideControl);
            _this.renderTarget.appendChild(controlbar);

            $(hideControl).sortable({
                placeholder: "sortable-placeholder",
                update: function (event, ui) {
                    _this.updateHiding($(ui.item).data('column-key'))
                }
            });
        }
    };

    _this.renderGroupControl = function () {

        if (_this.showGrouping) {
            var controlbar = document.createElement('div');
            controlbar.classList.add('controlbar');
            var controlName = document.createElement('span');
            controlName.appendChild(document.createTextNode('gegroepeerd'));
            controlbar.appendChild(controlName);
            var groupControl = document.createElement('ol');
            groupControl.classList.add('sortable');
            for (var i = 0; i < _this.grouping.length; i++) {
                groupControl.appendChild(_this.renderControlItem(_this.grouping[i], _this.closeGroupHandler));
            }
            controlbar.appendChild(groupControl);
            _this.renderTarget.appendChild(controlbar);

            $(groupControl).sortable({
                placeholder: "sortable-placeholder",
                update: function (event, ui) {
                    _this.updateGrouping($(ui.item).data('column-key'), ui.item.index())
                }
            });

        }

    };

    _this.dynamicSortMultiple = function (props) {
        return function (obj1, obj2) {
            var i = 0, result = 0, numberOfProperties = props.length;
            /* try getting a different result from 0 (equal)
             * as long as we have extra properties to compare
             */
            while (result === 0 && i < numberOfProperties) {
                result = _this.dynamicSort(props[i])(obj1, obj2);
                i++;
            }
            return result;
        }
    };

    _this.dynamicSort = function (property) {
        var sortOrder = 1;
        if (property[0] === "-") {
            sortOrder = -1;
            property = property.substr(1);
        }
        return function (a, b) {
            var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
            return result * sortOrder;
        }
    };

};



