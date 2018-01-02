package wf.garnier.annuaireimport.model

import javax.persistence.*

@Entity
@SequenceGenerator(name = "entreprise_id_entreprise_seq", sequenceName = "entreprise_id_entreprise_seq", allocationSize = 1)
data class Entreprise(
        @Id
        @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "entreprise_id_entreprise_seq")
        val id_entreprise: Int = 0,

        val nom: String = "",
        val slug: String = ""
)