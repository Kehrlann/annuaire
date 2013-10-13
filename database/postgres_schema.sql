-----------------------------------------------------------------
-- This is the PostgreSQL schema definition for the database.  --
-- This version is typically used on production  encironments  --
-----------------------------------------------------------------

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: adresse; Type: TABLE; Schema: public; Owner: daniel; Tablespace: 
--

CREATE TABLE adresse (
    id_adresse integer NOT NULL,
    adresse text,
    code text,
    id_ville integer NOT NULL
);


ALTER TABLE public.adresse OWNER TO daniel;

--
-- Name: adresse_id_adresse_seq; Type: SEQUENCE; Schema: public; Owner: daniel
--

CREATE SEQUENCE adresse_id_adresse_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.adresse_id_adresse_seq OWNER TO daniel;

--
-- Name: adresse_id_adresse_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: daniel
--

ALTER SEQUENCE adresse_id_adresse_seq OWNED BY adresse.id_adresse;


--
-- Name: ancien; Type: TABLE; Schema: public; Owner: daniel; Tablespace: 
--

CREATE TABLE ancien (
    id_ancien integer NOT NULL,
    nom text NOT NULL,
    nom_slug text NOT NULL,
    prenom text,
    prenom_slug text,
    promo smallint NOT NULL,
    ecole character(1) NOT NULL,
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


ALTER TABLE public.ancien OWNER TO daniel;

--
-- Name: ancien_id_ancien_seq; Type: SEQUENCE; Schema: public; Owner: daniel
--

CREATE SEQUENCE ancien_id_ancien_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ancien_id_ancien_seq OWNER TO daniel;

--
-- Name: ancien_id_ancien_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: daniel
--

ALTER SEQUENCE ancien_id_ancien_seq OWNED BY ancien.id_ancien;


--
-- Name: asso_ancien_adresse; Type: TABLE; Schema: public; Owner: daniel; Tablespace: 
--

CREATE TABLE asso_ancien_adresse (
    id_ancien integer,
    id_adresse integer,
    actif boolean DEFAULT false
);


ALTER TABLE public.asso_ancien_adresse OWNER TO daniel;

--
-- Name: entreprise; Type: TABLE; Schema: public; Owner: daniel; Tablespace: 
--

CREATE TABLE entreprise (
    id_entreprise integer NOT NULL,
    nom text NOT NULL,
    slug text NOT NULL
);


ALTER TABLE public.entreprise OWNER TO daniel;

--
-- Name: entreprise_id_entreprise_seq; Type: SEQUENCE; Schema: public; Owner: daniel
--

CREATE SEQUENCE entreprise_id_entreprise_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.entreprise_id_entreprise_seq OWNER TO daniel;

--
-- Name: entreprise_id_entreprise_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: daniel
--

ALTER SEQUENCE entreprise_id_entreprise_seq OWNED BY entreprise.id_entreprise;


--
-- Name: experience; Type: TABLE; Schema: public; Owner: daniel; Tablespace: 
--

CREATE TABLE experience (
    id_experience integer NOT NULL,
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


ALTER TABLE public.experience OWNER TO daniel;

--
-- Name: experience_id_experience_seq; Type: SEQUENCE; Schema: public; Owner: daniel
--

CREATE SEQUENCE experience_id_experience_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.experience_id_experience_seq OWNER TO daniel;

--
-- Name: experience_id_experience_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: daniel
--

ALTER SEQUENCE experience_id_experience_seq OWNED BY experience.id_experience;


--
-- Name: inscription; Type: TABLE; Schema: public; Owner: daniel; Tablespace: 
--

CREATE TABLE inscription (
    id_inscription integer NOT NULL,
    id_ancien integer NOT NULL,
    password text NOT NULL,
    date_inscription date NOT NULL,
    code_activation text NOT NULL
);


ALTER TABLE public.inscription OWNER TO daniel;

--
-- Name: inscription_id_inscription_seq; Type: SEQUENCE; Schema: public; Owner: daniel
--

CREATE SEQUENCE inscription_id_inscription_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.inscription_id_inscription_seq OWNER TO daniel;

--
-- Name: inscription_id_inscription_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: daniel
--

ALTER SEQUENCE inscription_id_inscription_seq OWNED BY inscription.id_inscription;


--
-- Name: pays; Type: TABLE; Schema: public; Owner: daniel; Tablespace: 
--

CREATE TABLE pays (
    id_pays integer NOT NULL,
    nom text NOT NULL
);


ALTER TABLE public.pays OWNER TO daniel;

--
-- Name: pays_id_pays_seq; Type: SEQUENCE; Schema: public; Owner: daniel
--

CREATE SEQUENCE pays_id_pays_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pays_id_pays_seq OWNER TO daniel;

--
-- Name: pays_id_pays_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: daniel
--

ALTER SEQUENCE pays_id_pays_seq OWNED BY pays.id_pays;


--
-- Name: s_id_photo; Type: SEQUENCE; Schema: public; Owner: daniel
--

CREATE SEQUENCE s_id_photo
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.s_id_photo OWNER TO daniel;

--
-- Name: utilisateur; Type: TABLE; Schema: public; Owner: daniel; Tablespace: 
--

CREATE TABLE utilisateur (
    id_utilisateur integer NOT NULL,
    id_ancien integer,
    mail text NOT NULL,
    password text NOT NULL
);


ALTER TABLE public.utilisateur OWNER TO daniel;

--
-- Name: utilisateur_id_utilisateur_seq; Type: SEQUENCE; Schema: public; Owner: daniel
--

CREATE SEQUENCE utilisateur_id_utilisateur_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.utilisateur_id_utilisateur_seq OWNER TO daniel;

--
-- Name: utilisateur_id_utilisateur_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: daniel
--

ALTER SEQUENCE utilisateur_id_utilisateur_seq OWNED BY utilisateur.id_utilisateur;


--
-- Name: ville; Type: TABLE; Schema: public; Owner: daniel; Tablespace: 
--

CREATE TABLE ville (
    id_ville integer NOT NULL,
    nom text NOT NULL,
    slug text NOT NULL,
    id_pays integer NOT NULL
);


ALTER TABLE public.ville OWNER TO daniel;

--
-- Name: ville_id_ville_seq; Type: SEQUENCE; Schema: public; Owner: daniel
--

CREATE SEQUENCE ville_id_ville_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ville_id_ville_seq OWNER TO daniel;

--
-- Name: ville_id_ville_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: daniel
--

ALTER SEQUENCE ville_id_ville_seq OWNED BY ville.id_ville;


--
-- Name: id_adresse; Type: DEFAULT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY adresse ALTER COLUMN id_adresse SET DEFAULT nextval('adresse_id_adresse_seq'::regclass);


--
-- Name: id_ancien; Type: DEFAULT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY ancien ALTER COLUMN id_ancien SET DEFAULT nextval('ancien_id_ancien_seq'::regclass);


--
-- Name: id_entreprise; Type: DEFAULT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY entreprise ALTER COLUMN id_entreprise SET DEFAULT nextval('entreprise_id_entreprise_seq'::regclass);


--
-- Name: id_experience; Type: DEFAULT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY experience ALTER COLUMN id_experience SET DEFAULT nextval('experience_id_experience_seq'::regclass);


--
-- Name: id_inscription; Type: DEFAULT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY inscription ALTER COLUMN id_inscription SET DEFAULT nextval('inscription_id_inscription_seq'::regclass);


--
-- Name: id_pays; Type: DEFAULT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY pays ALTER COLUMN id_pays SET DEFAULT nextval('pays_id_pays_seq'::regclass);


--
-- Name: id_utilisateur; Type: DEFAULT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY utilisateur ALTER COLUMN id_utilisateur SET DEFAULT nextval('utilisateur_id_utilisateur_seq'::regclass);


--
-- Name: id_ville; Type: DEFAULT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY ville ALTER COLUMN id_ville SET DEFAULT nextval('ville_id_ville_seq'::regclass);


--
-- Name: adresse_pkey; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY adresse
    ADD CONSTRAINT adresse_pkey PRIMARY KEY (id_adresse);


--
-- Name: ancien_pkey; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY ancien
    ADD CONSTRAINT ancien_pkey PRIMARY KEY (id_ancien);


--
-- Name: asso_ancien_adresse_id_adresse_key; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY asso_ancien_adresse
    ADD CONSTRAINT asso_ancien_adresse_id_adresse_key UNIQUE (id_adresse);


--
-- Name: entreprise_pkey; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY entreprise
    ADD CONSTRAINT entreprise_pkey PRIMARY KEY (id_entreprise);


--
-- Name: experience_id_adresse_key; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY experience
    ADD CONSTRAINT experience_id_adresse_key UNIQUE (id_adresse);


--
-- Name: experience_id_experience_linkedin_key; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY experience
    ADD CONSTRAINT experience_id_experience_linkedin_key UNIQUE (id_experience_linkedin);


--
-- Name: experience_pkey; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY experience
    ADD CONSTRAINT experience_pkey PRIMARY KEY (id_experience);


--
-- Name: inscription_id_ancien_key; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY inscription
    ADD CONSTRAINT inscription_id_ancien_key UNIQUE (id_ancien);


--
-- Name: inscription_pkey; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY inscription
    ADD CONSTRAINT inscription_pkey PRIMARY KEY (id_inscription);


--
-- Name: pays_nom_key; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY pays
    ADD CONSTRAINT pays_nom_key UNIQUE (nom);


--
-- Name: pays_pkey; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY pays
    ADD CONSTRAINT pays_pkey PRIMARY KEY (id_pays);


--
-- Name: utilisateur_id_ancien_key; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY utilisateur
    ADD CONSTRAINT utilisateur_id_ancien_key UNIQUE (id_ancien);


--
-- Name: utilisateur_mail_key; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY utilisateur
    ADD CONSTRAINT utilisateur_mail_key UNIQUE (mail);


--
-- Name: utilisateur_pkey; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY utilisateur
    ADD CONSTRAINT utilisateur_pkey PRIMARY KEY (id_utilisateur);


--
-- Name: ville_nom_id_pays_key; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY ville
    ADD CONSTRAINT ville_nom_id_pays_key UNIQUE (nom, id_pays);


--
-- Name: ville_pkey; Type: CONSTRAINT; Schema: public; Owner: daniel; Tablespace: 
--

ALTER TABLE ONLY ville
    ADD CONSTRAINT ville_pkey PRIMARY KEY (id_ville);


--
-- Name: adresse_id_ville_fkey; Type: FK CONSTRAINT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY adresse
    ADD CONSTRAINT adresse_id_ville_fkey FOREIGN KEY (id_ville) REFERENCES ville(id_ville);


--
-- Name: asso_ancien_adresse_id_adresse_fkey; Type: FK CONSTRAINT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY asso_ancien_adresse
    ADD CONSTRAINT asso_ancien_adresse_id_adresse_fkey FOREIGN KEY (id_adresse) REFERENCES adresse(id_adresse);


--
-- Name: asso_ancien_adresse_id_ancien_fkey; Type: FK CONSTRAINT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY asso_ancien_adresse
    ADD CONSTRAINT asso_ancien_adresse_id_ancien_fkey FOREIGN KEY (id_ancien) REFERENCES ancien(id_ancien);


--
-- Name: experience_id_adresse_fkey; Type: FK CONSTRAINT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY experience
    ADD CONSTRAINT experience_id_adresse_fkey FOREIGN KEY (id_adresse) REFERENCES adresse(id_adresse);


--
-- Name: experience_id_ancien_fkey; Type: FK CONSTRAINT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY experience
    ADD CONSTRAINT experience_id_ancien_fkey FOREIGN KEY (id_ancien) REFERENCES ancien(id_ancien);


--
-- Name: experience_id_entreprise_fkey; Type: FK CONSTRAINT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY experience
    ADD CONSTRAINT experience_id_entreprise_fkey FOREIGN KEY (id_entreprise) REFERENCES entreprise(id_entreprise);


--
-- Name: inscription_id_ancien_fkey; Type: FK CONSTRAINT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY inscription
    ADD CONSTRAINT inscription_id_ancien_fkey FOREIGN KEY (id_ancien) REFERENCES ancien(id_ancien);


--
-- Name: utilisateur_id_ancien_fkey; Type: FK CONSTRAINT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY utilisateur
    ADD CONSTRAINT utilisateur_id_ancien_fkey FOREIGN KEY (id_ancien) REFERENCES ancien(id_ancien);


--
-- Name: ville_id_pays_fkey; Type: FK CONSTRAINT; Schema: public; Owner: daniel
--

ALTER TABLE ONLY ville
    ADD CONSTRAINT ville_id_pays_fkey FOREIGN KEY (id_pays) REFERENCES pays(id_pays);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

