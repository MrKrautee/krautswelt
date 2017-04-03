from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.forms import ModelForm 
from django.forms import HiddenInput, Textarea, TextInput
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed

from contents.views import render_content_to_string

from captcha.fields import CaptchaField, CaptchaTextInput
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url 

from .models import BlogEntry
from .models import RichTextContent, ImageContent
from .models import Comment

class CommentForm(ModelForm):

    # captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'comment','parent']
        widgets = {'parent': HiddenInput(), }

class CaptchaCommentForm(ModelForm):
    captcha = CaptchaField(required=True)
    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'comment','parent']
        widgets = {
            'name': HiddenInput(), 
            'email': HiddenInput(), 
            'website': HiddenInput(), 
            'comment': HiddenInput(), 
            'parent': HiddenInput(), 
                  }


def comment_form_check(request):
    if request.method == "POST" and request.is_ajax():
        form = CommentForm(request.POST)
        if 'captcha_1' in request.POST.keys():
            form_captcha = CaptchaCommentForm(request.POST)
            if form_captcha.is_valid():
                form.save()
            else:
                key = CaptchaStore.generate_key()
                url = captcha_image_url(key)
                new_captcha = {
                    'url': url,
                    'key': key,
                }
                return JsonResponse(new_captcha)
        return JsonResponse(form.errors)
    else:
        return HttpResponseNotAllowed(('POST',))

def entry_detail(request, slug):
    entry = get_object_or_404(BlogEntry, slug=slug)
    contents = render_content_to_string(request, entry, [RichTextContent, ImageContent])
    comments = Comment.objects.get_comments(entry)
    comment_form = CommentForm(initial={'parent':entry, })
    comment_form_captcha = CaptchaCommentForm(initial={'parent':entry, })

    return render(request, 'blog/blogentry_detail.html', {
        'object': entry,
        'contents': contents,
        'comments': comments,
        'comment_form': comment_form,
        'comment_form_captcha': comment_form_captcha,
    })


def entry_list(request):
    pass


def category_list(request):
    pass
