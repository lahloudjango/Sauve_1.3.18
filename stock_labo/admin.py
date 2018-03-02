# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.contrib import admin
from models import *

#class ProductRequestAdmin(admin.ModelAdmin):
#	list_display = ("code", "nom", "date_mise_a_dispo", "colored_date_mise_a_dispo")


#admin.site.register(StatusContainer)
#admin.site.register(TypeIngredient)
#admin.site.register(AtelierDemandeur)
#admin.site.register(StatusDemande)
#admin.site.register(ProductRequest, ProductRequestAdmin)


class FlashPointMachineAdmin(admin.ModelAdmin):
	"""
	https://django.readthedocs.org/en/1.2.X/ref/contrib/admin
	"""
	raw_id_fields = ("nomenclature_lot", ) 								#Menu déroulant en champ id avec loupe de recherche

class ContenantAdmin(admin.ModelAdmin):
	"""
	https://django.readthedocs.org/en/1.2.X/ref/contrib/admin
	"""
#	class Media:
#		css = {"all": ("my_styles.css", ) }
#		js = ("my_code.js", )
#	list_display = ("code", "nom", "date_mise_a_dispo", "colored_date_mise_a_dispo")
	list_display = ("__unicode__", "date_creation", "date_suppression")
	list_display_links = list_display
	date_hierarchy  = "date_creation" 									# list horizontale
	list_filter = ("date_creation", "date_suppression", ) 				# liste verticale
	search_fields = ("code", ) 											# ^ = startswhith, = = = , @ = containe(default)
	save_on_top = True
	save_on_bottom = True
	list_per_page = 100
	ordering = ("code", )
	actions = ["suppression"]
	def suppression(modeladmin, request, queryset):
#		rows_updated = queryset.update(date_suppression = datetime.date.today(), responsable_suppression = request.user)
#		
#		rows_updated = queryset.update(status='p')
		if rows_updated == 1:
			self.message_user(request, "1 contenant NON supprimé déclaration de suppression(), suppression_parent()")
		else:
			self.message_user(request, "%s contenants supprimés" %(rows_updated))
	suppression.short_description = "Suppression (date de suppression)"

#	Formalaire de modufication
#	radio_fields = {"type_contenant": admin.VERTICAL} 					#Menu déroulant en colonne boutom_radio
#	radio_fields = {"type_contenant": admin.HORIZONTAL} 				#Menu déroulant en list boutom_radio
	raw_id_fields = ("nomenclature_lot", ) 								#Menu déroulant en champ id avec loupe de recherche
#	readonly_fields = ("nomenclature_lot", ) 							# afficher en bas de page sauf si on ajoute un ordre d'affichage
#	save_as = True

class NomenclatureLotAdmin(admin.ModelAdmin):
	list_display = ("__unicode__", "date_creation", "date_suppression")
	list_display_links = list_display
	date_hierarchy  = "date_creation" 									# list horizontale
	list_filter = ("date_creation", "date_suppression", ) 				# liste verticale
	search_fields = ("code", ) 											# ^ = startswhith, = = = , @ = containe(default)
	save_on_top = True
	save_on_bottom = True
	list_per_page = 100
	ordering = ("code", )

#	Formalaire de modufication
	raw_id_fields = ("nomenclature", ) 								#Menu déroulant en champ id avec loupe de recherche

class ContenantTypeAdmin(admin.ModelAdmin):
	list_display = ("code", "description", "capacite", )
	list_display_links = list_display
	ordering = ("capacite", )

class ImpressionDetailAdmin(admin.ModelAdmin):
	list_display = ("impression", "description", "__unicode__", )
	list_display_links = list_display
	search_fields = ("description", "impression__description", ) 		# ^ = startswhith, = = = , @ = containe(default)
#	save_on_top = True
#	save_on_bottom = True
	list_per_page = 100
	ordering = ("impression__id", "description", )

class ImpressionImprimanteAdmin(admin.ModelAdmin):
	list_display = ("description", "imprimante_port",)
	list_display_links = list_display

