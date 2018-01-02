package wf.garnier.annuaireimport.model

import javax.persistence.*


@Entity
@SequenceGenerator(name = "ville_id_ville_seq", sequenceName = "ville_id_ville_seq", allocationSize = 1)
data class Ville(
        @Id
        @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "ville_id_ville_seq")
        val id_ville: Int = 0,

        val nom: String = "",
        val slug: String = "",


        @ManyToOne(cascade = [CascadeType.ALL], optional = true)
        @JoinColumn(name = "id_pays", referencedColumnName = "id_pays")
        val pays: Pays? = null
)
