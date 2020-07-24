from django.shortcuts import render
from .models import Partners
# Create your views here.
def partner(request):
    #Partner object has information about current user and the partner they're linked to
    user=Partners.objects.get(user=request.user)
    partner=Partners.objects.get(user=user.partner)
    print(partner.name)
    return render(request,'partners/partner.html',{'partner':partner})
