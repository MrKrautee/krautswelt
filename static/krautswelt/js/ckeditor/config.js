// Loads a plugin from '/myplugins/sample/plugin.js'.
CKEDITOR.plugins.addExternal( 
  'page_links', 
  '/static/pages/js/ckeditor/plugins/page_links/plugin.js'
);

CKEDITOR.editorConfig = function( config ) {
    config.extraPlugins = 'page_links';
}; 
