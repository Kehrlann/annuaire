package wf.garnier.annuaireimport.model

import java.util.*
import javax.persistence.*

@Entity
@SequenceGenerator(name = "experience_id_experience_seq", sequenceName = "experience_id_experience_seq", allocationSize = 1)
data class Experience(
        @Id
        @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "experience_id_experience_seq")
        val id_experience: Int = 0,

        @ManyToOne(cascade = [CascadeType.ALL], optional = true)
        @JoinColumn(name = "id_adresse", referencedColumnName = "id_adresse", nullable = false)
        val adresse: Adresse? = null,

        @ManyToOne(cascade = [CascadeType.ALL], optional = true)
        @JoinColumn(name="id_entreprise")
        val entreprise: Entreprise? = null,

        @Temporal(TemporalType.DATE) val debut: Date? = null,
        @Temporal(TemporalType.DATE) val fin: Date? = null,
        val poste: String? = null,
        val description: String? = null,
        val actif: Boolean = false,
        val telephone: String? = null,
        val mobile: String? = null,
        val fax: String? = null,
        val mail: String? = null,
        val site: String? = null,
        val id_experience_linkedin: String? = null
)
