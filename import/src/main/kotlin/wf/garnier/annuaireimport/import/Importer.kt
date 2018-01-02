package wf.garnier.annuaireimport.import

import org.apache.poi.hssf.usermodel.HSSFWorkbook
import org.apache.poi.poifs.filesystem.POIFSFileSystem
import org.apache.poi.ss.usermodel.CellType
import org.slf4j.LoggerFactory
import java.io.File

class Importer(val path: String) {

    val thing = File(path)
    val logger = LoggerFactory.getLogger(Importer::class.java)

    fun loadRowsFromFile(): Collection<Row> {
        val poifsFileSystem = POIFSFileSystem(thing)
        val wbook = HSSFWorkbook(poifsFileSystem)

        val mainSheet = wbook.getSheetAt(0)
        val rowNum = 13103
        logger.info("XLS has $rowNum rows")

        return (1..rowNum).map {

            val row = mainSheet.getRow(it)
            val cellValues = mutableListOf<String>()

            (0..24).forEach {
                val cell = row.getCell(it)
                try {
                cellValues.add(
                        when (cell.cellTypeEnum) {
                            CellType.STRING -> cell.stringCellValue
                            CellType.NUMERIC -> cell.numericCellValue.toInt().toString()
                            else -> ""
                        }
                ) }
                 catch (e: Exception) {
                     cellValues.add("")
                 }

            }

            Row(
                    civilite = cellValues[0],
                    prenom = cellValues[1],
                    nom = cellValues[2],
                    dateNaissance = cellValues[3],
                    diplome1 = cellValues[4],
                    promo1 = cellValues[5],
                    annee1 = cellValues[6],
                    cdr1 = cellValues[7],
                    diplome2 = cellValues[8],
                    promo2 = cellValues[9],
                    contactA = cellValues[10],
                    contactB = cellValues[11],
                    contactC = cellValues[12],
                    codePostal_perso = cellValues[13],
                    pays_perso = cellValues[14],
                    ville_perso = cellValues[15],
                    complement = cellValues[16],
                    entreprise = cellValues[17],
                    fonction = cellValues[18],
                    secteur = cellValues[19],
                    poste = cellValues[20],
                    pays_pro = cellValues[21],
                    ville_pro = cellValues[22],
                    autreDip = cellValues[23],
                    maj = cellValues[24]
            )
        }
    }
}