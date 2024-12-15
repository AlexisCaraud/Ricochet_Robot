package ricochetRobot.ObjetsDuJeu;
public class Objective {
    String couleur; // "ROUGE", "BLEU", "VERT", "VIOLET"
    int posX;
    int posY;

    public Objective(String couleur, int posX, int posY) {
        this.couleur = couleur;
        this.posX = posX;
        this.posY = posY;
    }

    public String getCouleur() {
        return couleur;
    }

    public int getPosX() {
        return posX;
    }

    public int getPosY() {
        return posY;
    }
}