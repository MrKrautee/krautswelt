from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.forms import ModelForm 
from django.forms import HiddenInput, Textarea, TextInput
from django.http import JsonResponse, HttpResponseForbidden


from contents.views import render_content_to_string
from captcha.fields import CaptchaField, CaptchaTextInput

from .models import BlogEntry
from .models import RichTextContent, ImageContent
from .models import Comment

class CommentForm(ModelForm):

    # captcha = CaptchaField()


    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'comment',]
        # widgets = {'comment': HiddenInput(), }

class CaptchaCommentForm(CommentForm):
    captcha = CaptchaField(required=True)
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment',]
        widgets = {'name': HiddenInput(), 'email': HiddenInput(), 'comment':
                   HiddenInput(), 
                  }


def comment_form_check(request):
    if request.method == "POST" and request.is_ajax():
        form = CommentForm(request.POST)
        return JsonResponse(form.errors)
    return HttpResponseForbidden()

def comment_form(request):
    form = CommentForm()
    if request.POST:
        if request.is_ajax():
            if 'entry_id' in request.POST.keys():
                entry_id = request.POST.get('entry_id')
                form = CommentForm(request.POST)
                if form.is_valid():
                    c = form.save(commit=False)
                    c.parent = BlogEntry.objects.get(id=entry_id)
                    c.save()
                    return render(request,
                                  'blog/comments/comment_form_success.html',
                                  {'comment': c, })
                else:
                    return render(request, 'blog/comments/comment_form.html',
                                                      {'comment_form': form, })
            else:
                return render(request, 'blog/comments/comment_form.html',
                                                      {'comment_form': form, })
    return HttpResponseForbidden()

def entry_detail(request, slug):
    entry = get_object_or_404(BlogEntry, slug=slug)
    contents = render_content_to_string(request, entry, [RichTextContent, ImageContent])
    comments = Comment.objects.get_comments(entry)
    comment_form = CommentForm(initial={'parent':entry, })

    return render(request, 'blog/blogentry_detail.html', {
        'object': entry,
        'contents': contents,
        'comments': comments,
        'comment_form': comment_form,
    })


def entry_list(request):
    pass


def category_list(request):
    pass
