from django.db import models as dbmodels
from django.urls import reverse
from django.urls import NoReverseMatch
from django.db.models import Count

def _mk_ctype_name(model_cls, content_type):
    name = "%s%s" %  (model_cls.__name__, content_type.__name__)
    return name

def _mk_related_ctype_name(cls, content_type):
    name = _mk_ctype_name(cls, content_type)
    related_name='%s_%s_set'%(cls._meta.app_label, name.lower())
    return related_name

def create_content_type(cls, content_type, **kwargs):
    name = _mk_ctype_name(cls, content_type)
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
        'parent': dbmodels.ForeignKey(cls,
                                      related_name=_mk_related_ctype_name(cls,
                                                                         content_type),
                                      on_delete=dbmodels.CASCADE
                                     ),
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

def app_reverse(model_cls, view_name, args=None, kwargs=None, content_type=None):
    from .models import ApplicationContent
    content_type = content_type or ApplicationContent
    ctype_name = _mk_ctype_name(model_cls, content_type)
    related_name = _mk_related_ctype_name(model_cls, content_type)
    qs=model_cls.objects.annotate(num_appcontents=Count(related_name.lower()))
    url = None
    app_content = None
    for q in qs:
        print(q.num_appcontents)
        if q.num_appcontents:
            try:
                app_content = q.__getattribute__(related_name).all()[0]
                urls_conf = app_content.urls_conf
                url = reverse(view_name, urlconf=urls_conf, args=args,
                              kwargs=kwargs)
            except Exception as e:
                print(e)
                pass
            if url:
                break
    if not url:
        raise NoReverseMatch("app_reverse: no match for %s, with args=%s,kwargs=%s" %
                             (view_name, str(args), str(kwargs)))
    print(app_content)
    return "%s%s" % (app_content.parent.get_absolute_url(), url[1:])
