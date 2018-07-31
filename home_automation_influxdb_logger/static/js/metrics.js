jQuery(document).ready(function() {
    jQuery("#metric-row-container").on("click", ".btn-delete-metric", function() {
        jQuery(this).closest("tr").remove();
        return false;
    });

    jQuery("#btn-add-metric").click(function() {
        var template = jQuery("#template-metric-row").text();
        jQuery("#metric-row-container").append(template);
    });

    jQuery("#btn-save-metrics").click(function() {
        window.timerSaveRequestInProgress = true;
        var formData = serialiseMetricForm();
        jQuery.ajax({
            url: app.vars.moduleBasePath + "/action/save_metrics/",
            type: "POST",
            data: JSON.stringify(formData),
            contentType: "application/json",
            dataType: "json",
            success: function(data) {
                // TODO: Replace this with a nicer in-page alert
                alert(data.message);
            }            
        });
    });

    function serialiseMetricForm() {
        var metrics = [];
        jQuery("#metrics-form .metric-row").each(function() {
            var metric = {};
            metric["topic"] = jQuery(this).find("[name='topic']").val();
            metric["database"] = jQuery(this).find("[name='database']").val();
            metric["measurement"] = jQuery(this).find("[name='measurement']").val();
            metric["type"] = jQuery(this).find("[name='type']").val();

            metrics.push(metric);
        });
        return metrics;
    }
});