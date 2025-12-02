--
-- PostgreSQL database dump
--

\restrict BKm6eVwBObVyevniKC8FgDfkNLQvHDMlYl7l2pcHyXXnskOl4aRfB8HDC6NW8sN

-- Dumped from database version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: banks; Type: TABLE; Schema: public; Owner: db_user
--

CREATE TABLE public.banks (
    bank_id integer NOT NULL,
    bank_name character varying(255) NOT NULL,
    app_name character varying(255)
);


ALTER TABLE public.banks OWNER TO db_user;

--
-- Name: banks_bank_id_seq; Type: SEQUENCE; Schema: public; Owner: db_user
--

CREATE SEQUENCE public.banks_bank_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.banks_bank_id_seq OWNER TO db_user;

--
-- Name: banks_bank_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: db_user
--

ALTER SEQUENCE public.banks_bank_id_seq OWNED BY public.banks.bank_id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: db_user
--

CREATE TABLE public.reviews (
    review_id integer NOT NULL,
    bank_id integer,
    review_text text,
    rating integer,
    review_date timestamp without time zone,
    sentiment_label character varying(50),
    sentiment_score double precision,
    source character varying(50)
);


ALTER TABLE public.reviews OWNER TO db_user;

--
-- Name: reviews_review_id_seq; Type: SEQUENCE; Schema: public; Owner: db_user
--

CREATE SEQUENCE public.reviews_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reviews_review_id_seq OWNER TO db_user;

--
-- Name: reviews_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: db_user
--

ALTER SEQUENCE public.reviews_review_id_seq OWNED BY public.reviews.review_id;


--
-- Name: banks bank_id; Type: DEFAULT; Schema: public; Owner: db_user
--

ALTER TABLE ONLY public.banks ALTER COLUMN bank_id SET DEFAULT nextval('public.banks_bank_id_seq'::regclass);


--
-- Name: reviews review_id; Type: DEFAULT; Schema: public; Owner: db_user
--

ALTER TABLE ONLY public.reviews ALTER COLUMN review_id SET DEFAULT nextval('public.reviews_review_id_seq'::regclass);


--
-- Name: banks banks_pkey; Type: CONSTRAINT; Schema: public; Owner: db_user
--

ALTER TABLE ONLY public.banks
    ADD CONSTRAINT banks_pkey PRIMARY KEY (bank_id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: db_user
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (review_id);


--
-- Name: reviews reviews_bank_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: db_user
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_bank_id_fkey FOREIGN KEY (bank_id) REFERENCES public.banks(bank_id);


--
-- PostgreSQL database dump complete
--

\unrestrict BKm6eVwBObVyevniKC8FgDfkNLQvHDMlYl7l2pcHyXXnskOl4aRfB8HDC6NW8sN

