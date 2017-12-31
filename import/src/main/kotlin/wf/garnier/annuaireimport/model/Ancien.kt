package wf.garnier.annuaireimport.model

import javax.persistence.Entity
import javax.persistence.GeneratedValue
import javax.persistence.Id

@Entity
data class Ancien(
        @Id @GeneratedValue val id_ancien: Int,
        val nom: String,
        val nom_slug: String,
        val prenom: String,
        val prenom_slug: String,
        val promo: Short,
        val ecole: Char,
        val mail_asso: String,
        val mail_perso: String,
        val site: String,
        val telephone: String,
        val mobile: String,
        val photo: String,
        val diplome: String,
        val delegue: Boolean,
        val cotisant: Boolean,
        val minicv: String,
        val id_linkedin: String,
        val url_linkedin: String,
        val date_update: String, // date
        val fulltext: String, // tsvector
        val nouveau: Boolean,
        val actif: Boolean,
        val bloque: Boolean
)