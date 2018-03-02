# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django import forms
from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext_lazy as _
#from django.contrib.admin.widgets import AdminDateWidget

from fonction import *
from models import *

#from stock_labo.models_stock import StockSite, StockEntrepot, StockMagasin, SiteEntrepotMagasin
#from stock_labo.models_contenant import ContenantStat, ContenantType, Contenant
#from models_nomenclature import NomenclatureLotStat, NomenclatureType, Nomenclature, NomenclatureLot, NomenclatureLotIngredient, NomenclatureLotIngredientDosage
#from stock_labo.models_user import UnitMasse, UserPreference
#from stock_labo.models_etiquette import ImpressionImprimanteParam, ImpressionImprimanteParamDetail, Impression, ImpressionImprimante, ImpressionDetail
#from stock_labo.models_sample_lab import SampleLabStat

class FlashModeForm(forms.Form):
	"""
	Formulaire de filtre d'affichage stock perso sur emplacement
	"""
	mode = forms.ChoiceField(choices=[], label="Mode :", required = False)
	mode.widget.attrs.update({"onchange" : "select_onchange_mode(this)"})

class FlashModeVueForm(forms.Form):
	"""
	Formulaire selection mode
	"""
	mode = forms.ChoiceField(choices=[], label="Mode :", required = False)
	mode.widget.attrs.update({"onchange" : "select_onchange_mode(this)"})
	machine = forms.CharField(label="Code machine", required = False)
	machine.widget.attrs.update({"size" : "20"})
	machine.widget.attrs.update({ "placeholder" : machine.label})
	machine.widget.attrs.update({"onkeypress" : "if (event.keyCode==13) text_onkeypress_vue(this);"})
	machine.widget.attrs.update({"autofocus" : "autofocus"})

class FlashModeChargeForm(forms.Form):
	"""
	Formulaire flash mode chargement ( machine flash )
	"""
	mode = forms.ChoiceField(choices=[], label="Mode :", required = False)
	mode.widget.attrs.update({"onchange" : "select_onchange_mode(this)"})
	contenant = forms.CharField(label="Contenant", required = False)
	contenant.widget.attrs.update({"size" : "20"})
	contenant.widget.attrs.update({ "placeholder" : contenant.label})
	contenant.widget.attrs.update({"onkeypress" : "if (event.keyCode==13) text_onkeypress_charge(this)"})
	contenant.widget.attrs.update({"autofocus" : "autofocus"})
	empl_flash = forms.CharField(label="Empl. flash", required = False)
	empl_flash.widget.attrs.update({"size" : "20"})
	empl_flash.widget.attrs.update({ "placeholder" : empl_flash.label})
	empl_flash.widget.attrs.update({"onkeypress" : "if (event.keyCode==13) text_onkeypress_charge(this)"})

class FlashModeEnregistrementForm(forms.Form):
	"""
	Formulaire flash monde enregistrement flash
	"""
	mode = forms.ChoiceField(choices=[], label="Mode :", required = False)
	mode.widget.attrs.update({"onchange" : "select_onchange_mode(this)"})
	empl_flash = forms.CharField(label="Empl. flash", required = False)
	empl_flash.widget.attrs.update({"size" : "20"})
	empl_flash.widget.attrs.update({ "placeholder" : empl_flash.label})
	empl_flash.widget.attrs.update({"onkeypress" : "if (event.keyCode==13) text_onkeypress_charge(this)"})
	empl_flash.widget.attrs.update({"autofocus" : "autofocus"})
	flash_point = forms.CharField(label="Point Éclair", required = False, help_text="°C")
	flash_point.widget.attrs.update({"size" : "20"})
	flash_point.widget.attrs.update({ "placeholder" : flash_point.label})
	flash_point.widget.attrs.update({"onkeypress" : "if (event.keyCode==13) text_onkeypress_enregistrement(this)"})

class StockPersoFiltreForm(forms.Form):
	"""
	Formulaire de filtre d'affichage stock perso sur emplacement
	"""
	emplacement = forms.ChoiceField(choices=[], label="Emplacement :", required = False)
	emplacement.widget.attrs.update({"style" : "font-size: 120%;"})
	emplacement.widget.attrs.update({"onchange" : "select_onchange_empl(this)"})

class SampleLabForm(forms.ModelForm):
	"""
	Formulaire Sample Lab
	"""
	class Meta:
		model = SampleLabStat
		fields = "__all__"
#		exclude = ["code"]
#		exclude = ["nomenclature_lot"]

#	id_nomenclature = forms.IntegerField(label="ID nomenclature :", required=False)
	def __init__(self, *args, **kwargs):
		super(SampleLabForm, self).__init__(*args, **kwargs)
		self.fields["projet"].widget.attrs["autocomplete"] = "off"
		self.fields["projet"].widget.attrs["list"] = "id_projet_list"
		self.fields["client"].widget.attrs["autocomplete"] = "off"
		self.fields["client"].widget.attrs["list"] = "id_client_list"
		self.fields["client_ka"].widget.attrs["autocomplete"] = "off"
		self.fields["client_ka"].widget.attrs["list"] = "id_client_ka_list"
		self.fields["projet"].widget.attrs["size"] = "30"
		self.fields["client"].widget.attrs["size"] = "30"
		self.fields["client_ka"].widget.attrs["size"] = "30"
