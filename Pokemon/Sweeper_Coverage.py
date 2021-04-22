import os
import pandas
import sqlalchemy


def run():
    os.system('clear')
    os.chdir('../../')
    os.chdir('./config')
    conf = pandas.read_csv('config.csv')
    SQL_Username = conf.values[0][1]
    password = '76692623Snow!SQL'
    db_connection_str = 'mysql+pymysql://' + SQL_Username + ':' + password + '@localhost/pokedex'
    connection = sqlalchemy.create_engine(db_connection_str)

    pokemon = 'ludicolo'

    attacker_query ='select p.id pokemon_number, p.identifier pokemon, max(n1.name) type1, min(n1.name) type2, m.identifier move, n2.name move_type, s.identifier stat, ps.base_stat, m.accuracy accuracy, m.priority priority , case when max(n1.name) = n2.name or min(n1.name) = n2.name then 1.5 else 1 end STAB_mulitiplier ' \
                    'from pokemon p ' \
                    'join pokemon_moves pm on p.id = pm.pokemon_id ' \
                    'join moves m on m.id = pm.move_id ' \
                    'join pokemon_stats ps on ps.pokemon_id = p.id and case when damage_class_id = 2 then stat_id = 2 when damage_class_id = 3 then stat_id = 4 end ' \
                    'join stats s on ps.stat_id = s.id ' \
                    'join pokemon_types pt on p.id = pt.pokemon_id ' \
                    'join type_names n1 on pt.type_id = n1.type_id and n1.local_language_id = 9 ' \
                    'join type_names n2 on m.type_id = n2.type_id and n2.local_language_id = 9 ' \
                    'where p.identifier = \''+pokemon + '\' ' \
                    'group by pm.pokemon_id, m.id, n2.name, s.identifier, ps.base_stat'

    attacker = pandas.read_sql_query(attacker_query, connection)





    defender_query = 'select pok.pokemon as pokemon , n1.name as type1, n2.name as type2 , stat_type, def, hp , n3.name as  move_type , t1.damage_factor * t2.damage_factor/10000 as effectiveness ' \
                     'from ' \
                        '(  select p.identifier pokemon , max(pt.type_id) type1, min(pt.type_id) type2, s1.identifier stat_type, ps1.base_stat as def, ps2.base_stat hp ' \
                     '      from pokemon p ' \
                     '      join pokemon_types pt on p.id = pt.pokemon_id ' \
                     '      join pokemon_stats ps1 on p.id = ps1.pokemon_id ' \
                     '      join pokemon_stats ps2 on p.id = ps2.pokemon_id ' \
                     '      join stats s1 on ps1.stat_id = s1.id and s1.identifier in (\'defense\',\'special-defense\') ' \
                     '      join stats s2 on ps2.stat_id = s2.id and s2.identifier = \'hp\' ' \
                     '      group by p.id, s1.identifier, ps1.base_stat, ps2.base_stat) pok ' \
                     'join type_efficacy t1 on type1 = t1.target_type_id ' \
                     'join type_efficacy t2 on type2 = t2.target_type_id ' \
                     'join type_names n1 on pok.type1 = n1.type_id and n1.local_language_id = 9 ' \
                     'join type_names n2 on pok.type2 = n2.type_id and n2.local_language_id = 9 ' \
                     'join type_names n3 on t1.damage_type_id = n3.type_id and n3.local_language_id = 9 ' \
                     'where t1.damage_type_id = t2.damage_type_id ' \

    defender = pandas.read_sql_query(defender_query, connection
                                     )
    print(defender)


run()
