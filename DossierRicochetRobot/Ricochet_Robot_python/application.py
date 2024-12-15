import sys

import time

import os
os.system('color')

import colorama
colorama.init(convert=True, autoreset= True)

from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QProgressBar, QSpinBox, QGridLayout, 
QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QRadioButton, QHBoxLayout, QLabel, QLineEdit)
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer,QDateTime

from functools import partial


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from random import randint
import numpy as np
from plateau import *
from resolution import *


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ricochet Robot")
        self.setGeometry(100, 100, 1200, 800)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Left side: Game Area
        self.canvas = PlotCanvas(self, width=6, height=6, ex=self)
        self.layout.addWidget(self.canvas)

        # Right side: Controls
        self.control_panel = QWidget()
        self.control_layout = QVBoxLayout()
        self.control_panel.setLayout(self.control_layout)
        self.layout.addWidget(self.control_panel)

        self.time_increment = 0
        self.time_record = 0
        self.init_controls()

    def init_controls(self):
        _translate = QtCore.QCoreApplication.translate

        # Title
        title_label = QLabel("Ricochet Robot Controls")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        self.control_layout.addWidget(title_label)

        # Buttons Grid
        button_grid = QGridLayout()
        self.control_layout.addLayout(button_grid)

        self.new_map_btn = self.create_button("Nouvelle Map (c)", "c", self.canvas.begin)
        self.new_goal_btn = self.create_button("Nouvel Objectif (n)", "n", self.canvas.change)
        self.reset_btn = self.create_button("Reset (Space)", "Space", self.canvas.reset)
        self.validate_btn = self.create_button("Valider (v)", "v", self.canvas.register)
        self.load_btn = self.create_button("Ouvrir Map (o)", "o", self.canvas.ouvrir)
        self.exit_btn = self.create_button("Terminer (t)", "t", self.exit_game)
        self.previous_btn = self.create_button("Précédent (p)", "p", self.canvas.previous)
        self.modifier_carte_btn = self.create_button("Modifer Carte (m)", "m", self.canvas.modif)
        self.save_btn = self.create_button("Sauvegarder (s)", "s", self.canvas.save)

        button_grid.addWidget(self.new_map_btn, 0, 0)
        button_grid.addWidget(self.new_goal_btn, 0, 1)
        button_grid.addWidget(self.reset_btn, 1, 0)
        button_grid.addWidget(self.validate_btn, 1, 1)
        button_grid.addWidget(self.load_btn, 2, 0)
        button_grid.addWidget(self.exit_btn, 2, 1)
        button_grid.addWidget(self.previous_btn, 3, 0)
        button_grid.addWidget(self.modifier_carte_btn, 3, 1)
        button_grid.addWidget(self.save_btn, 4, 0)

        # Solution Buttons
        self.solution_layout = QVBoxLayout()
        self.control_layout.addLayout(self.solution_layout)

        self.fast_btn = self.create_button("Solution Rapide", None, self.canvas.sol_fast)
        self.non_optim_btn = self.create_button("Solution Non-Optimale", None, self.canvas.sol_non_optim)
        self.optim_btn = self.create_button("Solution Optimale", None, self.canvas.sol_optim)

        self.solution_layout.addWidget(self.fast_btn)
        self.solution_layout.addWidget(self.non_optim_btn)
        self.solution_layout.addWidget(self.optim_btn)

        # Robot Selection
        '''robot_label = QLabel("\u2699 Robots")
        robot_label.setFont(QFont("Arial", 14))
        robot_label.setAlignment(Qt.AlignCenter)
        self.control_layout.addWidget(robot_label)'''

        self.robot_buttons = []
        for idx, robot in enumerate(ROBOT):
            robot_button = QRadioButton(f"Robot {robot} {idx}")
            robot_button.setStyleSheet(f"color: {robot}")
            robot_button.setShortcut(_translate("MainWindow", f'{idx}'))
            if idx == 0:
                robot_button.setChecked(True)
            robot_button.clicked.connect(lambda _, r=robot: self.canvas.appui_bouton(r))
            self.robot_buttons.append(robot_button)
            self.control_layout.addWidget(robot_button)

        for rang, robot in enumerate(ROBOT):
            self.robot_buttons[rang].clicked.connect(partial(self.canvas.appui_bouton, robot))

        # Position and Map Name
        self.position_input = self.create_input_field("Position Robot (e.g., r0, 0, 0)")
        self.map_name_input = self.create_input_field("Nom de la carte")
        self.control_layout.addWidget(self.position_input)
        self.control_layout.addWidget(self.map_name_input)


        self.label_sol_fast = QLabel('Solution:', self)
        self.label_sol_fast.move(980, 880)
        self.label_sol_fast.resize(1000,30)
        self.label_sol_fast.setVisible(False)


        self.label_sol_non_optim = QLabel('Solution:', self)
        self.label_sol_non_optim.move(980, 910)
        self.label_sol_non_optim.resize(1000,30)
        self.label_sol_non_optim.setVisible(False)

        self.label_optim = QLabel('Solution: ', self)
        self.label_optim.move(980, 940)
        self.label_optim.resize(1000,30)
        self.label_optim.setVisible(False)

        self.nom_fichier = self.map_name_input.text()
        self.nom_modif = self.position_input.text()

        self.map_name_input.textChanged.connect(lambda: self.canvas.changer_nom_map())
        self.position_input.textChanged.connect(lambda: self.canvas.changer_position())

        # Info Labels
        self.record_label = QLabel("Record :{}".format(self.time_increment))
        self.counter_label = QLabel("Compteur :{}".format(self.time_record))
        self.control_layout.addWidget(self.record_label)
        self.control_layout.addWidget(self.counter_label)



        self.haut = QPushButton('haut', self)
        self.haut.move(0,300)
        self.haut.setGeometry(0,0,0,0)
        self.haut.setShortcut(_translate("MainWindow", "Up"))

        self.bas = QPushButton('bas', self)
        self.bas.move(0,350)
        self.bas.setGeometry(0,0,0,0)
        self.bas.setShortcut(_translate("MainWindow", "Down"))

        self.droite = QPushButton('droite', self)
        self.droite.move(0,400)
        self.droite.setGeometry(0,0,0,0)
        self.droite.setShortcut(_translate("MainWindow", "Right"))

        self.gauche = QPushButton('gauche', self)
        self.gauche.move(0,450)
        self.gauche.setGeometry(0,0,0,0)
        self.gauche.setShortcut(_translate("MainWindow", "Left"))

        for rang, robot in enumerate(ROBOT):
            self.robot_buttons[rang].clicked.connect(partial(self.canvas.appui_bouton, robot))


        self.gauche.clicked.connect(lambda: self.canvas.depp('gauche'))
        self.droite.clicked.connect(lambda: self.canvas.depp('droite'))
        self.haut.clicked.connect(lambda: self.canvas.depp('haut'))
        self.bas.clicked.connect(lambda: self.canvas.depp('bas'))

        self.control_layout.addStretch()

    def create_button(self, text, shortcut, callback):
        button = QPushButton(text)
        button.setFont(QFont("Arial", 12))
        button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        button.clicked.connect(callback)
        if shortcut:
            button.setShortcut(shortcut)
        return button
    
    def create_input_field(self, placeholder):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setFont(QFont("Arial", 12))
        input_field.setStyleSheet("padding: 5px; border: 1px solid gray; border-radius: 5px;")
        return input_field
    
    def exit_game(self):
        sys.exit(0)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=10, dpi=100, ex=None):
        self.app = ex
        self.jeu = Plateau(16,10)
        self.jeu.random()
        self.historique = [self.jeu.get_coord_robots()]
        self.objectif = self.jeu.objectif.couleur
        self.couleur = ROBOT[0] # robot 0 par défaut
        self.algo = Algo(self.jeu)
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)


        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()


    def plot(self):
        a = self.jeu.affich()
        self.objectif = self.jeu.objectif.couleur
        ax = self.figure.add_subplot(111)
        ax.imshow(a, interpolation='nearest')
        ax.set_title('Ricochet Robot')
        ax.axis('off')
        self.draw()

    def begin(self):
        self.app.time_record,self.app.time_increment = 0,0
        self.app.record_label.setText("Record " + str(self.app.time_record))
        self.app.counter_label.setText("Compteur " + str(self.app.time_increment))
        self.app.label_sol_fast.setVisible(False)
        self.app.label_sol_non_optim.setVisible(False)
        self.app.label_optim.setVisible(False)
        self.jeu.random()
        self.historique = [self.jeu.get_coord_robots()]
        self.plot()

    def change(self):
        self.app.time_record,self.app.time_increment = 0,0
        self.app.record_label.setText("Record " + str(self.app.time_record))
        self.app.counter_label.setText("Compteur " + str(self.app.time_increment))
        self.jeu.rand_obj()
        self.plot()

    def reset(self):
        self.app.time_increment = 0
        self.app.counter_label.setText("Compteur " + str(self.app.time_increment))
        self.jeu.replacer_robots(self.jeu.init)
        self.historique = [self.jeu.get_coord_robots()]
        self.app.label_sol_fast.setVisible(False)
        self.app.label_sol_non_optim.setVisible(False)
        self.app.label_optim.setVisible(False)
        self.plot()

    def register(self):
        if (self.app.time_record==0 or self.app.time_record > self.app.time_increment) and self.jeu.est_resolu():
            self.app.time_record = self.app.time_increment
            self.app.record_label.setText("Record " + str(self.app.time_record))
            self.app.time_increment = 0
            self.app.counter_label.setText("Compteur " + str(self.app.time_increment))
            self.message = QMessageBox(self)
            self.message.setText('Gagné !')
            self.message.exec()

    def sol_fast(self):
        sol = self.algo.solution_fast(self.objectif, np.inf)
        self.app.label_sol_fast.setText("Solution Rapide :" + self.affiche_texte_couleur(sol, self.objectif))
        self.app.label_sol_fast.setVisible(True)
        self.jeu.replacer_robots(self.jeu.init)
        self.historique = [self.jeu.get_coord_robots()]


    
    def sol_optim(self):
        start = time.perf_counter()
        sol = self.algo.solution_fast(self.objectif, np.inf)
        sol_optim = self.algo.branch_and_bound(self.objectif, sol, self.algo.nombre_dep_sec(sol), True)
        end =  time.perf_counter()
        sol_optim [2] = end-start
        self.app.label_optim.setText("Solution Optimale :" + self.affiche_texte_couleur(sol_optim, self.objectif))
        self.app.label_optim.setVisible(True)
        self.jeu.replacer_robots(self.jeu.init)
        self.historique = [self.jeu.get_coord_robots()]

    def sol_non_optim(self):
        start = time.perf_counter()
        sol = self.algo.solution_fast(self.objectif, np.inf)
        sol_optim = self.algo.branch_and_bound(self.objectif, sol, self.algo.nombre_dep_sec(sol))
        end =  time.perf_counter()
        sol_optim [2] = end-start
        self.app.label_sol_non_optim.setText("Solution non Optimale :" + self.affiche_texte_couleur(sol_optim, self.objectif))
        self.app.label_sol_non_optim.setVisible(True)
        self.jeu.replacer_robots(self.jeu.init)
        self.historique = [self.jeu.get_coord_robots()]

    def affiche_texte_couleur(self, texte, objectif):
        texte = [texte[0], self.convertir_liste_coup(texte[1], objectif), texte[2]]
        chaine = '['
        chaine += str(texte[0]) + ", "
        for i in range(0, len(texte[1]) - 1):
            for robot in ROBOT:
                if texte[1][i] == robot:
                    chaine += f'<span style="color:{robot};">{texte[1][i+1]}</span> '
        chaine += ", " + str(texte[2]) +']'
        return chaine
    
    def convertir_liste_coup(self,list_coup, main): # convertit en mettant aussi la couleur du robot principal
        new_list_coup = []
        if list_coup[0] in DIR:
            for l in range(len(list_coup)):
                new_list_coup.append(main)
                new_list_coup.append(list_coup[l])
            return new_list_coup
        for l in range(len(list_coup)):
            if list_coup[l] in ROBOT:
                new_list_coup.append(list_coup[l])
                new_list_coup.append(list_coup[l+1])
            elif l>0 and list_coup[l-1] not in ROBOT:
                new_list_coup.append(main)
                new_list_coup.append(list_coup[l])
        return new_list_coup






    def previous(self):
        if self.app.time_increment >=1:
            self.app.time_increment -= 1
            self.app.counter_label.setText("Compteur " + str(self.app.time_increment))
            self.jeu.replacer_robots(self.historique[-2])
            self.historique =copy.deepcopy(self.historique[:-1])
            self.plot()


    def appui_bouton(self, couleur):
        self.couleur = couleur

    def depp(self, direction):
        self.app.time_increment += 1
        self.app.counter_label.setText("Compteur " + str(self.app.time_increment))
        self.jeu.dep(self.couleur, direction)
        self.historique.append(self.jeu.get_coord_robots())
        self.plot()

    def changer_nom_map(self):
         self.app.nom_fichier = self.app.map_name_input.text()

    def changer_position(self):
         self.app.nom_modif = self.app.position_input.text()

    def save(self):
        lines = ""
        path = 'map/%s.txt' % (self.app.nom_fichier)
        with open (path, 'w') as f:
            for i in range (N):
                for j in range (N):
                    case = self.jeu.tableau[i][j]
                    for rang, robot in enumerate(ROBOT):
                        if case.robot.couleur == robot:
                            lines += "r%d,%d,%d\n" % (rang,i,j)
                        if case.objectif.couleur == robot:
                            lines += "o%d,%d,%d\n" % (rang,i,j)

                    if (i == 0 or i == N-1) and j != N-1 and case.mur.droite and self.jeu.tableau[i][j+1].mur.gauche:
                        lines += "bv,%d,%d\n" % (i,j)
                    elif (j == 0 or j == N-1) and i != N-1 and case.mur.bas and self.jeu.tableau[i+1][j].mur.haut:
                        lines += "bh,%d,%d\n" % (i,j)
                    if i !=0 and i != N-1 and j !=0 and j != N-1:
                        if case.mur.haut and case.mur.droite:
                            lines += "c_h_d,%d,%d\n" % (i,j)
                        elif case.mur.bas and case.mur.droite:
                            lines += "c_b_d,%d,%d\n" % (i,j)
                        elif case.mur.bas and case.mur.gauche:
                            lines += "c_b_g,%d,%d\n" % (i,j)
                        elif case.mur.gauche and case.mur.haut:
                            lines += "c_h_g,%d,%d\n" % (i,j)
            f.write(lines)

    def modif(self):
        change = self.app.nom_modif.split(',')
        k, h = int(change[1]), int(change[2])
        dic_robot = {}
        dic_obj = {}
        for rang, robot in enumerate(ROBOT):
            dic_robot['r%d' % (rang)] = robot   #dic_robot = {'r0': 'red', 'r1':etc...}
            dic_obj['o%d' % (rang)] = robot     #dic_obj = {'o0': 'red', 'o1':etc...}
        for cle in dic_robot.keys():
            if cle == change[0]:
                for i in range (N):
                        for j in range (N):
                            case = self.jeu.tableau[i][j]
                            if case.robot.couleur == dic_robot[cle]:
                                self.jeu.bouger_robot(case.robot.couleur, k, h)
        for cle in dic_obj.keys():
            if change[0] in(cle):
                for i in range (N):
                        for j in range (N):
                            case = self.jeu.tableau[i][j]
                            if case.objectif.couleur != None:
                                self.jeu.bouger_obj(dic_obj[cle],k, h)
        self.app.time_increment = 0
        self.app.nbr_compteur.setText(str(self.app.time_increment))
        self.historique = [self.jeu.get_coord_robots()]
        self.plot()


    def ouvrir(self):
        self.jeu.open(self.app.nom_fichier)
        self.app.time_increment = 0
        self.app.nbr_compteur.setText(str(self.app.time_increment))
        self.historique = [self.jeu.get_coord_robots()]
        self.plot()


    


    def end(self):
        sys.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.showFullScreen()
    sys.exit(app.exec_())