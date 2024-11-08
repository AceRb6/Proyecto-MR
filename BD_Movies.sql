PGDMP  :    
            
    |            Movies    16.3    16.3 #    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    19181    Movies    DATABASE     {   CREATE DATABASE "Movies" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Spain.1252';
    DROP DATABASE "Movies";
                postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                pg_database_owner    false            �           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                   pg_database_owner    false    4            �            1259    19217 	   directors    TABLE     e   CREATE TABLE public.directors (
    id integer NOT NULL,
    director_name character varying(255)
);
    DROP TABLE public.directors;
       public         heap    postgres    false    4            �            1259    19216    directors_id_seq    SEQUENCE     �   CREATE SEQUENCE public.directors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.directors_id_seq;
       public          postgres    false    4    221            �           0    0    directors_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.directors_id_seq OWNED BY public.directors.id;
          public          postgres    false    220            �            1259    19193    genres    TABLE     ^   CREATE TABLE public.genres (
    id integer NOT NULL,
    genre_name character varying(50)
);
    DROP TABLE public.genres;
       public         heap    postgres    false    4            �            1259    19192    genres_id_seq    SEQUENCE     �   CREATE SEQUENCE public.genres_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.genres_id_seq;
       public          postgres    false    218    4            �           0    0    genres_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.genres_id_seq OWNED BY public.genres.id;
          public          postgres    false    217            �            1259    19201    movie_genres    TABLE     c   CREATE TABLE public.movie_genres (
    movie_id integer NOT NULL,
    genre_id integer NOT NULL
);
     DROP TABLE public.movie_genres;
       public         heap    postgres    false    4            �            1259    19183    movies    TABLE     B  CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying(255),
    vote_average double precision,
    keywords text,
    cast_ text,
    director_id integer,
    CONSTRAINT movies_vote_average_check CHECK (((vote_average >= (0)::double precision) AND (vote_average <= (10)::double precision)))
);
    DROP TABLE public.movies;
       public         heap    postgres    false    4            �            1259    19182    movies_id_seq    SEQUENCE     �   CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.movies_id_seq;
       public          postgres    false    216    4            �           0    0    movies_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;
          public          postgres    false    215            *           2604    19220    directors id    DEFAULT     l   ALTER TABLE ONLY public.directors ALTER COLUMN id SET DEFAULT nextval('public.directors_id_seq'::regclass);
 ;   ALTER TABLE public.directors ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    221    221            )           2604    19196 	   genres id    DEFAULT     f   ALTER TABLE ONLY public.genres ALTER COLUMN id SET DEFAULT nextval('public.genres_id_seq'::regclass);
 8   ALTER TABLE public.genres ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    218    218            (           2604    19186 	   movies id    DEFAULT     f   ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);
 8   ALTER TABLE public.movies ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215    216            �          0    19217 	   directors 
   TABLE DATA           6   COPY public.directors (id, director_name) FROM stdin;
    public          postgres    false    221   �%       �          0    19193    genres 
   TABLE DATA           0   COPY public.genres (id, genre_name) FROM stdin;
    public          postgres    false    218   �(       �          0    19201    movie_genres 
   TABLE DATA           :   COPY public.movie_genres (movie_id, genre_id) FROM stdin;
    public          postgres    false    219   q)       �          0    19183    movies 
   TABLE DATA           W   COPY public.movies (id, title, vote_average, keywords, cast_, director_id) FROM stdin;
    public          postgres    false    216   �+       �           0    0    directors_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.directors_id_seq', 118, true);
          public          postgres    false    220            �           0    0    genres_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.genres_id_seq', 280, true);
          public          postgres    false    217            �           0    0    movies_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.movies_id_seq', 118, true);
          public          postgres    false    215            5           2606    19224 %   directors directors_director_name_key 
   CONSTRAINT     i   ALTER TABLE ONLY public.directors
    ADD CONSTRAINT directors_director_name_key UNIQUE (director_name);
 O   ALTER TABLE ONLY public.directors DROP CONSTRAINT directors_director_name_key;
       public            postgres    false    221            7           2606    19222    directors directors_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.directors
    ADD CONSTRAINT directors_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.directors DROP CONSTRAINT directors_pkey;
       public            postgres    false    221            /           2606    19200    genres genres_genre_name_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.genres
    ADD CONSTRAINT genres_genre_name_key UNIQUE (genre_name);
 F   ALTER TABLE ONLY public.genres DROP CONSTRAINT genres_genre_name_key;
       public            postgres    false    218            1           2606    19198    genres genres_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.genres
    ADD CONSTRAINT genres_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.genres DROP CONSTRAINT genres_pkey;
       public            postgres    false    218            3           2606    19205    movie_genres movie_genres_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.movie_genres
    ADD CONSTRAINT movie_genres_pkey PRIMARY KEY (movie_id, genre_id);
 H   ALTER TABLE ONLY public.movie_genres DROP CONSTRAINT movie_genres_pkey;
       public            postgres    false    219    219            -           2606    19191    movies movies_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.movies DROP CONSTRAINT movies_pkey;
       public            postgres    false    216            9           2606    19211 '   movie_genres movie_genres_genre_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.movie_genres
    ADD CONSTRAINT movie_genres_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES public.genres(id) ON DELETE CASCADE;
 Q   ALTER TABLE ONLY public.movie_genres DROP CONSTRAINT movie_genres_genre_id_fkey;
       public          postgres    false    219    4657    218            :           2606    19206 '   movie_genres movie_genres_movie_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.movie_genres
    ADD CONSTRAINT movie_genres_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(id) ON DELETE CASCADE;
 Q   ALTER TABLE ONLY public.movie_genres DROP CONSTRAINT movie_genres_movie_id_fkey;
       public          postgres    false    4653    219    216            8           2606    19225    movies movies_director_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_director_id_fkey FOREIGN KEY (director_id) REFERENCES public.directors(id);
 H   ALTER TABLE ONLY public.movies DROP CONSTRAINT movies_director_id_fkey;
       public          postgres    false    221    216    4663            �   �  x�5TKr9]����R�����rٖ��T��+���i6�"���W�1�b:���������M��<��g�u���{2L^�h&X�>:֕�l<��y`ĭ��s:���dx��Y�Àa@6��_�3:+S���.W���@R��Q�z"�+|�z������`e/��]��4��4Q;����ڠ���'�H���s��B��\=�!�{gG]j�Lpo)�CڭTw7�7���]�N��p�I�z��L �ƽ.�7��+Z�.n�}+�>Ą�Tk�^>;����t�H9Wx��`���i$���ht���qGaB]R#��L�Z��=�.�7c-l�܎��ԣ�<�H�z��������8Q�e�+����[������$����/�����ZHc�nt2NW�ϵ'���R���|���{�U��=rkBb���;�[W�zu��Ls^�0]5��<�7r;]���aL��[���H�\��D��L�b;�����t��Ug,�YX���u!��
