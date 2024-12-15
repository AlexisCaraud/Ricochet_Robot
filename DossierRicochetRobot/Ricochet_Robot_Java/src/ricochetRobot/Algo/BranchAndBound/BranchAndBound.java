package ricochetRobot.Algo.BranchAndBound;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import ricochetRobot.Deplacements.Chemin;
import ricochetRobot.Deplacements.Deplacement;
import ricochetRobot.Etats.EtatPlateau;
import ricochetRobot.Etats.GestionEtat;
import ricochetRobot.ObjetsDuJeu.Plateau;

public class BranchAndBound {
    Plateau plateau;
    GestionEtat listEtatsVisites;
    List<EtatPlateau> listEtatsATraiter;
    Chemin meilleurChemin;
    public static final String[] DIRECTION = {"HAUT", "BAS", "GAUCHE", "DROITE"};
    public static String[] ROBOT = {"ROUGE", "VERT", "BLEU", "VIOLET"};

    public BranchAndBound(Plateau plateau){
        this.plateau = plateau;
    }

    public void reset_memory(){
        listEtatsVisites = new GestionEtat();
        listEtatsATraiter = new ArrayList<>();
    }


    public Chemin BranchAndBoundAlgo(int max_dep_sec){
        return BranchAndBoundAlgo(max_dep_sec, false);
    }

    /**
     * Methode qui renvoie le meilleur chemin pour résoudre le plateau (chemin optimal)
     * @param max_dep_sec on s'arrête si on a testé tous les chemins avec max_dep_sec déplacements secondaires
     * @param rapide si rapide=true, le robot principal ne peut pas être bouger dans les déplacements secondaires, donc possibilité de rater le chemin optimal
     */

    public Chemin BranchAndBoundAlgo(int max_dep_sec, boolean rapide){
        reset_memory();
        plateau.replacerRobot(plateau.getCoordInit());
        
        String couleur = plateau.getObjective().getCouleur();
        int obj_x = plateau.getObjective().getPosX();
        int obj_y = plateau.getObjective().getPosY();

        int rob_x = plateau.getCoordRobot().get(couleur).getX();
        int rob_y = plateau.getCoordRobot().get(couleur).getX();

        // on initialise les listes des états et le meilleur chemin
        meilleurChemin = plateau.cheminBFS(rob_x, rob_y, obj_x, obj_y, couleur);
        EtatPlateau etatInit = new EtatPlateau(plateau);
        listEtatsVisites.ajouterEtat(etatInit);
        listEtatsATraiter.add(etatInit);

        if (rapide){
            ArrayList<String> list = new ArrayList<>(Arrays.asList(ROBOT));

            // Retire le robot principal
            list.remove(couleur);
            ROBOT = list.toArray(new String[0]);
        }

        int dist_min = plateau.cheminBFS(rob_x, rob_y, obj_x, obj_y, couleur, true).getLongueur();
        int dep_sec = 0;

        int LowerBound = dist_min + dep_sec;
        int UpperBound = meilleurChemin.getLongueur();

        while (LowerBound < UpperBound){
            if (dep_sec > max_dep_sec){
                // Aucun chemin trouvé
                throw new RuntimeException("Aucun chemin trouvé !");
            }
            int ecart = UpperBound-LowerBound;
            System.out.println("ECART: " + ecart + " UpperBound: " + UpperBound + " dep_sec: " + dep_sec);

            meilleurChemin = parcoursEtatSuivant(dep_sec, rapide);
            
            LowerBound ++;
            UpperBound = meilleurChemin.getLongueur();
            dep_sec ++;
        }
        return meilleurChemin;
    }

    /**
     * Methode qui parcourt tous les états à traiter
     * Pour chaque états qui n'a pas encore été visités, on garde son chemin s'il est meilleur que meilleurChemin
     * @param dep_sec nombre de déplacements secondaires des chemins des états à traiter
     */

    public Chemin parcoursEtatSuivant(int dep_sec, boolean rapide){

        int xobj = plateau.getObjective().getPosX();
        int yobj = plateau.getObjective().getPosY();
        String couleur = plateau.getObjective().getCouleur();
        

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
                        if (!(robot == direction)){     // on test que si on a bougé un robot secondaire
                            int xrob = nouvelEtat.getRobots().get(couleur).getX();
                            int yrob = nouvelEtat.getRobots().get(couleur).getY();
                            Chemin cheminPourFinir = plateau.cheminBFS(xrob, yrob, xobj, yobj, couleur);
                            // si on peut terminier avec cheminPourFinir et que le chemin concaténé entre le chemin actuel et cheminPourFinir est meilleur que meilleuChemin:
                            if (cheminPourFinir.getLongueur() < Integer.MAX_VALUE 
                            && nouvelEtat.getChemin().getLongueur() + cheminPourFinir.getLongueur() < meilleurChemin.getLongueur()){
                                nouvelEtat.getChemin().ajoutCheminFin(cheminPourFinir);
                                meilleurChemin =  nouvelEtat.getChemin();
                            }
                        }
                    }
                }
            }
        }
        listEtatsATraiter = newlistEtat;
        return meilleurChemin;
    }
}

