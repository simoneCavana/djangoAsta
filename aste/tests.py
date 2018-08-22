# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from .models import Asta
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# Create your tests here.

# testing Asta model
class AstaModelTests(TestCase):
    def test_getState_with_ended_auction(self):
        time = timezone.now() - datetime.timedelta(days=30)
        ended_auction = Asta(data_inizio=time)
        self.assertEqual(ended_auction.getState(), 0)

    def test_getState_with_running_auction(self):
        time = timezone.now()
        running_auction = Asta(data_inizio=time)
        self.assertEqual(running_auction.getState(), 1)

    def test_getState_with_future_auction(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_auction = Asta(data_inizio=time)
        self.assertEqual(future_auction.getState(), 2)

    def test_descrizione_max_length(self):
        asta = Asta(descrizione='testing')
        max_length = asta._meta.get_field('descrizione').max_length
        self.assertEqual(max_length, 200)

# testing Asta view with setup method
class AstaViewTests(TestCase):
    def setUp(self):
        u = User.objects.create(username='prova', email='ciccio@pippo.net', password='qwerty')
        for auctions_id in range(1,12):
            Asta.objects.create(
                descrizione = 'obj' + str(auctions_id),
                data_inizio = timezone.now(),
                prezzo = auctions_id,
                added_by = u,
            )

    def test_pagination_is_five(self):
        response = self.client.get(reverse('aste:indice'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['latest_auctions_list']) == 5)

    def test_detail_view_success_status_code(self):
        url = reverse('aste:dettagli', kwargs={'asta_id' : 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_not_found_status_code(self):
        url = reverse('aste:dettagli', kwargs={'asta_id' : 51})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

# testing Asta view without auctions
class AstaViewTestsNoAuctions(TestCase):
    def test_index_view_with_no_auctions(self):
        """
        If no auctions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('aste:indice'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Non sono disponibili aste.")
        self.assertQuerysetEqual(response.context['latest_auctions_list'], [])
