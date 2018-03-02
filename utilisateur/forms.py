# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from stock_labo.models import *


class UserLoginForm(forms.Form):
	username = forms.CharField(label='Utilisateur :')
	username.widget.attrs.update({"size" : "10"})
	username.widget.attrs.update({"style" : "font-size: 100%;"})
	password = forms.CharField(label='Mot de passe :', widget = forms.PasswordInput)
	password.widget.attrs.update({"size" : "10"})
	password.widget.attrs.update({"style" : "font-size: 100%;"})

	username.widget.attrs.update({'autofocus' : 'autofocus'})

class UserPasswordChangeForm(forms.Form):
	password = forms.CharField(label='Mot de passe :', widget = forms.PasswordInput)
	password.widget.attrs.update({"size" : "10"})
	password.widget.attrs.update({"style" : "font-size: 100%;"})
	password1 = forms.CharField(label='Mot de passe :', widget = forms.PasswordInput)
	password1.widget.attrs.update({"size" : "10"})
	password1.widget.attrs.update({"style" : "font-size: 100%;"})

	password.widget.attrs.update({'autofocus' : 'autofocus'})

class UserChangeForm(forms.Form):
	username = forms.CharField(label='Utilisateur :')
	username.widget.attrs.update({"size" : "10"})
	username.widget.attrs.update({"style" : "font-size: 100%;"})
	email = forms.EmailField(label='Email :', required=False)
	email.widget.attrs.update({"size" : "30"})
	email.widget.attrs.update({"style" : "font-size: 100%;"})
	first_name = forms.CharField(label='Prénom :', required=False)
	first_name.widget.attrs.update({"size" : "15"})
	first_name.widget.attrs.update({"style" : "font-size: 100%;"})
	last_name = forms.CharField(label='Nom :', required=False)
	last_name.widget.attrs.update({"size" : "15"})
	last_name.widget.attrs.update({"style" : "font-size: 100%;"})

	unit_masse = forms.ChoiceField(choices=[], label="Unitée d'affichage :")
	unit_masse.widget.attrs.update({"size" : "1"})
	unit_masse.widget.attrs.update({"style" : "font-size: 100%;"})
	site_perso = forms.ChoiceField(choices=[], label="Site personnel :")
	site_perso.widget.attrs.update({"size" : "1"})
	site_perso.widget.attrs.update({"style" : "font-size: 100%;"})
	entrepot_perso = forms.ChoiceField(choices=[], label="Entrepôt personnel :")
	entrepot_perso.widget.attrs.update({"size" : "1"})
	entrepot_perso.widget.attrs.update({"style" : "font-size: 100%;"})
	magasin_perso = forms.ChoiceField(choices=[], label="Magasin personnel :")
	magasin_perso.widget.attrs.update({"size" : "1"})
	magasin_perso.widget.attrs.update({"style" : "font-size: 100%;"})
	emplacement_perso = forms.CharField(label="Emplacement perso", required=False)
	emplacement_perso.widget.attrs.update({"size" : "15"})
	emplacement_perso.widget.attrs.update({"style" : "font-size: 100%;"})
	etiquette_contenant = forms.ChoiceField(choices=[], label="Etiquette contenants :")
	etiquette_contenant.widget.attrs.update({"size" : "1"})
	etiquette_contenant.widget.attrs.update({"style" : "font-size: 100%;"})
	etiquette_lot = forms.ChoiceField(choices=[], label="Etiquette lots :")
	etiquette_lot.widget.attrs.update({"size" : "1"})
	etiquette_lot.widget.attrs.update({"style" : "font-size: 100%;"})
	etiquette_nomenclature = forms.ChoiceField(choices=[], label="Etiquette Article :")
	etiquette_nomenclature.widget.attrs.update({"size" : "1"})
	etiquette_nomenclature.widget.attrs.update({"style" : "font-size: 100%;"})
	etiquette_login = forms.ChoiceField(choices=[], label="Badge de login :")
	etiquette_login.widget.attrs.update({"size" : "1"})
	etiquette_login.widget.attrs.update({"style" : "font-size: 100%;"})
	etiquette_emplacement = forms.ChoiceField(choices=[], label="Etiquette emplacement :")
	etiquette_emplacement.widget.attrs.update({"size" : "1"})
	etiquette_emplacement.widget.attrs.update({"style" : "font-size: 100%;"})

	username.widget.attrs.update({'autofocus' : 'autofocus'})
	def __init__(self, *args, **kwargs):
		super(UserChangeForm, self).__init__(*args, **kwargs)
		self.fields["unit_masse"].choices = [(p.id, unicode(p)) for p in UnitMasse.objects.all()]
		self.fields["site_perso"].choices = [(p.id, unicode(p)) for p in StockSite.objects.all()]
		self.fields["entrepot_perso"].choices = [(p.id, unicode(p)) for p in StockEntrepot.objects.all()]
		self.fields["magasin_perso"].choices = [(p.id, unicode(p)) for p in StockMagasin.objects.all()]
		self.fields["etiquette_contenant"].choices = [(p.id, p.description) for p in Impression.objects.all()]
		self.fields["etiquette_lot"].choices = [(p.id, p.description) for p in Impression.objects.all()]
		self.fields["etiquette_nomenclature"].choices = [(p.id, p.description) for p in Impression.objects.all()]
		self.fields["etiquette_login"].choices = [(p.id, p.description) for p in Impression.objects.all()]
		self.fields["etiquette_emplacement"].choices = [(p.id, p.description) for p in Impression.objects.all()]
