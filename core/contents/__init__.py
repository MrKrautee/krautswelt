from django.db import models as dbmodels
from django.shortcuts import render
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

class _ContentHandler(object):
    _ctype_register = {} # { model: [ctype1, ctype2] }

    def register_ctype(self, model_cls, content_type):
        if model_cls in self._ctype_register.keys():
            self._ctype_register[model_cls].append(content_type)
        else:
            self._ctype_register[model_cls] = [content_type, ]

    def get_ctype_names(self, model_cls):
        return [ c.__name__ for c in self._ctype_register[model_cls] ]

    def get_ctypes(self, model_cls=None):
        if model_cls:
            return list(self._ctype_register[model_cls])
        else:
            return dict(self._ctype_register)

    def _get_contents(self, model, ctype):
        model_cls= model.__class__
        ct_name = model_cls._meta.app_label
        ct_related = "%s_%s_set" % (ct_name, ctype.__name__.lower())
        contents = model.__getattribute__(ct_related).all()
        return contents

    def get_app_content(self, model):
        from .models import ApplicationContent
        app_cnt_name = _mk_ctype_name(model.__class__, ApplicationContent)
        ctypes_names = self.get_ctype_names(model.__class__)
        ctypes= self.get_ctypes(model.__class__)
        if app_cnt_name in ctypes_names:
            ctype = None
            for ct in ctypes:
                if ct.__name__ == app_cnt_name:
                    ctype = ct
            app_contents = self._get_contents(model, ct)
            if app_contents:
                return app_contents[0]
            return None
        return None

    def get_contents(self, model):
        model_cls= model.__class__
        ctypes = self.get_ctypes(model_cls)
        all_contents = []
        for ct in ctypes:
            contents = self._get_contents(model, ct)
            all_contents += list(contents)
        all_contents = sorted(all_contents, key=lambda a: a.ordering)
        return all_contents

content_register = _ContentHandler()

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

    related_name=_mk_related_ctype_name(cls, content_type)
    attrs = {
        '__module__': cls.__module__,
        '__str__': __str__,
        'get_queryset': get_queryset,
        'Meta': Meta,
        'parent': dbmodels.ForeignKey(cls, related_name=related_name,
                                      on_delete=dbmodels.CASCADE),
        'region': dbmodels.CharField(max_length=255),
        'ordering': dbmodels.IntegerField(default=0),
    }
    try:
        content_type.init(**kwargs)
    except AttributeError as e:
        if 'init' not in str(e):
            raise e
    ctype = type(name, (content_type,), attrs)

    def render(self, *args, **kwargs):
        keyw_args = { 'content_info' : self}
        keyw_args.update(kwargs)
        return super(ctype, self).render(*args, **keyw_args)

    ctype.render = render
    content_register.register_ctype(cls, ctype)
    return ctype

def _app_reverse_model(model_cls, view_name, args=None, kwargs=None,
                       content_type=None):
    from .models import ApplicationContent
    content_type = content_type or ApplicationContent
    ctype_name = _mk_ctype_name(model_cls, content_type)
    related_name = _mk_related_ctype_name(model_cls, content_type)
    qs=model_cls.objects.annotate(num_appcontents=Count(related_name.lower()))
    url = None
    app_content = None
    for q in qs:
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
        raise NoReverseMatch("app_reverse: no match for %s, "
                             "with args=%s,kwargs=%s" %
                             (view_name, str(args), str(kwargs)))
    return "%s%s" % (app_content.parent.get_absolute_url(), url[1:])

def _app_reverse_full(view_name, args=None, kwargs=None, content_type=None):
    model_contents = content_register.get_ctypes()
    url = None
    try:
        for model, contens in model_contents.items():
            url = _app_reverse_model(model, view_name, args, kwargs,
                                     content_type)
    except Exception as e:
        pass
    if not url:
        raise NoReverseMatch("app_reverse: no match for %s, "
                             "with args=%s,kwargs=%s" %
                             (view_name, str(args), str(kwargs)))
    return url

def app_reverse(*args, **kwargs):
    if len(args) == 2:
        # @TODO: BUG not working for BlogEntry, 'entry_detail'
        return _app_reverse_model(*args, **kwargs)
    elif len(args) == 1:
        return _app_reverse_full(*args, **kwargs)
    raise ValueError("need 1 or 2 positional arguments.")

