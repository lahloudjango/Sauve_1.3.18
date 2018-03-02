# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
http://linuxcnc.org/docs/html/gcode/gcode_fr.html
"""

__author__ = "Charly GONTERO"
__date__ = "2017-04-09 16:14:05"
__version__ = 1.0
__credits__ = """
 *  g_code.py
 *
 *  Copyright 2011 Charly GONTERO
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *  MA 02110-1301, USA.
"""
FIN_DE_LIGNE="\n"
VERSION = __version__
def version():
	return __version__

class G_Code(object):
	def G0(self, X, Y, Z):
		"""Interpolation linéaire en vitesse rapide"""
		return "GO X%s Y%s Z%s%s" %(X, Y, Z, FIN_DE_LIGNE)
	def G1(self, X, Y, Z):
		"""Interpolation linéaire en vitesse travail"""
		return "G1 X%s Y%s Z%s%s" %(X, Y, Z, FIN_DE_LIGNE)
	def G2(self, X, Y, Z, R=None, I=None, J=None, K=None, P=None):
		"""Interpolation circulaire en vitesse travail sens horaire
			Plan XY (G17)
				G2 ou G3 <X- Y- Z- I- J- P->
					Z - hélicoïde
					I - décalage en X
					J - décalage en Y
					P - nombre de tours
			Plan XZ (G18)
				G2 ou G3 <X- Z- Y- I- K- P->
					Y - hélicoïde
					I - décalage en X
					K - décalage en Z
					P - nombre de tours
			YZ-plane (G19)
				G2 ou G3 <Y- Z- X- J- K- P->
					X - hélicoïde
					J - décalage en Y
					K - décalage en Z
					P - nombre de tours
		"""
		x = "G2 X%s Y%s Z%s" %(X, Y, Z)
		if R != None:
			x += " R%s" %(R)
		if I != None:
			x += " I%s" %(I)
		if J != None:
			x += " J%s" %(J)
		if K != None:
			x += " K%s" %(K)
		if P != None:
			x += " P%s" %(P)
		return x + FIN_DE_LIGNE
	def G3(self, X, Y, Z, R=None, I=None, J=None, K=None):
		"""
		Interpolation circulaire en vitesse travail sens anti-horaire
			Plan XY (G17)
				G2 ou G3 <X- Y- Z- I- J- P->
					Z - hélicoïde
					I - décalage en X
					J - décalage en Y
					P - nombre de tours
			Plan XZ (G18)
				G2 ou G3 <X- Z- Y- I- K- P->
					Y - hélicoïde
					I - décalage en X
					K - décalage en Z
					P - nombre de tours
			YZ-plane (G19)
				G2 ou G3 <Y- Z- X- J- K- P->
					X - hélicoïde
					J - décalage en Y
					K - décalage en Z
					P - nombre de tours
		"""
		x = "G3 X%s Y%s Z%s" %(X, Y, Z)
		if R != None:
			x += " R%s" %(R)
		if I != None:
			x += " I%s" %(I)
		if J != None:
			x += " J%s" %(J)
		if K != None:
			x += " K%s" %(K)
		return x + FIN_DE_LIGNE
	def G4(self, P):
		"""
		Temporisation
			P - durée de la temporisation en secondes (un flottant)
		"""
		return "G4 P%s%s" %(P, FIN_DE_LIGNE)
	def G7(self): + FIN_DE_LIGNE
		"""Mode diamètre sur les tours"""
		return "G7" + FIN_DE_LIGNE
	def G8(self):
		"""Mode rayon sur les tours"""
		return "G8" + FIN_DE_LIGNE
	def G10_L1(self, P, R, X=None, Y=None, Z=None, I=None, J=None, Q=None):
		"""
		Ajustements dans la table d’outils
			P - numéro d’outil
			R - rayon de bec
			I - angle frontal (tour)
			J - angle arrière (tour)
			Q - orientation (tour)
		"""
		x "G10 L1 P%s R%s" %(P, R)
		if X != None:
			x += " X%s" %(X)
		if Y != None:
			x += " Y%s" %(Y)
		if Z != None:
			x += " Z%s" %(Z)
		if I != None:
			x += " I%s" %(I)
		if J != None:
			x += " J%s" %(J)
		if Q != None:
			x += " Q%s" %(Q)
		return x + FIN_DE_LIGNE
	def G10_L2(self, P, X=None, Y=None, Z=None, R=None):
		"""
		Établissement de l’origine d’un système de coordonnées
			P - système de coordonnées (0 à 9)
			R - rotation autour de l’axe Z
		"""
		x "G10 L2 P%s" %(P)
		if X != None:
			x += " X%s" %(X)
		if Y != None:
			x += " Y%s" %(Y)
		if Z != None:
			x += " Z%s" %(Z)
		if R != None:
			x += " R%s" %(R)
		return x + FIN_DE_LIGNE
	def G10_L10(self, P, X=None, Y=None, Z=None, R=None, I=None, J=None, Q=None):
		"""
		Modifie les offsets d’outil dans la table d’outils
			P - numéro d’outil
			R - rotation autour de l’axe Z
			I - angle frontal (tour)
			J - angle arrière (tour)
			Q - orientation (tour)
		"""
		return "G10 L10 P%s" %(P)
		if X != None:
			x += " X%s" %(X)
		if Y != None:
			x += " Y%s" %(Y)
		if Z != None:
			x += " Z%s" %(Z)
		if R != None:
			x += " R%s" %(R)
		if I != None:
			x += " I%s" %(I)
		if J != None:
			x += " J%s" %(J)
		if Q != None:
			x += " Q%s" %(Q)
		return x + FIN_DE_LIGNE
	def G10_L11(self, P, X=None, Y=None, Z=None, R=None, I=None, J=None, Q=None):
		"""
		Fixe les valeurs de l’outil dans la table d’outils
			P - numéro d’outil
			R - rotation autour de l’axe Z
			I - angle frontal (tour)
			J - angle arrière (tour)
			Q - orientation (tour)
		"""
		return "G10 L11 P%s" %(P)
		if X != None:
			x += " X%s" %(X)
		if Y != None:
			x += " Y%s" %(Y)
		if Z != None:
			x += " Z%s" %(Z)
		if R != None:
			x += " R%s" %(R)
		if I != None:
			x += " I%s" %(I)
		if J != None:
			x += " J%s" %(J)
		if Q != None:
			x += " Q%s" %(Q)
		return x + FIN_DE_LIGNE
	def G10_L20(self, P, X=None, Y=None, Z=None):
		"""
		Établissement de l’origine d’un système de coordonnées
			P - système de coordonnées (0-9)
		"""
		return "G10 L20 P%s" %(P)
		if X != None:
			x += " X%s" %(X)
		if Y != None:
			x += " Y%s" %(Y)
		if Z != None:
			x += " Z%s" %(Z)
		if R != None:
		return x + FIN_DE_LIGNE
	def G17(self):
		"""Choix du plan de travail XY"""
		return "G17" + FIN_DE_LIGNE
	def G18(self):
		"""Choix du plan de travail ZX"""
		return "G18" + FIN_DE_LIGNE
	def G19(self):
		"""Choix du plan de travail YZ"""
		return "G19" + FIN_DE_LIGNE
	def G17_1(self):
		"""Choix du plan de travail UV"""
		return "G17.1" + FIN_DE_LIGNE
	def G18_1(self):
		"""Choix du plan de travail WU"""
		return "G18.1" + FIN_DE_LIGNE
	def G19_1(self):
		"""Choix du plan de travail VW"""
		return "G19.1" + FIN_DE_LIGNE
	def G20(self):
		"""Unités machine pouce"""
		return "G20" + FIN_DE_LIGNE
	def G21(self):
		"""Unités machine mm"""
		return "G21" + FIN_DE_LIGNE
	def G28(self):
		"""Effectue un mouvement en vitesse rapide de la position courante à la position absolue enregistrée dans les paramètres 5161 à 5166"""
		return "G28" + FIN_DE_LIGNE
	def G28_1(self):
		"""Enregistre la position absolue courante dans les paramètres 5161 à 5166"""
		return "G28.1" + FIN_DE_LIGNE
	def G30(self):
		"""Effectue un mouvement en vitesse rapide de la position courante à la position absolue stockée dans les paramètres 5181 à 5186"""
		return "G30" + FIN_DE_LIGNE
	def G30_1(self):
		"""Enregistre la position absolue courante dans les paramètres 5181 à 5186"""
		return "G30.1" + FIN_DE_LIGNE
	def G33(self, X, Y, Z, K):
		"""
		Mouvement avec broche synchronisée
			K - distance par tour
		"""
		return "G33 X%s Y%s Z%s K%s%s" %(X, Y, Z, K, FIN_DE_LIGNE)
	def G33_1(self, X, Y, Z, K):
		"""
		Taraudage rigide
			K - distance par tour
		"""
		return "G33.1 X%s Y%s Z%s K%s%s" %(X, Y, Z, K, FIN_DE_LIGNE)
	def G38_2(self, X, Y, Z):
		"""Palpe vers la pièce, stoppe au toucher, signale une erreur en cas de défaut"""
		return "G38.2 X%s Y%s Z%s%s" %(X, Y, Z, FIN_DE_LIGNE)
	def G38_3(self, X, Y, Z):
		"""Palpe vers la pièce, stoppe au toucher"""
		return "G38.3 X%s Y%s Z%s%s" %(X, Y, Z, FIN_DE_LIGNE)
	def G38_4(self, X, Y, Z):
		"""Palpe en quittant la pièce, stoppe en perdant le contact, signal une erreur en cas de défaut"""
		return "G38.4 X%s Y%s Z%s%s" %(X, Y, Z, FIN_DE_LIGNE)
	def G38_5(self, X, Y, Z):
		"""Palpe en quittant la pièce, stoppe en perdant le contact"""
		return "G38.5 X%s Y%s Z%s%s" %(X, Y, Z, FIN_DE_LIGNE)
	def G40(self):
		"""Révocation de la compensation de rayon d’outil"""
		return "G40" + FIN_DE_LIGNE
	def G41(self, D=None):
		"""
		Compensation de rayon d’outil à gauche du profil
			D - Numéro d’outil
		"""
		if D == None:
			return "G41" + FIN_DE_LIGNE
		else:
			return "G41 D%s%s" %(D, FIN_DE_LIGNE)
	def G42(self, D=None):
		"""
		Compensation de rayon d’outil à droite du profil
			D - Numéro d’outil
		"""
		if D == None:
			return "G41" + FIN_DE_LIGNE
		else:
			return "G41 D%s%s" %(D, FIN_DE_LIGNE)
	def G41_1(self, D, L=None):
		"""Compensation dynamique d’outilà gauche du profil
			D - Numéro d’outil
			L - Orientation d'outil
		"""
		if L == None:
			return "G41.1 D%s%s" %(D, FIN_DE_LIGNE)
		else:
			return "G41.1 D%s L%s%s" %(D, L, FIN_DE_LIGNE)
	def G42_1(self, D, L=None):
		"""
		Compensation dynamique d’outilà droite du profil
			D - Numéro d’outil
			L - Orientation d'outil
		"""
		if L == None:
			return "G42.1 D%s%s" %(D, FIN_DE_LIGNE)
		else:
			return "G42.1 D%s L%s%s" %(D, L, FIN_DE_LIGNE)
	def G43(self, H=None):
		"""Activation de la compensation de longueur d’outil
			H - Numéro d’outil
		"""
		if H == None:
			return "G43" + FIN_DE_LIGNE
		else:
			return "G43 H%s%s" %(H, FIN_DE_LIGNE)
	def G43_1(self, X, Y, Z):
		"""Compensation dynamique de longueur d’outil"""
		return "G43.1 X%s Y%s Z%s%s" %(X, Y, Z, FIN_DE_LIGNE)
	def G49(self):
		"""Révocation de la compensation de longueur d’outil"""
		return "G49" + FIN_DE_LIGNE
	def G53(self, X, Y, Z):
		"""Mouvement en coordonnées absolues"""
		return "G53 X%s Y%s Z%s%s" %(X, Y, Z, FIN_DE_LIGNE)
	def G54(self):
		"""Choix du système de coordonnées 1"""
		return "G54" + FIN_DE_LIGNE
	def G55(self):
		"""Choix du système de coordonnées 2"""
		return "G55" + FIN_DE_LIGNE
	def G56(self):
		"""Choix du système de coordonnées 3"""
		return "G56" + FIN_DE_LIGNE
	def G57(self):
		"""Choix du système de coordonnées 4"""
		return "G57" + FIN_DE_LIGNE
	def G58(self):
		"""Choix du système de coordonnées 5"""
		return "G58" + FIN_DE_LIGNE
	def G59(self):
		"""Choix du système de coordonnées 6"""
		return "G59" + FIN_DE_LIGNE
	def G59_1(self):
		"""Choix du système de coordonnées 7"""
		return "G59.1" + FIN_DE_LIGNE
	def G59_2(self):
		"""Choix du système de coordonnées 8"""
		return "G59.2" + FIN_DE_LIGNE
	def G59_3(self):
		"""Choix du système de coordonnées 9"""
		return "G59.3" + FIN_DE_LIGNE
	def G61(self):
		"""Contrôle de trajectoire exacte"""
		return "G61" + FIN_DE_LIGNE
	def G61_1(self):
		"""Contrôle d'arrêts exacte"""
		return "G61.1" + FIN_DE_LIGNE
	def G64(self, P=None, Q=None):
		"""
		Contrôle de trajectoire continue avec tolérance
			P - Déviation maximale tolérée par rapport à la trajectoire programmée.
			Q - Tolérance naïve cam.
		"""
		return "G64"
		if P != None:
			x += " P%s" %(P)
		if Q != None:
			x += " Q%s" %(Q)
		return x + FIN_DE_LIGNE
	def G73(self, X, Y, Z, R, Q, L=None):
		"""Cycle de perçage avec brise copeaux
			R - Position du plan de retrait en Z
			Q - Incrément delta parallèle à l’axe Z
			L - Répétition
		"""
		x "G73 X%s Y%s Z%s" %(P, R)
		if L != None:
			x += " L%s" %(L)
		return x + FIN_DE_LIGNE
	def G76(self, P, Z, I, J, R, K, Q, H, E, L):
		"""Cycle de filetage préprogrammé
		Ligne pilote - La ligne pilote est une ligne imaginaire, parallèle à l’axe de la broche (Z), située en sécurité à l’extérieur du matériau à fileter. La ligne pilote va du point initial en Z jusqu'à la fin du filetage donnée par la valeur de Z dans la commande.
			P - Le pas du filet en distance de déplacement par tour.
			Z - La position finale du filetage. A la fin du cycle, l’outil sera à cette position Z.
			I - La crête du filet est une distance entre la ligne pilote et la surface de la pièce. Une valeur négative de I, indique un filetage externe et une valeur positive, indique un filetage interne. C’est généralement à ce diamètre nominal que le matériau est cylindré avant de commencer le cycle G76.
			J - Une valeur positive, spécifie la profondeur de la passe initiale. La première passe sera à J au delà de la crête du filet I.
			K - Une valeur positive, spécifie la profondeur finale du filet. La dernière passe du filetage sera à K au delà de la crête du filet I.
		Paramètres facultatifs:
			R - La profondeur de dégressivité. R1.0 spécifie une profondeur de passe constante pour les passes successives du filetage. R2.0 spécifie une surface constante. Les valeurs comprises entre 1.0 et 2.0 spécifient une profondeur décroissante mais une surface croissante. Enfin, les valeurs supérieures à 2.0 sélectionnent une surface décroissante.
			Q - L’angle de pénétration oblique. C’est l’angle (en degrés) décrivant de combien, les passes successives doivent être décalées le long de l’axe Z. C’est utilisé pour faire enlever plus de matériau d’un côté de l’outil que de l’autre. Une valeur positive de Q fait couper d’avantage le bord de l’outil. Typiquement, les valeurs sont 29, 29.5 ou 30 degrés.
			H - Le nombre de passes de finition. Les passes de finition sont des passes additionnelles en fond de filet. Pour ne pas faire de passe de finition, programmer H0.
		Les entrées et sorties de filetage peuvent être programmées coniques avec les valeurs de E et L.
			E - Spécifie la longueur des parties coniques le long de l’axe Z. L’angle du cône ira de la profondeur de la dernière passe à la crête du filet I. E2.0 donnera un cône d’entrée et de sortie d’une longueur de 2.0 unités dans le sens du filetage. Pour un cône à 45 degrés, programmer E identique à K.
			L - Spécifie quelles extrémités du filetage doivent être coniques. Programmer L0 pour aucune (par défaut), L1 pour une entrée conique, L2 pour une sortie conique, ou L3 pour l’entrée et la sortie coniques.
		Note
			En mode diamètre G7, les valeurs I, J et K sont des mesures de diamètre. En mode rayon G8, les valeurs I, J et K sont des mesures de rayon.
		Attention
			Les valeurs inutilement hautes de dégressivité, produiront un nombre inutilement important de passes. (dégressivité = plongée par paliers)
		"""
		return "G76 P%s Z%s I%s J%s R%s K%s Q%s H%s E%s L%s%s" %(P, Z, I, J, R, K, Q, H, E, L, FIN_DE_LIGNE)
	def G80(self):
		"""Révocation des codes modaux"""
		return "G80" + FIN_DE_LIGNE
	def G81(self, X, Y, Z, R, L):
		"""Cycle de perçage"""
		return "G81 X%s Y%s Z%s R%s L%s%s" %(X, Y, Z, R, L, FIN_DE_LIGNE)
	def G82(self, X, Y, Z, R, L, P):
		"""Cycle de perçage avec temporisation"""
		return "G82 X%s Y%s Z%s R%s L%s P%s%s" %(X, Y, Z, R, L, P, FIN_DE_LIGNE)
	def G83(self, X, Y, Z, R, L, Q):
		"""Cycle de perçage avec débourrage"""
		return "G83 X%s Y%s Z%s R%s L%s Q%s%s" %(X, Y, Z, R, L, Q, FIN_DE_LIGNE)
	def G84(self):
		"""Cycle de taraudage à droite"""
		return None
	def G85(self, X, Y, Z, R, L):
		"""Cycle d’alésage, sans temporisation, retrait en vitesse travail"""
		return "G85 X%s Y%s Z%s R%s L%s%s" %(X, Y, Z, R, L, FIN_DE_LIGNE)
	def G86(self, X, Y, Z, R, L, P):
		"""Cycle d’alésage, arrêt de broche, retrait en vitesse rapide"""
		return "G86 X%s Y%s Z%s R%s L%s P%s%s" %(X, Y, Z, R, L, P, FIN_DE_LIGNE)
	def G87(self):
		"""Alésage inversé"""
		return None
	def G88(self):
		"""Alésage, arrêt de broche, retrait en manuel"""
		return None
	def G89(self, X, Y, Z, R, L, P):
		"""Cycle d’alésage, temporisation, retrait en vitesse travail"""
		return "G89 X%s Y%s Z%s R%s L%s P%s%s" %(X, Y, Z, R, L, P, FIN_DE_LIGNE)
	def G90(self):
		"""Modes de déplacement absolu"""
		return "G90" + FIN_DE_LIGNE
	def G91(self):
		"""Modes de déplacement relatif"""
		return "G91" + FIN_DE_LIGNE
	def G90_1(self):
		"""Mode de déplacement en arc (I, J et K) absolu"""
		return "G90.1" + FIN_DE_LIGNE
	def G91_1(self):
		"""Mode de déplacement en arc (I, J et K) relatif"""
		return "G91.1" + FIN_DE_LIGNE
	def G92(self, X, Y, Z):
		"""Décalage d’origine des systèmes de coordonnées"""
		return "G92 X%s Y%s Z%s%s" %(X, Y, Z, FIN_DE_LIGNE)
	def G92_1(self):
		"""Remise à zéro des décalages des systèmes de coordonnées
		Positionne les décalages d’axes à 0 et passe les paramètres 5211 à 5219 à zéro"""
		return "G91.1" + FIN_DE_LIGNE
	def G92_2(self):
		"""Remise à zéro des décalages des systèmes de coordonnées
		Positionne les décalages d’axes à 0, laisse les valeurs des paramètres inchangées, elles ne seront pas utilisées"""
		return "G92.2" + FIN_DE_LIGNE
	def G92_3(self):
		"""Restauration des décalages d’axe"""
		return "G92.3" + FIN_DE_LIGNE
	def G93(self):
		"""Choix des modes de vitesse en mode inverse du temps"""
		return "G93" + FIN_DE_LIGNE
	def G94(self):
		"""Choix des modes de vitesse en mode unités par minute"""
		return "G94" + FIN_DE_LIGNE
	def G95(self):
		"""Choix des modes de vitesse en mode unités par tour"""
		return "G95" + FIN_DE_LIGNE
	def G96(self, D, S):
		"""Modes de contrôle de la broche vitesse de coupe constante
			D - Vitesse de broche maximale en tours par minute.
			S - Vitesse de coupe constante.
		"""
		return "G96 D%s S%s" %(D, S, FIN_DE_LIGNE)
	def G97(self):
		"""Modes de contrôle de la broche mode tr/mn"""
		return "G97" + FIN_DE_LIGNE
	def G98(self):
		"""Options du plan de retrait perpendiculaire au plan de travail courant jusqu'à la position qui était celle de cet axe juste avant le début du cycle de perçage"""
		return "G98" + FIN_DE_LIGNE
	def G99(self):
		"""Options du plan de retrait perpendiculaire au plan de travail courant jusqu'à la position indiquée par le mot R"""
		return "G99" + FIN_DE_LIGNE

