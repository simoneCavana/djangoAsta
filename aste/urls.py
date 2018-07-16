from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /aste/
    url(r'^$', views.IndiceView.as_view(), name='indice'),
    # ex: /aste/5/
    url(r'^(?P<asta_id>[0-9]+)/$', views.dettagli, name='dettagli'),
    # ex: /aste/sendmail
    url(r'^sendmail/$', views.send_mail, name='send_mail'),
    # ex: /aste/creaAsta
    url(r'^crea/$', views.creaAsta, name='creaAsta'),

]
