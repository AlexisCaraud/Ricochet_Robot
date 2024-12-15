from matplotlib import colors
import numpy as np
import time
from random import *
import webcolors
import colorsys
import matplotlib.pyplot as plt

from scipy.spatial import KDTree
from webcolors import (CSS3_HEX_TO_NAMES , hex_to_rgb)

def generate_distinct_colors(n):
    colors = []
    for i in range(n):
        hue = float(i) / n
        saturation = 1.0
        value = 1.0
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        colors.append(tuple(int(c * 255) for c in rgb))
    return colors

def convert_rgb_to_names(rgb_tuple):
    
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES 
    names = []
    rgb_values = []    
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)    
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]

N = 16 # taille de la grille
CENTRAL = 2 # taille de la case centrale
v=10   # précision d'affichage
NBR_ROBOT = 4  # nombre de robot
NBR_COIN = 1 # nombre de coins différents par quart de plateau
NBR_BARRE = 1 # nombre de barres verticales (et horizontales) par quart de plateau
COULEUR_ROBOT = generate_distinct_colors(NBR_ROBOT)
ROBOT = [convert_rgb_to_names(tuple) for tuple in COULEUR_ROBOT]
DIR=['haut', 'droite', 'bas', 'gauche']     # liste des déplacements


class Robot:
	def __init__(self, couleur=None, x=None, y=None, principal=False):
		self.couleur = couleur
		self.x = x
		self.y = y
		self.principal = principal	#True si c'est le robot principal

	def coord(self):
		return (self.x, self.y)

	def __repr__(self):
		return 'x:{} y:{} couleur:{}'.format(self.x, self.y, self.couleur)
	

class Objectif:
	def __init__(self,  x=None, y=None, couleur=None):
		self.couleur = couleur
		self.x = x
		self.y = y

	def coord(self):
		return (self.x, self.y)

	def __repr__(self):
		return 'x:{} y:{} couleur:{}'.format(self.x, self.y, self.couleur)

class Mur:
	def __init__(self, *args): # args: directions où le mur est présent
		self.haut = False
		self.bas = False
		self.droite = False
		self.gauche = False
		for arg in args:
			if arg == 'droite':
				self.droite = True
			elif arg == 'gauche':
				self.gauche = True
			elif arg == 'haut':
				self.haut = True
			elif arg == 'bas':
				self.bas = True

	def __repr__(self):
		return 'haut:{} bas:{} gauche:{} droite:{} '.format(self.haut, self.bas, self.gauche, self.droite)

class Case:
	def __init__(self, x, y, robot, objectif, mur):
		self.x = x
		self.y = y
		self.robot = robot
		self.objectif = objectif
		self.mur = mur

	def __repr__(self):
		return 'x:{} y:{} '.format(self.x, self.y)

	def crée_mur(self, direction):
		if direction == 'haut':
			self.mur.haut = True
		elif direction == 'bas':
			self.mur.bas = True
		elif direction == 'droite':
			self.mur.droite = True
		else:
			self.mur.gauche = True


