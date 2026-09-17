#!/usr/bin/env python3
"""Corpus manifest: which parsed play (TCP id + play index) is what, with authorship labels.
Groups: SH Shakespeare solo; FL Fletcher solo (Hoy's canon); BF Beaumont & Fletcher; FX Fletcher with others;
BE Beaumont; MA Massinger; JAC other Jacobean/Caroline dramatists; COLLAB Shakespeare-Fletcher collaborations;
ADAPT Restoration/18C adaptations of Jacobean plays; R18 18th-century plays by others; DF Double Falsehood.
Sources: EEBO-TCP/ECCO-TCP XML (ids); external OCR texts are added by build_corpus.py from corpus/raw_external."""
import csv, sys, os

M = []  # (id, play_index, key, group, author, date, note)
def add(i, p, key, group, author, date, note=''):
    M.append((i, p, key, group, author, date, note))

# --- Shakespeare First Folio 1623 (A11954), play index -> key
F1 = ['tempest','two_gentlemen','merry_wives','measure','errors','much_ado','lll','mnd','merchant','ayl','shrew','alls_well','twelfth_night',
      'winters_tale','john','richard2','1henry4','2henry4','henry5','1henry6','2henry6','3henry6','richard3','henry8','troilus','coriolanus',
      'titus','romeo','timon','julius_caesar','macbeth','hamlet','lear','othello','antony','cymbeline']
SH_SOLO = {'tempest','two_gentlemen','merry_wives','errors','much_ado','lll','mnd','merchant','ayl','shrew','twelfth_night','winters_tale','john',
           'richard2','1henry4','2henry4','henry5','richard3','troilus','coriolanus','romeo','julius_caesar','hamlet','lear','othello','antony','cymbeline'}
SH_DATE = {'tempest':1611,'two_gentlemen':1591,'merry_wives':1597,'measure':1604,'errors':1594,'much_ado':1598,'lll':1595,'mnd':1595,'merchant':1596,
           'ayl':1599,'shrew':1592,'alls_well':1605,'twelfth_night':1601,'winters_tale':1610,'john':1596,'richard2':1595,'1henry4':1597,'2henry4':1598,
           'henry5':1599,'1henry6':1592,'2henry6':1591,'3henry6':1591,'richard3':1593,'henry8':1613,'troilus':1602,'coriolanus':1608,'titus':1592,
           'romeo':1595,'timon':1606,'julius_caesar':1599,'macbeth':1606,'hamlet':1601,'lear':1605,'othello':1604,'antony':1607,'cymbeline':1610}
for i, k in enumerate(F1):
    if k in SH_SOLO: add('A11954', i, 'sh_' + k, 'SH', 'Shakespeare', SH_DATE[k], 'F1 1623')
    elif k == 'henry8': add('A11954', i, 'collab_henry8', 'COLLAB', 'Shakespeare+Fletcher', 1613, 'F1 1623')
    elif k in ('measure','timon','alls_well','macbeth'): add('A11954', i, 'shx_' + k, 'SHX', 'Shakespeare(+Middleton?)', SH_DATE[k], 'F1 1623; excluded from training')
    else: add('A11954', i, 'shx_' + k, 'SHX', 'Shakespeare+other', SH_DATE[k], 'F1 1623; collaborative; excluded')
add('A00969', 0, 'collab_tnk', 'COLLAB', 'Shakespeare+Fletcher', 1613, 'Q 1634')

# --- Beaumont & Fletcher folio 1647 (A27177): index -> key, group
BF1647 = [('mad_lover','FL'),('spanish_curate','FX'),('little_french_lawyer','FX'),('custom_of_country','FX'),('noble_gentleman','FX'),('captain','BF'),
          ('beggars_bush','FX'),('coxcomb','BF'),('false_one','FX'),('chances','FL'),('loyal_subject','FL'),('laws_of_candy','FX'),('lovers_progress','FX'),
          ('island_princess','FL'),('humorous_lieutenant','FL'),('nice_valour','FX'),('maid_in_mill','FX'),('prophetess','FX'),('bonduca','FL'),('sea_voyage','FX'),
          ('double_marriage','FX'),('pilgrim','FL'),('knight_of_malta','FX'),('womans_prize','FL'),('loves_cure','FX'),('honest_mans_fortune','FX'),
          ('queen_of_corinth','FX'),('women_pleased','FL'),('wife_for_month','FL'),('wit_at_several_weapons','FX'),('valentinian','FL'),('fair_maid_of_inn','FX'),
          ('loves_pilgrimage','FX'),('masque_grays_inn','BE'),('four_plays_in_one','FX'),('wild_goose_chase','FL')]
