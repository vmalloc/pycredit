Overview
========

pycredit is a Python library for fetching and parsing credit card statements from various credit card services.

Usage
=====

```python

from pycredit.il_leumi_card import LeumiCardImporter

importer = LeumiCardImporter((username, password))
for charge in importer.fetch()
	print('Paid', charge.amount, 'to', charge.payee, 'on', charge.date)

Supported Providers
===================

* LeumiCard (Israel)

Licence
=======

BSD3

