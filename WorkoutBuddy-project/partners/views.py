from django.shortcuts import render
from .models import Partners
# Create your views here.
def partner(request):
    #Partner object has information about current user and the partner they're linked to
    partner=Partners.objects.get(partner=request.user)
    return render(request,'partners/partner.html',{'partner':partner,'days':days,'workout_type':workout_type})
