/* @TODO: change description --> global SelectBox, interpolate*/
// Handles related-objects functionality: lookup link for raw_id_fields
// and Add Another links.

(function($) {
    'use strict';

    // IE doesn't accept periods or dashes in the window name, but the element IDs
    // we use to generate popup window names may contain them, therefore we map them
    // to allowed characters in a reversible way so that we can locate the correct
    // element when the popup window is dismissed.

    function windowname_to_id(text) {
        text = text.replace(/__dot__/g, '.');
        text = text.replace(/__dash__/g, '-');
        return text;
    }

    function insertPageLink(win, chosenId) {
      var name = windowname_to_id(win.name);
      if(name.startsWith("ckeditor_name:")){
        // called form ckeditor
        var instance_name = name.replace("ckeditor_name:", "");
        var editor = CKEDITOR.instances[instance_name];
        var selection = editor.getSelectedHtml(true);
        var a_html_str = '<a href="kwelt://pages/Page/'+ chosenId+'/">'+
          selection+'</a>';
        var page_link = CKEDITOR.dom.element.createFromHtml(a_html_str );
        editor.insertElement(page_link);
        win.close();
      }else{ 
        // standard django RelatedObjectLookup
        window.normal_dismissRelatedLookupPopup(win, chosenId);
      }
    }


    // overwrite method from django internal RelatedObjectLookups.js
    window.insertPageLink = insertPageLink;
    window.normal_dismissRelatedLookupPopup = window.dismissRelatedLookupPopup;
    window.dismissRelatedLookupPopup = insertPageLink;

// not needed. cause its already implemented in RelatedOjectLookups.js
// here you see how the insertPageLink method is called:

//     $(document).ready(function() {
//         $("a[data-popup-opener]").click(function(event) {
//             event.preventDefault();
//             opener.insertPageLink(window, $(this).data("popup-opener"));
//         });
// 
//     });

})(django.jQuery);
