from django.shortcuts import render
from datetime import datetime
from . import util

# Create your views here.
def index(request):
    return render(request, "baseball/index.html")

def standings(request):
    date_str = request.GET["date"]
    # assumes date is valid
    d = datetime.strptime(date_str, '%Y-%m-%d').date()
    standings = util.standings(d, league='AL')
    context = {"standings": standings, "date": d}
    return render(request, "baseball/standings.html", context)
