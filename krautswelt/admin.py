from django.contrib.admin import AdminSite, site


class KrautsweltAdminSite(AdminSite):

    site_header = 'krautswelt administration'
    site_title = 'krautswelt admin'
    index_template = 'krautswelt/admin/index.html'
    app_index_template = 'krautswelt/admin/app_index.html'

    def __init__(self, *args, **kwargs):
        super(KrautsweltAdminSite, self).__init__(*args, **kwargs)
        # use django default admin.site registry.
        # self._registry = site._registry
        self._notificions_callbacks = {}

    # use django default admin.site registry.
    def _registry_getter(self):
        return site._registry

    def _registry_setter(self, value):
        site._registry = value
    _registry = property(_registry_getter, _registry_setter)

    '''
     register an message callback to display app messages on the
     admin index page.
     msg_callback should return an dictionary with keys:
        url, message.
        message - string message to display.
        url - string url to open on click on message.
    '''
    def register_notification(self, model, msg_callback):
            self._notificions_callbacks.update(
                {model: msg_callback, })

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        msgs = {}
        for model, callback in self._notificions_callbacks.items():
            msg = callback(request)
            if msg:
                msgs[model] = msg
        extra_context['notifications'] = msgs
        # add extra context
        return super(KrautsweltAdminSite,
                     self).index(request, extra_context=extra_context)

admin_site = KrautsweltAdminSite()
