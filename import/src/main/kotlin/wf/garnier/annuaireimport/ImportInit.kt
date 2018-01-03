package wf.garnier.annuaireimport

import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.boot.CommandLineRunner
import org.springframework.stereotype.Component
import wf.garnier.annuaireimport.import.Importer
import wf.garnier.annuaireimport.import.Row
import wf.garnier.annuaireimport.model.*
import kotlin.system.measureTimeMillis

@Component
class ImportInit(val repo: AncienRepository) : CommandLineRunner {

    @Value("\${xls.path}")
    lateinit var path: String

    private val logger = LoggerFactory.getLogger(ImportInit::class.java)

    override fun run(vararg p0: String?) {
        val importer = Importer(path)

        logger.info("Loading rows from file")

        val time = measureTimeMillis {
            val rows = importer.loadRowsFromFile()
            logger.info("Found ${rows.size} rows.")

            val pays = getAllPays(rows)
            val villes = getAllVille(rows, pays)
            val entreprise = getAllEntreprise(rows)

            saveAllAnciens(rows, villes, entreprise)
        }

        logger.info("Loading done, took $time ms.")
    }

    private fun saveAllAnciens(rows: Collection<Row>, villes: Map<String, Ville>, entreprises: Map<String, Entreprise>) {
        logger.info("Purging.")
        repo.purge()
        logger.info("Purged.")

        val anciens = rows.map {

            val adressePerso =
                if (it.ville_perso.isNotBlank() && it.pays_perso.isNotBlank())
                    listOf(
                        Adresse(
                            adresse = "${it.contactA}\n${it.contactB}\n${it.contactC}",
                            code = it.codePostal_perso,
                            ville = villes[it.ville_perso + it.pays_perso.toUpperCase()]
                        )
                    )
                else listOf()

            val experience =
                if (it.entreprise.isNotBlank())
                    listOf(
                        Experience(
                            entreprise = entreprises[it.entreprise.toUpperCase()],
                            poste = it.poste,
                            adresse =
                            if (it.ville_pro.isNotBlank() && it.pays_pro.isNotBlank())
                                Adresse(
                                    ville = villes[it.ville_pro + it.pays_pro.toUpperCase()]
                                )
                            else null
                        )
                    )
                else
                    listOf()

            Ancien(
                nom = it.nom,
                nom_slug = "",
                prenom = it.prenom,
                prenom_slug = "",
                promo = it.annee1.toShort(),
                diplome = it.diplome1,
                experiences = experience,
                adresses = adressePerso
            )
        }
        logger.info("Saving ...")
        repo.save(anciens)
        logger.info("Saved.")

    }

    private fun getAllPays(rows: Collection<Row>) =
        rows
            .map { it.pays_perso }
            .union(rows.map { it.pays_pro })
            .map { it.toUpperCase() }
            .filter { it.isNotBlank() }
            .distinct()
            .map { Pays(nom = it) }
            .associate { it.nom to it }


    private fun getAllVille(rows: Collection<Row>, pays: Map<String, Pays>) =
        rows
            .map { Ville(nom = it.ville_perso, pays = pays[it.pays_perso.toUpperCase()]) }
            .union(
                rows
                    .map { Ville(nom = it.ville_pro, pays = pays[it.pays_pro.toUpperCase()]) }
            )
            .filter { it.pays != null }
            .distinctBy { v -> v.nom + v.pays!!.nom }
            .associate { it.nom + it.pays!!.nom.toUpperCase() to it }

    private fun getAllEntreprise(rows: Collection<Row>) =
        rows
            .map { it.entreprise }
            .filter { it.isNotBlank() }
            .distinct()
            .associate { it.toUpperCase() to Entreprise(nom = it) }
}