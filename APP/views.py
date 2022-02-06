from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse, response
from .serializers import BigyoSerializer
from .models import Bigyo, Hf, Mentoral, Repo

@login_required
def index(request: HttpRequest) -> HttpResponse:
    return redirect(f'http://{request.get_host()}/hf/fontos/')


@login_required
def hazik(request: HttpRequest, szuro: str) -> HttpResponse:
    return render(request, "hf.html", { 
        'hazik': Hf.lista(request.user) if szuro=="osszes" else Hf.lista(request.user, Hf.fontos)
    })

@login_required
def mentoralas(request: HttpRequest, szuro: str) -> HttpResponse:
    mentoraltak_hazijai = []
    for mentorkapcsolat in Mentoral.objects.filter(mentor=request.user):
        mentoraltak_hazijai+= Hf.lista(mentorkapcsolat.mentoree) if szuro =="osszes" else Hf.lista(mentorkapcsolat.mentoree, Hf.mentorfontos)
    return render(request, "mentoralas.html", { 
        'hazik': mentoraltak_hazijai
    })


@login_required
def repo_check(request: HttpRequest, hfid: int) -> HttpResponse:
    a_hf = Hf.objects.filter(id=hfid).first()
    a_repo = Repo.objects.filter(hf=a_hf)
    if a_repo.exists():
        return redirect(f'http://{request.get_host()}/hf/{hfid}/repo/edit/{a_repo.first().id}/')
    else:
        return redirect(f'http://{request.get_host()}/hf/{hfid}/repo/create/')


@login_required
def repo_create(request:HttpRequest, hfid:int) -> HttpResponse:
    return render(request, "repo_editor.html", {        
        'hfid': hfid 
        })


@login_required
def repo_editor(request:HttpRequest, hfid:int, repoid:int) -> HttpResponse:
    a_hf = Hf.objects.filter(id=hfid).first()
    return render(request, "repo_editor.html", {
        'hf': a_hf,
        'repoid': repoid,
    })

