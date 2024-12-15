package ricochetRobot.ObjetsDuJeu;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.Queue;

import ricochetRobot.Deplacements.Chemin;
import ricochetRobot.Deplacements.Deplacement;

public class Plateau {
    Case[][] plateau;
    int taille;
    ArrayList<Robot> robots = new ArrayList<>(); // Change ici de tableau statique à ArrayList
    Objective objective;
    Map<String, Coordonnees> coordInit = new HashMap<>();
    
    

    public Plateau(int taille) {
        this.taille = taille;
        plateau = new Case[taille][taille];
    
        // Initialisation des cases
        for (int i = 0; i < taille; i++) {
            for (int j = 0; j < taille; j++) {
                plateau[i][j] = new Case(false, false, false, false);
            }
        }
    
        // Ajouter les murs extérieurs
        for (int i = 0; i < taille; i++) {
            plateau[0][i].setMurHaut(true);
            plateau[taille - 1][i].setMurBas(true);
            plateau[i][0].setMurGauche(true);
            plateau[i][taille - 1].setMurDroite(true);
        }

        // Ajouter le carré central 2x2
        int centre = taille / 2;
        plateau[centre - 1][centre - 2].setMurDroite(true);
        plateau[centre][centre - 2].setMurDroite(true);
        plateau[centre - 1][centre+1].setMurGauche(true);
        plateau[centre][centre+1].setMurGauche(true);
        plateau[centre+1][centre - 1].setMurHaut(true);
        plateau[centre+1][centre].setMurHaut(true);
        plateau[centre-2][centre - 1].setMurBas(true);
        plateau[centre-2][centre].setMurBas(true);
    }

    public Map<String, Coordonnees> getCoordInit() {
        return coordInit;
    }
    
    public Objective getObjective() {
        return objective;
    }

    public Case[][] getPlateau() {
        return plateau;
    }

    public ArrayList<Robot> getRobots() {
        return robots;
    }

    public int getTaille() {
        return taille;
    }

    public void add_coin_h_d(int x, int y) {    // Mur en haut et à droite
        addCoin(x, y, true, false, false, true);
    }
    
    public void add_coin_b_d(int x, int y) {    // Mur en bas et à droite
        addCoin(x, y, false, true, false, true);
    }
    
    public void add_coin_b_g(int x, int y) {    // Mur en bas et à gauche
        addCoin(x, y, false, true, true, false);
    }
    
    public void add_coin_h_g(int x, int y) {    // Mur en haut et à gauche
        addCoin(x, y, true, false, true, false);
    }

    public void addCoin(int x, int y, boolean haut, boolean bas, boolean gauche, boolean droite) {
        if (haut) {
            this.plateau[x-1][y].setMurBas(true); // Mur au-dessus de la case courante
            this.plateau[x][y].setMurHaut(true);
        }
        if (bas) {
            this.plateau[x+1][y].setMurHaut(true); // Mur en dessous de la case courante
            this.plateau[x][y].setMurBas(true);
        }
        if (gauche) {
            this.plateau[x][y-1].setMurDroite(true); // Mur à gauche de la case courante
            this.plateau[x][y].setMurGauche(true);
        }
        if (droite) {
            this.plateau[x][y+1].setMurGauche(true); // Mur à droite de la case courante
            this.plateau[x][y].setMurDroite(true);
        }
    }
    

    public void add_barrev(int x, int y){   // barre verticale à droite
        this.plateau[x][y].setMurDroite(true);
        this.plateau[x][y+1].setMurGauche(true);
    }

    public void add_barreh(int x, int y){   // barre horizontale en bas
        this.plateau[x][y].setMurBas(true);
        this.plateau[x+1][y].setMurHaut(true);
    }

    public void add_robot(Robot robot){
        this.plateau[robot.getPosX()][robot.getPosY()].robot = robot.getCouleur();
        this.robots.add(robot);
    }

    public void add_objective(Objective objective){
        this.plateau[objective.getPosX()][objective.getPosY()].objective = objective.getCouleur();
        this.objective = objective;
    }

    public Robot getRobot(String color){
        for(Robot robot : this.robots){
            if(robot.couleur == color){
                return robot;
            }
        }
        return null;
    }

