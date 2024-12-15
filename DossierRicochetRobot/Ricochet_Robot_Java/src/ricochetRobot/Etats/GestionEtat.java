package ricochetRobot.Etats;
import java.util.*;

public class GestionEtat {
    private Set<EtatPlateau> etatsRencontres;

    public GestionEtat() {
        etatsRencontres = new HashSet<>();
    }

    // Ajouter un nouvel état
    public void ajouterEtat(EtatPlateau etat) {
        etatsRencontres.add(etat);
    }

    // Vérifier si un état a déjà été rencontré
    public boolean estDejaRencontre(EtatPlateau etat) {
        return etatsRencontres.contains(etat);
    }

    // Afficher les états rencontrés (facultatif)
    public void afficherEtats() {
        for (EtatPlateau etat : etatsRencontres) {
            System.out.println(etat);
        }
    }
}
