# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms


class ScanCBForm(forms.Form):
	cb = forms.Field(label="Scan CB ", required = False)
	cb.widget.attrs.update({"autofocus" : "autofocus"})
	cb.widget.attrs.update({"size" : "25"})
	cb.widget.attrs.update({"style" : "font-size: 100%;"})

class ScanCBPistoletForm(forms.Form):
	cb = forms.Field(label="Scan CB ", help_text="0=Menu - 99=Logoff", required = False)
	cb.widget.attrs.update({"autofocus" : "autofocus"})
	cb.widget.attrs.update({"size" : "25"})
	cb.widget.attrs.update({"style" : "font-size: 100%;"})
	cb.widget.attrs.update({"placeholder" : "Scan ici"})

class MenuSelectForm(forms.Form):
	menu = forms.Field(label="Choix", required = False)
	menu.widget.attrs.update({"size" : "1"})
	menu.widget.attrs.update({"style" : "font-size: 75%;"})

	menu.widget.attrs.update({"autofocus" : "autofocus"})