#		self.fields["client"].validators=[self.validate_client,]
#		self.fields["client"].error_messages={"inconnu": "Aucun résultat pour ce critère", "multiple": "Résultat multiple pour ce critère"}
#		self.fields["client"].widget.attrs.update({ "placeholder" : "recherche automatique"})
#		self.fields["client_ka"].widget.attrs.update({ "placeholder" : "recherche automatique"})
#		self.fields["code"].widget = forms.HiddenInput()
#		self.fields["code"].widget.attrs["readonly"] = True

class RechercheFichierArticleForm(forms.Form):
	"""
	Recherche fichier article
	"""
	code = forms.CharField(label="Code contenant", required = False)
	code.widget.attrs.update({"size" : "12"})
	code.widget.attrs.update({ "placeholder" : code.label})

	code.widget.attrs.update({"autofocus" : "autofocus"})

class RechercheLogForm(forms.Form):
	"""
	Formulaire de recherche de log
	"""
	contenant_code = forms.CharField(label="Code contenant", required = False)
	contenant_code.widget.attrs.update({"size" : "12"})
	contenant_code.widget.attrs.update({ "placeholder" : contenant_code.label})
	nomenclature_lot_code = forms.CharField(label="Code Lot", required = False)
	nomenclature_lot_code.widget.attrs.update({"size" : "12"})
	nomenclature_lot_code.widget.attrs.update({ "placeholder" : nomenclature_lot_code.label})
	nomenclature_code = forms.CharField(label="Code Article", required = False)
	nomenclature_code.widget.attrs.update({"size" : "12"})
	nomenclature_code.widget.attrs.update({ "placeholder" : nomenclature_code.label})
	nomenclature_description = forms.CharField(label="Description", required = False)
	nomenclature_description.widget.attrs.update({"size" : "20"})
	nomenclature_description.widget.attrs.update({ "placeholder" : nomenclature_description.label})
	limit_du = forms.CharField(label="Du ", required = False)
	limit_du.widget.attrs.update({"size" : "2"})
	limit_du.widget.attrs.update({"style" : "font-size: 75%;"})
#	limit_du.widget.attrs["readonly"] = True
#	limit_du.widget = forms.HiddenInput()
	limit_au = forms.CharField(label="au ", required = False)
	limit_au.widget.attrs.update({"size" : "3"})
	limit_au.widget.attrs.update({"style" : "font-size: 75%;"})
#	limit_au.widget.attrs["readonly"] = True
#	limit_au.widget = forms.HiddenInput()

	contenant_code.widget.attrs.update({"autofocus" : "autofocus"})

class NbrContenantForm(forms.Form):
	"""
	Formulaire concentré roxane champ nombre contenant
	"""
	contenant_type1 = forms.ChoiceField(choices=[], label="Contenant type 1:", required = False)
	contenant_nombre1 = forms.IntegerField(label="Nombre de contenants type 1:", required = False)
	contenant_nombre1.widget.attrs.update({ "placeholder" : "nbr contenants type 1"})
	contenant_nombre1.widget.attrs.update({"size" : "12"})
	contenant_type2 = forms.ChoiceField(choices=[], label="Contenant type 2:", required = False)
	contenant_nombre2 = forms.IntegerField(label="Nombre de contenants type 2:", required = False)
	contenant_nombre2.widget.attrs.update({ "placeholder" : "nbr contenants type 2"})
	contenant_nombre2.widget.attrs.update({"size" : "12"})
	contenant_type3 = forms.ChoiceField(choices=[], label="Contenant type 2:", required = False)
	contenant_nombre3 = forms.IntegerField(label="Nombre de contenants type 2:", required = False)
	contenant_nombre3.widget.attrs.update({ "placeholder" : "nbr contenants type 2"})
	contenant_nombre3.widget.attrs.update({"size" : "12"})
	contenant_type4 = forms.ChoiceField(choices=[], label="Contenant type 2:", required = False)
	contenant_nombre4 = forms.IntegerField(label="Nombre de contenants type 2:", required = False)
	contenant_nombre4.widget.attrs.update({ "placeholder" : "nbr contenants type 2"})
	contenant_nombre4.widget.attrs.update({"size" : "12"})
	def __init__(self, *args, **kwargs):
		super(NbrContenantForm, self).__init__(*args, **kwargs)
		self.fields["contenant_type1"].choices = [(p.id, unicode(p)) for p in ContenantType.objects.all()]
		self.fields["contenant_type2"].choices = [(p.id, unicode(p)) for p in ContenantType.objects.all()]
		self.fields["contenant_type3"].choices = [(p.id, unicode(p)) for p in ContenantType.objects.all()]
		self.fields["contenant_type4"].choices = [(p.id, unicode(p)) for p in ContenantType.objects.all()]

