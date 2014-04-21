function format(state) {
    if (!state.id) return state.text; // optgroup
    return "<img class='flag' src='/admin/cerci_content/issuecontent/thumbnail/" + state.id + "'/><span class='figure_name'>" + state.text + '</span>';
}

$(document).ready(function(){
    $("#id_authors, #id_cover_design").select2();
    $("#id_figures").select2({
        formatResult: format,
        formatSelection: format,
        escapeMarkup: function(m) { return m; }
    });
});