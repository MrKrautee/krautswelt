from datetime import date
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.forms import ModelForm
from django.forms import HiddenInput
from django.views.generic import ListView
from django.views.generic import DetailView
from django.urls import reverse

from core.contents.views import render_content_to_string
from core.contents import app_reverse

from contrib.kcaptcha.forms import captcha_form_factory
from contrib.kcaptcha.forms import CaptchaModelForm

from .models import Article
from .models import ArticleManager
from .models import Comment

class CommentForm(CaptchaModelForm):
    js_form_name = 'CommentKCaptcha'
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = _("name *")
        self.fields['email'].widget.attrs['placeholder'] = _("email *")
        self.fields['website'].widget.attrs['placeholder'] = _("my.website.com *")
        self.fields['comment'].widget.attrs['placeholder'] = _("your comment ...")
        self.fields['comment'].widget.attrs['rows'] = 3
    class Meta(CaptchaModelForm.Meta):
        model = Comment
        fields = ['name', 'email', 'website', 'comment', 'parent',
                  'notify_new_entry', 'notify_new_comment']
        widgets = {'parent': HiddenInput(), }

    class Media(CaptchaModelForm.Media):
        js = ('blog/js/comments.js',)

    @property
    def js_config(self):
        return dict(
            url = app_reverse('comment_form_check'),
            model_form_selector = 'div#comment_form form',
            captcha_form_selector = 'div#comment_form_captcha form',
        )

class ArticleDetail(DetailView):
    context_object_name = "object"
    queryset = Article.objects.get_active()
    template_name = ('%s/%s_detail.html') % (Article._meta.app_label,
                                             Article._meta.model_name)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = self.get_object()
        contents = render_content_to_string(self.request, entry)
        comments = Comment.objects.get_comments(entry)
        comment_form = CommentForm(initial={'parent': entry, })
        CaptchaCommentForm = captcha_form_factory(comment_form)
        comment_form_captcha = CaptchaCommentForm(initial={'parent': entry, })
        extra_context = {
            'object': entry,
            'contents': contents,
            'comments': comments,
            'comment_form': comment_form,
            'comment_form_captcha': comment_form_captcha,
        }
        context.update(extra_context)
        return context

class ArticleListView(ListView):
    queryset = Article.objects.get_active()
    template_name = '%s/%s_list.html' % (Article._meta.app_label,
                                         Article._meta.model_name)
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['site_title'] = _("All articles")
        return context


class ArticleYearArchive(ArticleListView):
    def get_context_data(self, **kwargs):
        context = super(ArticleYearArchive, self).get_context_data(**kwargs)
        context['site_title'] = _('Archive for %s') % self.args[0]
        return context

    def get_queryset(self):
        year = self.args[0]
        qs = Article.objects.get_for_year(year)
        return qs

class ArticleMonthArchive(ArticleListView):
    def get_context_data(self, **kwargs):
        context = super(ArticleMonthArchive, self).get_context_data(**kwargs)
        month_name = date(day=1, month=int(self.args[1]), year=2017).strftime('%B')
        context['site_title'] = _('Archive for %s') % month_name
        return context

    def get_queryset(self):
        month = self.args[1]
        year = self.args[0]
        qs = Article.objects.get_for_month(year, month)
        return qs

class ArticleDayArchive(ArticleListView):
    def get_context_data(self, **kwargs):
        context = super(ArticleDayArchive, self).get_context_data(**kwargs)
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
        qs = Article.objects.get_for_day(year, month, day)
        return qs

# @TODO: use generic view class
def article_archive(request):
    template_name = ('%s/%s_archive.html') % (Article._meta.app_label,
                                             Article._meta.model_name)
    years = Article.objects.get_years()
    month = Article.objects.get_months()
    month_plus_count = []
    for m in month:
        count = Article.objects.get_for_month(m.year, m.month).count()
        tmp = {}
        tmp['count'] = count
        tmp['month'] = m
        month_plus_count.append(tmp)
    return render(request, template_name, {'years': years,
                                           'month': month_plus_count})

def category_list(request):
    pass
