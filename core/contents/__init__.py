from django.db import models as dbmodels

def create_content_type(cls, content_type, **kwargs):
    name = "%s%s" %  (cls.__name__, content_type.__name__)
    class Meta:
        app_label = cls._meta.app_label
        ordering = ['ordering']
        verbose_name = content_type._meta.verbose_name
        verbose_name_plural = content_type._meta.verbose_name_plural

    def __str__(self):
        return '%s<region=%s ordering=%s pk=%s>' % (
            self._meta.label,
            self.region,
            self.ordering,
            self.pk,
        )

    @classmethod
    def get_queryset(cls):
        return cls.objects.all()

    attrs = {
        '__module__': cls.__module__,
        '__str__': __str__,
        'get_queryset': get_queryset,
        'Meta': Meta,
        'parent': dbmodels.ForeignKey(cls, related_name='%s_%s_set'%(cls._meta.app_label,
                                name.lower()),on_delete=dbmodels.CASCADE),
        'region': dbmodels.CharField(max_length=255),
        'ordering': dbmodels.IntegerField(default=0),
    }
    try:
        content_type.init(**kwargs)
    except Exception as e:
        print(e)
    ctype = type(name, (content_type,), attrs)

    def render(self, request, **kwargs):
        keyw_args = { 'base_content' : self}
        keyw_args.update(kwargs)
        return super(ctype, self).render(request, **keyw_args)

    ctype.render = render
    return ctype

