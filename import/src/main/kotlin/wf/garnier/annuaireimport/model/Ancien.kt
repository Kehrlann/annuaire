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
        val prenom: String? = null,
        val prenom_slug: String? = null,
        val promo: Short = 0,
        val ecole: Char = 'P',
        val mail_asso: String? = null,
        val mail_perso: String? = null,
        val site: String? = null,
        val telephone: String? = null,
        val mobile: String? = null,
        val photo: String? = null,
        val diplome: String? = null,
        val delegue: Boolean = false,
        val cotisant: Boolean = false,
        val minicv: String? = null,
        val id_linkedin: String? = null,
        val url_linkedin: String? = null,
        @Basic @Temporal(TemporalType.DATE) val date_update: Date = Date.from(LocalDate.now().atStartOfDay().toInstant(ZoneOffset.UTC)), // date
        @Transient val fulltext: String = "", // tsvector
        val nouveau: Boolean = false,
        val actif: Boolean = true,
        val bloque: Boolean = false,

        @OneToMany(cascade = [CascadeType.ALL])
        @JoinColumn(name="id_ancien", referencedColumnName="id_ancien", nullable = false)
        val experiences: Collection<Experience> = listOf(),


        @OneToMany(cascade = [CascadeType.ALL])
        @JoinTable(name = "asso_ancien_adresse", joinColumns = [JoinColumn(name="id_ancien", referencedColumnName="id_ancien", nullable = false)], inverseJoinColumns = [JoinColumn(name="id_adresse", referencedColumnName="id_adresse", nullable = false)])
        val adresses: Collection<Adresse> = listOf()
)