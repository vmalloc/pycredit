#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime

import logbook
import requests
from bs4 import BeautifulSoup

from urlobject import URLObject

from .core import Card, Charge
from .importer import Importer

_logger = logbook.Logger(__name__)

_LEUMI_URL = URLObject('https://online.leumi-card.co.il')


class LeumiCardImporter(Importer):

    def __init__(self, auth):
        super(LeumiCardImporter, self).__init__()
        self._auth = auth
        self._session = requests.Session()

    def fetch(self):
        self._login()
        returned = []
        for link in self._fetch_print_links():
            _logger.debug('Found print link: {}', link)
            page = self._fetch_charge_page(link)
            page = BeautifulSoup(page, 'html.parser')
            for c in self._parse_charges(page):
                returned.append(c)

        return returned

    def _login(self):
        _logger.debug('Fetching login page')
        username, password = self._auth
        login = self._session.post(_LEUMI_URL.add_path(
            '/Anonymous/Login/CardHoldersLogin.aspx'), data={'username': username, 'password': password})
        login.raise_for_status()
        _logger.debug('Login success')

    def _fetch_print_links(self):
        page = self._session.get(_LEUMI_URL.add_path('/Registred/Transactions/ChargesDeals.aspx')).content.decode('utf-8')
        soup = BeautifulSoup(page, "html.parser")
        for credit_details in soup.find_all('div', {'class': 'jobResults creditCard_results'}):
            for charge_table in credit_details.find_all('table', {'class': 'NotPaddingTable'}):
                for download_link in charge_table.find_all('a', {'class': 'printLink'}):
                    yield _LEUMI_URL + download_link.attrs['href']

    def _fetch_charge_page(self, print_page_link):
        return self._session.get(print_page_link).content.decode('utf-8')

    def _parse_charges(self, page):
        card = self._parse_card(page)
        table = page.find('table', {'class': 'NotPaddingTable'})
        for tr in table.find_all('tr', recursive=False):
            if tr.find('th') is not None:
                continue
            if 'display: none' in tr.attrs.get('style', ''):
                continue
            if set(tr.attrs.get('class', [])) & {'creditTotal', 'jobsBottom'}:
                continue
            cells = tr.find_all('td', recursive=False)
            charge_date = _parse_date(cells[2].getText())
            charge_amount = _parse_sum(cells[6].getText())
            payment_string = cells[7].getText().strip()
            if u'תשלום' in payment_string:
                _logger.debug('Analyzing payment {}', payment_string.split())
                _, payment_number, _, payments, *_ = payment_string.split()
                payment_number = int(payment_number)
                payments = int(payments)
            else:
                payment_number = payments = None

            business_name = cells[3].getText().strip()
            charge = Charge(
                payee=business_name,
                card=card,
                date=_parse_date(cells[1].getText().strip()),
                charge_date=charge_date,
                num_payments = payments,
                payment_number = payment_number,
                amount=charge_amount)
            yield charge



    def _parse_card(self, page):
        ul = page.find('ul', {'class': 'creditCard_name'})
        assert ul
        card_id = ul.find('li').nextSibling.getText().split('(')[1].split(')')[0]
        return Card(card_id)

def _parse_date(s):
    s = s.strip()
    d, m, y = [int(x) for x in s.split('/')]
    return datetime.date(day=d, month=m, year=y)

def _parse_sum(s):
    return float(s.replace(',', ''))