class NomenclatureForm4(forms.Form):
	"""
	Formulaire de création formule roxane
	"""
	nomenclature_type = forms.ChoiceField(choices=[], label="Type d'article :", required = True)
	nomenclature_code = forms.CharField(label="Code :", required = True)
	nomenclature_description = forms.CharField(label="Description article :", required = False)
	nomenclature_commentaire = forms.CharField(label="Commentaire article :", required = False, widget=forms.Textarea)
	nomenclature_duree_validite = forms.CharField(label="Durée de validité :", required = False)
	nomenclature_lot_poids_reference = forms.FloatField(label="Poids de référence :", required = True, help_text="g")
	nomenclature_lot_code = forms.CharField(label="Code lot :", required = True)
	nomenclature_lot_commentaire = forms.CharField(label="Commentaire lot :", required = False, widget=forms.Textarea)
	nomenclature_lot_projet = forms.CharField(label="Projet :", required = False)
	nomenclature_lot_client = forms.CharField(label="Client :", required = False)
	nomenclature_lot_client.widget.attrs.update({ "placeholder" : "recherche automatique"})
	nomenclature_lot_client_ka = forms.CharField(label="Client KA :", required = False)
	nomenclature_lot_client_ka.widget.attrs.update({ "placeholder" : "recherche automatique"})
	nomenclature_lot_roxane = forms.CharField(label="N° Roxane :", required = True)
	nomenclature_lot_roxane_robot = forms.CharField(label="Nbr dosage robot :", required = True)
	nomenclature_lot_roxane_robot.widget.attrs.update({"min" : "0"})
	nomenclature_lot_roxane_manuel = forms.CharField(label="Nbr dasage manuel :", required = True)
	nomenclature_lot_roxane_manuel.widget.attrs.update({"min" : "0"})
	nomenclature_site_entrepot_magasin = forms.ChoiceField(choices=[], label="Emplacement de stockage :", required = False)
	contenant_date_creation = forms.CharField(label="Date de création :", required = False)
	contenant_provenance_site = forms.ChoiceField(choices=[], label="Site de fabrication :", required = True)

	nomenclature_description.widget.attrs.update({"autofocus" : "autofocus"})

	def __init__(self, *args, **kwargs):
		super(NomenclatureForm4, self).__init__(*args, **kwargs)
		self.fields["nomenclature_commentaire"].widget.attrs["rows"] = 2
		self.fields["nomenclature_commentaire"].widget.attrs["cols"] = 50
		self.fields["nomenclature_lot_commentaire"].widget.attrs["rows"] = 2
		self.fields["nomenclature_lot_commentaire"].widget.attrs["cols"] = 50
		self.fields["nomenclature_type"].choices = [(p.id, unicode(p)) for p in NomenclatureType.objects.all()]
		self.fields["nomenclature_site_entrepot_magasin"].choices = [(p.id, p.nom_court()) for p in SiteEntrepotMagasin.objects.all()]
		self.fields["contenant_provenance_site"].choices = [(p.id, unicode(p)) for p in StockSite.objects.all()]

class NomenclatureForm3(forms.Form):
	"""
	Formulaire de création serie/coupage en un
	"""
	nomenclature_type = forms.ChoiceField(choices=[], label="Type d'article :", required = True)
	nomenclature_code_barre = forms.CharField(label="Code barre :", required = False)
	nomenclature_code_barre.widget.attrs.update({ "placeholder" : "Code barre contenant model"})
	nomenclature_code = forms.CharField(label="Code :", required = False)
	nomenclature_description = forms.CharField(label="Description article :", required = False)
	nomenclature_commentaire = forms.CharField(label="Commentaire article :", required = False, widget=forms.Textarea)
	nomenclature_duree_validite = forms.CharField(label="Durée de validité :", required = False)
	nomenclature_lot_poids_reference = forms.FloatField(label="Poids de référence :", required = True, help_text="g")
	nomenclature_lot_code = forms.CharField(label="Code lot :", required = True)
	nomenclature_lot_commentaire = forms.CharField(label="Commentaire lot :", required = False, widget=forms.Textarea)
	nomenclature_lot_projet = forms.CharField(label="Projet :", required = False)
	nomenclature_lot_client = forms.CharField(label="Client :", required = False)
	nomenclature_lot_client.widget.attrs.update({ "placeholder" : "recherche automatique"})
	nomenclature_lot_client_ka = forms.CharField(label="Client KA :", required = False)
	nomenclature_lot_client_ka.widget.attrs.update({ "placeholder" : "recherche automatique"})
	nomenclature_lot_roxane_manuel = forms.IntegerField(label="Nbr de lignes manuel :", required = True)
	nomenclature_lot_roxane_manuel.widget.attrs.update({"min" : "0"})
	nomenclature_site_entrepot_magasin = forms.ChoiceField(choices=[], label="Emplacement de stockage :", required = False)
	contenant_date_creation = forms.CharField(label="Date de création :", required = False)
	contenant_provenance_site = forms.ChoiceField(choices=[], label="Site de fabrication :", required = True)
	contenant_type1 = forms.ChoiceField(choices=[], label="Contenant type 1:", required = False)
	contenant_nombre1 = forms.IntegerField(label="Nombre de contenants type 1:", required = False)
	contenant_nombre1.widget.attrs.update({ "placeholder" : "nbr contenants type 1"})
	contenant_nombre1.widget.attrs.update({"size" : "12"})
	contenant_type2 = forms.ChoiceField(choices=[], label="Contenant type 2:", required = False)
	contenant_nombre2 = forms.IntegerField(label="Nombre de contenants type 2:", required = False)
	contenant_nombre2.widget.attrs.update({ "placeholder" : "nbr contenants type 2"})
	contenant_nombre2.widget.attrs.update({"size" : "12"})
	
	def __init__(self, *args, **kwargs):
		super(NomenclatureForm3, self).__init__(*args, **kwargs)
		self.fields["nomenclature_commentaire"].widget.attrs["rows"] = 2
		self.fields["nomenclature_commentaire"].widget.attrs["cols"] = 50
		self.fields["nomenclature_lot_commentaire"].widget.attrs["rows"] = 2
		self.fields["nomenclature_lot_commentaire"].widget.attrs["cols"] = 50
		self.fields["nomenclature_lot_client"].widget.attrs["readonly"] = True
		self.fields["nomenclature_lot_client_ka"].widget.attrs["readonly"] = True
		self.fields["nomenclature_type"].choices = [(p.id, unicode(p)) for p in NomenclatureType.objects.all()]
		self.fields["nomenclature_site_entrepot_magasin"].choices = [(p.id, p.nom_court()) for p in SiteEntrepotMagasin.objects.all()]
		self.fields["contenant_provenance_site"].choices = [(p.id, unicode(p)) for p in StockSite.objects.all()]
		self.fields["contenant_type1"].choices = [(p.id, unicode(p)) for p in ContenantType.objects.all()]
		self.fields["contenant_type2"].choices = [(p.id, unicode(p)) for p in ContenantType.objects.all()]

