# CheckATradeCode

Install postgresql in system and setup password to access postgresql

Give postgre password in line 10 and 39 of checkATrade.py program

Run below commands in postgresql query tool

1. drop table if exists public.run
2. drop table if exists public.records
3. CREATE TABLE public.run
                     (
                         runid SERIAL PRIMARY KEY,
                         run_time timestamp	,
                         records integer)
 4.CREATE TABLE public.records(
                     name char(100),
                     height integer,
                     mass integer,
                     hair_color char(100),
                     skin_color char(100),
                     eye_color char(100),
                     birth_year char(100),
                     gender char(10),
                     homeworld char(100),
                     films char(100),
                     species json,
                     vehicles json,
                     starships json,
                     created char(100),
                     edited char(100),
                     url char(100))

Run python program.
