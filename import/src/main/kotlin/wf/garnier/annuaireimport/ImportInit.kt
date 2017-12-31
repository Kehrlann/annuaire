package wf.garnier.annuaireimport

import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.boot.CommandLineRunner
import org.springframework.stereotype.Component
import wf.garnier.annuaireimport.import.Importer
import kotlin.system.measureTimeMillis

@Component
class ImportInit : CommandLineRunner {

    @Value("\${xls.path}")
    lateinit var path: String

    private val logger = LoggerFactory.getLogger(ImportInit::class.java)

    override fun run(vararg p0: String?) {
        val importer = Importer(path)

        logger.info("Loading rows from file")

        val time = measureTimeMillis {
            val rows = importer.loadRowsFromFile()
            logger.info("Found ${rows.size} rows.")
        }

        logger.info("Loading done, took $time ms.")
    }
}