--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.4
-- Dumped by pg_dump version 9.6.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: increment_pkey; Type: SEQUENCE; Schema: public; Owner: rickynyairo
--

CREATE SEQUENCE increment_pkey
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE increment_pkey OWNER TO rickynyairo;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: answers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE answers (
    answer_id numeric DEFAULT nextval('increment_pkey'::regclass) NOT NULL,
    question_id numeric NOT NULL,
    user_id numeric NOT NULL,
    text character varying(1000) NOT NULL,
    up_votes numeric DEFAULT 0,
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
    user_preferred boolean DEFAULT false NOT NULL
);


ALTER TABLE answers OWNER TO postgres;

--
-- Name: TABLE answers; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE answers IS 'This tables stores the answers given by users on the platform';


--
-- Name: comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE comments (
    comment_id numeric DEFAULT nextval('increment_pkey'::regclass) NOT NULL,
    answer_id numeric NOT NULL,
    user_id numeric NOT NULL,
    text character varying(200) NOT NULL,
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
);


ALTER TABLE comments OWNER TO postgres;

--
-- Name: questions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE questions (
    question_id numeric DEFAULT nextval('increment_pkey'::regclass) NOT NULL,
    user_id numeric NOT NULL,
    text character varying(200) NOT NULL,
    description character varying(1000),
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
);


ALTER TABLE questions OWNER TO postgres;

--
-- Name: TABLE questions; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE questions IS 'This tables stores the details of a question asked on the platform';


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE users (
    user_id numeric DEFAULT nextval('increment_pkey'::regclass) NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50),
    username character varying(50) NOT NULL,
    email character varying(50),
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
    password character varying(500) NOT NULL
);


ALTER TABLE users OWNER TO postgres;

--
-- Name: TABLE users; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE users IS 'Store user details';


--
-- Data for Name: answers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY answers (answer_id, question_id, user_id, text, up_votes, date_created, user_preferred) FROM stdin;



--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY comments (comment_id, answer_id, user_id, text, date_created) FROM stdin;



--
-- Name: increment_pkey; Type: SEQUENCE SET; Schema: public; Owner: rickynyairo
--

SELECT pg_catalog.setval('increment_pkey', 4, true);


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY questions (question_id, user_id, text, description, date_created) FROM stdin;



--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (user_id, first_name, last_name, username, email, date_created, password) FROM stdin;



--
-- Name: answers answers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answers
    ADD CONSTRAINT answers_pkey PRIMARY KEY (answer_id);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (comment_id);


--
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (question_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: comments answers_answer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT answers_answer_id_fkey FOREIGN KEY (answer_id) REFERENCES answers(answer_id) ON UPDATE CASCADE;


--
-- Name: answers questions_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answers
    ADD CONSTRAINT questions_question_id_fkey FOREIGN KEY (question_id) REFERENCES questions(question_id) ON UPDATE CASCADE NOT VALID;


--
-- Name: questions users_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY questions
    ADD CONSTRAINT users_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE NOT VALID;


--
-- Name: answers users_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answers
    ADD CONSTRAINT users_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE NOT VALID;


--
-- Name: comments users_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT users_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE;


--
-- PostgreSQL database dump complete
--

