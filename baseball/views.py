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


def logos(request):
    d = datetime.strptime("2022-01-01", '%Y-%m-%d').date()
    standings = []
    for l in ['AL', 'NL']:
        standings.extend(util.standings(d, league=l))
    logos = []
    for s in standings:
        code = s.code
        name = util.team_name(code)
        url = util.team_logo(code)
        logos.append((code, name, url))
    return render(request, "baseball/logos.html", {"logos": logos})


def redsox(request):
    return oneteam("BOS")


def oneteam(request, code):
    code = code.upper()
    name = util.team_name(code)
    url = util.team_logo(code)
    return render(request, "baseball/oneteam.html",
                  {"code": code, "name": name, "url": url})
