 CKEDITOR.plugins.add( 'internal_links', {
    icons: 'internal_links',
    init: function( editor ) {
        editor.addCommand( 'openLinkPopUp', {
            exec: function( editor ) {
							var name = 'ckeditor_name:'+editor.name;
							var options = 'height=700,width=1300,resizable=yes,scrollbars=yes';
							var url = '/admin/pages/page/?_popup=1' //&_to_field=id
              window.open(url, name, options);
              // editor.insertHtml( 'The current date and time is: <em>' );
            }
        });
        editor.ui.addButton( 'Link', {
            label: 'Insert Page Link',
            command: 'openLinkPopUp',
            toolbar: 'insert'
        });
    }
});
