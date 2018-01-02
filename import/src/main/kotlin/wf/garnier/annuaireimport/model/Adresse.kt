package wf.garnier.annuaireimport.model

import javax.persistence.*

@Entity
@SequenceGenerator(name = "adresse_id_adresse_seq", sequenceName = "adresse_id_adresse_seq", allocationSize = 1)
data class Adresse(
        @Id
        @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "adresse_id_adresse_seq")
        val id_adresse: Int = 0,

        val adresse: String = "",
        val code: String = "",

        @ManyToOne(cascade = [CascadeType.ALL], optional = true)
        @JoinColumn(name = "id_ville", referencedColumnName = "id_ville")
        val ville: Ville? = null
)
