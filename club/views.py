from club.models import Member
from django.http import HttpResponse

def index(request):
    members = Member.objects.order_by('-weight')
    s = ''
    return HttpResponse(s)
