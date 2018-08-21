# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.views import generic
from django.utils import timezone
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Max, Min
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Asta, Puntata

# Create your views here.

class IndiceView(generic.ListView):
    template_name = 'aste/indice.html'
    context_object_name = 'latest_auctions_list'
    paginate_by = 5

    def get_queryset(self):
        # seleziona solo gli elementi da request.get che iniziano con 'data_inizio' e
        # trasformo i value da stringhe a funzioni
        filtro_data = {k: eval(v) for k,v in self.request.GET.items() if k.startswith('data_inizio') and v.startswith('timezone.')}
        # creo un Q object
        q_objects = Q()
        # metto in OR i vari filtri
        for key, value in filtro_data.items():
            q_objects.add(Q(**{key: value}), Q.OR)

        # prende il valore per il prezzo e lo splitta in due, prima e dopo '-'
        try:
            filtro_prezzo = (self.request.GET.get('prezzo')).split('-')
        except AttributeError:
            filtro_prezzo = [0, (Asta.objects.all().aggregate(Max('prezzo')))['prezzo__max']]

        return Asta.objects.filter(q_objects,
            prezzo__range=(filtro_prezzo[0], filtro_prezzo[1])
        ).order_by('-data_inizio')

# two different behaviour based on the request (get or post)
def dettagli(request, asta_id):
    if request.method == 'GET':
        asta = get_object_or_404(Asta, pk=asta_id)
        return render(request, 'aste/dettagli.html', {'asta': asta})
    if request.method == 'POST':
        if request.user.is_authenticated():
            # and request.user.has_perm('Asta.can_bid')
            asta = get_object_or_404(Asta, pk=asta_id)
            u = get_object_or_404(User, pk=request.user.id)
            # controllo che l'asta sia in corso e che l'utente che rilancia non sia quello che l'ha creata
            if asta.getState() == 1 and asta.added_by != u:

                pun = Puntata()
                pun.asta = asta
                pun.utente = u
                pun.somma = asta.prezzo + 0.25
                pun.data_puntata = timezone.now()
                pun.save()

                asta.prezzo = pun.somma
                asta.save()
                return render(request, 'aste/dettagli.html', {'asta': asta})
            else:
                return HttpResponseServerError("Utente creatore dell'asta non può rilanciare")
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

@login_required
def send_mail(request):
    if request.method == 'POST':
        asta = get_object_or_404(Asta, pk=request.POST.get("asta_id"))
        u = get_object_or_404(User, pk=request.user.id)
        if asta.getState() == 2:
            msg="L'asta " + str(asta.descrizione) + " inizerà il " + str(asta.data_inizio) + ". \nPronto a vincere?"
            email = EmailMessage('Promemoria asta', msg, to=[u.email])
            email.send(fail_silently=False)
            return HttpResponseRedirect('/aste')
        else:
            return HttpResponseServerError("Bad request")

@staff_member_required
def creaAsta(request):
    return HttpResponseRedirect('/admin/aste/asta/add/')