    /**
     * Methode qui sauvegarde les coordonnées initiales des robots
     */

    public void InitCoord(){
        for(Robot robot : this.robots){
            coordInit.put(robot.getCouleur(), new Coordonnees(robot.getPosX(), robot.getPosY()));
        }
    }

    /**
     * Methode qui renvoie les coordonnées actuelles des robots
     */

    public Map<String, Coordonnees> getCoordRobot(){
        Map<String, Coordonnees> coordRobot = new HashMap<>();
        for(Robot robot : this.robots){
            coordRobot.put(robot.getCouleur(), new Coordonnees(robot.getPosX(), robot.getPosY()));
        }
        return coordRobot;
    }

    /**
     * Methode qui replace les robots du plateau aux coordonnées 'coordRobot'
     */

    public void replacerRobot(Map<String, Coordonnees> coordRobot){
        for(Robot robot : this.robots){
            change_pos_robot(robot.getCouleur(), coordRobot.get(robot.getCouleur()).getX(), coordRobot.get(robot.getCouleur()).getY());
        }
    }
    
    /**
     * Methode qui déplace un robot dans une direction
     * @param color_robot couleur du robot à déplacer
     */

    public void deplacer_robot(String color_robot, String direction) {
        Robot robot = getRobot(color_robot);

        // Supprimer le robot de sa position actuelle sur le plateau
        plateau[robot.getPosX()][robot.getPosY()].robot = " ";

        switch (direction) {
            case "HAUT":
                while (robot.getPosX() > 0 && !plateau[robot.getPosX()][robot.getPosY()].isMurHaut() 
                       && plateau[robot.getPosX() - 1][robot.getPosY()].robot.equals(" ")) {
                        robot.setPosX(robot.getPosX() - 1);
                }
                break;
            case "BAS":
                while (robot.getPosX() < taille - 1 && !plateau[robot.getPosX()][robot.getPosY()].isMurBas() 
                       && plateau[robot.getPosX() + 1][robot.getPosY()].robot.equals(" ")) {
                        robot.setPosX(robot.getPosX() + 1);
                }
                break;
            case "GAUCHE":
                while (robot.getPosY() > 0 && !plateau[robot.getPosX()][robot.getPosY()].isMurGauche() 
                       && plateau[robot.getPosX()][robot.getPosY() - 1].robot.equals(" ")) {
                        robot.setPosY(robot.getPosY() - 1);
                }
                break;
            case "DROITE":
                while (robot.getPosY() < taille - 1 && !plateau[robot.getPosX()][robot.getPosY()].isMurDroite() 
                       && plateau[robot.getPosX()][robot.getPosY() + 1].robot.equals(" ")) {
                        robot.setPosY(robot.getPosY() + 1);
                }
                break;
            default:
                System.err.println("Direction deplacement invalide : " + direction);
                return;
        }

        // Mettre à jour la nouvelle position du robot sur le plateau
        plateau[robot.getPosX()][robot.getPosY()].setRobot(robot.getCouleur());
    }

    public void change_pos_robot(String robot, int xFinal, int yFinal){
        int xInit = getRobot(robot).getPosX();
        int yInit = getRobot(robot).getPosY();
        plateau[xInit][yInit].setRobot(" "); // on enlève le robot de sa position initiale
        plateau[xFinal][yFinal].setRobot(robot);  // on ajoute le robot de à position finale
        for(Robot rob : this.robots){
            if(rob.getCouleur() == robot){
                rob.setPosX(xFinal);
                rob.setPosY(yFinal);
            }
        }
    }

    /**
     * Methode qui renvoie la distance entre une case(x,y) et le premier obstacle rencontré dans la direction 'direction'
     */

