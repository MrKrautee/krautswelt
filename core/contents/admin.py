from django.contrib import admin

from content_editor.admin import ContentEditorInline
from . import content_register

def create_inlines(model):
    inlines = []
    for ct in content_register.get_ctypes(model):
        inlines.append(ContentEditorInline.create(model=ct))
    return inlines
