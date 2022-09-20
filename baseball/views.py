from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "baseball/index.html")

from datetime import datetime
def standings(request):
    date = request.GET["date"]
    # if d is not valid, redirect to home page

    # other, figure out the record of teams on given date
    standings = []
    date_object = datetime.strptime(date, '%Y-%m-%d').date()
    context = {"standings": standings, "date": date_object.strftime("%B %d, %Y")}
    return render(request, "baseball/standings.html", context)

