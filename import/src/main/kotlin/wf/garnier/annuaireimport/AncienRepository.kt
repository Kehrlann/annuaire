package wf.garnier.annuaireimport

import org.springframework.data.jpa.repository.Modifying
import org.springframework.data.jpa.repository.Query
import org.springframework.data.repository.CrudRepository
import wf.garnier.annuaireimport.model.Ancien
import javax.transaction.Transactional

interface AncienRepository : CrudRepository<Ancien, Int> {
    @Modifying
    @Transactional
    @Query(
        "delete from asso_ancien_adresse; " +
            "delete from experience; " +
            "delete from entreprise; " +
            "delete from adresse; " +
            "delete from ville; " +
            "delete from pays; " +
            "delete from ancien; ",
        nativeQuery = true
    )
    fun purge()

    @Modifying
    @Transactional
    @Query(
        "UPDATE ancien SET nom_slug=slugify(nom), prenom_slug=slugify(prenom); " +
            "UPDATE entreprise SET slug=slugify(nom); " +
            "UPDATE ville SET slug=slugify(nom);",
        nativeQuery = true
    )
    fun updateSlugs()
}