class NomenclatureForm2(forms.Form):
	"""
	Formulaire de création article/lot/contenant en un
	"""
	nomenclature_type = forms.ChoiceField(choices=[], label="Type d'article :", required = True)
	nomenclature_code = forms.CharField(label="Code :", required = False)
	nomenclature_description = forms.CharField(label="Description article :", required = False)
	nomenclature_commentaire = forms.CharField(label="Commentaire article :", required = False, widget=forms.Textarea)
	nomenclature_duree_validite = forms.CharField(label="Durée de validité :", required = False)
	nomenclature_lot_poids_reference = forms.FloatField(label="Poids de référence :", required = True, help_text="g")
	nomenclature_lot_code = forms.CharField(label="Code lot :", required = True)
	nomenclature_lot_commentaire = forms.CharField(label="Commentaire lot :", required = False, widget=forms.Textarea)
	nomenclature_lot_projet = forms.CharField(label="Projet :", required = False)
	nomenclature_lot_client = forms.CharField(label="Client :", required = False)
	nomenclature_lot_client.widget.attrs.update({ "placeholder" : "recherche automatique"})
	nomenclature_lot_client_ka = forms.CharField(label="Client KA :", required = False)
	nomenclature_lot_client_ka.widget.attrs.update({ "placeholder" : "recherche automatique"})
	nomenclature_site_entrepot_magasin = forms.ChoiceField(choices=[], label="Emplacement de stockage :", required = False)
	contenant_date_creation = forms.CharField(label="Date de création :", required = False)
	contenant_provenance_site = forms.ChoiceField(choices=[], label="Site de fabrication :", required = True)
	contenant_type1 = forms.ChoiceField(choices=[], label="Contenant type 1:", required = False)
	contenant_nombre1 = forms.IntegerField(label="Nombre de contenants type 1:", required = False)
	contenant_nombre1.widget.attrs.update({ "placeholder" : "nbr contenants type 1"})
	contenant_nombre1.widget.attrs.update({"size" : "12"})
	contenant_type2 = forms.ChoiceField(choices=[], label="Contenant type 2:", required = False)
	contenant_nombre2 = forms.IntegerField(label="Nombre de contenants type 2:", required = False)
	contenant_nombre2.widget.attrs.update({ "placeholder" : "nbr contenants type 2"})
	contenant_nombre2.widget.attrs.update({"size" : "12"})
	contenant_type3 = forms.ChoiceField(choices=[], label="Contenant type 3:", required = False)
	contenant_nombre3 = forms.IntegerField(label="Nombre de contenants type 3:", required = False)
	contenant_nombre3.widget.attrs.update({ "placeholder" : "nbr contenants type 3"})
	contenant_nombre3.widget.attrs.update({"size" : "12"})
	def __init__(self, *args, **kwargs):
		super(NomenclatureForm2, self).__init__(*args, **kwargs)
		self.fields["nomenclature_commentaire"].widget.attrs["rows"] = 2
		self.fields["nomenclature_commentaire"].widget.attrs["cols"] = 50
		self.fields["nomenclature_lot_commentaire"].widget.attrs["rows"] = 2
		self.fields["nomenclature_lot_commentaire"].widget.attrs["cols"] = 50
#		self.fields["nomenclature_lot_client"].widget.attrs["readonly"] = True
#		self.fields["nomenclature_lot_client_ka"].widget.attrs["readonly"] = True
		self.fields["nomenclature_type"].choices = [(p.id, unicode(p)) for p in NomenclatureType.objects.all()]
		self.fields["nomenclature_site_entrepot_magasin"].choices = [(p.id, p.nom_court()) for p in SiteEntrepotMagasin.objects.all()]
		self.fields["contenant_provenance_site"].choices = [(p.id, unicode(p)) for p in StockSite.objects.all()]
		self.fields["contenant_type1"].choices = [(p.id, unicode(p)) for p in ContenantType.objects.all()]
		self.fields["contenant_type2"].choices = [(p.id, unicode(p)) for p in ContenantType.objects.all()]
		self.fields["contenant_type3"].choices = [(p.id, unicode(p)) for p in ContenantType.objects.all()]

class ReceptionForm(forms.Form):
	"""
	Formulaire le réception des contenants
	"""
	contenant = forms.CharField(label="Code barre :", required = False)
	contenant.widget.attrs.update({"size" : "15"})
	site = forms.ChoiceField(choices=[], label="Site :")
	site.widget.attrs.update({"size" : "1"})
	entrepot = forms.ChoiceField(choices=[], label="Stock :")
	entrepot.widget.attrs.update({"size" : "1"})
	magasin = forms.ChoiceField(choices=[], label="Magasin :")
	magasin.widget.attrs.update({"size" : "1"})
	emplacement = forms.CharField(label="Emplacement :", required=False)
	emplacement.widget.attrs.update({"size" : "15"})
	#emplacement.widget = forms.HiddenInput()
	contenant_type = forms.ChoiceField(choices=[], label="Contenant type :")
	contenant_type.widget.attrs.update({"size" : "1"})
