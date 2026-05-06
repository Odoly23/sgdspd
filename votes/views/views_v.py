from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import VotingResult, VotingPlace
from membro.models import Membru

@login_required
def input_voting(request):
    if request.method == 'POST':
        total_votes = request.POST.get('total_votes')
        photo = request.FILES.get('photo')
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        membro = Membru.objects.get(membrouser__user=request.user)
        lokasi = membro.locationtl
        voting_place, created = VotingPlace.objects.get_or_create(
            municipality=lokasi.municipality,
            administrativepost=lokasi.administrativepost,
            village=lokasi.village,
            aldeia=lokasi.aldeia,
            defaults={
                'name': f"TPS {lokasi.aldeia}"
            }
        )
        VotingResult.objects.create(
            membro=membro,
            voting_place=voting_place,
            total_votes=total_votes,
            photo=photo,
            latitude=lat,
            longitude=lng
        )

        return redirect('success')

    return render(request, 'voting/add.html')