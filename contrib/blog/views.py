from datetime import date
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404
from django.forms import ModelForm
from django.forms import HiddenInput
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from core.contents.views import render_content_to_string
from core.contents import app_reverse

from captcha.fields import CaptchaField
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from .models import BlogEntry
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
    contents = render_content_to_string(request, entry)
    comments = Comment.objects.get_comments(entry)
    comment_form = CommentForm(initial={'parent': entry, })
    comment_form_captcha = CaptchaCommentForm(initial={'parent': entry, })
    template_name = ('%s/%s_detail.html') % (BlogEntry._meta.app_label,
                                             BlogEntry._meta.model_name)
    context = {
        'object': entry,
        'contents': contents,
        'comments': comments,
        'comment_form': comment_form,
        'comment_form_captcha': comment_form_captcha,
    }
    return render(request, template_name, context)


class BlogEntryListView(ListView):

    queryset = BlogEntry.objects.get_active()
    template_name = '%s/%s_list.html' % (BlogEntry._meta.app_label,
                                         BlogEntry._meta.model_name)
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super(BlogEntryListView, self).get_context_data(**kwargs)
        context['site_title'] = _("All articles")
        return context


class BlogEntryYearArchive(BlogEntryListView):

    def get_context_data(self, **kwargs):
        context = super(BlogEntryYearArchive, self).get_context_data(**kwargs)
        context['site_title'] = _('Archive for %s') % self.args[0]
        return context

    def get_queryset(self):
        year = self.args[0]
        qs = BlogEntry.objects.get_for_year(year)
        return qs


class BlogEntryMonthArchive(BlogEntryListView):

    def get_context_data(self, **kwargs):
        context = super(BlogEntryMonthArchive, self).get_context_data(**kwargs)
        month_name = date(day=1, month=int(self.args[1]), year=2017).strftime('%B')
        context['site_title'] = _('Archive for %s') % month_name
        return context

    def get_queryset(self):
        month = self.args[1]
        year = self.args[0]
        qs = BlogEntry.objects.get_for_month(year, month)
        return qs


class BlogEntryDayArchive(BlogEntryListView):

    def get_context_data(self, **kwargs):
        context = super(BlogEntryDayArchive, self).get_context_data(**kwargs)
        day_date = date(day=int(self.args[2]), month=int(self.args[1]),
                          year=int(self.args[0]))

        title_attrs = {
            'month_name' : day_date.strftime('%B'),
            'day_name' : day_date.strftime('%A'),
            'day' : self.args[2],
            'year' : self.args[0],
        }
        context['site_title'] = _(
            'Archive for %(day_name)s, %(day)s. %(month_name)s %(year)s'
        ) % title_attrs
        return context

    def get_queryset(self):
        day = self.args[2]
        month = self.args[1]
        year = self.args[0]
        qs = BlogEntry.objects.get_for_day(year, month, day)
        return qs

def entry_archive(request):

    template_name = ('%s/%s_archive.html') % (BlogEntry._meta.app_label,
                                             BlogEntry._meta.model_name)
    years = BlogEntry.objects.get_years()
    month = BlogEntry.objects.get_months()

    month_plus_count = []
    for m in month:
        count = BlogEntry.objects.get_for_month(m.year, m.month).count()
        tmp = {}
        tmp['count'] = count
        tmp['month'] = m
        month_plus_count.append(tmp)

    return render(request, template_name, {'years': years,
                                           'month': month_plus_count})

def category_list(request):
    pass
