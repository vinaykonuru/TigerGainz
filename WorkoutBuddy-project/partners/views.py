from django.shortcuts import render
from .models import Partners
from buddyrequest.matching_algorithm import to_words
# Create your views here.
def partner(request):
    #Partner object has information about current user and the partner they're linked to
    partner=Partners.objects.get(partner=request.user)
    days,workout_type=to_words(partner.days,partner.workout_type)
    print(partner.name)
    return render(request,'partners/partner.html',{'partner':partner,'days':days,'workout_type':workout_type})