FL_DATE = {'mad_lover':1617,'chances':1617,'loyal_subject':1618,'island_princess':1621,'humorous_lieutenant':1619,'bonduca':1613,'pilgrim':1621,
           'womans_prize':1611,'women_pleased':1620,'wife_for_month':1624,'valentinian':1614,'wild_goose_chase':1621,'faithful_shepherdess':1608,
           'monsieur_thomas':1615,'rule_a_wife':1624,'wit_without_money':1614}
for i, (k, g) in enumerate(BF1647):
    auth = {'FL':'Fletcher','FX':'Fletcher+other','BF':'Beaumont+Fletcher','BE':'Beaumont'}[g]
    add('A27177', i, ('fl_' if g=='FL' else 'fx_') + k, g, auth, FL_DATE.get(k, 1620), 'Folio 1647')
# Fletcher solo quartos
add('A00962', 0, 'fl_faithful_shepherdess', 'FL', 'Fletcher', 1608, 'Q 1610')
add('B13574', 0, 'fl_monsieur_thomas', 'FL', 'Fletcher', 1615, 'Q 1639')
add('A00967', 0, 'fl_rule_a_wife', 'FL', 'Fletcher', 1624, 'Q 1640')
add('A27204', 0, 'fl_wit_without_money', 'FL', 'Fletcher', 1614, 'Q 1661; sole authorship disputed by some')
add('A00966', 0, 'fx_night_walker', 'FX', 'Fletcher rev. Shirley', 1611, 'Q 1640')
# Beaumont & Fletcher quartos and Beaumont
add('A06343', 0, 'bf_philaster', 'BF', 'Beaumont+Fletcher', 1609, 'Q 1620')
add('A06289', 0, 'bf_maids_tragedy', 'BF', 'Beaumont+Fletcher', 1610, 'Q 1619')
add('A06207', 0, 'bf_king_no_king', 'BF', 'Beaumont+Fletcher', 1611, 'Q 1619')
add('A06389', 0, 'bf_scornful_lady', 'BF', 'Beaumont+Fletcher', 1610, 'Q 1616')
add('A06177', 0, 'bf_cupids_revenge', 'BF', 'Beaumont+Fletcher', 1608, 'Q 1615')
add('A06252', 0, 'be_knight_burning_pestle', 'BE', 'Beaumont', 1607, 'Q 1613')
add('A06458', 0, 'be_woman_hater', 'BE', 'Beaumont(+Fletcher)', 1606, 'Q 1607')
# Fletcher with Massinger etc. quartos
add('A00960', 0, 'fx_elder_brother', 'FX', 'Fletcher+Massinger', 1625, 'Q 1637')
add('A00958', 0, 'fx_bloody_brother', 'FX', 'Fletcher+Massinger+others', 1617, 'Q 1639')
add('A00968', 0, 'fx_thierry', 'FX', 'Fletcher+Massinger+Beaumont?', 1617, 'Q 1621')
# Massinger solo
for i, k, d in [('A07234','bondman',1623),('A07237','duke_of_milan',1621),('A07238','emperor_of_east',1631),('A07239','great_duke_florence',1627),
                ('A07240','maid_of_honour',1621),('A07241','new_way',1625),('A07245','picture',1629),('A07246','renegado',1624),('A07247','roman_actor',1626),
                ('A07248','unnatural_combat',1624),('A50090','city_madam',1632)]:
    add(i, 0, 'ma_' + k, 'MA', 'Massinger', d, 'Q')
