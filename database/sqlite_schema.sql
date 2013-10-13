-------------------------------------------------------------
-- This is the SQLite schema definition for the database.  --
-- It does not contain constrains other than "NOT NULL".   --
-------------------------------------------------------------
CREATE TABLE adresse (
    id_adresse integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    adresse text,
    code text,
    id_ville integer NOT NULL
);
CREATE TABLE ancien (
    id_ancien integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    nom text NOT NULL,
    nom_slug text NOT NULL,
    prenom text,
    prenom_slug text,
    promo smallint NOT NULL,
    ecole char(1) NOT NULL,
    mail_asso text,
    mail_perso text,
    site text,
    telephone text,
    mobile text,
    photo text,
    diplome text,
    delegue boolean DEFAULT false,
    cotisant boolean DEFAULT false,
    minicv text,
    id_linkedin text,
    url_linkedin text,
    date_update date
);
CREATE TABLE asso_ancien_adresse (
    id_ancien integer,
    id_adresse integer,
    actif boolean DEFAULT false
);
CREATE TABLE entreprise (
    id_entreprise integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    nom text NOT NULL,
    slug text NOT NULL
);
CREATE TABLE experience (
    id_experience integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    id_adresse integer,
    id_entreprise integer,
    id_ancien integer NOT NULL,
    debut date,
    fin date,
    poste text,
    description text,
    actif boolean DEFAULT false,
    telephone text,
    mobile text,
    fax text,
    mail text,
    site text,
    id_experience_linkedin text
);
CREATE TABLE pays (
    id_pays integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    nom text NOT NULL
);
CREATE TABLE utilisateur (
    id_utilisateur integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    id_ancien integer,
    mail text NOT NULL,
    password text NOT NULL
);
CREATE TABLE ville (
    id_ville integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    nom text NOT NULL,
    slug text NOT NULL,
    id_pays integer NOT NULL
);
CREATE TABLE inscription (
  id_inscription integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  id_ancien integer NOT NULL,
  password text NOT NULL,
  date_inscription date NOT NULL,
  code_activation text NOT NULL
);
