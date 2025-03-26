--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;


--
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION vector IS 'vector data type and ivfflat and hnsw access methods';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: image_embeddings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.image_embeddings (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name text NOT NULL,
    embeddings public.vector NOT NULL
);


ALTER TABLE public.image_embeddings OWNER TO postgres;

--
-- Name: image_embeddings image_embeddings_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.image_embeddings
    ADD CONSTRAINT image_embeddings_pk PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

