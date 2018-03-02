# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class droits_fonctions(models.Model):
	class Meta:
		permissions = (
			("article", "Article"),
			("article_nettoyage", "Article Nettoyage"),
			("recherche", "Recherche"),
			("mouvement", "Mouvement"),
			("panier", "Panier"),
			("stock_perso", "Stock de travail"),
			("param_perso", "Mes Paramètres"),
			("import", "Import"),
			("reception", "Réception"),
			("sample_lab", "Sample Lab"),
			("flash", "Point Éclair"),
			("log", "Log"),
		)
 
