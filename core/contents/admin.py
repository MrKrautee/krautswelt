from django.contrib import admin

from content_editor.admin import ContentEditorInline
# Register your models here.

def create_inline(**kwargs):
    '''
        ImageInline = create_inline(model=ImageContent)
    '''
    return ContentEditorInline.create(model=kwargs['model'])
