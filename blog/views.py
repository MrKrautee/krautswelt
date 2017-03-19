from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.forms import ModelForm 
from django.forms import HiddenInput, Textarea, TextInput
from django.http import JsonResponse

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
        print(form.errors.as_json())
        return JsonResponse(form.errors)

def comment_form(request):
    print("DRINNNNNNNNNN")
    form = CommentForm()
    if request.POST and 'entry_id' in request.POST.keys():
        if request.is_ajax():
            entry_id = request.POST.get('entry_id')
            form = CommentForm(request.POST)
            if form.is_valid():
                c = form.save(commit=False)
                c.parent = BlogEntry.objects.get(id=entry_id)
                c.save()
                return render(request, 'blog/comments/comment_form_success.html')
            return render(request, 'blog/comments/comment_form.html',
                          {'comment_form': form, })
    return render(request, 'blog/comments/comment_form.html',
                  {'comment_form': form, })

def entry_detail(request, slug):
    entry = get_object_or_404(BlogEntry, slug=slug)
    contents = render_content_to_string(request, entry, [RichTextContent, ImageContent])
    comments = Comment.objects.filter(parent=entry)
    comment_form = CommentForm(initial={'parent':entry, })
    if request.POST and 'captcha_1' in request.POST:
        comment_form = CaptchaCommentForm(request.POST, )
        print("CHECK")
        if comment_form.is_valid():
            print("SUCCESS")
            c = comment_form.save(commit=False)
            c.parent = entry
            c.save()
            comment_form = None

    elif request.POST:
        comment_form = CaptchaCommentForm(request.POST)


    return render(request, 'blog/blogentry_detail.html', {
        'object': entry,
        'contents': contents,
        'comment_form': comment_form,
        'comments': comments,
    })


def entry_list(request):
    pass


def category_list(request):
    pass
