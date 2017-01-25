/* Using pure javascript instead of jquery so as to not go through the hasle of checking if the appropriate 
version of jQuery exists or load another one. */

document.onreadystatechange = function(){   // Listen to changes in the readyState of the DOM.
    var state = document.readyState;

    if (state === 'interactive'){   //  DOM elements are loaded but images and other assets are yet to load.
        main();
    }
}

function main(){
    var widgetType = document.getElementById("tursh_widget").getAttribute("widgetType");
    var customStyle = document.getElementById("tursh_widget").getAttribute("customStyle");

    if (customStyle != 'true'){
        customStyle = 'false';
    }

    if (widgetType != 'long'){
        widgetType = 'short';
    }

    /* Due to Cross-Domain rule, ajax request cannot be sent to a website on different server so we're sending our request 
    via jsonp (json with padding) by simply injecting a script tag into the document body and adding a callback in the GET request. 
    The callback is very essential for jsonp requests. */

    var script_tag = document.createElement("script");
    script_tag.type = "text/javascript";
    script_tag.src = "http://www.tursh.net/widget/?widget_type=" + widgetType + "&callback=loadWidget";
    script_tag.id = "widLoadWidget";

    /* Append the script to the document body. We're using body instead of head so as not slow down 
    the website before the page loads. */
    document.body.appendChild(script_tag);

    if (customStyle == 'false'){    // Append widget's stylesheet.
        // TODO:0 - load only styles needed by widget instead of the whole bootstrap.
        // TODO:1 - rename all ids and classes to something that will rarely clash with the ones on the website.
        var css_link = document.createElement("link");
        css_link.rel = "stylesheet";
        css_link.type = "text/css";
        css_link.href = "http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css"

        document.head.appendChild(css_link);
    }
}

function loadWidget(data){
    /* Callback function that's called when the jsonp request to /widget is done. */
    document.getElementById("tursh_widget").innerHTML = data.html;   // Append widget's html to urlshortener_widget div.
    // Remove appended script tag used for the jsonp request 'cos it's no longer needed.
    document.getElementById("widLoadWidget").remove();
}

function post_url(){
    /* Handles posting of the form when the 'Shrink' button has been clicked. */
    var widgetType = document.getElementById("tursh_widget").getAttribute("widgetType");

    if (widgetType != 'long'){
        widgetType = 'short';
    }

    var shortUrl = "";

    if (widgetType == 'long'){  // Only long widget types have a short url field.
        shortUrl = document.getElementById("widShortUrl").value;
    }

    var fullUrl = document.getElementById("widFullUrl").value;

    if (fullUrl == ''){
        document.getElementById("pFullUrlError").innerText = "Full Url must not be empty";
        document.getElementById("pFullUrlError").style.visibility = "visible";
    }
    else {
        /* Script used for jsonp request to submit the url entered. */
        var script_tag = document.createElement("script");
        script_tag.type = "text/javascript";
        script_tag.src = "http://www.tursh.net/process_widget/?full_url=" + fullUrl + "&short_url=" + shortUrl + "&callback=shortenUrl";
        script_tag.id = "widShortenUrl";

        document.body.appendChild(script_tag);  // Append script tag to document body.
    }
}

function shortenUrl(data){
    if (data.error.short_url){  // If short_url error exists.
        document.getElementById("pShortUrlError").innerText = data.error.short_url;
        document.getElementById("pShortUrlError").style.visibility = "visible";
    }
    else {
        if (document.getElementById("urlshortener_widget").getAttribute("widgetType") == 'long'){
            /* JS raises an error when used with short widgetType since the paragraph with id pShortUrlError doesn't exist
            The whole part might be removed later if deemed unneccessary */
            document.getElementById("pShortUrlError").style.visibility = "hidden";
        }
    }

    if (data.error.full_url){   // If full_url error exists.
        document.getElementById("pFullUrlError").innerText = data.error.full_url;
        document.getElementById("pFullUrlError").style.visibility = "visible";
    }
    else {
        document.getElementById("pFullUrlError").style.visibility = "hidden";
    }

    if (!data.error.short_url && !data.error.full_url){ // If there are no errors.
        if (data.data.short_url){   // If short_url is returned.
            /* Set the value of the widFullUrl textbox with the returned short_url */
            document.getElementById("widFullUrl").value = data.data.short_url;

            // NOTE:0 - Should I add copy functionality by using clipboard.js or let user copy manually?
        }
    }

    // Remove appended script tag used for the jsonp request 'cos it's no longer needed.
    document.getElementById("widShortenUrl").remove();
}
