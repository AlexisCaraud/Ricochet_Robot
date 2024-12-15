package ricochetRobot.Algo;
import java.util.ArrayList;
import java.util.List;

import ricochetRobot.Deplacements.Chemin;
import ricochetRobot.Deplacements.Deplacement;
import ricochetRobot.Etats.EtatPlateau;
import ricochetRobot.Etats.GestionEtat;
import ricochetRobot.ObjetsDuJeu.Plateau;

public class BFS {
    Plateau plateau;
    GestionEtat listEtatsVisites;
    List<EtatPlateau> listEtatsATraiter;
    Chemin meilleurChemin;

    public BFS(Plateau plateau) {
        this.plateau = plateau;
    }

    public void reset_memory(){
        listEtatsVisites = new GestionEtat();
        listEtatsATraiter = new ArrayList<>();
    }

    public Chemin random(){

        reset_memory();
        plateau.replacerRobot(plateau.getCoordInit());

        String [] DIRECTION = {"HAUT", "BAS", "GAUCHE", "DROITE"};
        String [] ROBOT = {"ROUGE", "VERT", "BLEU", "VIOLET"};

        int xobj = plateau.getObjective().getPosX();
        int yobj = plateau.getObjective().getPosY();
        String couleur = plateau.getObjective().getCouleur();
    
        
        if (listEtatsATraiter.size() == 0){
            EtatPlateau etatInit = new EtatPlateau(plateau);
            listEtatsVisites.ajouterEtat(etatInit);
            listEtatsATraiter.add(etatInit);
        }

        int count = 0;

        while (true){
            List<EtatPlateau> newlistEtat = new ArrayList<>();
            for (EtatPlateau etatPrecedents:listEtatsATraiter){
                for (String direction: DIRECTION){
                    for (String robot: ROBOT){
                        plateau.replacerRobot(etatPrecedents.getRobots());
                        plateau.deplacer_robot(robot, direction);
                        EtatPlateau nouvelEtat = new EtatPlateau(plateau);
                        if (!listEtatsVisites.estDejaRencontre(nouvelEtat)){
                            Chemin copieChemin = etatPrecedents.getChemin().copy(); // Crée une copie indépendante du chemin
                            nouvelEtat.setChemin(copieChemin);
                            nouvelEtat.getChemin().addDepFin(new Deplacement(robot, direction));
                            listEtatsVisites.ajouterEtat(nouvelEtat);
                            newlistEtat.add(nouvelEtat);
                            Chemin [][] tab_distance = plateau.tableauDistanceBFS(xobj, yobj, couleur);
                            int xrob = nouvelEtat.getRobots().get(couleur).getX();
                            int yrob = nouvelEtat.getRobots().get(couleur).getY();
                            Chemin cheminPourFinir = tab_distance[xrob][yrob];
                            if (cheminPourFinir.getLongueur() == 2){
                                nouvelEtat.getChemin().ajoutCheminFin(cheminPourFinir);
                                return nouvelEtat.getChemin();
                            }
                        }
                    }
                }
            }
            listEtatsATraiter = newlistEtat;
            count +=1;
            System.out.println("Chemins à " + count + " coups parcourus");
        }
    }
}