class Plateau:
	def __init__(self, taille, précision):
		self.taille = taille
		self.précision = précision
		self.robots = {couleur: Robot(couleur) for couleur in ROBOT}
		self.objectif = Objectif()
		self.tableau = [ [ Case(i, j, Robot(), Objectif(), Mur()) for i in range(self.taille)] for j in range(self.taille)]
		self.init = {}	#coordonnées initiales des robots
		self.list_coins = []

	'''REINITIALISER PLATEAU'''

	def clear(self):
		self.tableau = [ [ Case(i, j, Robot(), Objectif(), Mur()) for i in range(self.taille)] for j in range(self.taille)]
		self.list_coins = []

	'''FONCTIONS SUR LES ROBOTS'''

	def coord_init(self):
		for couleur, robot in self.robots.items():
			self.init[couleur] = robot.coord()

	def get_coord_robots(self):
		coord = {}
		for robot in self.robots:
			coord[robot] = self.robots[robot].coord()
		return coord
	
	def bouger_robot(self, couleur, x_new, y_new):
		(x_init, y_init) = self.robots[couleur].coord()
		if x_init != None and y_init != None:	#permet de placer le robot s'il n'est pas encore sur le plateau
			self.tableau[x_init][y_init].robot.couleur = None
		self.tableau[x_new][y_new].robot.couleur = couleur
		self.robots[couleur].x = x_new
		self.robots[couleur].y = y_new
		self.robots[couleur].principal = (couleur == self.objectif.couleur)

	def replacer_robots(self, list):
		for robot in self.robots:
			(x_new, y_new) = list[robot]
			self.bouger_robot(robot, x_new, y_new)

	def remove_robot(self, couleur):
		x,y = self.robots[couleur].coord()
		self.tableau[x][y].robot.couleur = None
		self.robots[couleur] = Robot(couleur=couleur)

	def dep(self, couleur, direction):
		(x,y) = self.robots[couleur].coord()
		directions = {'haut': self.dep_haut,
    				  'bas': self.dep_bas,
    				  'droite': self.dep_droite,
    				  'gauche': self.dep_gauche}
		directions[direction](couleur, x, y)

	def dep_haut(self, couleur, a, b):
		if self.tableau[a][b].mur.haut == True or self.tableau[a-1][b].robot.couleur != None:
			return
		i = 1
		while not(self.tableau[a-i][b].mur.haut==True or self.tableau[a-1-i][b].robot.couleur !=None):
			i+=1
		self.bouger_robot(couleur, a-i, b)
		
	def dep_bas(self, couleur, a, b):
		if self.tableau[a][b].mur.bas == True or self.tableau[a+1][b].robot.couleur != None:
			return
		i = 1
		while not(self.tableau[a+i][b].mur.bas==True or self.tableau[a+1+i][b].robot.couleur !=None):
			i+=1
		self.bouger_robot(couleur, a+i, b)

	def dep_droite(self, couleur, a, b):
		if self.tableau[a][b].mur.droite == True or self.tableau[a][b+1].robot.couleur != None:
			return
		i = 1
		while not(self.tableau[a][b+i].mur.droite==True or self.tableau[a][b+1+i].robot.couleur !=None):
			i+=1
		self.bouger_robot(couleur, a, b+i)

	def dep_gauche(self, couleur, a, b):
		if self.tableau[a][b].mur.gauche == True or self.tableau[a][b-1].robot.couleur != None:
			return
		i = 1
		while not(self.tableau[a][b-i].mur.gauche==True or self.tableau[a][b-1-i].robot.couleur !=None):
			i+=1
		self.bouger_robot(couleur, a, b-i)

	'''FONCTIONS SUR L'OBJECTIF'''

	def bouger_obj(self, couleur, x_new, y_new):
		x,y = self.objectif.coord()
		if x != None and y != None:		#permet de placer l'objectif s'il n'est pas encore sur le plateau
			self.tableau[x][y].objectif.couleur = None
		self.objectif = Objectif(x_new, y_new, couleur)
		self.tableau[x_new][y_new].objectif.couleur = couleur
		for robot in self.robots:
			self.robots[robot].principal = False
		self.robots[couleur].principal = True

	'''CONSTRUCTION DU PLATEAU'''

	def ajout_murs(self, direction, x, y):
		self.tableau[x][y].crée_mur(direction)
		if direction == 'haut':
			self.tableau[x-1][y].mur.bas = True
		elif direction == 'bas':
			self.tableau[x+1][y].mur.haut = True
		elif direction == 'droite':
			self.tableau[x][y+1].mur.gauche = True
		else:
			self.tableau[x][y-1].mur.droite = True
	
	def init1(self):	#place les murs sur les bords
		for i in range(self.taille):
			self.tableau[i][0].mur.gauche = True
			self.tableau[i][self.taille-1].mur.droite = True
		for j in range(self.taille):
			self.tableau[0][j].mur.haut = True
			self.tableau[self.taille-1][j].mur.bas = True

	def init2(self):	#place les murs centraux
		for i in range(self.taille//2 -1, self.taille//2 +1):
			self.ajout_murs('gauche', i, self.taille//2 -1)
			self.ajout_murs('droite', i, self.taille//2)
		for j in range(self.taille//2 -1, self.taille//2 +1):
			self.ajout_murs('haut', self.taille//2 -1, j)
			self.ajout_murs('bas', self.taille//2, j)

	def coin_b_d(self, a, b):
		self.ajout_murs('bas', a, b)
		self.ajout_murs('droite', a, b)

	def coin_h_d(self, a, b):
		self.ajout_murs('haut', a, b)
		self.ajout_murs('droite', a, b)

	def coin_b_g(self, a, b):
		self.ajout_murs('bas', a, b)
		self.ajout_murs('gauche', a, b)

	def coin_h_g(self, a, b):
		self.ajout_murs('haut', a, b)
		self.ajout_murs('gauche', a, b)

	def coint(self, a,b,c,d,e,f,g,h):
		self.coin_h_g(a,b)
		self.coin_b_d(c,d)
		self.coin_b_g(e,f)
		self.coin_h_d(g,h)

	def barre_v(self, a, b):  # b est à gauche de la barre
		self.ajout_murs('droite', a, b)

	def barrevt(self, L):
		for l in L:
			self.barre_v(l[0],l[1])

	def barre_h(self, a, b):  # a est en haut de la barre
		self.ajout_murs('bas', a, b)
			
	def barreht(self, L):
		for l in L:
			self.barre_h(l[0],l[1])



	'''FONCTIONS SUR LES DISTANCES ENTRE LES CASES'''

	def distance_obstacle_droite(self, a, b, sans_robot=False):       # renvoie la distance entre la case (a,b) et son premier ostacle vers la droite
		i = 0
		while not (self.tableau[a][b+i].mur.droite  or (self.tableau[a][b+1+i].robot.couleur != None and not sans_robot)):
			i += 1
		return i

	def distance_obstacle_gauche(self, a, b, sans_robot=False):      # renvoie la distance entre la case (a,b) et son premier ostacle vers la gauche
		i = 0
		while not (self.tableau[a][b-i].mur.gauche  or (self.tableau[a][b-1-i].robot.couleur != None and not sans_robot)):
			i += 1
		return i

	def distance_obstacle_bas(self, a, b, sans_robot=False):     # renvoie la distance entre la case (a,b) et son premier ostacle vers le bas
		i = 0
		while not (self.tableau[a+i][b].mur.bas  or (self.tableau[a+i+1][b].robot.couleur != None and not sans_robot)):
			i += 1
		return i

	def distance_obstacle_haut(self, a, b, sans_robot=False):        # renvoie la distance entre la case (a,b) et son premier ostacle vers le haut
		i = 0
		while not (self.tableau[a-i][b].mur.haut  or (self.tableau[a-i-1][b].robot.couleur != None and not sans_robot)):
			i += 1
		return i
	
	def tableau_distance(self, x, y, couleur):	#renvoie pour chaque case une liste [distance, [dep1,dep2,...]] pour que le robot 'couleur' arrive sur la case (x,y)
		n = self.taille
		(x_robot, y_robot) = self.robots[couleur].coord()
		self.remove_robot(couleur)	#on enlève le robot
		tab_dis = [[ [ [], []] for i in range(n)] for j in range(n)]
		tab_dis[x][y][0] = 0	#case départ
		compteur2 = 0
		arret  = True
		mem = [(x, y)]
		while arret:
			arret = False
			for i in range(n):
				for j in range(n):
					if tab_dis[i][j][0] == compteur2:

						d = self.distance_obstacle_droite(i, j)
						if self.tableau[i][j].mur.gauche or self.tableau[i][j-1].robot.couleur != None:
							for t in range(1, d+1):
								if (i,j+t) not in mem:
									tab_dis[i][j+t][0] = compteur2 + 1
									tab_dis[i][j+t][1] = ['gauche'] + tab_dis[i][j][1]
									mem.append((i,j+t))
									arret = True
						
						g = self.distance_obstacle_gauche(i, j)
						if self.tableau[i][j].mur.droite or self.tableau[i][j+1].robot.couleur != None:
							for t in range(1, g+1):
								if (i, j-t) not in mem:
									tab_dis[i][j-t][0] = compteur2 + 1
									tab_dis[i][j-t][1] = ['droite'] + tab_dis[i][j][1]
									mem.append((i, j-t))
									arret = True

						h = self.distance_obstacle_haut(i, j)
						if self.tableau[i][j].mur.bas or self.tableau[i+1][j].robot.couleur != None:
							for t in range(1, h+1):
								if ((i-t), j) not in mem:
									tab_dis[i-t][j][0] = compteur2 + 1
									tab_dis[i-t][j][1] = ['bas'] + tab_dis[i][j][1]
									mem.append(((i-t), j))
									arret  = True

						bas = self.distance_obstacle_bas(i, j)
						if self.tableau[i][j].mur.haut or self.tableau[i-1][j].robot.couleur != None:
							for t in range(1, bas+1):
								if ((i+t), j) not in mem:
									tab_dis[i+t][j][0] = compteur2 + 1
									tab_dis[i+t][j][1] = ['haut'] + tab_dis[i][j][1]
									mem.append(((i+t), j))
									arret = True
			compteur2 += 1
		self.bouger_robot(couleur, x_robot, y_robot)  # on remet le robot
		return tab_dis
	
	def tableau_distance_min(self, a, b): # tableau associant à chaque case la distance minimale qui la sépare de la case (a,b)
		n = self.taille
		tab_dis_min = [[ [] for i in range(n)] for j in range(n)]
		tab_dis_min[a][b] = 0
		compteur2 = 0
		mem = [(a, b)] # liste contentant toutes les cases déjà visiter
		while len(mem) <n*n - CENTRAL*CENTRAL: # on s'arrête quand on est passé sur toutes les cases (sauf les centrales)
			for i in range(n):
				for j in range(n):
					if tab_dis_min[i][j] == compteur2:

						d = self.distance_obstacle_droite(i, j, sans_robot=True)
						for t in range(1, d+1):
							if (i,j+t) not in mem:
								tab_dis_min[i][j+t] = compteur2 + 1
								mem.append((i,j+t))

						g = self.distance_obstacle_gauche(i, j, sans_robot=True)
						for t in range(1, g+1):
							if (i, j-t) not in mem:
								tab_dis_min[i][j-t] = compteur2 + 1
								mem.append((i, j-t))

						h = self.distance_obstacle_haut(i, j, sans_robot=True)
						for t in range(1, h+1):
							if ((i-t), j) not in mem:
								tab_dis_min[i-t][j] = compteur2 + 1
								mem.append(((i-t), j))

						bas = self.distance_obstacle_bas(i, j, sans_robot=True)
						for t in range(1, bas+1):
							if ((i+t), j) not in mem:
								tab_dis_min[i+t][j] = compteur2 + 1
								mem.append(((i+t), j))
			compteur2 += 1
		return tab_dis_min
	
	
	'''AFFICHAGE DU PLATEAU'''

	def affich(self):
		m = self.taille * self.précision
		a = 255 * np.ones((m, m, 3), dtype=np.uint8)
		for i in range (m):
			for j in range (m):
				if i%self.précision==0 or j%self.précision==0:
					a[i][j]=[200,200,200] # colorie le quadrillage en gris
		a[(self.taille-CENTRAL)//2*self.précision:(self.taille+CENTRAL)//2*self.précision,(self.taille-CENTRAL)//2*self.précision:(self.taille+CENTRAL)//2*self.précision]=[1,1,1] #colorie le carré central en noir
		
		if self.objectif != None:
			i, j = self.objectif.x, self.objectif.y
			for rang, robot in enumerate(ROBOT):
				if robot == self.objectif.couleur:
					a[self.précision*i+1:self.précision*i+self.précision,self.précision*j+1:self.précision*j+self.précision] = COULEUR_ROBOT[rang]		# colorie l'objectif
					a[self.précision*i+1+(self.précision//5):self.précision*i+self.précision-(self.précision//5),self.précision*j+1+(self.précision//5):self.précision*j+self.précision-(self.précision//5)] = [255,255,255]
		for rang, robot in enumerate(ROBOT):
			x,y = self.robots[robot].coord()
			a[self.précision*x+1:self.précision*x+self.précision,self.précision*y+1:self.précision*y+self.précision] = COULEUR_ROBOT[rang]

		for i in range (self.taille):
			for j in range (self.taille):
				if self.tableau[i][j].mur.haut:
					a[self.précision*i,self.précision*j:self.précision*j+self.précision,:]=0 #colorie les murs 1 en noir
				if self.tableau[i][j].mur.droite:
					a[self.précision*i:self.précision*i+self.précision,self.précision*j+self.précision-1,:]=0 #colorie les murs 2 en noir
				if self.tableau[i][j].mur.bas:
					a[self.précision*i+self.précision-1,self.précision*j:self.précision*j+self.précision,:]=0 #colorie les murs 3 en noir
				if self.tableau[i][j].mur.gauche:
					a[self.précision*i:self.précision*i+self.précision,self.précision*j,:]=0 #colorie les murs 4 en noir
		'''plt.figure(figsize=(6, 6))
		plt.imshow(a, interpolation='nearest')
		plt.axis('off')
		plt.show()'''
		return a
	
	
	'''GENERATION PLATEAU ALEATOIRE'''

	def random(self):	#crée une grille aléatoire (avec coins, barres, robots et objectif)
		self.clear()
		self.init1()
		self.init2()
		max = self.taille-1         # max = 15
		moitie = self.taille//2 - 1 # moitie = 7

		for k in range(NBR_BARRE):
			vert1, vert2, vert3, vert4, hor1, hor2, hor3, hor4 =  self.rand_barres()
			self.barrevt([[0,vert1],[0,vert2+moitie],[max,vert3],[max,vert4+moitie]]) # place les barres verticales
			self.barreht([[hor1,0],[hor2+moitie,0],[hor3,max],[hor4+moitie,max]]) # place les barres horizontales

		L = [[0,0], [0,moitie], [moitie,0], [moitie,moitie]]  # liste qui permet de placer les coins à la bonne place dans chaque quart de plateau
		for k in range(NBR_COIN):
			for t in range (4):
				x_coin1,y_coin1,x_coin2,y_coin2,x_coin3,y_coin3,x_coin4,y_coin4 = self.rand_coin(t,L, moitie)
				while (self.grille_pas_bonne(x_coin1,y_coin1,x_coin2,y_coin2,x_coin3,y_coin3,x_coin4,y_coin4)):
					x_coin1,y_coin1,x_coin2,y_coin2,x_coin3,y_coin3,x_coin4,y_coin4 = self.rand_coin(t,L, moitie)
				self.coin_b_d(x_coin1, y_coin1)
				self.coin_b_g(x_coin2, y_coin2)
				self.coin_h_d(x_coin3, y_coin3)
				self.coin_h_g(x_coin4, y_coin4)
				self.list_coins.append(Case(x_coin1, y_coin1, Robot(), Objectif(), Mur('bas', 'droite')))
				self.list_coins.append(Case(x_coin2, y_coin2, Robot(), Objectif(), Mur('bas', 'gauche')))
				self.list_coins.append(Case(x_coin3, y_coin3, Robot(), Objectif(), Mur('haut', 'droite')))
				self.list_coins.append(Case(x_coin4, y_coin4, Robot(), Objectif(), Mur('haut', 'gauche')))
		self.rand_obj()
		for robot in self.robots:       # place les robots
			x,y = randint(1, max), randint(1, max)
			while (self.tableau[x][y].robot.couleur != None or self.central(x,y)): # si la case est vide et non centrale
				x,y = randint(1, max), randint(1, max)
			self.bouger_robot(robot, x, y) #place le robot
		self.coord_init()	#stock les coordonnées initiales des robots

	def rand_barres(self):	# renvoie les coordonnées des barres verticales et horizontales (1 barre vert et hor / quart de plateau)
		nmax = (N-CENTRAL)//2 -1
		vert1, vert2, vert3, vert4, hor1, hor2, hor3, hor4=randint(1,nmax),randint(1,nmax),randint(1,nmax),randint(1,nmax),randint(1,nmax),randint(1,nmax),randint(1,nmax),randint(1,nmax)
		return vert1, vert2, vert3, vert4, hor1, hor2, hor3, hor4
	
	def rand_coin(self, t,L,moitie): # renvoie les coordonnées des 4 coins du quart de plateau
		[A,C,E,G] , [B,D,F,H] = sample([i for i in range(1,moitie)],4),sample([i for i in range(1,moitie)],4) # tire deux quadruplet de nombre différents pour avoir les 4 coordonnées des coins et qu'ils ne soient pas alignés
		return A+L[t][0],B+L[t][1],C+L[t][0],D+L[t][1],E+L[t][0],F+L[t][1],G+L[t][0],H+L[t][1] 

	def rand_obj(self):
		liste_coins = []
		for coin in self.list_coins:
			if self.objectif.x == None or (coin.x != self.objectif.x and coin.y != self.objectif.y):
				liste_coins.append([coin.x, coin.y])
		coin_choisi, couleur_obj = sample(liste_coins, 1)[0], sample(ROBOT, 1)[0]
		self.tableau[coin_choisi[0]][coin_choisi[1]].objectif.couleur = couleur_obj
		self.objectif = Objectif(coin_choisi[0], coin_choisi[1], couleur_obj)
		self.robots[couleur_obj].principal = True

	def grille_pas_bonne(self, a,b,c,d,e,f,g,h): # renvoie True si la grille n'est pas bonne, c'est à dire que les coins sont adjacents ou que les coins adjacents à un mur
		return (self.autour(a,b,c,d) or self.autour(a,b,e,f) or self.autour(a,b,g,h) or self.autour(c,d,e,f) or self.autour(c,d,g,h) or self.autour(e,f,g,h)) or (self.voisin(a,b) or self.voisin(c,d) or self.voisin(e,f) or self.voisin(g,h))

	def voisin(self,i,j):	# renvoie True si la case (i,j) a un mur adjacent
		return (self.tableau[i][j].mur.haut or self.tableau[i][j].mur.bas or self.tableau[i][j-1].mur.haut or self.tableau[i][j-1].mur.bas or self.tableau[i][j+1].mur.haut or self.tableau[i][j+1].mur.bas or self.tableau[i-1][j].mur.droite or self.tableau[i-1][j].mur.gauche or self.tableau[i+1][j].mur.droite or self.tableau[i+1][j].mur.gauche)
	
	def autour(self, x1,y1,x2,y2): # renvoie True si la case (x1,y1) est située dans les 8 cases self.autour de celle (x2,y2) (ou même case)
		return (x2>=x1-1 and x2<=x1+1) and (y2>=y1-1 and y2<=y1+1)

	def central(self, x,y):
		a, b = (N-CENTRAL)//2, (N+CENTRAL)//2
		l=[(i,j) for i in range(a,b) for j in range(a,b)]
		for k in l:
			if (x,y)==(k):
				return True
		return False

	'''RESOLUTION PLATEAU'''

	def est_resolu(self):	#renvoie True si le bon robot est sur l'objectif
		return self.objectif.coord() == self.robots[self.objectif.couleur].coord()
	
	
	'''OUVERTURE CARTE FICHER TEXTE'''	

	def open(self, name):
		self.clear()
		self.init1()
		self.init2()
		path = 'map/%s.txt' % (name)
		with open (path, 'r') as f:
			lines = f.read().splitlines()
		lines2 = [l.split(',') for l in lines]
		for l in lines2:
			i, j = int(l[1]), int(l[2])
			for rang, robot in enumerate(ROBOT):
				if l[0] == 'r%d' % (rang):
					self.bouger_robot(robot, i, j)
				if l[0] == 'o%d' % (rang):
					self.bouger_obj(robot, i, j)
			if l[0] == 'bv':
				self.barre_v(i,j)
			if l[0] == 'bh':
				self.barre_h(i,j)
			if l[0] == 'c1' or l[0] == 'c_h_d':
				self.coin_h_d(i,j)
				self.list_coins.append(Case(i, j, Robot(), Objectif(), Mur('haut', 'droite')))
			if l[0] == 'c2'or l[0] == 'c_b_d':
				self.coin_b_d(i,j)
				self.list_coins.append(Case(i, j, Robot(), Objectif(), Mur('bas', 'droite')))
			if l[0] == 'c3'or l[0] == 'c_b_g':
				self.coin_b_g(i,j)
				self.list_coins.append(Case(i, j, Robot(), Objectif(), Mur('bas', 'gauche')))
			if l[0] == 'c4'or l[0] == 'c_h_g':
				self.coin_h_g(i,j)
				self.list_coins.append(Case(i, j, Robot(), Objectif(), Mur('haut', 'gauche')))
			self.coord_init()


if __name__=='__main__':
	T = Plateau(16, 10)
	T.open('3dep')
	tab_dis = T.tableau_distance(2,2,"red")
	T.affich()