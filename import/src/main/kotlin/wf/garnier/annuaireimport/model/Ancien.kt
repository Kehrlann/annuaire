package wf.garnier.annuaireimport.model

import java.time.LocalDate
import java.time.LocalDateTime
import java.time.ZoneOffset
import java.util.*
import javax.persistence.*

@Entity
@SequenceGenerator(name = "ancien_id_ancien_seq", sequenceName = "ancien_id_ancien_seq", allocationSize = 1)
data class Ancien(
        @Id @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "ancien_id_ancien_seq") val id_ancien: Int = 0,
        val nom: String = "",
        val nom_slug: String = "",
        val prenom: String = "",
        val prenom_slug: String = "",
        val promo: Short = 0,
        val ecole: Char = 'P',
        val mail_asso: String = "",
        val mail_perso: String = "",
        val site: String = "",
        val telephone: String = "",
        val mobile: String = "",
        val photo: String = "",
        val diplome: String = "",
        val delegue: Boolean = false,
        val cotisant: Boolean = false,
        val minicv: String = "",
        val id_linkedin: String = "",
        val url_linkedin: String = "",
        @Basic @Temporal(TemporalType.DATE) val date_update: Date = Date.from(LocalDate.now().atStartOfDay().toInstant(ZoneOffset.UTC)), // date
        @Transient val fulltext: String = "", // tsvector
        val nouveau: Boolean = false,
        val actif: Boolean = false,
        val bloque: Boolean = false
)