class ImpressionAdmin(admin.ModelAdmin):
	list_display = ("description", "etiquette_format", "imp_auto", )
	list_display_links = list_display

class NomenclatureLotIngredientDosageAdmin(admin.ModelAdmin):
#	Formalaire de modufication
	raw_id_fields = ("nomenclature_lot_ingredient", ) 								#Menu déroulant en champ id avec loup de recherche

class NomenclatureLotIngredientAdmin(admin.ModelAdmin):
#	Formalaire de modufication
	raw_id_fields = ("formule", "ingredient", ) 								#Menu déroulant en champ id avec loup de recherche

class NomenclatureAdmin(admin.ModelAdmin):
	list_display = ("code", "description", "__unicode__", )
	list_display_links = list_display
	search_fields = ("code", ) 											# ^ = startswhith, = = = , @ = containe(default)
	date_hierarchy  = "date_creation" 									# list horizontale
	list_filter = ("date_creation", "date_suppression", ) 				# liste verticale

class UserPreferenceAdmin(admin.ModelAdmin):
	list_display = ("initial", "__unicode__",)
	list_display_links = list_display

class ContenantStatAdmin(admin.ModelAdmin):
	list_display = ("contenant_code", "contenant_date_creation", "contenant_date_suppression", "contenant_responsable_suppression_login", "nomenclature_code", "nomenclature_lot_code")
	date_hierarchy  = "contenant_date_creation" 									# list horizontale
	list_display_links = list_display
	list_filter = ("contenant_date_creation", "contenant_date_suppression", ) 				# liste verticale
	search_fields = ("contenant_code", "contenant_responsable_suppression_login", ) 											# ^ = startswhith, = = = , @ = containe(default)

class NomenclatureLotStatAdmin(admin.ModelAdmin):
	list_display = ("code", "nomenclature_code", "date_creation", "responsable_creation_login")
	date_hierarchy  = "date_creation" 									# list horizontale
	list_display_links = list_display
	list_filter = ("date_creation", "responsable_creation_login", ) 				# liste verticale
	search_fields = ("code", ) 											# ^ = startswhith, = = = , @ = containe(default)

class ImpressionImprimanteParamDetailAdmin(admin.ModelAdmin):
	list_display = ("impression_imprimante_param", "description", )
	list_display_links = list_display
	search_fields = ("description", "impression_imprimante_param", ) 											# ^ = startswhith, = = = , @ = containe(default)

admin.site.register(ContenantType, ContenantTypeAdmin)
admin.site.register(Contenant, ContenantAdmin)
admin.site.register(Impression, ImpressionAdmin)
admin.site.register(ImpressionImprimante, ImpressionImprimanteAdmin)
admin.site.register(ImpressionDetail, ImpressionDetailAdmin)
admin.site.register(ImpressionImprimanteParam)
admin.site.register(ImpressionImprimanteParamDetail, ImpressionImprimanteParamDetailAdmin)
admin.site.register(NomenclatureType)
admin.site.register(Nomenclature, NomenclatureAdmin)
admin.site.register(NomenclatureLot, NomenclatureLotAdmin)
admin.site.register(NomenclatureLotIngredient, NomenclatureLotIngredientAdmin)
admin.site.register(NomenclatureLotIngredientDosage, NomenclatureLotIngredientDosageAdmin)
admin.site.register(NomenclatureLotStat, NomenclatureLotStatAdmin)
#admin.site.register(Log)
admin.site.register(SampleLabStat)
admin.site.register(StockSite)
admin.site.register(StockEntrepot)
admin.site.register(StockMagasin)
admin.site.register(SiteEntrepotMagasin)
admin.site.register(UnitMasse)
admin.site.register(UserPreference, UserPreferenceAdmin)
admin.site.register(ContenantStat, ContenantStatAdmin)
admin.site.register(OracleClient)
admin.site.register(FlashPointHist)
admin.site.register(FlashPointMachine, FlashPointMachineAdmin)