#	reception_d = forms.BooleanField(label="Empl. de réception :", help_text="Mettre à jour l'emplacement de réception avec cette emplacement")
	reception_d = forms.BooleanField(label="Empl. de réception :", required = False)
	reception_d.widget.attrs.update({"style" : "height: 1.5em; width: 1.5em;"})
	def __init__(self, *args, **kwargs):
		super(ReceptionForm, self).__init__(*args, **kwargs)
		self.fields["contenant_type"].choices = [(p.id, p.description) for p in ContenantType.objects.all()]
		self.fields["site"].choices = [(p.id, unicode(p)) for p in StockSite.objects.all()]
		self.fields["entrepot"].choices = [(p.id, unicode(p)) for p in StockEntrepot.objects.all()]
		self.fields["magasin"].choices = [(p.id, unicode(p)) for p in StockMagasin.objects.all()]

class RechercheContenantForm(forms.Form):
	"""
	Formulaire du module recherche de recherche de contenant
	"""
	unite_stock = forms.CharField(label="Code barre", required = False)
	unite_stock.widget.attrs.update({"size" : "12"})
	unite_stock.widget.attrs.update({ "placeholder" : unite_stock.label})
	code = forms.CharField(label="Code article", required = False)
	code.widget.attrs.update({"size" : "12"})
	code.widget.attrs.update({ "placeholder" : code.label})
	description = forms.CharField(label="Description", required = False)
	description.widget.attrs.update({"size" : "20"})
	description.widget.attrs.update({ "placeholder" : description.label})
	lot = forms.CharField(label="Code lot", required = False)
	lot.widget.attrs.update({"size" : "12"})
	lot.widget.attrs.update({ "placeholder" : lot.label})
	type_nomenclature = forms.CharField(label="Type article", required = False)
	type_nomenclature.widget.attrs.update({"size" : "8"})
	type_nomenclature.widget.attrs.update({ "placeholder" : type_nomenclature.label})
	#type_contenant = forms.CharField(label="Type contenant", required = False)
	#type_contenant.widget.attrs.update({"size" : "10"})
	#type_contenant.widget.attrs.update({ "placeholder" : type_contenant.label})
	date_du = forms.CharField(label="Après le", required = False)
	date_du.widget.attrs.update({"size" : "8"})
	date_du.widget.attrs.update({ "placeholder" : date_du.label})
	date_au = forms.CharField(label="Avant le", required = False)
	date_au.widget.attrs.update({"size" : "8"})
	date_au.widget.attrs.update({ "placeholder" : date_au.label})
	#commentaire = forms.CharField(label="commentaire", required = False)
	#commentaire.widget.attrs.update({"size" : "8"})
	#commentaire.widget.attrs.update({ "placeholder" : commentaire.label})
	limit_du = forms.CharField(label="Du ", required = False)
	limit_du.widget.attrs.update({"size" : "2"})
	limit_du.widget.attrs.update({"style" : "font-size: 80%;"})
#	limit_du.widget.attrs["readonly"] = True
#	limit_du.widget = forms.HiddenInput()
	limit_au = forms.CharField(label="au ", required = False)
	limit_au.widget.attrs.update({"size" : "3"})
	limit_au.widget.attrs.update({"style" : "font-size: 80%;"})
#	limit_au.widget.attrs["readonly"] = True
#	limit_au.widget = forms.HiddenInput()
	collection = forms.BooleanField(label="Articles collection :", help_text="Afficher les articles enregistrés collection", required = False)
	collection.widget.attrs.update({"style" : "height: 1.2em; width: 1.2em;"})
	sup = forms.BooleanField(label="Articles Supp. :", help_text="Afficher les articles supprimés", required = False)
	sup.widget.attrs.update({"style" : "height: 1.2em; width: 1.2em;"})

	#code.widget.attrs.update({"autofocus" : "autofocus"})
	unite_stock.widget.attrs.update({"autofocus" : "autofocus"})

class MouvementForm(forms.Form):
	"""
	Formulaire le déplacement des contenants
	"""
	site = forms.ChoiceField(choices=[], label="Site :")
	site.widget.attrs.update({"size" : "1"})
	entrepot = forms.ChoiceField(choices=[], label="Stock :")
	entrepot.widget.attrs.update({"size" : "1"})
	magasin = forms.ChoiceField(choices=[], label="Magasin :")
	magasin.widget.attrs.update({"size" : "1"})
	emplacement = forms.CharField(label="Emplacement :", required=False)
	emplacement.widget.attrs.update({"size" : "15"})
	#emplacement.widget = forms.HiddenInput()
#	stock_d = forms.BooleanField(label="Empl. de stockage :", help_text="Définir cet emplacement comme emplacement par défaut")
	stock_d = forms.BooleanField(label="Empl. de stockage :", required = False)
	stock_d.widget.attrs.update({"style" : "height: 1.5em; width: 1.5em;"})
