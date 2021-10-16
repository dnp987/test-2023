select * from dealers order by Name;

select * from dealers where ID like '%Chrysler';

delete from dealers;

# alter table dealers modify column Make varchar(100)  after ID; # move a column within a table

delete from prices;
alter table prices auto_increment = 1;