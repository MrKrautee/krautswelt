from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags, mark_safe

from content_editor.models import create_plugin_base, Region

from core.contents.models import WithContents
from core.contents.models import ImageContent
from core.contents.models import RichTextContent

try:
    from core.contents import app_reverse
except:
    from django.urls import reverse
    def app_reverse( view_name, **kwargs):
        return reverse(view_name, urlconf='contrib.blog.urls', **kwargs)

class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)

    def __str__(self):
        return self.name


class ArticleManager(models.Manager):

    active_filter = dict (
                        is_active=True,
                        pub_date__lte=timezone.now(),
                         )

    def get_queryset(self):
        qs = super(ArticleManager, self).get_queryset()
        return qs

    def get_active(self, **kwargs):
        qs = self
        if kwargs:
            qs = qs.filter(**kwargs)
        qs = qs.filter(**self.active_filter)
        qs = qs.order_by('-pub_date')
        return qs

    def get_for_year(self, year):
        qs = self.get_active()
        qs = qs.filter(pub_date__year=year)
        qs.order_by('-pub_date')
        return qs

    def get_for_month(self, year, month):
        qs = self.get_active()
        qs = qs.filter(pub_date__year=year, pub_date__month=month)
        qs.order_by('-pub_date')
        return qs

    def get_for_day(self, year, month, day):
        qs = self.get_active()
        qs = qs.filter(pub_date__year=year, pub_date__month=month,
                       pub_date__day=day)
        qs.order_by('-pub_date')
        return qs

    # get all years with active comments
    def get_years(self):
        qs = self.get_active()
        return qs.dates('pub_date', 'year')

    # get month with active comments
    def get_months(self):
        qs = self.get_active()
        return qs.dates('pub_date', 'month')


class Article(WithContents):

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    pub_date = models.DateTimeField(_('publication date'))
    create_date = models.DateTimeField(_('creation date'), auto_now_add=True,
                                       editable=False)
    is_featured = models.BooleanField(_('is featured'), default=False)
    is_active = models.BooleanField(_('is active'), default=False)

    categories = models.ManyToManyField(Category, verbose_name=_('categories'),
                                        related_name='articles',
                                        blank=True)

    # @TODO: related_entries
    related_articles = models.ManyToManyField("self",
                                             related_name='articles',
                                             blank=True,
                                             verbose_name=_('related articles'))

    regions = (Region(key='main', title=_('Main')), )

    objects = ArticleManager()

    def get_excerpt(self, word_count=350):
        return self.getFirstRichText().excerpt(word_count=word_count)

    def get_comments(self):
        qs = self.comment_set.filter(is_active=True)
        qs = qs.order_by('-pub_date')
        return qs

    def get_comments_count(self):
        return self.get_comments().count()

    def get_absolute_url(self):
        url = app_reverse('article_detail', args=(self.slug,))
        return url

    def __str__(self):
        return "%s" % self.title[:20]


Article.create_content_type(ImageContent)
Article.create_content_type(RichTextContent)

class CommentManager(models.Manager):

    def get_comments(self, entry):
        qs = self.get_queryset()
        # until there is no feature to activate comments, show
        # inactive ones, too.
        qs_filtered = qs.filter(is_active=True, parent=entry)
        qs_filtered = qs_filtered.order_by('-date')
        return qs_filtered

    def get_unapproved(self):
        qs = self.get_queryset()
        qs = qs.filter(is_active=False)
        qs = qs.order_by('-date')
        return qs


class Comment(models.Model):

    parent = models.ForeignKey(Article, models.CASCADE)

    name = models.CharField(_('name'),
                            max_length=100,
                            help_text=_('Your name will be published.'))
    email = models.EmailField(
        _('email'),
        help_text=_('Your email will never shown to anyone else'))
    website = models.URLField(_('website'), blank=True)
    comment = models.TextField(_('comment'))
    date = models.DateTimeField(_('date'), auto_now_add=True,
                                editable=False)

    is_active = models.BooleanField(_('id active'), default=False)
    notify_new_comment = models.BooleanField(_('notify  new comments'),
                                             help_text=_('notify me for new comments'),
                                             default=False)
    notify_new_entry = models.BooleanField(_('notify new blog entries'),
                                           help_text=_('notify me for new entries'),
                                           default=False)
    objects = CommentManager()

    def approve(self):
        self.is_active = True
        return self.save()

    def set_spam(self):
        return self.delete()

    def comment_excerpt(self):
        return self.comment[:100]
