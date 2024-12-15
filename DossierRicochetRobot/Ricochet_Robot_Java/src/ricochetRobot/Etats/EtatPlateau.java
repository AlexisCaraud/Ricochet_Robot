package ricochetRobot.Etats;
import java.util.*;

import ricochetRobot.Deplacements.Chemin;
import ricochetRobot.Deplacements.Deplacement;
import ricochetRobot.ObjetsDuJeu.Coordonnees;
import ricochetRobot.ObjetsDuJeu.Plateau;

public class EtatPlateau {
    private Map<String, Coordonnees> robots; // Associe un nom de robot à ses coordonnées
    private Plateau plateau;
    private Chemin chemin;


    public EtatPlateau(Plateau plateau) {
        this.robots = new HashMap<>(plateau.getCoordRobot()); // Copie pour éviter les modifications externes
        this.plateau = plateau;
        this.chemin = new Chemin(); // Chemin impossible par défaut
    }

    public Map<String, Coordonnees> getRobots() {
        return robots;
    }

    public Chemin getChemin() {
        return chemin;
    }

    public void setChemin(Chemin chemin) {
        this.chemin = chemin;
    }

    /**
     * Methode qui renvoie pour un état donné tous les états accessibles en 1 déplacement de robot
     */

    public List<EtatPlateau> getVoisins(){
        List<EtatPlateau> voisins = new ArrayList<>();
        String [] DIRECTION = {"HAUT", "BAS", "GAUCHE", "DROITE"};
        String [] ROBOT = {"ROUGE", "VERT", "BLEU", "VIOLET"};
        Map<String, Coordonnees> coordActuel = plateau.getCoordRobot();
        for (String robot: ROBOT){
            for (String direction: DIRECTION){
                plateau.deplacer_robot(robot, direction);
                EtatPlateau newEtat = new EtatPlateau(plateau);
                voisins.add(newEtat);
                plateau.replacerRobot(coordActuel);
            }
        }
        return voisins;
    }

    /**
     * Methode qui le déplacement opéré pour passer de l'état actuel (this) un autre état (etatfinal)
     */

    public Deplacement depEntreDeuxEtat(EtatPlateau etatfinal){
        for (String color : getRobots().keySet()) {
            Coordonnees startCoords = getRobots().get(color);
            Coordonnees endCoords = etatfinal.getRobots().get(color);

            // Vérifier si les coordonnées ont changé
            if (startCoords.getX() != endCoords.getX() || startCoords.getY() != endCoords.getY()) {
                String direction;
                if (startCoords.getX() != endCoords.getX()) {
                    direction = (endCoords.getX() > startCoords.getX()) ? "BAS" : "HAUT";
                }
                else {
                    direction = (endCoords.getY() > startCoords.getY()) ? "DROITE" : "GAUCHE";
                }
                return new Deplacement(color, direction);
            }
        }
        throw new RuntimeException("Aucun déplacement possible entre les états " + this + " et " + etatfinal);
    }

    /**
     * 2 états sont égaux s'ils ont les mêmes coordonnées de robots
     */

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        EtatPlateau other = (EtatPlateau) obj;
        return Objects.equals(robots, other.robots);
    }

    @Override
    public int hashCode() {
        return Objects.hash(robots);
    }

    @Override
    public String toString() {
        return "EtatPlateau{" +
                "robots=" + robots +
                '}';
    }
}

