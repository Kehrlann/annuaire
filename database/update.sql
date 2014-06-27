DROP TABLE inscription CASCADE;

ALTER TABLE ancien ADD CONSTRAINT id_linkedin_unique UNIQUE(id_linkedin);
ALTER TABLE utilisateur ADD COLUMN actif BOOL NOT NULL DEFAULT FALSE;
UPDATE utilisateur SET actif=TRUE;