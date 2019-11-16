
-- Drop table

-- DROP TABLE public.link;

CREATE TABLE public.link (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	link varchar NULL DEFAULT true,
	estado bool NULL,
	nombre varchar NULL,
	autor varchar NULL
);
CREATE UNIQUE INDEX link_link_idx ON public.link (link);
CREATE UNIQUE INDEX links_id_idx ON public.link (id);



-- Drop table

-- DROP TABLE public.precio;

CREATE TABLE public.precio (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	idlink int4 NOT NULL,
	precio int4 NOT NULL,
	fecha date NULL,
	nuevo bool NULL
);
CREATE UNIQUE INDEX precios_id_idx ON public.precio USING btree (id);


-- Drop table

-- DROP TABLE public.usuario_link;

CREATE TABLE public.usuario_link (
	idusuario int4 NULL,
	idlink int4 NULL,
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY
);
CREATE UNIQUE INDEX usuario_link_idlink_idx ON public.usuario_link (idlink,idusuario);
CREATE UNIQUE INDEX usuario_link_id_idx ON public.usuario_link (id);




-- Drop table

-- DROP TABLE public.usuariotelegram;

CREATE TABLE public.usuariotelegram (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	idusuario int4 NOT NULL,
	estado bool NULL,
	idchat int4 NULL
);
CREATE UNIQUE INDEX usuariotelegram_idchat_idx ON public.usuariotelegram (idchat,idusuario);
CREATE UNIQUE INDEX usuariotelegram_id_idx ON public.usuariotelegram (id);

