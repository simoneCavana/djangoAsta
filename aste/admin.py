# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Asta, Puntata

class PuntataInline(admin.StackedInline):
    model = Puntata
    readonly_fields = ('utente', 'somma', 'data_puntata')
    can_delete = False
    def has_add_permission(self, request):
         return False

class AstaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['descrizione']}),
        (None,               {'fields': ['data_inizio']}),
	    # opzione collapse
	    ('Foto',             {'fields': ['foto'], 'classes': ['collapse']}),
        (None,               {'fields': ['prezzo']}),
        (None,               {'fields': ['added_by']}),
    ]
    readonly_fields = ('added_by',)
    list_display = ('descrizione', 'data_inizio', 'prezzo')
    list_filter = ['data_inizio']
    search_fields = ['descrizione']
    date_hierarchy = 'data_inizio'
    inlines = [PuntataInline]
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'added_by', None) is None:
            obj.added_by = request.user
        obj.last_modified_by = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(AstaAdmin, self).get_queryset(request)
        # If super-user, show all comments
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(added_by=request.user)

class PuntataAdmin(admin.ModelAdmin):
    list_display = ('asta', 'utente', 'somma', 'data_puntata')
    readonly_fields = ('asta', 'utente', 'somma', 'data_puntata')

    # Remove the delete Admin Action for this Model
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super(PuntataAdmin, self).get_queryset(request)
        # If super-user, show all comments
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(utente=request.user)

admin.site.register(Asta, AstaAdmin)
admin.site.register(Puntata, PuntataAdmin)
