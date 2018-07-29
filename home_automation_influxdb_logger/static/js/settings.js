jQuery(document).ready(function() {
    jQuery("#form-settings").submit(function() {
        jQuery.ajax({
            url: app.vars.moduleBasePath + "/action/save_settings/",
            type: "POST",
            data: JSON.stringify({
                "host": jQuery("#host").val(),
                "port": jQuery("#port").val(),
                "username": jQuery("#username").val(),
                "password": jQuery("#password").val()
            }),
            contentType: "application/json",
            dataType: "json",
            success: function(data) {
                // TODO: Replace this with a nicer in-page alert
                alert(data.message);
            }            
        });

        return false;
    });
});