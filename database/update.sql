DROP TABLE inscription CASCADE;

ALTER TABLE ancien ADD CONSTRAINT id_linkedin_unique UNIQUE(id_linkedin);
ALTER TABLE utilisateur ADD COLUMN actif BOOL NOT NULL DEFAULT FALSE;
UPDATE utilisateur SET actif=TRUE;

ALTER TABLE ancien ADD COLUMN nouveau BOOL NOT NULL DEFAULT FALSE;
ALTER TABLE ancien ALTER COLUMN nouveau SET DEFAULT TRUE;
ALTER TABLE ancien ADD COLUMN actif BOOL NOT NULL DEFAULT TRUE;
ALTER TABLE ancien ADD COLUMN bloque BOOL NOT NULL DEFAULT FALSE;


ALTER TABLE utilisateur ADD COLUMN admin BOOL NOT NULL DEFAULT FALSE;