#	reception_d = forms.BooleanField(label="Empl. de réception :", help_text="Définir cet emplacement comme emplacement de réception")
	reception_d = forms.BooleanField(label="Empl. de stockage par défaut :", required = False)
	reception_d.widget.attrs.update({"style" : "height: 1.5em; width: 1.5em;"})
	def __init__(self, *args, **kwargs):
		super(MouvementForm, self).__init__(*args, **kwargs)
		self.fields["site"].choices = [(p.id, unicode(p)) for p in StockSite.objects.all()]
		self.fields["entrepot"].choices = [(p.id, unicode(p)) for p in StockEntrepot.objects.all()]
		self.fields["magasin"].choices = [(p.id, unicode(p)) for p in StockMagasin.objects.all()]

class UserParamChangeForm(forms.Form):
	"""
	Formulaire pour le changement des préférences utilisateur
	"""
	first_name = forms.CharField(label="Prénom", required=False)
	first_name.widget.attrs.update({"size" : "15"})
	last_name = forms.CharField(label="Nom", required=False)
	last_name.widget.attrs.update({"size" : "15"})
	email = forms.EmailField(label="Email", required=False)
	email.widget.attrs.update({"size" : "30"})
	unit_masse = forms.ChoiceField(choices=[], label="Unité")
	unit_masse.widget.attrs.update({"size" : "1"})
	site_perso = forms.ChoiceField(choices=[], label="Site personnel")
	site_perso.widget.attrs.update({"size" : "1"})
	entrepot_perso = forms.ChoiceField(choices=[], label="Stock personnel")
	entrepot_perso.widget.attrs.update({"size" : "1"})
	magasin_perso = forms.ChoiceField(choices=[], label="Magasin personnel")
	magasin_perso.widget.attrs.update({"size" : "1"})
	emplacement_perso = forms.CharField(label="Emplacement perso", required=False)
	emplacement_perso.widget.attrs.update({"size" : "15"})
	etiquette_contenant = forms.ChoiceField(choices=[], label="Etiquette contenant")
	etiquette_contenant.widget.attrs.update({"size" : "1"})
	etiquette_contenant_imprimante = forms.ChoiceField(choices=[], label="Imprimante etiquette contenant")
	etiquette_contenant_imprimante.widget.attrs.update({"size" : "1"})
	etiquette_lot = forms.ChoiceField(choices=[], label="Etiquette lot")
	etiquette_lot.widget.attrs.update({"size" : "1"})
	etiquette_lot_imprimante = forms.ChoiceField(choices=[], label="Imprimante etiquette lot")
	etiquette_lot_imprimante.widget.attrs.update({"size" : "1"})
	etiquette_nomenclature = forms.ChoiceField(choices=[], label="Etiquette Article")
	etiquette_nomenclature.widget.attrs.update({"size" : "1"})
	etiquette_nomenclature_imprimante = forms.ChoiceField(choices=[], label="Imprimante etiquette Article")
	etiquette_nomenclature_imprimante.widget.attrs.update({"size" : "1"})
	etiquette_login = forms.ChoiceField(choices=[], label="Badge de login")
	etiquette_login.widget.attrs.update({"size" : "1"})
	etiquette_login_imprimante = forms.ChoiceField(choices=[], label="Imprimante badge de login")
	etiquette_login_imprimante.widget.attrs.update({"size" : "1"})
	etiquette_emplacement = forms.ChoiceField(choices=[], label="Etiquette emplacement")
	etiquette_emplacement.widget.attrs.update({"size" : "1"})
	etiquette_emplacement_imprimante = forms.ChoiceField(choices=[], label="Imprimante etiquette emplacement")
	etiquette_emplacement_imprimante.widget.attrs.update({"size" : "1"})
	etiquette_emplacement_machine_flash = forms.ChoiceField(choices=[], label="Etiquette empl. machine flash")
	etiquette_emplacement_machine_flash.widget.attrs.update({"size" : "1"})
	etiquette_emplacement_machine_flash_imprimante = forms.ChoiceField(choices=[], label="Imprimante etiquette empl. machine flash")
	etiquette_emplacement_machine_flash_imprimante.widget.attrs.update({"size" : "1"})
	password = forms.EmailField(label="Password badge", required=False)
	password.widget.attrs.update({"size" : "15"})
	def __init__(self, *args, **kwargs):
		super(UserParamChangeForm, self).__init__(*args, **kwargs)
		self.fields["unit_masse"].choices = [(p.id, unicode(p)) for p in UnitMasse.objects.all()]
		self.fields["site_perso"].choices = [(p.id, unicode(p)) for p in StockSite.objects.all()]
		self.fields["entrepot_perso"].choices = [(p.id, unicode(p)) for p in StockEntrepot.objects.all()]
		self.fields["magasin_perso"].choices = [(p.id, unicode(p)) for p in StockMagasin.objects.all()]
		self.fields["etiquette_contenant"].choices = [(p.id, p) for p in Impression.objects.all()]
		self.fields["etiquette_contenant_imprimante"].choices = [(p.id, p) for p in ImpressionImprimante.objects.all()]
		self.fields["etiquette_lot"].choices = [(p.id, p) for p in Impression.objects.all()]
		self.fields["etiquette_lot_imprimante"].choices = [(p.id, p) for p in ImpressionImprimante.objects.all()]
		self.fields["etiquette_nomenclature"].choices = [(p.id, p) for p in Impression.objects.all()]
		self.fields["etiquette_nomenclature_imprimante"].choices = [(p.id, p) for p in ImpressionImprimante.objects.all()]
		self.fields["etiquette_login"].choices = [(p.id, p) for p in Impression.objects.all()]
		self.fields["etiquette_login_imprimante"].choices = [(p.id, p) for p in ImpressionImprimante.objects.all()]
		self.fields["etiquette_emplacement"].choices = [(p.id, p) for p in Impression.objects.all()]
		self.fields["etiquette_emplacement_imprimante"].choices = [(p.id, p) for p in ImpressionImprimante.objects.all()]
		self.fields["etiquette_emplacement_machine_flash"].choices = [(p.id, p) for p in Impression.objects.all()]
		self.fields["etiquette_emplacement_machine_flash_imprimante"].choices = [(p.id, p) for p in ImpressionImprimante.objects.all()]

