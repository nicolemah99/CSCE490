from django.shortcuts import render
from . import util

# Create your views here.
def index(request):
    return render(request, "baseball/index.html")

from datetime import datetime
def standings(request):
    date = request.GET["date"]
    # assumes date is valid
    standings = util.standings(date, league='AL')
    date_object = datetime.strptime(date, '%Y-%m-%d').date()
    context = {"standings": standings, "date": date_object.strftime("%B %d, %Y")}
    return render(request, "baseball/standings.html", context)