    public int distanceObstacle(int x, int y, String direction) {
        int i = 0;
        switch (direction) {
            case "DROITE":
                while (!plateau[x][y + i].isMurDroite() && plateau[x][y + i + 1].getRobot().equals(" ")) {
                    i++;
                }
                break;
            case "GAUCHE":
                while (!plateau[x][y - i].isMurGauche() && plateau[x][y - i - 1].getRobot().equals(" ")) {
                    i++;
                }
                break;
            case "HAUT":
                while (!plateau[x - i][y].isMurHaut() && plateau[x - i - 1][y].getRobot().equals(" ")) {
                    i++;
                }
                break;
            case "BAS":
                while (!plateau[x + i][y].isMurBas() && plateau[x + i + 1][y].getRobot().equals(" ")) {
                    i++;
                }
                break;
            default:
                throw new IllegalArgumentException("Direction obstacle invalide : " + direction);
        }
        return i;
    }
    
    /**
     * Methode qui renvoie un tableau de chemin entre une case et la case(x,y)
     * @param minimum si minimum: on renvoie les meilleurs minimaux (on suppose que le robot peut s'arrêter même si pas d'obstacle devant lui)
     */

    public Chemin[][] tableauDistanceBFS(int x, int y, String couleur, boolean minimum) {
        
        Robot robot = getRobot(couleur);
        int xRobot = robot.getPosX();
        int yRobot = robot.getPosY();
        plateau[xRobot][yRobot].setRobot(" ");; // Enlève le robot temporairement

        if (minimum){
            for (Robot rob : robots){
                plateau[rob.getPosX()][rob.getPosY()].setRobot(" ");; // Enlève les robots temporairement
                }
        }

        int rows = plateau.length;
        int cols = plateau[0].length;

        // Initialisation de la matrice des chemins
        Chemin[][] chemins = new Chemin[rows][cols];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                chemins[i][j] = new Chemin(); // Par défaut, chemins non définis
            }
        }

        // Initialisation de la file pour BFS
        Queue<Coordonnees> queue = new LinkedList<>();
        Coordonnees start = new Coordonnees(x, y);
        queue.add(start);
        chemins[x][y] = new Chemin(); // Case cible : longueur 0
        chemins[x][y].setLongueur(0);

        // Déplacements possibles (haut, bas, gauche, droite)
        int[] dx = {-1, 1, 0, 0};
        int[] dy = {0, 0, -1, 1};
        String[] directions = {"HAUT", "BAS", "GAUCHE", "DROITE"};
        String[] directionsOpposees = {"BAS", "HAUT", "DROITE", "GAUCHE"};

        // BFS
        while (!queue.isEmpty()) {
            Coordonnees current = queue.poll();
            int currentX = current.getX();
            int currentY = current.getY();
            Chemin currentChemin = chemins[currentX][currentY];

            for (int i = 0; i < 4; i++) {

                // Distance obstacle dans la direction directions[i]
                int dist = distanceObstacle(currentX, currentY, directionsOpposees[i]);
                if (minimum ||this.plateau[currentX][currentY].getMur(directions[i]) || 
                    !this.plateau[currentX + dx[i]][currentY + dy[i]].robot.equals(" ")) {
                    for (int t = 1; t <= dist; t++) {
                        int newX = currentX - t * dx[i];
                        int newY = currentY - t * dy[i];
                        Chemin neighborChemin = chemins[newX][newY];

                        // Construire un nouveau chemin vers le voisin
                        Chemin newChemin = currentChemin.copy();
                        newChemin.addDepDebut(new Deplacement(couleur, directions[i]));

                        // Mettre à jour le chemin si une meilleure solution est trouvée
                        if (neighborChemin.getLongueur() > newChemin.getLongueur()) {
                            chemins[newX][newY] = newChemin;
                            queue.add(new Coordonnees(newX, newY));
                            }
                        }
                    }
                }
            }
            plateau[xRobot][yRobot].setRobot(couleur);;  // Remet le robot à sa place d'origine

            if (minimum){
                for (Robot rob : robots){
                    plateau[rob.getPosX()][rob.getPosY()].robot = rob.getCouleur(); // Remet les robots
                    }
                }

            return chemins;
        }

        public Chemin[][] tableauDistanceBFS(int x, int y, String couleur) {
            return tableauDistanceBFS(x, y, couleur, false);
        }

    /**
     * Methode qui renvoie le plus court chemin entre la case (xDepart, yDepart) et (xArrivee, yArrivee)
     * Renvoie un chemin de longueur infini si aucun n'existe
     * @param minimum si minimum: on renvoie le chemin minimal (on suppose que le robot peut s'arrêter même si pas d'obstacle devant lui)
     */

        public Chemin cheminBFS(int xDepart, int yDepart, int xArrivee, int yArrivee, String couleur, boolean minimum) {
        
            Robot robot = getRobot(couleur);
            int xRobot = robot.getPosX();
            int yRobot = robot.getPosY();
            plateau[xRobot][yRobot].setRobot(" ");; // Enlève le robot temporairement
    
            if (minimum){
                for (Robot rob : robots){
                    plateau[rob.getPosX()][rob.getPosY()].setRobot(" ");; // Enlève les robots temporairement
                    }
            }
    
            int rows = plateau.length;
            int cols = plateau[0].length;
    
            // Initialisation de la matrice des chemins
            Chemin[][] chemins = new Chemin[rows][cols];
            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < cols; j++) {
                    chemins[i][j] = new Chemin(); // Par défaut, chemins non définis
                }
            }
    
            // Initialisation de la file pour BFS
            Queue<Coordonnees> queue = new LinkedList<>();
            Coordonnees start = new Coordonnees(xArrivee, yArrivee);
            queue.add(start);
            chemins[xArrivee][yArrivee] = new Chemin(); // Case cible : longueur 0
            chemins[xArrivee][yArrivee].setLongueur(0);
            if (xArrivee==xDepart && yArrivee==yDepart){
                return chemins[xArrivee][yArrivee];
            }
    
            // Déplacements possibles (haut, bas, gauche, droite)
            int[] dx = {-1, 1, 0, 0};
            int[] dy = {0, 0, -1, 1};
            String[] directions = {"HAUT", "BAS", "GAUCHE", "DROITE"};
            String[] directionsOpposees = {"BAS", "HAUT", "DROITE", "GAUCHE"};
    
            // BFS
            while (!queue.isEmpty()) {
                Coordonnees current = queue.poll();
                int currentX = current.getX();
                int currentY = current.getY();
                Chemin currentChemin = chemins[currentX][currentY];
    
                for (int i = 0; i < 4; i++) {
    
                    // Distance obstacle dans la direction directions[i]
                    int dist = distanceObstacle(currentX, currentY, directionsOpposees[i]);
                    if (minimum ||this.plateau[currentX][currentY].getMur(directions[i]) || 
                        !this.plateau[currentX + dx[i]][currentY + dy[i]].robot.equals(" ")) {
                        for (int t = 1; t <= dist; t++) {
                            int newX = currentX - t * dx[i];
                            int newY = currentY - t * dy[i];
                            Chemin neighborChemin = chemins[newX][newY];
    
                            // Construire un nouveau chemin vers le voisin
                            Chemin newChemin = currentChemin.copy();
                            newChemin.addDepDebut(new Deplacement(couleur, directions[i]));

                            // Si on est remonté jusqu'au point de départ:
                            if (newX == xDepart && newY == yDepart){
                                plateau[xRobot][yRobot].setRobot(couleur);;  // Remet le robot à sa place d'origine
                                if (minimum){
                                    for (Robot rob : robots){
                                        plateau[rob.getPosX()][rob.getPosY()].robot = rob.getCouleur(); // Remet les robots
                                    }
                                }
                                return newChemin;
                            }
    
                            // Mettre à jour le chemin si une meilleure solution est trouvée
                            if (neighborChemin.getLongueur() > newChemin.getLongueur()) {
                                chemins[newX][newY] = newChemin;
                                queue.add(new Coordonnees(newX, newY));
                                }
                            }
                        }
                    }
                }
                //plateau[xRobot][yRobot].setRobot(couleur);;  // Remet le robot à sa place d'origine
    
                if (minimum){
                    for (Robot rob : robots){
                        plateau[rob.getPosX()][rob.getPosY()].robot = rob.getCouleur(); // Remet les robots
                    }
                }
    
                return new Chemin();
            }

            public Chemin cheminBFS(int xDepart, int yDepart, int xArrivee, int yArrivee, String couleur) {
                return cheminBFS(xDepart, yDepart, xArrivee, yArrivee, couleur, false);
            }
        
        


    @Override
    public String toString() {
        return getCoordRobot().toString();
    }
}