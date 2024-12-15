package ricochetRobot.Algo.BranchAndBound;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Set;

import ricochetRobot.Deplacements.Chemin;
import ricochetRobot.Deplacements.Deplacement;
import ricochetRobot.Etats.EtatPlateau;
import ricochetRobot.ObjetsDuJeu.Plateau;

public class BranchAndBound2 {
    Plateau plateau;
    Set<EtatPlateau> etatsDejaTraites;
    Queue<EtatPlateau> etatsATraiter;
    Chemin meilleurChemin;

    public BranchAndBound2(Plateau plateau){
        this.plateau = plateau;
    }

    @SuppressWarnings({ "unchecked", "rawtypes" })
    public void reset_memory(){
        etatsDejaTraites = new HashSet();
        etatsATraiter = new LinkedList();
    }

    public Chemin BranchAndBoundAlgo(int max_dep_sec){
        return BranchAndBoundAlgo(max_dep_sec, false);
    }

    public Chemin BranchAndBoundAlgo(int max_dep_sec, boolean rapide){
        reset_memory();
        plateau.replacerRobot(plateau.getCoordInit());
        String couleur = plateau.getObjective().getCouleur();
        int obj_x = plateau.getObjective().getPosX();
        int obj_y = plateau.getObjective().getPosY();

        int rob_x = plateau.getCoordRobot().get(couleur).getX();
        int rob_y = plateau.getCoordRobot().get(couleur).getX();

        meilleurChemin = plateau.tableauDistanceBFS(obj_x, obj_y, couleur)[rob_x][rob_y];
        EtatPlateau etatInit = new EtatPlateau(plateau);
        etatsATraiter.offer(etatInit);

        int dist_min = plateau.tableauDistanceBFS(obj_x, obj_y, couleur, true)[rob_x][rob_y].getLongueur();
        int dep_sec = 0;

        int LowerBound = dist_min + dep_sec;
        int UpperBound = meilleurChemin.getLongueur();

        while (LowerBound < UpperBound){
            meilleurChemin = parcoursEtatSuivant(dep_sec, rapide);
            
            dep_sec = meilleurChemin.nbr_dep_secondaire(couleur);
            LowerBound = dist_min + dep_sec;
            UpperBound = meilleurChemin.getLongueur();
            }
        return meilleurChemin;
        }

    public Chemin parcoursEtatSuivant(int dep_sec, boolean rapide){
        String [] DIRECTION = {"HAUT", "BAS", "GAUCHE", "DROITE"};
        String [] ROBOT = {"ROUGE", "VERT", "BLEU", "VIOLET"};

        int x = plateau.getObjective().getPosX();
        int y = plateau.getObjective().getPosY();
        String couleur = plateau.getObjective().getCouleur();

        if (rapide){
            ArrayList<String> list = new ArrayList<>(Arrays.asList(ROBOT));

            // Retire le robot principal
            list.remove(couleur);
            ROBOT = list.toArray(new String[0]);
        }
        
        Chemin [][] tab_distance;

        EtatPlateau etatActuel = etatsATraiter.poll();
        etatsDejaTraites.add(etatActuel);
            for (String direction: DIRECTION){
                for (String robot: ROBOT){
                    plateau.replacerRobot(etatActuel.getRobots());
                    plateau.deplacer_robot(robot, direction);
                    EtatPlateau nouvelEtat = new EtatPlateau(plateau);

                    if (!etatsATraiter.contains(nouvelEtat) && !etatsDejaTraites.contains(nouvelEtat)){
                        Chemin copieChemin = etatActuel.getChemin().copy(); // Crée une copie indépendante du chemin
                        nouvelEtat.setChemin(copieChemin);
                        nouvelEtat.getChemin().addDepFin(new Deplacement(robot, direction));
                        etatsATraiter.offer(nouvelEtat);
                        if (!(robot == direction)){
                            tab_distance = plateau.tableauDistanceBFS(x, y, couleur);
                            int xrob = nouvelEtat.getRobots().get(couleur).getX();
                            int yrob = nouvelEtat.getRobots().get(couleur).getY();
                            Chemin cheminTest = tab_distance[xrob][yrob];
                            if (cheminTest.getLongueur() < Integer.MAX_VALUE && cheminTest.getLongueur() + dep_sec + 1 < meilleurChemin.getLongueur()){
                                nouvelEtat.getChemin().ajoutCheminFin(cheminTest);
                                meilleurChemin =  nouvelEtat.getChemin();
                            }
                        }
                    }
                }
            }
        return meilleurChemin;

    }
}