I��e�������fQ�]��Lb����ʎ��i�^ n��&������M=�I��Q�
���:�;Y�o2%��2�(����&W[OaK����)�J��]f�J��r��f���RԟH�4�8˄|���hM�lH"�z�[A��ÞS�L��3���g�c�/)Q����`%3n��X�U��[Yئ����ߌs'�F=\g�?y$8f���ی�^���?�7Z�� ��Q�      �   �   x�-�AN�0E�N�T���t�n�d3r�h��F��[���������u�ʹCo�$��qb�x[�/�S���$�(S�'�3O�S�w1+F;�g�f1-�w�%ϋUC�kI���o+�t���Ы䨼��<�J\j~摎��������X��?�Ej�\x���O������a�����D�      �   b  x�-�ǵ�0C�V1sLIL����\�-Q� �e�-{����|���R_�+��v�q���Cc��4������3�h�O�Sp�:,�Y�����&<����`2�.�l�(~�F?�{��a_���\o\o��xބ"p����\�� �yX�+���s��'>\�| 'g2HxM�e��I�r��x�u��|	��x	��g��ݘ$�N�֔����S7�C�!"�pߒ<��NS��_$8�:%u� �ZN�MG(��t'bG��~w��@�<�qd82rr'�N�Zu�� �@�2�f{�7���A�'�Y��p��YrL����HdP����^я�˰u>��p�r�$z����I�"GT�$iI�����$�����BO�8(
"�ǩPN��
i*��4���5�*��R�(Z���%EWV�.}��ʙ#��׋HhQ#�̦1���OS����ˆ���&�V�<4ِ��-�h1�B۴i�݄�P7q�;�K!쵱ml�A�����|�y`�;�|�yhޘC1����l��I����y��:�CƟa�w�H��~><��D���7�\���g{��ԃa��3h9�#�r�Q��ٵ���������      �      x��[Ms�8�=���9tЊb}W�aC���e��h�t�E��p�  U����бч��	�c�2ɒe�{#6vFVlYUD"����*���G�o�5�Q�>��R��CSi�?�❎3S�R��yUĕjUpq�t����.d�M��8̽	�QV�B��Vu.�u��>���;+��M�|-�h(���ʷ�e�_��̈́Z���\����鮌KS�Z�Vj��9��8w�yq�Jy�0ީJ7�Ҥ�+���<ҥ��y-��Hh]�ScR-��ӽ��o�.���۱Jk��&�����3�	һ���:��{;#����Y+.`������꣱�*y�f�C�H{c���'U���w�+1���ͅk&b��P�k���/�ґ�k���Z�d���Eʹ��Pk�]�Wb��)-K�5���0�Hݙ�/��q���w��O�Man�åX�6�|���W�旱*�\��OZ�j��M��p8���|�+�xma���Z1����j�V���:
��
, n���+�B��:^��/�k�v�ąY��0cu+nUK_�r�ɰ�pxQUb���x���� �	�R{y���ʛ��9L���af�7g��:�i��6u���8�3��y	B�[y���C�<���?�?����b}��%�������fb��Z�A*/c�	��x�)�B��Ftx��j���rE��O�[ۥ���]X����&��L�'Ϟ��
g,l���D9�}���wZL�[x#�����â�IAg�/X׽�t��i�aQ�h2$A�r?,����h�pe�Aa.��E�d[]"I�d(�LHr�X��(�5Rot��;���0���/���!�V�+xPQ�p��5E�E(�@�h�ʳ>��¤�c�.����Ե�g"4X�(<��ǻ;�
,���k��
q�>9 �̛�`<K`��U�G7�6�\$�(�#x�r��Re�g��w�Rp�\܃,R���쁻%����|��MQ�/�;*�UZvs�UEg��c�����Z��XL��Y��R���)��y!�q�L`�=}k�8�\C�<,R��t���uG�A�^׈���J�B���?���|G��S�]�+��ý5�=n&�J+3}ea3{e��0k&/L����!���C��'=G�Ȗ��+��wPgé��(a((!TB>9w�� E�6�������X��)��B�17ȧ*34���M����f�o/�G�Y�0N��L�s)T���/D�u[�ٸ�A��bԿ��נ` ��1��+���i��C� U��za2J��l^!w@�T1+�]�)��>���Y4CF��CʂE��݊�u(��B\a|D{���T�̑�@�
%�V)m�]�8u6�o�}��Y�܋�<.�;�1>����Xk-�ފ�=�7��haV�(��X��k���I٘d1f�w�n �k� d��z�_r����"�~�RU���?��O365��*���t/�\-N]x�k�U�/�2�J��J������!������_��Q"�$�4���D$zTD��X�����C��fH$�)�8* ��v���O�\�"��t��@���\nmv�*v���Wc31J�J�R���*Ex��.cy|KT���( �i�����5��o�U��k*@��� ̬\�fZ�L����
�i~��M~Z���"6���[�#��� ����8�C1�U�v���6i�6�Y�w��F�h,�<T��D�l��r�52pJ(�"V=nH�Pw�#nc�K��!�Ȅ�\Q��>���g;a�%T����_���ͩ�f����!Y�s�Љy��P�hX3h1�"0A!������ܥ�U��}Eq�[�σ�q\#L/Ժ1 ܳ�~E�r�6�
@�I4�"���+���0J������R�DU��ў�)6T��ziy�aa��CA��N��4�:�beױ�k��䤸�`䉎��M �ōYw���PA�q|�"��P���X�Y4"wAb�Ƈ�v������Fd)-nhG�6�t+��*�o2y��7�VB�KJk��<#-r�BD�R��]L��sG�
1�G#h�,Cf�'
z��?��с{?:E��\���8ړu%
7�Et�|��!+�Jv�����IST�]r�&2=m�/����p-hf������*����TX���(O�����G\j\E�YZ�5�Ba��%w
c &�|p�=-W��y�� �1�6I�
�J��D���K4��(�KX�U�7�$�F�h�M%,/[g�]�9BW9=�R*+ P�Vb�D���ԁ���S��᯿D��w�+ �N�X �����f4#L�R+ŷ�>��e���bO��0���Ҭ�{Y-oLfUU�,� ��tg\AZbw_\`�C���#)o3)�f4Ur"-��x����A����/��Di��昡*;jy���>LgT�'v�������(*oH
iH��0�O͈���(�ج�x�'��	L ��ii( k���KN����4����ם�i�	T3�W%9�ÙW�h�1�Dc�߮Ж�}��쐶��H;@7r< � :�ϭ�^�M'_}�WUm�_Q��0���uxj�\����V����h�S~�����)Ν͜e����cm�,KB���Qj,R�޵2�0�G~ n"V)냻;�w��g�~A+��Mͭ�SGM�4�̢1�t\�*>�
^H�X�,&�D��(| �e���o�����������Z���&��}����d�����V���x!N0(c#�B~$ސ7�	��GM��w��P�����w��򩲀m`a�LX�-�eo��B13�ψ�,c�����LZ��j�c��f��"�Ĺ�Ӝo�����d�$x50�o�?��4g�#���9^���FL�$�cmL��s�`�͢qm�����V�� �R&�ϻI��s�N�U��S-=8[nişw�:1��Kˠ��=�1ȝ�(jV+Ob�+1�aT�s>��� �����4m�*�t�:D�`O�!p5i�B��I=�i�Vns�gO�V���4��#c7�Z[�[h<��5��8�P宨�q�K�Ry��6�b������� ���]�e����*ST�X\�ao�=���8��DӾ�s�y�*괉�$�L���������
Y���P�;W�&���֔��or'�\��ʕF� 9�׭����bz�(��4�����?\�p#�{3a5�	j�.��}d�k�<L6A�b���l����� �OA�a.��H�P�t�Z���?��~�B�Ϣ�\�&�XA���9�L���� V��RЗkƹ ��j�/M�aM<=~�4)_��nY��=2馇6�I�!�(OP�xM� �.�A��V)9��&;�pģ���6Կi��?��%URt�F�7�`�{�/����;��?YA~�I���[��T����}��Y嗬��L(�v	S�EH��r�;�=]g��ZB��Pl6���\*t�>�� ��d�CmN�&���?|�$�)/La
Te��Z�k�DEp�;�� t5�rW�̭c� 4�uc!������1�A�o[�AaaIs�	��tMG�'ju��y��R�e�;z���p. �T��]/���E�S<R4v%�G� ��T��O���
��-�sa�Q4m:�y�qp �
�T�T���h��ڥ�+U����U2���f@�FL@�n6I�����z�m��lIw���_�~�q4�T�p2����]�����ۗm9�������3ܐ�����q�^NE�R����>�>JF"xr�}�������)Sg����U��k&J�R�M�'�#N%X�/�d!Y��wHg��;�k(�oSā��`4*���
�Q�N��L�bC �T᠎;@T
*1f:��*0�IS��w�3��47�̃Z�:�Y43R�)�l�e{H��S��̑���!�$T�T1�9���� ��u�L�D��7�c�PK+�[y���tM��]V�,�o���(_s�T+͈n���u�����^�~[�rW��TÑ���s;����յ���a�t͞��]��� �  G�4m�@��cʱI��փ��[�aw�H���{�PU�M;D�P���J���Quʢ��Os1D�D�d�X(�tF>�<|0XH�l��[*��ʩ��t�D�6|�[Ԝ ̮�E�82yŭ��~`&�:V0�bϒh6dJ6��]�Kj6�0b�	��X��?2��9fGh}����ڔ�����{�B��~O�w��T��l���+��k�K�X۾���R!6,5� N�M�]�7�<���=��7�+1 ���eE;�C����~�E]"P8-� �(��o\N�\�,�3G�c���h>w�W�8�~�MIYp6�f�^@��7ME���F" �����D�MRG�\����Z��(z�H[��2Ն$��i���U����K�[��&���i�:U��M���_YN�f�ҧ�_9:�����K7�ɋ�8|ŝ���57~%�8��+1d�:ڤ��+�c�����ū2g1x��E�}ߝ����?~፱���~�����[0��ċ?�Fv2��}�d��S�/|�"�^|��KfI��j�:~P0�}������?�?X�sj��A:ޙ�G�3�,f��z�N���NC�t�C~�H3�Z���Z_A���G���t�j ��:����S~!-%`G�$q����s;'�5�WL�����y��%�'�ʴ�� ���b����H-H��gQwS�	7�m��By�'�P��YZ�g�qAD)�3�M�+�{L�!�4q3�A��j�`umW>�K'W�yָ@�P��S��א�s�H���]��{a��R�M��m�Z?a�H5r���nSg�!7h������x�5�s�N$�ĭ����/�֨P%���A/���<�4ԖL(֒����r�户�>���n{����v>��)�f��*����_�p �\�i�B\��LWP&�#�|��ӎف�f�r�(�����AXяd~8<���������Q�^�d���~�;J	L�BΡ�n��x*�Tè��$\h9�^��	E���.q��H
.O�p(W`g�{�@�k_�Ձ�Cڱ#�A�	��G��K��A>�SE}���_~yS*�׻:�v�P!�����iK��ǥ	'�2k5��t��`�S�G�'`i �C����aI?_@��(�협SA�ݦ��VQ+��k��׀��[�t��!J|E3�G݋�� �ʙ     