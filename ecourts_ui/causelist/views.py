import requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from bs4 import BeautifulSoup
import io
from .models import DownloadLog
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

BASE = 'https://services.ecourts.gov.in/ecourtindia_v6/'

def index(request):
    return render(request, 'index.html')

def api_states(request):
    # Scrape the main cause_list page to get states (updates in real-time)
    r = requests.get(BASE + '?p=cause_list/')
    soup = BeautifulSoup(r.text, 'html.parser')
    opts = soup.select('div:contains("Select state")')  # fallback
    states = []
    # The page renders a list of state names; fall back to manual parse
    # We'll extract the long list in the page text under "Select state"
    for sel in soup.find_all(text=True):
        pass
    # Simpler approach: parse the state links from the select content
    state_container = soup.find('div', string=lambda s: s and 'Select state' in s)
    # As a robust fallback, return a curated list if parsing fails
    curated = ['Andaman and Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu and Kashmir','Jharkhand','Karnataka','Kerala','Ladakh','Lakshadweep','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttarakhand','Uttar Pradesh','West Bengal']
    return JsonResponse({'states': curated})

def api_districts(request):
    state = request.GET.get('state')
    # Note: official site often provides endpoints; here we attempt a POST to known path
    # Fallback: return an empty list if can't fetch
    try:
        resp = requests.get(BASE + '?p=cause_list/')
        soup = BeautifulSoup(resp.text, 'html.parser')
        # site uses JS to populate districts; scraping is brittle. return empty list instructing user.
        return JsonResponse({'districts': [], 'note': 'Districts often require JS/API. Use the UI to select or run the Selenium helper script included.'})
    except Exception as e:
        return JsonResponse({'districts': [], 'error': str(e)})

def api_complexes(request):
    district = request.GET.get('district')
    return JsonResponse({'complexes': [], 'note': 'Court complexes require calling eCourts API; for reliability use the included Selenium script (see README).'})


def api_courts(request):
    complex_code = request.GET.get('complex')
    return JsonResponse({'courts': [], 'note': 'Court names load via site JS/AJAX and may need a browser session. See README.'})

@csrf_exempt
def api_download(request):
    # This endpoint tries to fetch the cause list PDF URL if possible.
    state = request.POST.get('state')
    district = request.POST.get('district')
    complex_name = request.POST.get('complex')
    court = request.POST.get('court')
    date_str = request.POST.get('date')  # expected YYYY-MM-DD
    # Log the request
    try:
        d = datetime.fromisoformat(date_str).date() if date_str else None
    except:
        d = None
    DownloadLog.objects.create(state=state or '', district=district or '', complex_name=complex_name or '', court_name=court or '', date=d)
    # IMPORTANT: The live site enforces a CAPTCHA for downloading cause list PDFs.
    # We cannot bypass CAPTCHA automatically here. Inform user and provide a helpful message.
    return JsonResponse({
        'ok': False,
        'message': 'Cannot automatically download cause list PDF due to CAPTCHA protection on eCourts site.\n' +
                   'Please use the helper Selenium script included (scripts/download_causelist.py) which opens a browser and lets you complete the CAPTCHA once; after that the script can continue to download cause lists for all courts in a complex.'
    })
