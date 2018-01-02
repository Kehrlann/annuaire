package wf.garnier.annuaireimport.model

import org.springframework.stereotype.Repository
import javax.persistence.*

@Repository
@Entity
@SequenceGenerator(name = "pays_id_pays_seq", sequenceName = "pays_id_pays_seq", allocationSize = 1)
data class Pays(
        @Id
        @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "pays_id_pays_seq")
        val id_pays: Int = 0,

        val nom: String = ""
)