# Other Jacobean/Caroline dramatists (impostors)
JAC = [('A12128','Shirley','bird_in_cage',1633),('A12129','Shirley','changes',1632),('A12130','Shirley','constant_maid',1636),('A12138','Shirley','grateful_servant',1629),
       ('A12140','Shirley','hyde_park',1632),('A12141','Shirley','humorous_courtier',1631),('A12142','Shirley','lady_of_pleasure',1635),('A12143','Shirley','loves_cruelty',1631),
       ('A12145','Shirley','maids_revenge',1626),('A12148','Shirley','opportunity',1634),('A12150','Shirley','royal_master',1637),('A12152','Shirley','school_of_complement',1625),
       ('A12154','Shirley','traitor',1631),('A12155','Shirley','wedding',1626),('A12157','Shirley','witty_fair_one',1628),
       ('A07493','Middleton','chaste_maid',1613),('A07495','Middleton','family_of_love',1605),('A07505','Middleton','michaelmas_term',1605),('A07507','Middleton','phoenix',1604),
       ('A07511','Middleton','trick_to_catch',1605),('A07498','Middleton','game_at_chess',1624),
       ('A01046','Ford','broken_heart',1630),('A01047','Ford','perkin_warbeck',1633),('A01052','Ford','ladys_trial',1638),('A01055','Ford','lovers_melancholy',1628),
       ('A01056','Ford','loves_sacrifice',1632),('A01057','Ford','tis_pity',1630),
       ('A14872','Webster','duchess_of_malfi',1613),('A14869','Webster','devils_law_case',1618),('A14875','Webster','white_devil',1612),
       ('A04633','Jonson','bartholomew_fair',1614),('A04639','Jonson','case_is_altered',1597),('A04647','Jonson','every_man_in',1598),('A04653','Jonson','cynthias_revels',1600),
       ('A04658','Jonson','new_inn',1629),('A46228','Jonson','devil_is_an_ass',1616),
       ('A18400','Chapman','all_fools',1604),('A18403','Chapman','bussy',1604),('A18404','Chapman','byron',1608),('A18415','Chapman','may_day',1602),('A18421','Chapman','revenge_bussy',1610),
       ('A18425','Chapman','caesar_pompey',1613),('A18426','Chapman','widows_tears',1605),('A69093','Chapman','monsieur_dolive',1605),('A01911','Chapman','gyles_goosecap',1602),
       ('A07063','Marston','antonio_mellida',1599),('A07064','Marston','antonios_revenge',1600),('A07083','Marston','sophonisba',1605),('A20867','Marston','jack_drum',1600),('A07067','Marston','insatiate_countess',1610),
       ('A20066','Dekker','if_it_be_not_good',1611),('A20076','Dekker','old_fortunatus',1599),('A20083','Dekker','shoemakers_holiday',1599),('A20088','Dekker','match_me',1621),('A20092','Dekker','whore_of_babylon',1606),
       ('A03190','Heywood','challenge_for_beauty',1635),('A03195','Heywood','english_traveller',1627),('A03201','Heywood','fair_maid_west',1610),('A03240','Heywood','maidenhead_well_lost',1633),
       ('A03244','Heywood','rape_of_lucrece',1607),('A03248','Heywood','royal_king',1602),('A03255','Heywood','wise_woman',1604),
       ('A11151','Rowley','match_at_midnight',1622),('A11152','Rowley','shoemaker_gentleman',1608),('A11153','Rowley','new_wonder',1611),('A11155','Rowley','alls_lost_by_lust',1619),
       ('A00723','Field','amends_for_ladies',1611),('A00725','Field','woman_weathercock',1609),
       ('A16923','Brome','antipodes',1638),('A16924','Brome','northern_lass',1629),('A16927','Brome','sparagus_garden',1635),
       ('A19876','Davenant','cruel_brother',1627),('A19881','Davenant','albovine',1628),('A19883','Davenant','wits',1634),
       ('A13840','Tourneur','atheists_tragedy',1609),('A13843','Middleton?','revengers_tragedy',1606),('A19757','Daborne','christian_turned_turk',1610),
       ('A21136','Anon','merry_devil',1602),('A11264','Middleton?','puritan',1606)]
for i, a, k, d in JAC:
    add(i, 0, 'jac_' + a.lower().replace('?','') + '_' + k, 'JAC', a, d, 'Q')
# Restoration / 18C adaptations: (id, play_index, key, adapter, original key, original author, date)
ADAPT = [('A39799',0,'chances_1682','Buckingham','fl_chances','Fletcher',1682),('A39808',0,'pilgrim_1700','Vanbrugh','fl_pilgrim','Fletcher',1700),
         ('A39812',0,'valentinian_1685','Rochester','fl_valentinian','Fletcher',1685),('A27197',0,'prophetess_1690','Betterton','fx_prophetess','Fletcher+Massinger',1690),
         ('A27180',0,'bonduca_1696','Powell?','fl_bonduca','Fletcher',1696),('A27196',0,'philaster_1695','Settle','bf_philaster','Beaumont+Fletcher',1695),
         ('A37025',0,'trick_for_trick_1678','DUrfey','fl_monsieur_thomas','Fletcher',1678),('A36966',0,'commonwealth_women_1686','DUrfey','fx_sea_voyage','Fletcher+Massinger',1686),
         ('A62964',0,'island_princess_1687','Tate','fl_island_princess','Fletcher',1687),('A51499',0,'island_princess_1699','Motteux','fl_island_princess','Fletcher',1699),
         ('A36513',0,'sham_lawyer_1697','Drake','fl_wit_without_money','Fletcher',1697),('A58829',0,'unhappy_kindness_1697','Scott','fl_wife_for_month','Fletcher',1697),
         ('A39804',0,'humorous_lieutenant_1697','anon','fl_humorous_lieutenant','Fletcher',1697),('A27198',0,'rule_a_wife_1697','anon','fl_rule_a_wife','Fletcher',1697),
         ('B17587',0,'loyal_subject_1700','anon','fl_loyal_subject','Fletcher',1700),('A39806',0,'night_walker_1661','anon','fx_night_walker','Fletcher',1661),
         ('A39805',0,'island_princess_1669','anon','fl_island_princess','Fletcher',1669),
         ('A59503',0,'macbeth_1674','Davenant','shx_macbeth','Shakespeare',1674),('A59520',0,'tempest_1670','Dryden+Davenant','sh_tempest','Shakespeare',1670),
         ('A59422',0,'timon_1678','Shadwell','shx_timon','Shakespeare',1678),('A59493',0,'lear_1681','Tate','sh_lear','Shakespeare',1681),
         ('A59496',0,'richard2_1681','Tate','sh_richard2','Shakespeare',1681),('A53517',0,'caius_marius_1680','Otway','sh_romeo','Shakespeare',1680),
         ('A36983',0,'injured_princess_1682','DUrfey','sh_cymbeline','Shakespeare',1682),('A59525',0,'titus_1687','Ravenscroft','shx_titus','Shakespeare',1687),
         ('A36704',0,'troilus_1679','Dryden','sh_troilus','Shakespeare',1679),('A62946',0,'coriolanus_1682','Tate','sh_coriolanus','Shakespeare',1682),
         ('A35289',0,'misery_civil_war_1680','Crowne','shx_2henry6','Shakespeare',1680),('A35283',0,'henry6_1681','Crowne','shx_2henry6','Shakespeare',1681),
         ('A48052',0,'sauny_scot_1698','Lacy','sh_shrew','Shakespeare',1698),('A59508',0,'measure_1700','Gildon','shx_measure','Shakespeare',1700),
         ('A59501',0,'henry4_1700','Betterton','sh_1henry4','Shakespeare',1700),('A59527',0,'hamlet_1676','Davenant(cuts)','sh_hamlet','Shakespeare',1676),
         ('A59497',0,'julius_caesar_1684','anon(light)','sh_julius_caesar','Shakespeare',1684),('K039442.000',0,'marina_1738','Lillo','pericles','Shakespeare+Wilkins',1738),
         ('K046085.000',0,'tempest_opera_1756','Garrick','sh_tempest','Shakespeare',1756),('K046340.000',0,'timon_1772','Cumberland','shx_timon','Shakespeare',1772)]
