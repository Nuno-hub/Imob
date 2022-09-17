--#########################################
--###  Create table script for imoveis: ###
--#########################################
CREATE TABLE IF NOT EXISTS imoveis
 (num_carregamento INTEGER, 
 id_anuncio INTEGER,
 ref_interna TEXT, 
 titulo TEXT, 
 tipologia TEXT, 
 preco REAL, 
 area_util REAL, 
 area_bruta REAL, 
 area_terreno REAL,
 zona TEXT, 
 distrito TEXT, 
 concelho TEXT, 
 freguesia TEXT, 
 data_ins_anuncio TEXT, 
 data_alt_anuncio TEXT, 
 --site TEXT, 
 url TEXT, 
 agencia TEXT, 
 descricao TEXT, 
 estado TEXT, 
 ano_construcao INTEGER, 
 wc TEXT, 
 cert_energetico TEXT, 
 uso TEXT, 
 tipo_imovel TEXT,
 lic_utilizacao TEXT,
 data_carregamento_bd text,
 CONSTRAINT PK_IMOVEIS PRIMARY KEY (num_carregamento, id_anuncio));

--#########################################
--###  Create table script for control: ###
--#########################################
CREATE TABLE IF NOT EXISTS loadcontrol
 (num_carregamento INTEGER, 
 siteimob TEXT,
 datetime_start TEXT,
 datetime_stop TEXT, 
 details TEXT,
 CONSTRAINT PK_LOADCONTROL PRIMARY KEY (num_carregamento));


-- Aggregated table
CREATE table imoveis_agg as SELECT * from 
(select count(*) num_reg, round(avg(comp.preco/comp.area_util), 2) preco_m2,
comp.distrito, comp.concelho, comp.freguesia, comp.uso, comp.tipologia,
comp.tipo_imovel
FROM imoveis comp
WHERE comp.num_carregamento=1
AND comp.uso = 'comprar'
--AND comp.tipo_imovel='apartamento' 
GROUP BY comp.distrito, comp.concelho, comp.freguesia, comp.uso, comp.tipologia,
IFNULL(comp.tipo_imovel, 'null')
UNION ALL
select count(*) num_reg, round(avg(arr.preco/arr.area_util), 2) preco_m2, 
arr.distrito, arr.concelho, arr.freguesia, arr.uso, arr.tipologia,
arr.tipo_imovel
FROM imoveis arr
WHERE arr.num_carregamento=1
AND arr.uso = 'arrendar'
--AND arr.tipo_imovel='apartamento' 
GROUP BY arr.distrito, arr.concelho, arr.freguesia, arr.uso, arr.tipologia,
arr.tipo_imovel);



-- KPI for profitability
SELECT arr.preco_m2 preco_arrendar_m2, comp.preco_m2 preco_comprar_m2, 
round((comp.preco_m2-arr.preco_m2*12*15), 2) Profit_KPI15,
round((comp.preco_m2-arr.preco_m2*12*10), 2) Profit_KPI10,
arr.num_reg num_imoveis_arrendar, comp.num_reg num_imoveis_comprar,
comp.distrito, comp.concelho, comp.freguesia, 
comp.tipologia, comp.tipo_imovel
FROM imoveis_agg comp, imoveis_agg arr
WHERE comp.num_carregamento = arr.num_carregamento
AND comp.distrito = arr.distrito
AND comp.concelho = arr.concelho
AND comp.freguesia = arr.freguesia
AND comp.uso = 'comprar'
AND arr.uso = 'arrendar'
AND comp.tipologia = arr.tipologia
AND comp.tipo_imovel = arr.tipo_imovel
AND comp.num_carregamento = 1
AND comp.concelho = 'Lisboa' 
AND comp.tipologia in ('T0', 'T1', 'T2', 'T3')
ORDER BY Profit_KPI10;

