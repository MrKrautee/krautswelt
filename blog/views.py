from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.forms import ModelForm
from django.forms import HiddenInput
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from contents.views import render_content_to_string

from captcha.fields import CaptchaField
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from .models import BlogEntry
from .models import RichTextContent, ImageContent
from .models import Comment


class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = _("name *")
        self.fields['email'].widget.attrs['placeholder'] = _("email *")
        self.fields['website'].widget.attrs['placeholder'] = _("my.website.com *")
        self.fields['comment'].widget.attrs['placeholder'] = _("your comment ...")
        self.fields['comment'].widget.attrs['rows'] = 3

    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'comment', 'parent']
        widgets = {'parent': HiddenInput(), }



class CaptchaCommentForm(ModelForm):
    captcha = CaptchaField(required=True)


    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'comment', 'parent']
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
                audio_url = reverse('captcha-audio', args=[key])
                reload_popover_html = render_to_string(
                    'captcha/reload_popover.html',
                                {})
                # need no exact error message but captcha reload.
                # use data structure same as form.erros because javascript
                # expecting it... (? dirty or not ?)
                new_captcha = {
                    'captcha_1': {
                        'url': url,
                        'audio_url': audio_url,
                        'key': key,
                        'errors':
                        form_captcha.errors['captcha'],
                        'error_placeholder': _('please try again.'),
                        'reload_popover_html': reload_popover_html,
                    }
                }
                return JsonResponse(new_captcha)
        return JsonResponse(form.errors)
    else:
        return HttpResponseNotAllowed(('POST',))


def entry_detail(request, slug):
    entry = get_object_or_404(BlogEntry, slug=slug)
    contents = render_content_to_string(request, entry,
                                        [RichTextContent, ImageContent])
    comments = Comment.objects.get_comments(entry)
    comment_form = CommentForm(initial={'parent': entry, })
    comment_form_captcha = CaptchaCommentForm(initial={'parent': entry, })
    template_name = ('%s/%s_detail.html') % (BlogEntry._meta.app_label,
                                             BlogEntry._meta.model_name)
    return render(request, template_name), {
        'object': entry,
        'contents': contents,
        'comments': comments,
        'comment_form': comment_form,
        'comment_form_captcha': comment_form_captcha,
    })


class BlogEntryListView(ListView):

    queryset = BlogEntry.objects.get_active()
    template_name = '%s/%s_list.html' % (BlogEntry._meta.app_label,
                                         BlogEntry._meta.model_name) 



def category_list(request):
    pass
