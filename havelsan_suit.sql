PGDMP     "                     |            havelsan_suit    15.6    15.6     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    40960    havelsan_suit    DATABASE     �   CREATE DATABASE havelsan_suit WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Turkish_T�rkiye.1254';
    DROP DATABASE havelsan_suit;
                postgres    false            �            1259    40961    users    TABLE     g  CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    password character varying(120) NOT NULL,
    sys_role integer NOT NULL,
    email character varying(250) NOT NULL,
    address character varying(250) NOT NULL,
    firstname character varying(250),
    lastname character varying(250),
    phone numeric
);
    DROP TABLE public.users;
       public         heap    postgres    false            �          0    40961    users 
   TABLE DATA           m   COPY public.users (id, username, password, sys_role, email, address, firstname, lastname, phone) FROM stdin;
    public          postgres    false    214   �       e           2606    40965    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    214            g           2606    40967    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public            postgres    false    214            �   �   x�]�A�0E��Ø�2�;51.��1!�4H,մ`��
�g��KD0������%
��jUu�b��g��z�{yի�4�LO���� ]l� 	�)�#���BBZ�	�P�^!��ݾ���R6��sa}1H�q@z>�u\q����d�RC�hbK��N���p��>
�H��@��?��k��a�	c�D�b)     