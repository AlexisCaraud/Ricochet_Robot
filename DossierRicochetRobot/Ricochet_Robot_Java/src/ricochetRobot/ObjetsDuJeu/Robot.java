package ricochetRobot.ObjetsDuJeu;
public class Robot {
    String couleur; // "ROUGE", "BLEU", "VERT", "VIOLET"
    int posX;
    int posY;

    public Robot(String couleur, int posX, int posY) {
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

    public void setPosX(int posX) {
        this.posX = posX;
    }

    public void setPosY(int posY) {
        this.posY = posY;
    }
}

