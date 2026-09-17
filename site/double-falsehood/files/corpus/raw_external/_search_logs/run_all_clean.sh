#!/bin/bash
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/.."
C="$HERE/clean_ocr.py"
run(){ python3 $C "$@"; }
run persian_princess_1715/bim_eighteenth-century_the-persian-princess-or_theobald-mr-lewis_1715_djvu.txt persian_princess_1715/persian_princess_1715.clean.txt --runhead 'persian\s*princess' --runhead 'royal\s*villain'
run perfidious_brother_1715/bim_eighteenth-century_the-perfidious-brother-_mestayer-henry_1715_djvu.txt perfidious_brother_1715/perfidious_brother_1715.clean.txt --runhead 'perfidious\s*brother'
run mestayer_perfidious_brother_1720/bim_eighteenth-century_the-perfidious-brother-_mestayer-henry_1720_djvu.txt mestayer_perfidious_brother_1720/mestayer_perfidious_brother_1720.clean.txt --runhead 'perfidious\s*brother'
run orestes_1731/bim_eighteenth-century_orestes-a-dramatic-oper_theobald-mr-lewis_1731_djvu.txt orestes_1731/orestes_1731.clean.txt --runhead '^\W*orestes\W*$' --runhead 'dramatic\s*opera'
run fatal_secret_1735/bim_eighteenth-century_the-fatal-secret-a-trag_theobald-mr_1735_djvu.txt fatal_secret_1735/fatal_secret_1735.clean_UNUSABLE.txt --runhead 'fatal\s*secret'
run happy_captive_1741/bim_eighteenth-century_the-happy-captive-an-en_theobald-mr_1741_djvu.txt happy_captive_1741/happy_captive_1741.clean.txt --runhead 'happy\s*captive'
run electra_1714/bim_eighteenth-century_electra-a-tragedy-tran_sophocles_1714_djvu.txt electra_1714/electra_1714_copyA.clean.txt --runhead '^\W*electra\W*$'
run electra_1714/bim_eighteenth-century_electra-a-tragedy-tran_sophocles_1714_0_djvu.txt electra_1714/electra_1714_copyB.clean.txt --runhead '^\W*electra\W*$'
run oedipus_1715/bim_eighteenth-century_oedipus-king-of-thebes_sophocles_1715_djvu.txt oedipus_1715/oedipus_1715.clean.txt --runhead 'king\s*of\s*thebes' --runhead '^\W*oedipus\W*$'
run plutus_1715/bim_eighteenth-century_plutus-or-the-worlds-_aristophanes_1715_djvu.txt plutus_1715/plutus_1715.clean.txt --runhead "world'?s\s*idol" --runhead '^\W*plutus\W*$'
run clouds_1715/bim_eighteenth-century_the-clouds-a-comedy-tr_aristophanes_1715_djvu.txt clouds_1715/clouds_1715.clean.txt --runhead '^\W*(the\s*)?clouds\W*$'
run cave_of_poverty_1715/bim_eighteenth-century_the-cave-of-poverty-a-p_theobald-mr-lewis_1715_djvu.txt cave_of_poverty_1715/cave_of_poverty_1715_copyA.clean.txt --runhead 'cave\s*of\s*poverty'
run cave_of_poverty_1715/bib_fict_4103198_djvu.txt cave_of_poverty_1715/cave_of_poverty_1715_copyB_JHU.clean.txt --runhead 'cave\s*of\s*poverty'
run mausoleum_1714/bim_eighteenth-century_the-mausoleum-a-poem-s_theobald-mr_1714_djvu.txt mausoleum_1714/mausoleum_1714.clean.txt --runhead '^\W*(the\s*)?mausoleum\W*$'
run pindarick_ode_union_1707/bim_eighteenth-century_a-pindarick-ode-on-the-u_theobald-mr-lewis_1707_djvu.txt pindarick_ode_union_1707/pindarick_ode_union_1707.clean.txt --runhead 'pindarick\s*ode'
run shakespeare_restored_1726/bim_eighteenth-century_shakespeare-restored-or_theobald-mr-lewis_1726_djvu.txt shakespeare_restored_1726/shakespeare_restored_1726.clean.txt --runhead "shakespeare\s*restor'?d"
run harlequin_sorcerer_1725/bim_eighteenth-century_a-dramatick-entertainmen_theobald-mr-lewis_1725_djvu.txt harlequin_sorcerer_1725/harlequin_sorcerer_1725.clean.txt --runhead 'harlequin\s*a\s*sorcerer'
run rape_of_proserpine_1727/bim_eighteenth-century_the-rape-of-proserpine-_theobald-mr-lewis_1727_djvu.txt rape_of_proserpine_1727/rape_of_proserpine_1727.clean.txt --runhead 'rape\s*of\s*proserpine'
run perseus_and_andromeda_1730/bim_eighteenth-century_perseus-and-andromeda-a_theobald-mr-lewis_1730_djvu.txt perseus_and_andromeda_1730/perseus_and_andromeda_1730_copyA.clean.txt --runhead 'perseus\s*and\s*andromeda'
run perseus_and_andromeda_1730/perseusandromeda00theo_djvu.txt perseus_and_andromeda_1730/perseus_and_andromeda_1730_copyB_Rice.clean.txt --runhead 'perseus\s*and\s*andromeda'
run orpheus_and_eurydice_1740/bim_eighteenth-century_orpheus-and-eurydice-an_theobald-mr-lewis_1740_djvu.txt orpheus_and_eurydice_1740/orpheus_and_eurydice_1740.clean.txt --runhead 'orpheus\s*and\s*eurydice'
run orpheus_and_eurydice_1740/bim_eighteenth-century_orpheus-and-eurydice-an_theobald-mr-lewis_1739_djvu.txt orpheus_and_eurydice_1740/orpheus_and_eurydice_1739.clean.txt --runhead 'orpheus\s*and\s*eurydice'
run decius_and_paulina_1719/bim_eighteenth-century_decius-and-paulina-a-ma_theobald-mr_1719_djvu.txt decius_and_paulina_1719/decius_and_paulina_1719.clean.txt --runhead 'decius\s*and\s*paulina'
run pan_and_syrinx_1718/bim_eighteenth-century_pan-and-syrinx-an-opera_theobald-mr-lewis_1718_djvu.txt pan_and_syrinx_1718/pan_and_syrinx_1718.clean.txt --runhead 'pan\s*and\s*syrinx'
run apollo_and_daphne_1726/bim_eighteenth-century_vocal-parts-of-an-entert_theobald-mr-lewis_1726_djvu.txt apollo_and_daphne_1726/apollo_and_daphne_1726.clean.txt --runhead 'apollo\s*and\s*daphne'
run epistle_to_orrery_1732/bim_eighteenth-century_an-epistle-humbly-addres_theobald-mr-lewis_1732_djvu.txt epistle_to_orrery_1732/epistle_to_orrery_1732.clean.txt
run antiochus_and_stratonice_1717/bim_eighteenth-century_the-history-of-the-loves_theobald-mr-lewis_1717_djvu.txt antiochus_and_stratonice_1717/antiochus_and_stratonice_1717.clean.txt --runhead 'antiochus\s*and\s*stratonice'
run life_of_cato_1713/lifeofcharactero00theo_djvu.txt life_of_cato_1713/life_of_cato_1713.clean.txt --runhead 'life\s*and\s*character'
run memoirs_of_raleigh_1719/bim_eighteenth-century_memoirs-of-sir-walter-ra_theobald-mr-lewis_1719_djvu.txt memoirs_of_raleigh_1719/memoirs_of_raleigh_1719.clean.txt --runhead 'sir\s*walter\s*ra'
run censor_1717/sim_censor_the-censor_april-11-june-17-1715_1_1-30_djvu.txt censor_1717/censor_vol1_nos1-30.clean.txt --runhead '^\W*(the\s*)?censor\W*$'
run censor_1717/sim_censor_the-censor_january-01-march-16-1717_2_31-63_djvu.txt censor_1717/censor_vol2_nos31-63.clean.txt --runhead '^\W*(the\s*)?censor\W*$'
run censor_1717/sim_censor_the-censor_march-19-june-01-1717_3_64-96_djvu.txt censor_1717/censor_vol3_nos64-96.clean.txt --runhead '^\W*(the\s*)?censor\W*$'
run cibber_love_makes_a_man_1701/bim_eighteenth-century_love-makes-a-man-or-th_cibber-colley_1701_0_djvu.txt cibber_love_makes_a_man_1701/cibber_love_makes_a_man_1701_copyB_1701_0.clean.txt --runhead 'love\s*makes\s*a\s*man' --runhead "fop'?s\s*fortune"
run cibber_love_makes_a_man_1701/bim_eighteenth-century_love-makes-a-man-or-th_cibber-colley_1701_djvu.txt cibber_love_makes_a_man_1701/cibber_love_makes_a_man_1701_copyA_1701.clean.txt --runhead 'love\s*makes\s*a\s*man' --runhead "fop'?s\s*fortune"
run farquhar_inconstant_1702/bim_eighteenth-century_the-inconstant-or-the-_farquhar-george_1702_djvu.txt farquhar_inconstant_1702/farquhar_inconstant_1702.clean.txt --runhead '^\W*(the\s*)?inconstant' --runhead 'way\s*to\s*win\s*him'
run cibber_richard_iii_1700/bim_early-english-books-1641-1700_the-tragical-history-of-_shakespeare-william_1700_djvu.txt cibber_richard_iii_1700/cibber_richard_iii_1700.clean.txt --runhead 'richard\s*(the\s*)?(iii|third)' --runhead 'tragical\s*history'
run granville_jew_of_venice_1701/bim_eighteenth-century_the-jew-of-venice-a-com_lansdowne-george-granvi_1701_djvu.txt granville_jew_of_venice_1701/granville_jew_of_venice_1701.clean.txt --runhead 'jew\s*of\s*venice'
run burnaby_love_betrayd_1703/bim_eighteenth-century_love-betrayd-or-the-a_burnaby-william_1703_djvu.txt burnaby_love_betrayd_1703/burnaby_love_betrayd_1703.clean.txt --runhead "love\s*betray'?d" --runhead 'agreeable\s*disap'
run hill_henry_v_1723/bim_eighteenth-century_king-henry-the-fifth-or_hill-aaron_1723_djvu.txt hill_henry_v_1723/hill_henry_v_1723.clean.txt --runhead 'henry\s*the\s*fifth' --runhead 'conquest\s*of\s*france'
# ---- extracts from multi-work volumes ----
M=motteux_don_quixote_1700/bim_early-english-books-1641-1700_the-history-of-the-renow_cervantes-miguel-de_1700_djvu.txt
P=phillips_don_quixote_1687/bim_early-english-books-1641-1700_the-history-of-the-most-_cervantes-miguel-de_1687_djvu.txt
W=preface_works_of_shakespeare_1733/worksofshakespe01shak_djvu.txt
S=$(ls sheffield_julius_caesar_1723/*_1723_1_djvu.txt)
G=preface_works_of_shakespeare_1733/gutenberg_16346-0.txt
rm -f motteux_don_quixote_1700/motteux_dq_partI_ch23-37_cardenio.clean.txt*
sed -n '17046,30428p' $M > $SC/motteux_extract.txt; run $SC/motteux_extract.txt motteux_don_quixote_1700/motteux_dq_partI_ch23-36_cardenio.clean.txt --keep-start --runhead 'Life and Atchievements' --runhead "of the Renown'?d Don Quixote"
sed -n '11701,21199p' $P > $SC/phillips_extract.txt; run $SC/phillips_extract.txt phillips_don_quixote_1687/phillips_dq_partI_ch23-36_cardenio.clean.txt --keep-start --runhead 'Don Quixote of Mancha' --runhead 'History of the most renowned'
sed -n '125,3384p' $W > $SC/works_extract.txt; run $SC/works_extract.txt preface_works_of_shakespeare_1733/theobald_1733_dedication_and_preface.ocr.clean.txt --keep-start --runhead '^\W*(The\s+)?P\s?R\s?E\s?F\s?A\s?C\s?E\W*$' --runhead '^\W*D\s?E\s?D\s?I\s?C\s?A\s?T\s?I\s?O\s?N\W*$'
END=$(grep -n "The Editors of THE AUGUSTAN REPRINT SOCIETY" $G | head -1 | cut -d: -f1); END=$((END-4))
sed -n "296,${END}p" $G | sed 's/^\s*\*\s*\*\s*\*.*$//' > preface_works_of_shakespeare_1733/theobald_1733_preface.gutenberg_transcription.txt
sed -n '11749,17598p' $S > $SC/sheffield_jc.txt; run $SC/sheffield_jc.txt sheffield_julius_caesar_1723/sheffield_julius_caesar_1723.clean.txt --keep-start --runhead 'JULIUS\s*C'
sed -n '17599,24327p' $S > $SC/sheffield_mb.txt; run $SC/sheffield_mb.txt sheffield_julius_caesar_1723/sheffield_marcus_brutus_1723.clean.txt --keep-start --runhead 'MARCUS\W*BRU'
echo ALL-CLEAN-DONE
