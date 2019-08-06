from django.db.models import signals
from django.utils.functional import curry
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
class WhoIsMiddleware(object):
    def process_request(self, request):
        if not request.method in ('GET','HEAD','OPTIONS', 'TRACE'):
            if not hasattr(request, 'user') and request.user.is_authenticated():
                user = request.user
            else:
                user = None
            mark_whodid = curry(self.whodid, user)
            signals.pre_save.connect(mark_whodid, dispatch_uid=(self.__class__, request,),weak=False)
    def process_response(self, request, response):
        signals.pre_save.disconnect(dispatch_uid=(self.__class__, request),)
        return response
    def mark_whodid(self, user, sender, instance, **kwargs):
        if 'owner' in instance._meta.fields and not instance.owner:
            instance.owner = user
        if 'updated_by' in instance._meta.fields:
            instance.updated_by = user
    def process_exception(self, request, exception):
        return HttpResponse('this exception')