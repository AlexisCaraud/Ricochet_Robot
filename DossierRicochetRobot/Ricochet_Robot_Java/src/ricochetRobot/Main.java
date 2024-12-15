package ricochetRobot;

import ricochetRobot.Algo.BFS;
import ricochetRobot.Algo.SolutionRapide;
import ricochetRobot.Algo.AStar.Astar;
import ricochetRobot.Algo.AStar.Heuristique.HeuristiqueManhattan;
import ricochetRobot.Algo.BranchAndBound.BranchAndBound;
import ricochetRobot.Deplacements.Chemin;
import ricochetRobot.GestionMap.FichierLecteur;
import ricochetRobot.ObjetsDuJeu.Plateau;



public class Main {
    public static void main(String[] args) {

        
        Plateau plateau = new Plateau(16); // Plateau de 16x16

        // Chemin vers le fichier
        String cheminFichier = "src/ricochetRobot/MapSaved/264secondes.txt";

        // Lire le fichier et peupler le plateau
        FichierLecteur.lireFichier(cheminFichier, plateau);

        /*Astar astar = new Astar(plateau, new HeuristiqueManhattan());

        long debut = System.currentTimeMillis();

        Chemin chemin = astar.aStarSearch();

        long fin = System.currentTimeMillis();

        long tempsEcoule = (fin - debut) / 1000;

        System.out.println("AStar: " + chemin + " time " + tempsEcoule + "secondes");*/


        SolutionRapide algoRapide = new SolutionRapide(plateau);
        BranchAndBound algoBB = new BranchAndBound(plateau);

        Chemin cheminFast = algoRapide.sol_fast(100);

        System.out.println("solution fast: " + cheminFast);

        long debut2 = System.currentTimeMillis();

        Chemin chemin2 = algoBB.BranchAndBoundAlgo(20, true);

        long fin2 = System.currentTimeMillis();

        long tempsEcoule2 = (fin2 - debut2) / 1000;

        System.out.println("solution B&B: " + chemin2 + " time: " + tempsEcoule2 + "secondes");

        /*BFS algoBFS = new BFS(plateau);
        
        long debut3 = System.currentTimeMillis();

        Chemin cheminRand = algoBFS.random();

        long fin3 = System.currentTimeMillis();

        long tempsEcoule3 = (fin3 - debut3) / 1000;

        System.out.println(("solution rand: " + cheminRand + " time: " + tempsEcoule3 + "secondes"));*/
    }
}