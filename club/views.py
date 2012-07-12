from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response, redirect
from django.template import RequestContext

def checkin(request):
    return render_to_response("checkin.html", {
        }, RequestContext(request))
