package ricochetRobot.GestionMap;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

import ricochetRobot.ObjetsDuJeu.Objective;
import ricochetRobot.ObjetsDuJeu.Plateau;
import ricochetRobot.ObjetsDuJeu.Robot;

public class FichierLecteur {

    public static void lireFichier(String cheminFichier, Plateau plateau) {
        try (BufferedReader br = new BufferedReader(new FileReader(cheminFichier))) {
            String ligne;
            while ((ligne = br.readLine()) != null) {
                traiterLigne(ligne, plateau);
            }
            plateau.InitCoord();
        } catch (IOException e) {
            System.err.println("Erreur lors de la lecture du fichier : " + e.getMessage());
        }
    }

    private static void traiterLigne(String ligne, Plateau plateau) {
        // Découper la ligne par les virgules
        String[] parties = ligne.split(",");
        if (parties.length != 3) {
            System.err.println("Ligne invalide : " + ligne);
            return;
        }

        // Lire le type d'élément, et ses coordonnées
        String type = parties[0];
        int x = Integer.parseInt(parties[1]);
        int y = Integer.parseInt(parties[2]);

        // Appliquer l'effet en fonction du type
        switch (type) {
            case "bv": // Mur vertical
            plateau.add_barrev(x, y);
                break;
            case "bh": // Mur horizontal
            plateau.add_barreh(x, y);
                break;
            case "c_h_d": // Coin spécifique (type 1)
                plateau.add_coin_h_d(x, y);
                break;
            case "c1": // Coin spécifique (type 1)
                plateau.add_coin_h_d(x, y);
                break;
            case "c_h_g": // Coin spécifique (type 2)
                plateau.add_coin_h_g(x, y);
                break;
            case "c4": // Coin spécifique (type 2)
                plateau.add_coin_h_g(x, y);
                break;
            case "c_b_d": // Coin spécifique (type 3)
                plateau.add_coin_b_d(x, y);
                break;
            case "c2": // Coin spécifique (type 3)
                plateau.add_coin_b_d(x, y);
                break;
            case "c_b_g": // Coin spécifique (type 4)
                plateau.add_coin_b_g(x, y);
                break;
            case "c3": // Coin spécifique (type 4)
                plateau.add_coin_b_g(x, y);
                break;
            case "r0": // Robot de type 0
                Robot robot0 = new Robot("ROUGE", x, y);
                plateau.add_robot(robot0);
                break;
            case "r1": // Robot de type 1
                Robot robot1 = new Robot("VERT", x, y);
                plateau.add_robot(robot1);
                break;
            case "r2": // Robot de type 2
                Robot robot2 = new Robot("BLEU", x, y);
                plateau.add_robot(robot2);
                break;
            case "r3": // Robot de type 3
                Robot robot3 = new Robot("VIOLET", x, y);
                plateau.add_robot(robot3);
                break;
            case "o0": // Objectif 0
                Objective obj0 = new Objective("ROUGE", x, y);
                plateau.add_objective(obj0);
                break;
            case "o1": // Objectif 1
                Objective obj1 = new Objective("VERT", x, y);
                plateau.add_objective(obj1);
                break;
            case "o2": // Objectif 2
                Objective obj2 = new Objective("BLEU", x, y);
                plateau.add_objective(obj2);
                break;
            case "o3": // Objectif 3
                Objective obj3 = new Objective("VIOLET", x, y);
                plateau.add_objective(obj3);
                break;
            case "o4": // Objectif 4
                Objective obj4 = new Objective("MULTICOLORE", x, y);
                plateau.add_objective(obj4);
                break;
            default:
                System.err.println("Type inconnu : " + type);
        }
    }
}
