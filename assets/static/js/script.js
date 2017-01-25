$(document).ready(function() {
    var viewModel = {
        customShortUrl: ko.observable(false),
    };

    ko.applyBindings(viewModel);

    var csrftoken = Cookies.get('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#submitForm").click(function(){
        var fullUrl = $("input[name=full_url]").val();
        var shortUrl = "";

        if ($("#chkShortUrl").prop('checked') == true ){
            shortUrl = $("input[name=short_url]").val();

            if (!shortUrl){
                $("#pShortUrlError").text('Short Url must not be empty');
                $("#pShortUrlError").css('visibility', 'visible');
            }
        }
        else {
            $("#pShortUrlError").css('visibility', 'hidden');
        }

        if (fullUrl){
            $("#pFullUrlError").css('visibility', 'hidden');

            $.ajax({
                type: "POST",
                url: "/shorten_url/",
                data: {
                    "full_url": fullUrl,
                    "short_url": shortUrl
                },
                success: function(data){
                    if (data.error.short_url) {
                        $("#pShortUrlError").text(data.error.short_url);
                        $("#pShortUrlError").css('visibility', 'visible');
                    }
                    else {
                        $("#pShortUrlError").css('visibility', 'hidden');
                    }

                    if (data.error.full_url) {
                        $("#pFullUrlError").text(data.error.full_url);
                        $("#pFullUrlError").css('visibility', 'visible');
                    }
                    else {
                        $("#pFullUrlError").css('visibility', 'hidden');
                    }

                    if (!data.error.short_url && !data.error.full_url){
                        if (data.data.short_url) {
                            $("input[name=full_url]").val(data.data.short_url);
                            $("#submitForm").remove();
                            $("#btnDiv").append("<button class='form-control btn-primary' type='button' id='btnCopy' data-clipboard-target='#shortenedUrl' data-toggle='tooltip' data-placement='bottom' title='Copied'>Copy</button>");
                            var clipboard = new Clipboard('#btnCopy');
                            $("[data-toggle='tooltip']").tooltip({
                                trigger: 'click focus',
                                delay: {show: 500, hide: 100}
                            });

                            clipboard.on('success', function(event){
                                
                            });                     
                        }
                    }
                },
                dataType: 'json'
            });
        }
        else {
            $("#pFullUrlError").text('Full Url must not be empty');
            $("#pFullUrlError").css('visibility', 'visible');
        }
    });
})