class NomenclatureForm(forms.ModelForm):
	"""
	Formulaire édition d'Articles/Formules/Essais/Ingrédients
	"""
	class Meta:
		model = Nomenclature
		fields = "__all__"

	id_nomenclature = forms.IntegerField(label="Nomenclature :", required=False)
	def __init__(self, *args, **kwargs):
		super(NomenclatureForm, self).__init__(*args, **kwargs)
		self.fields["id_nomenclature"].widget = forms.HiddenInput()
		self.fields["id_nomenclature"].widget.attrs["readonly"] = True
		self.fields["description"].widget.attrs["size"] = 50
		self.fields["commentaire"].widget.attrs["rows"] = 2
		self.fields["commentaire"].widget.attrs["cols"] = 50
		self.fields["date_creation"].widget.attrs["placeholder"] = "JJ/MM/AAAA"
		self.fields["date_suppression"].widget.attrs["placeholder"] = "JJ/MM/AAAA"
		self.fields["reception_emplacement"].widget = forms.HiddenInput()
		self.fields["collection"].widget = forms.HiddenInput()
#		self.fields["description"].widget.attrs["style"] = "font-size: 100%;"
#		self.fields["definition"].widget = forms.HiddenInput()
#		self.fields["id_nomenclature"].widget = forms.HiddenInput()

class NomenclatureLotForm(forms.ModelForm):
	"""
	Formulaire édition de lots
	"""
	class Meta:
		model = NomenclatureLot
		fields = "__all__"
#		exclude = ["definition"]
#		exclude = ["nomenclature"]

	id_nomenclature = forms.IntegerField(label="Nomenclature :", required=False)
	id_nomenclature_lot = forms.IntegerField(label="Lot :", required=False)
	def __init__(self, *args, **kwargs):
		super(NomenclatureLotForm, self).__init__(*args, **kwargs)
#		self.fields["definition"].widget = forms.HiddenInput()
		self.fields["definition"].widget = forms.HiddenInput()
		self.fields["definition"].widget.attrs["readonly"] = True
		self.fields["nomenclature"].widget = forms.HiddenInput()
		self.fields["nomenclature"].widget.attrs["readonly"] = True
		self.fields["client"].widget.attrs["placeholder"] = "recherche automatique"
		self.fields["client_ka"].widget.attrs["placeholder"] = "recherche automatique"
		self.fields["id_nomenclature"].widget = forms.HiddenInput()
		self.fields["id_nomenclature"].widget.attrs["readonly"] = True
		self.fields["id_nomenclature_lot"].widget = forms.HiddenInput()
		self.fields["id_nomenclature_lot"].widget.attrs["readonly"] = True
		self.fields["date_creation"].widget.attrs["placeholder"] = "JJ/MM/AAAA"
		self.fields["date_fin_validite"].widget.attrs["placeholder"] = "JJ/MM/AAAA"
		self.fields["date_suppression"].widget.attrs["placeholder"] = "JJ/MM/AAAA"
		self.fields["commentaire"].widget.attrs["rows"] = 2
		self.fields["commentaire"].widget.attrs["cols"] = 44
#		self.fields["nomenclature"].widget = forms.HiddenInput()
#		self.fields["nomenclature"].widget.attrs["readonly"] = True

class ContenantForm(forms.ModelForm):
	"""
	Formulaire édition contenants
	"""
	class Meta:
		model = Contenant
		fields = "__all__"
#		exclude = ["code"]
#		exclude = ["nomenclature_lot"]

	id_nomenclature = forms.IntegerField(label="ID nomenclature :", required=False)
	id_nomenclature_lot = forms.IntegerField(label="ID lot :", required=False)
	id_contenant = forms.IntegerField(label="ID contenant :", required=False)
	def __init__(self, *args, **kwargs):
		super(ContenantForm, self).__init__(*args, **kwargs)
		self.fields["code"].widget = forms.HiddenInput()
		self.fields["code"].widget.attrs["readonly"] = True
		self.fields["nomenclature_lot"].widget = forms.HiddenInput()
		self.fields["nomenclature_lot"].widget.attrs["readonly"] = True
		self.fields["id_nomenclature"].widget = forms.HiddenInput()
		self.fields["id_nomenclature"].widget.attrs["readonly"] = True
		self.fields["id_nomenclature_lot"].widget = forms.HiddenInput()
		self.fields["id_nomenclature_lot"].widget.attrs["readonly"] = True
		self.fields["id_contenant"].widget = forms.HiddenInput()
		self.fields["id_contenant"].widget.attrs["readonly"] = True
		self.fields["date_creation"].widget.attrs["placeholder"] = "JJ/MM/AAAA"
		self.fields["date_reception"].widget.attrs["placeholder"] = "JJ/MM/AAAA"
		self.fields["date_suppression"].widget.attrs["placeholder"] = "JJ/MM/AAAA"
		self.fields["date_fin_validite"].widget.attrs["placeholder"] = "JJ/MM/AAAA"
		#self.fields["actuel_emplacement"].widget = forms.HiddenInput()
		#self.fields["stock_emplacement"].widget = forms.HiddenInput()
		self.fields["tare"].widget = forms.HiddenInput()
		self.fields["poids"].widget = forms.HiddenInput()
		self.fields["seuil_alarme"].widget = forms.HiddenInput()
		self.fields["responsable_suppression"].widget.attrs["readonly"] = True
