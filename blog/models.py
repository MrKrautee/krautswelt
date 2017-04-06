import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags, mark_safe

from content_editor.models import create_plugin_base, Region

from contents.models import AbstractImageContent, AbstractRichTextContent


class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)

    def __str__(self):
        return self.name


class BlogEntryManager(models.Manager):

    def get_queryset(self):
        qs = super(BlogEntryManager, self).get_queryset()
        return qs

    def get_active(self):
        qs = self.get_queryset().filter(is_active=True)
        qs = qs.filter(pub_date__lte=datetime.datetime.now())
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

    # get year, month dict with active comments
    def get_months(self):
        qs = self.get_active()
        return qs.dates('pub_date', 'month')


class BlogEntry(models.Model):

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    pub_date = models.DateTimeField(_('publication date'))
    create_date = models.DateTimeField(_('creation date'), auto_now_add=True,
                                       editable=False)
    is_featured = models.BooleanField(_('is featured'), default=False)
    is_active = models.BooleanField(_('is active'), default=False)

    categories = models.ManyToManyField(Category, verbose_name=_('categories'),
                                        related_name='blogentries',
                                        blank=True)

    # @TODO: related_entries

    regions = (Region(key='main', title=_('Main')), )

    objects = BlogEntryManager()

    def get_excerpt(self, length=777):
        richtxt_contents = self.blog_richtextcontent_set.all()
        richtxt_contents = richtxt_contents.order_by('ordering')
        if richtxt_contents.count():
            return mark_safe(richtxt_contents[0].as_str()[:length])
        return ''

    def get_comments(self):
        qs = self.comment_set.filter(is_active=True)
        qs = qs.order_by('-pub_date')
        return qs

    def get_comments_count(self):
        return self.get_comments().count()

    def get_first_image(self):
        qs = self.blog_imagecontent_set.order_by('ordering')
        if qs.count():
            return qs[0]
        return None


    def __str__(self):
        return "%s" % self.title[:20]

BlogEntryContent = create_plugin_base(BlogEntry)


class ImageContent(AbstractImageContent, BlogEntryContent):

    LEFT = 'l'
    RIGHT = 'r'
    NONE = 'n'

    IMAGE_ALIGN_CHOICES = ((LEFT, 'left'), (RIGHT, 'right'), (NONE, 'none'))

    css_float = models.CharField(_('css float'),
                                 max_length=1,
                                 choices=IMAGE_ALIGN_CHOICES,
                                 default=RIGHT)


class RichTextContent(AbstractRichTextContent, BlogEntryContent):

    def as_str(self):
        return mark_safe(strip_tags(self.text))


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

    parent = models.ForeignKey(BlogEntry)

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
    notify_new_comment = models.BooleanField(_('notify me for new comments'),
                                             default=False)
    notify_new_entry = models.BooleanField(_('notify me for new blog entries'),
                                           default=False)
    objects = CommentManager()

    def approve(self):
        self.is_active = True
        return self.save()

    def set_spam(self):
        return self.delete()

    def comment_excerpt(self):
        return self.comment[:100]
