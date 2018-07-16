# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Asta
from django.core.urlresolvers import reverse
# Create your tests here.

# testing Asta model, getState method
class AstaMethodTests(TestCase):
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

# testing Asta view, get_queryset method
class AstaViewTests(TestCase):
    def test_index_view_with_no_auctions(self):
        """
        If no auctions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('aste:indice'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Non sono disponibili aste.")
        self.assertQuerysetEqual(response.context['latest_auctions_list'], [])