#		self.fields["responsable_suppression"].widget = forms.HiddenInput()

class FormuleImportForm(forms.Form):
	"""
	Formulaire d'import de fichiers
	"""
	TYPE_IMPORT = {
		"ing_cont": "Ingrédient Contexa",
		"f_rox_ex": "Roxane Export",
		"f_rox_imp": "Roxane Import",
		"f_cont": "Formule Contexa",
		"gen": "Import generic",
		"sap_nav": "Import fichier navette sap",
		"sol_vin": "Import fichier solution vincent",
		"collection": "Import statut collection",
		"validite": "Import duree validité",
		"article": "Import article",
		"flash" : "Import valeur flash",
		}
	FIN_DE_LIGNE = {
		"CRLF": "Fichier d'origine Windows",
		"LF": "Fichier d'origine Unix-Linux",
		"CR": "Fichier d'origine Mac",
		}
	_FIN_DE_LIGNE = {
		"CRLF": r"\r\n",
		"LF": r"\n",
		"CR": r"\r",
		}
	type_fichier = forms.ChoiceField(choices = TYPE_IMPORT.items(), required = True, label = "Format du fichier")
	type_fichier.widget.attrs.update({"size" : "8"})
	type_fichier.widget.attrs.update({"style" : "font-size: 100%;"})
	emplacement = forms.CharField(label="Dossier :", required = True)
	emplacement.widget.attrs.update({"size" : "60"})
	emplacement.widget.attrs.update({"style" : "font-size: 100%;"})
	code = forms.CharField(label="Code / Nom :", required = True)
	code.widget.attrs.update({"size" : "25"})
	code.widget.attrs.update({"style" : "font-size: 100%;"})
	extention = forms.CharField(label="Extention fichier :", required = True)
	extention.widget.attrs.update({"size" : "5"})
	extention.widget.attrs.update({"style" : "font-size: 100%;"})
	fin_de_ligne = forms.ChoiceField(choices = FIN_DE_LIGNE.items(), required = True, label = "Format du fichier")
	fin_de_ligne.widget.attrs.update({"size" : "3"})
	fin_de_ligne.widget.attrs.update({"style" : "font-size: 100%;"})
#	username.widget.attrs.update({"autofocus" : "autofocus"})

class RechercheNomenclatureForm(forms.Form):
	"""
	Formulaire module article du filtre de recherche d'Articles/Formules/Essais/Ingrédients
	"""
	code = forms.CharField(label="Code", required = False)
	code.widget.attrs.update({"size" : "8"})
	code.widget.attrs.update({"style" : "font-size: 100%;"})
	code.widget.attrs.update({ "placeholder" : code.label})
	description = forms.CharField(label="Description", required = False)
	description.widget.attrs.update({"size" : "20"})
	description.widget.attrs.update({"style" : "font-size: 100%;"})
	description.widget.attrs.update({ "placeholder" : description.label})
	type_nomenclature = forms.CharField(label="Type", required = False)
	type_nomenclature.widget.attrs.update({"size" : "5"})
	type_nomenclature.widget.attrs.update({"style" : "font-size: 100%;"})
	type_nomenclature.widget.attrs.update({ "placeholder" : type_nomenclature.label})
	date_du = forms.CharField(label="Après le", required = False)
	date_du.widget.attrs.update({"size" : "10"})
	date_du.widget.attrs.update({"style" : "font-size: 100%;"})
	date_du.widget.attrs.update({ "placeholder" : date_du.label})
	date_au = forms.CharField(label="Avant le", required = False)
	date_au.widget.attrs.update({"size" : "10"})
	date_au.widget.attrs.update({"style" : "font-size: 100%;"})
	date_au.widget.attrs.update({ "placeholder" : date_au.label})
	commentaire = forms.CharField(label="commentaire", required = False)
	commentaire.widget.attrs.update({"size" : "8"})
	commentaire.widget.attrs.update({ "placeholder" : commentaire.label})
	limit_du = forms.CharField(label="Du ", required = False)
	limit_du.widget.attrs.update({"size" : "2"})
	limit_du.widget.attrs.update({"style" : "font-size: 75%;"})
#	limit_du.widget.attrs["readonly"] = True
#	limit_du.widget = forms.HiddenInput()
	limit_au = forms.CharField(label="au ", required = False)
	limit_au.widget.attrs.update({"size" : "3"})
	limit_au.widget.attrs.update({"style" : "font-size: 75%;"})
#	limit_au.widget.attrs["readonly"] = True
#	limit_au.widget = forms.HiddenInput()
	collection = forms.BooleanField(label="Articles collection :", help_text="Afficher les articles enregistrés collection", required = False)
	collection.widget.attrs.update({"style" : "height: 1.2em; width: 1.2em;"})
	sup = forms.BooleanField(label="Articles Supp. :", help_text="Afficher les articles supprimés", required = False)
	sup.widget.attrs.update({"style" : "height: 1.2em; width: 1.2em;"})

	code.widget.attrs.update({"autofocus" : "autofocus"})


