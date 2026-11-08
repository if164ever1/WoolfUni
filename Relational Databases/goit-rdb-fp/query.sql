/*1. Create a schema
======================================================================================================================================================
*/
create schema pandemic;
use pandemic;

/*
2. Normalize table to 3NF
======================================================================================================================================================
*/
-- create a table for countries
create table countries(
	id int auto_increment primary key,
    Entity varchar(255),
    Code varchar(10)
);

insert into countries(Entity, Code)
select distinct Entity, Code
from infectious_cases;

-- create table of sickness
create table infectious_cases_norm(
	id int auto_increment primary key,
    country_id int,
    year int,
    Number_yaws double,
    polio_cases double,
    cases_guinea_worm double,
    Number_rabies double,
    Number_malaria double,
    Number_hiv double,
    Number_tuberculosis double,
    Number_smallpox double,
    Number_cholera_cases double,
    foreign key (country_id) references countries(id)
);

-- insert into table
insert into infectious_cases_norm(
	country_id, year, Number_yaws, polio_cases, cases_guinea_worm,
    Number_rabies, Number_malaria, Number_hiv, Number_tuberculosis, 
    Number_smallpox, Number_cholera_cases
)
select 
	c.id, t.year, 
    nullif(t.Number_yaws, '') as Number_yaws,
    nullif(t.polio_cases, '') as polio_cases,
    nullif(t.cases_guinea_worm, '') as cases_guinea_worm,
    nullif(t.Number_rabies, '') as Number_rabies,
    nullif(t.Number_malaria, '') as Number_malaria,
    nullif(t.Number_hiv, '') as Number_hiv,
    nullif(t.Number_tuberculosis, '') as Number_tuberculosis, 
    nullif(t.Number_smallpox, '') as Number_smallpox,
    nullif(t.Number_cholera_cases, '') as Number_cholera_cases
from infectious_cases t
join countries c on t.Entity = c.Entity;

-- check count of rows
select count(*) from infectious_cases;

/*
3. Analize data
======================================================================================================================================================
*/
select
	c.Entity,
    c.Code,
    avg(n.Number_rabies) as avg_rabies,
    min(n.Number_rabies) as min_rabies,
    max(n.Number_rabies) as max_rabies,
    sum(n.Number_rabies) as sum_rabies
from infectious_cases_norm n
join countries c on n.country_id = c.id
where n.Number_rabies is not null and n.Number_rabies != ''
group by c.Entity, c.Code
order by avg_rabies desc
limit 10;

/*
4. Years difference
======================================================================================================================================================
*/
select 
	year,
    makedate(year, 1) as first_jan_date,
    curdate() as current_date_val,
    timestampdiff(year, makedate(year, 1), curdate()) as year_diff
from infectious_cases_norm
limit 10;

/*
5. Own function
======================================================================================================================================================
*/
drop function if exists CalculateYearDiff;

DELIMITER //

create function CalculateYearDiff(input_year int)
returns int
deterministic
begin
	declare result int;
    set result = timestampdiff(year, makedate(input_year, 1), curdate());
    return result;
end //

DELIMITER ;

select
	year, 
    CalculateYearDiff(year) as year_diff_func
from infectious_cases_norm
limit 10;