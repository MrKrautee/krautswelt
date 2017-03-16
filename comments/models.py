from django.db import models
from django.utils.translation import ugettext_lazy as _

def create_comment_class(comment_base):

    class Comments(models.Model):

        parent = models.ForeignKey(comment_base)

        name = models.CharField(_('name'), max_length=100)
        email = models.EmailField(_('email'), blank=True)
        comment = models.TextField(_('comment'))
        date = models.DateTimeField(_('date'), auto_now_add=True,
                                    editable=False)

        class Meta:
            abstract = True

    return Comments

