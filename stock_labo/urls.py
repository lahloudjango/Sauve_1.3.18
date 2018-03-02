# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django
if django.VERSION[:2] == (1,4):
	from django.conf.urls.defaults import patterns, url, include
elif django.VERSION[:2] < (1,8):
	from django.conf.urls import patterns, url, include
else:
	from django.conf.urls import url, include
	def patterns(a,*u):
		return [z for z in u]

import views

urlpatterns = patterns("",
	url(r"^$", views.nomenclature, name="nomenclature"),

	url(r"^nomenclature/$", views.nomenclature, name="nomenclature"),
	url(r"^nomenclature_edit/$", views.nomenclature_edit, name="nomenclature_edit"),
	url(r"^nomenclature_edit2/$", views.nomenclature_edit2, name="nomenclature_edit2"),
	url(r"^nomenclature_edit3/$", views.nomenclature_edit3, name="nomenclature_edit3"),
	url(r"^nomenclature_edit4/$", views.nomenclature_edit4, name="nomenclature_edit4"),
	url(r"^nomenclature_edit5/$", views.nomenclature_edit5, name="nomenclature_edit5"),
	url(r"^nomenclature_etiquette_print/$", views.nomenclature_etiquette_print, name="nomenclature_etiquette_print"),
	url(r"^nomenclature_lot_edit/$", views.nomenclature_lot_edit, name="nomenclature_lot_edit"),
	url(r"^nomenclature_lot_etiquette_print/$", views.nomenclature_lot_etiquette_print, name="nomenclature_lot_etiquette_print"),
	url(r"^nomenclature_contenant_edit/$", views.nomenclature_contenant_edit, name="nomenclature_contenant_edit"),
	url(r"^nomenclature_contenant_panier/$", views.nomenclature_contenant_panier, name="nomenclature_contenant_panier"),
	url(r"^nomenclature_contenant_etiquette_print/$", views.nomenclature_contenant_etiquette_print, name="nomenclature_contenant_etiquette_print"),
	url(r"^nomenclature_nettoyage/$", views.nettoyage, name="nomenclature_nettoyage"),

	url(r"^mouvement/$", views.mouvement, name="mouvement"),

	url(r"^panier/$", views.panier, name="panier"),
	url(r"^panier_contenant_edit/$", views.panier_contenant_edit, name="panier_contenant_edit"),
	url(r"^panier_contenant_panier/$", views.panier_contenant_panier, name="panier_contenant_panier"),

	url(r"^stock_perso/$", views.stock_perso, name="stock_perso"),
	url(r"^stock_perso_contenant_edit/$", views.stock_perso_contenant_edit, name="stock_perso_contenant_edit"),
	url(r"^stock_perso_contenant_panier/$", views.stock_perso_contenant_panier, name="stock_perso_contenant_panier"),


	url(r"^param_utilisateur/$", views.param_utilisateur, name="param_utilisateur"),

	url(r"^entree/$", views.entree, name="import"),

	url(r"^recherche/$", views.recherche, name="recherche"),
	url(r"^recherche_contenant_etiquette_print/$", views.recherche_contenant_etiquette_print, name="recherche_contenant_etiquette_print"),

	url(r"^reception/$", views.reception, name="reception"),

	url(r"^sample_lab/$", views.sample_lab, name="sample_lab"),
	url(r"^ajax_sample_lab_projet/$", views.ajax_sample_lab_projet, name="ajax_sample_lab_projet"),
	url(r"^ajax_sample_lab_client/$", views.ajax_sample_lab_client, name="ajax_sample_lab_client"),
	url(r"^ajax_sample_lab_client_ka/$", views.ajax_sample_lab_client_ka, name="ajax_sample_lab_client_ka"),

	url(r"^flash/$", views.flash, name="flash"),

	url(r"^log/$", views.log, name="log"),

	url(r"^ajax_etiquette/$", views.ajax_etiquette, name="ajax_ajax_etiquette"),

	#url(r"^brython/$", views.brython, name="brython"),
	#url(r"^brython/ajax_brython/$", views.ajax_brython, name="ajax_brython"),

	#url(r'^admin/', include(admin.site.urls)),

	#url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


	#url(r'^login/$', views.login, name='login'),
	)



