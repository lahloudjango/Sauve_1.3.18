# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Class de création de PDF pour étiquette
"""

from reportlab.graphics.barcode import code39, code128, qr
from reportlab.graphics.shapes import Drawing 
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.pdfbase.pdfdoc import PDFDocument
#from reportlab.platypus import Image
from svglib.svglib import svg2rlg

__author__ = "Charly GONTERO"
__date__ = "2016-01-18 22:01:56"
__version__ = 1.1
__credits__ = """
 *  etiquette_pdf.py
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

VERSION = __version__
def version():
	return __version__


class EtiquettePDF(object):
	"""
	Class de création de PDF pour étiquette
	"""
	def __init__ (self,filename, pagesize_mm=(210, 297), orientation=0):
		"""
		orientation=0 : portrait
		orientation=1 : landscape
		"""
		from reportlab.lib.pagesizes import landscape, portrait
		if orientation == 1:
			self.canvas = canvas.Canvas(filename, pagesize=landscape((pagesize_mm[0]*mm, pagesize_mm[1]*mm)))
		else:
			self.canvas = canvas.Canvas(filename, pagesize=portrait((pagesize_mm[0]*mm, pagesize_mm[1]*mm)))

	def font_size(self, font, size):
		"""
		Défini la taille et la police
		"""
		fonts = self.canvas.getAvailableFonts()
		if font in fonts:
			self.canvas.setFont(font, size)
		else:
			print fonts

	def font_color(self, R, V, B):
		"""
		Police color : R,V,B (255, 255, 255)
		"""
		self.canvas.setFillColorRGB(R/255, V/255, B/255)

	def back_ground_color(self, R, V, B):
		"""
		Défini la couleur de l"arrière plan format R,V,B (255, 255, 255)
		"""
		self.canvas.setStrokeColorRGB(R/255, V/255, B/255)

	def ligne(self, x, y, len_x, len_y):
		"""
		Dessine une ligne
		"""
		self.canvas.line(x*mm,y*mm,len_x*mm,len_y*mm)

	def carre(self, x, y, len_x, len_y, fond=0, bordure=1):
		"""
		Dessine un carré
		"""
		self.canvas.rect(x*mm, y*mm, len_x*mm, len_y*mm, stroke=bordure, fill=fond)

	def orientation(self, angle):
		"""
		Faire tourné l'orientation des axes X et Y autour de l'origine
		"""
		self.canvas.rotate(angle)

	def origin(self, x, y):
		"""
		Déplace l'origine en relatif par rapport à l'origine courante
		"""
		self.canvas.translate(x, y)

	def impression_text(self, x, y, t, alignement="L"):
		"""
		Impression d"une ligne de text
		"""
		if alignement == "L":
			self.canvas.drawString(x*mm, y*mm, t)
		if alignement == "R":
			self.canvas.drawRightString(x*mm, y*mm, t)
		if alignement == "C":
			self.canvas.drawCentredString(x*mm, y*mm, t)

	def cercle(self, cen_x, cen_y, r, fond=0, bordure=1):
		"""
		Dessine un cercle
		"""
		self.canvas.circle(cen_x*mm, cen_y*mm, r*mm, stroke=bordure, fill=fond)

	def carre_rond(self, x, y, len_x, len_y, r, fond=0, bordure=1):
		"""
		Dessine un carré avec les coins arrondi
		"""
		self.canvas.roundRect(x*mm, y*mm, len_x*mm, len_y*mm, r*mm, stroke=bordure, fill=fond)

	def image(self, x, y, image):
		"""
		
		"""
		self.canvas.drawImage(self, image, x*mm, y*mm, width=None,height=None,mask=None)

	def save_state(self):
		"""
		Sauvegarde la position du repère et l'orientation dans une pile de sauvegarde
		"""
		self.canvas.saveState()

	def restore_state(self):
		"""
		Restaure la position du repère en dépilant les sauvegardes
		"""
		self.canvas.restoreState()

	def page_next(self):
		"""
		Crée une nouvelle page
		"""
		self.canvas.showPage()

	def save(self):
		"""
		Sauvegarde la page
		"""
		self.canvas.save()

	def print_code_qr(self, x, y, text, taille=10):
		"""
		Insert un code QR
		"""
		qr_code = qr.QrCodeWidget(text)
		bounds = qr_code.getBounds()
		width = bounds[2] - bounds[0]
		height = bounds[3] - bounds[1]
		d = Drawing(taille*mm/inch, taille*mm/inch, transform=[taille*mm/inch,0,0,taille*mm/inch,0,0])
		d.add(qr_code)
		renderPDF.draw(d, self.canvas, x*mm, y*mm)

	def print_code_128(self, x, y, text, hauteur=20, largeur=1, font_size=6, human_readable=1):
		"""
		Insert un code 128
		"""
		barcode128 = code128.Code128(text, barHeight = hauteur, barWidth = largeur, fontSize = font_size, human_readable = human_readable, quiet = 0)
		barcode128.drawOn(self.canvas, x*mm, y*mm)

	def print_image_file(self, x, y, len_x, len_y, image_file):
		"""
		Insert une image .gif .bmp .png
		"""
		self.canvas.drawImage(image_file, x*mm, y*mm, width=len_x*mm, height=len_y*mm)

	def print_svg_file(self, x, y, facteur_x, facteur_y, image_file):
		"""
		Insert une image .svg
		"""
		d = Drawing(facteur_x, facteur_y, transform=[facteur_x,0,0,facteur_y,0,0])
		d.add(svg2rlg(image_file))
		renderPDF.draw(d, self.canvas, x*mm, y*mm)

	def get_pdf(self):
		"""
		Retourne la page PDF
		"""
		
		return self.canvas._doc.GetPDFData(self.canvas)



if __name__ == "__main__":
#	createBarCodes()
	etiquette = EtiquettePDF("label.pdf", pagesize_mm=(100,50), orientation=1)
	etiquette.font_color(255,0,0)
	etiquette.carre(1,1,98,48)
	etiquette.font_size("Courier", 14)
	etiquette.impression_text(70, 40, "GONTERO", "L")
	etiquette.cercle(30,15,10)
	etiquette.font_color(0,0,0)
	etiquette.save_state()
	etiquette.orientation(90)
	etiquette.print_code_128(5, -10, "00;122", hauteur=20, largeur=1, font_size=6, human_readable=1)
	etiquette.impression_text(25, -18, "Charly", "C")
	etiquette.restore_state()
	etiquette.print_code_qr(30, 32, "CharlyGONTERO;40 Impasse de Chappet;01170;CROZET;France", 10)
#	etiquette.print_image_file(23, 13, 12, 6, "/media/gonteroc/charly/charly/dev/git_tools_robots/static/logo_150.png")
#	etiquette.print_svg_file(40, 1, 0.35, 0.35, "/media/gonteroc/charly/charly/dev/git_tools_robots/static/logo_vectored.svg")
#	etiquette.print_svg_file(80, 2, 0.08, 0.08, "/media/gonteroc/charly/charly/dev/git_tools_robots/static/svg/pictogrammes sans fond/SGH08-GHS-pictogram-silhouete.svg")

	etiquette.page_next()

	etiquette.save()