for i, p, k, ad, ok, oa, d in ADAPT:
    add(i, p, 'ad_' + k, 'ADAPT', ad, d, 'orig=' + ok + ' by ' + oa)
# 18th-century plays by others (impostors for the Theobald period)
R18 = [('K049485.000','Rowe','ambitious_stepmother',1700),('K049942.000','Rowe','tamerlane',1701),('K109300.000','Rowe','fair_penitent',1703),('K049483.000','Rowe','ulysses',1705),
       ('K046880.000','Rowe','lady_jane_gray',1715),('K032335.000','Addison','cato',1713),('K015532.000','Addison','drummer',1715),('K016151.000','Hill','fatal_extravagance',1721),
       ('K002806.000','Hill','athelwold',1731),('K132743.000','Thomson','sophonisba',1730),('K019154.000','Thomson','edward_eleonora',1739),('K027367.000','Congreve','mourning_bride',1697),
       ('K001985.000','Congreve','love_for_love',1695),('K121177.000','Congreve','double_dealer',1693),('K036683.000','Centlivre','cruel_gift',1716),('K032330.000','Centlivre','perjured_husband',1700),
       ('K000039.000','Centlivre','basset_table',1705),('K009642.000','Centlivre','busie_body',1709),('K032319.000','Centlivre','wonder',1714),('K032308.000','Centlivre','artifice',1722),
       ('K040557.000','Dennis','liberty_asserted',1704),('K039296.000','Manley','lucius',1717),('K050786.000','Philips','briton',1722),('K100402.000','Savage','overbury',1723),
       ('K037803.000','T.Cibber','henry6_civil_wars',1723),('K040713.000','Lillo','london_merchant',1731),('K120974.000','C.Cibber','non_juror',1717),('A36592',0,'dryden_all_for_love',1677,'x')]
for row in R18:
    if len(row) == 4:
        i, a, k, d = row; add(i, 0, 'r18_' + a.lower().replace('.','') + '_' + k, 'R18', a, d, 'ECCO/EEBO')
    else:
        i, p, k, d, _ = row; add(i, p, 'r18_' + k, 'R18', 'Dryden', d, 'EEBO')
# Sources of Cardenio story and Fatal Secret
add('A31538', 0, 'src_shelton_quixote_1652', 'SRC', 'Shelton (tr. Cervantes)', 1612, 'Shelton translation, 1652 ed.')
# Double Falsehood
add('K036934.000', 0, 'df_double_falsehood', 'DF', 'Theobald (claims Shakespeare)', 1728, 'ECCO-TCP first edition 1728')

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'corpus/MANIFEST.tsv'
    with open(out, 'w') as fh:
        fh.write('id\tplay_index\tkey\tgroup\tauthor\tdate\tnote\n')
        for r in M: fh.write('\t'.join(str(x) for x in r) + '\n')
    print(len(M), 'entries ->', out)
