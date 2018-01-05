-- Methode qui, pour un ancien donne (defini par son id_ancien),
-- va chercher son nom, prenom, ecole, promo, ville, pays et entreprises
-- et cree un tsvector approprie avec ces infos
CREATE OR REPLACE FUNCTION
    create_tsvector_by_id_ancien(input_id INTEGER) RETURNS tsvector
AS $$
    DECLARE
		ancien_record RECORD;
		adresse_record RECORD;
        entreprise_record RECORD;
        res tsvector;
    BEGIN
		
		-- Ajouter au fulltext prenom, nom, ecole et promo de l'ancien
		SELECT a.prenom, a.nom, a.ecole, a.promo, e.nom as ecole_nom
			FROM ancien as a
				JOIN ecole as e ON a.ecole = e.id_ecole
			INTO ancien_record 
			WHERE id_ancien = input_id;
		
		res := setweight(to_tsvector('french', slugify(coalesce(ancien_record.prenom, ''))), 'A')
			|| setweight(to_tsvector('french', slugify(coalesce(ancien_record.nom, ''))), 'A')
			|| setweight(to_tsvector('french', ancien_record.ecole_nom), 'B')
			|| setweight(to_tsvector('french', CAST(ancien_record.promo AS TEXT)), 'B')
			|| setweight(to_tsvector('french', ancien_record.ecole || substring(CAST(ancien_record.promo AS TEXT) FROM 3 FOR 2)), 'B');
		
		-- Ajouter la ville et le pays de l'adresse (adresse active)
		SELECT v.nom as ville, p.nom as pays
			FROM asso_ancien_adresse as aaa
				JOIN adresse as ad ON aaa.id_ancien = input_id AND aaa.id_adresse = ad.id_adresse AND aaa.actif is TRUE 
				JOIN ville as v ON v.id_ville = ad.id_ville
				JOIN pays as p ON p.id_pays = v.id_pays
			INTO adresse_record;
			
		IF adresse_record IS NOT NULL THEN
			res := res
				|| setweight(to_tsvector('french', slugify(coalesce(adresse_record.ville, ''))), 'D')
				|| setweight(to_tsvector('french', slugify(coalesce(adresse_record.pays, ''))), 'D');				
		END IF;
		
		-- Ajouter l'entreprise, le poste, la ville et le pays des experiences pro
        FOR entreprise_record IN
            SELECT ex.poste, ex.description, ent.nom, v.nom as ville, p.nom as pays
                FROM experience as ex
                    JOIN entreprise as ent ON ex.id_entreprise = ent.id_entreprise
					LEFT OUTER JOIN adresse as ad ON ex.id_adresse = ad.id_adresse
					LEFT OUTER JOIN ville as v ON v.id_ville = ad.id_ville
					LEFT OUTER JOIN pays as p ON p.id_pays = v.id_pays
                WHERE ex.id_ancien=input_id
        LOOP
			res := res
				|| setweight(to_tsvector('french', slugify(coalesce(entreprise_record.poste, ''))), 'C')
				|| setweight(to_tsvector('french', slugify(coalesce(entreprise_record.nom, ''))), 'B')
        || setweight(to_tsvector('french', slugify(coalesce(entreprise_record.description, ''))), 'C')
				|| setweight(to_tsvector('french', slugify(coalesce(entreprise_record.ville, ''))), 'D')
				|| setweight(to_tsvector('french', slugify(coalesce(entreprise_record.pays, ''))), 'D');
        END LOOP;

        RETURN res;
        
    END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION
  reset_fulltext_by_id_ancien(id INTEGER) RETURNS VOID
AS $$
  BEGIN
    UPDATE ancien SET fulltext = create_tsvector_by_id_ancien(id) WHERE id_ancien = id;
  END;
$$ LANGUAGE plpgsql;


-- Methode pour créer les tsvectors pour tous les anciens
CREATE OR REPLACE FUNCTION
    index_all_anciens() RETURNS INT
AS $$
	DECLARE
		id INTEGER;
    BEGIN
		-- Mettre à jour tous les fulltext
        FOR id IN
            SELECT id_ancien as id
                FROM ancien
				ORDER BY id_ancien asc
        LOOP
			RAISE NOTICE 'Traitement ancien %', id; 
			-- Mise à jour fulltext
			UPDATE ancien SET fulltext = create_tsvector_by_id_ancien(id) WHERE id_ancien = id;
        END LOOP;
    RETURN 0;
    END;
$$ LANGUAGE plpgsql;
