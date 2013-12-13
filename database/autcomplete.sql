-- Methode python pour slugify une string
CREATE OR REPLACE FUNCTION 
	slugify(texte TEXT) RETURNS TEXT 
AS $$
DECLARE
    result TEXT;
BEGIN
    result := replace(texte , 'æ', 'ae');
    result := replace(result , 'œ', 'oe');
    result := replace(result , '€', 'euros');
    result := replace(result , '$', 'dollars');
    result := replace(result , '£', 'pound');
    result := replace(result , '¥', 'yen');
    result := regexp_replace(translate(lower(result), 
        'áàâãäåāăąÁÂÃÄÅĀĂĄèééêëēĕėęěĒĔĖĘĚìíîïìĩīĭÌÍÎÏÌĨĪĬóôõöōŏőÒÓÔÕÖŌŎŐùúûüũūŭůÙÚÛÜŨŪŬŮçÇÿ&,.ñÑ',
        'aaaaaaaaaaaaaaaaaeeeeeeeeeeeeeeeiiiiiiiiiiiiiiiiooooooooooooooouuuuuuuuuuuuuuuuccy---nn'), E'[^\\w]+', '-', 'g');
    RETURN result;
END;
$$ LANGUAGE PLPGSQL;

SELECT slugify('abécédaire; ;mais qui est tu ?? lolwSQdwq1443%pourcentê');

-- Méthode qui prend un mot, son slug, le nombre d'occurences
-- et qui l'ajoute à la table mot (ou update si nécessaire)
CREATE OR REPLACE FUNCTION
	insert_or_update_mot(input_string TEXT, slugged_string TEXT, input_occurence INTEGER) RETURNS VOID
AS $$
	DECLARE
		comptage mot%ROWTYPE;
	BEGIN
		IF input_string IS NOT NULL and input_string <> ''  THEN
			SELECT * FROM mot WHERE slug = slugged_string INTO comptage;
			IF comptage IS NOT NULL THEN
				UPDATE mot SET occurence = comptage.occurence+input_occurence WHERE id_mot = comptage.id_mot;
			ELSE
				INSERT INTO mot(mot, slug, occurence) VALUES(input_string, slugged_string, input_occurence);
			END IF;
		END IF;
	END;
$$ LANGUAGE plpgsql;


-- Methode qui, pour un ancien donne (defini par son id_ancien),
-- va chercher son nom, prenom, ecole, promo, ville, pays et entreprises
-- et update la table mot en le specifiant
CREATE OR REPLACE FUNCTION
    index_all_words() RETURNS VOID
AS $$
    DECLARE 
        ancien_record RECORD;
		ville_record RECORD;
		pays_record RECORD;
        entreprise_record RECORD;
		ecole_record RECORD;

    BEGIN
	
		-- Purger la table mot
		DELETE FROM mot;
		
		-- ancien.prenom
		RAISE NOTICE 'Insertion des prenoms';
		FOR ancien_record IN
			SELECT prenom, slugify(prenom) as s, COUNT(0) as c
				FROM ancien 
				GROUP BY s, prenom
				ORDER BY c
		LOOP
			PERFORM insert_or_update_mot(ancien_record.prenom, ancien_record.s, CAST(ancien_record.c AS INTEGER));
		END LOOP;
		RAISE NOTICE 'Insertion des prenoms ... done';
		
		-- ancien.nom
		RAISE NOTICE 'Insertion des noms';
		FOR ancien_record IN
			SELECT nom, slugify(nom) as s, COUNT(0) as c
				FROM ancien 
				GROUP BY s, nom
				ORDER BY c
		LOOP
			PERFORM insert_or_update_mot(ancien_record.nom, ancien_record.s, CAST(ancien_record.c AS INTEGER));
		END LOOP;
		RAISE NOTICE 'Insertion des noms ... done';

		-- ecole
		RAISE NOTICE 'Insertion des ecoles';
		FOR ecole_record IN
			SELECT e.*, COUNT(0) as c
				FROM ecole as e
					JOIN ancien as a ON e.id_ecole=a.ecole
				GROUP BY e.id_ecole, e.nom
				ORDER BY c
		LOOP
			PERFORM insert_or_update_mot(ecole_record.nom, slugify(ecole_record.nom), CAST(ecole_record.c AS INTEGER));
		END LOOP;
		RAISE NOTICE 'Insertion des ecoles ... done';

		-- entreprise.nom
		RAISE NOTICE 'Insertion des entreprises';
		FOR entreprise_record IN
			SELECT entreprise.nom, entreprise.slug as s, COUNT(0) as c
				FROM entreprise JOIN experience USING(id_entreprise)
				GROUP BY s, nom
				ORDER BY c
		LOOP
			PERFORM insert_or_update_mot(entreprise_record.nom, entreprise_record.s, CAST(entreprise_record.c AS INTEGER));
		END LOOP;
		RAISE NOTICE 'Insertion des entreprises ... done';

		-- premiers mots d'une entreprise (afin d'avoir edf, sncf, etc)
		RAISE NOTICE 'Insertion des premiers mots des entreprises';
		FOR entreprise_record IN
			SELECT nom, s, SUM(c1) as c FROM
				(SELECT substring(nom from '\w{3,}') as nom, substring(slug from '\w{3,}') as s, COUNT(0) as c1
					FROM entreprise JOIN experience USING(id_entreprise) GROUP BY nom, s) as foo
				GROUP BY s, nom
				ORDER BY c desc
		LOOP
			PERFORM insert_or_update_mot(entreprise_record.nom, entreprise_record.s, CAST(entreprise_record.c AS INTEGER));
		END LOOP;
	
		RAISE NOTICE 'Insertion des premiers mots des entreprises ... done';
		
		
		-- ville.nom
		RAISE NOTICE 'Insertion des villes';
		FOR ville_record IN
			SELECT nom, slugify(nom) as s, COUNT(0) as c
				FROM ville 
				GROUP BY s, nom
				ORDER BY c
		LOOP
			PERFORM insert_or_update_mot(ville_record.nom, ville_record.s, CAST(ville_record.c AS INTEGER));
		END LOOP;
		RAISE NOTICE 'Insertion des villes ... done';

		
		-- pays.nom
		RAISE NOTICE 'Insertion des pays';
		FOR pays_record IN
			SELECT nom, slugify(nom) as s, COUNT(0) as c
				FROM pays 
				GROUP BY s, nom
				ORDER BY c
		LOOP
			PERFORM insert_or_update_mot(pays_record.nom, pays_record.s, CAST(pays_record.c AS INTEGER));
		END LOOP;
		RAISE NOTICE 'Insertion des pays ... done';
		
		
    END;
$$ LANGUAGE plpgsql;