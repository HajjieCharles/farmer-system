from django.shortcuts import render
from .models import Farmer

def home(request):
    if request.method == 'POST':
        Farmer.objects.create(
            farmer_name=request.POST.get('farmer_name'),
            phone_number=request.POST.get('phone_number'),
            parish=request.POST.get('parish'),
            land_location=request.POST.get('land_location'),
            land_size=request.POST.get('land_size'),
            crop_type=request.POST.get('crop_type')
        )
        return render(request, 'farmers/home.html', {'success': True})

    return render(request, 'farmers/home.html')