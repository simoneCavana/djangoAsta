# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

# setto l'email dell'utente obbligatoria
User._meta.get_field('email').blank = False

class Asta(models.Model):
    descrizione = models.CharField(max_length=200, help_text='Obbligatorio.')
    data_inizio = models.DateTimeField('data e ora di inizio', help_text='Obbligatorio.')
    foto = models.ImageField(default='default.png', help_text='Obbligatorio.')
    prezzo = models.FloatField(help_text='Obbligatorio.', validators=[MinValueValidator(0.1)])
    added_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    class Meta:
        permissions = ( ('can_bid', 'Can Bid Auctions'), )
    def __str__(self):
        return self.descrizione
    def getState(self):
        if self.getClosingTime() < timezone.now():
            # l'asta è già finita
            return 0;
        elif self.data_inizio > timezone.now():
            # l'asta deve ancora iniziare
            return 2;
        else:
            # l'asta si sta svolgendo ora
            return 1;
    def getClosingTime(self):
        # durata dell'asta espressa in secondi
        DURATA_ASTA = 120
        return self.data_inizio + datetime.timedelta(0,DURATA_ASTA)

class Puntata(models.Model):
    asta = models.ForeignKey(
        Asta,
        on_delete=models.CASCADE,
    )
    utente = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    somma = models.FloatField()
    data_puntata = models.DateTimeField('data e ora puntata')
    def __str__(self):
            return str(self.somma) + " " + str(self.data_puntata)
