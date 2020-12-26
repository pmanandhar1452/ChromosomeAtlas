
import re
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import string
from enum import Enum
import time

class CapStyle(Enum):
    AS_IS     = 0
    LOWER     = 1
    CAP_WORDS = 2

class LatexGenerator:

    latex_file = None
    current_genus = ''
    num_species_in_fam = 0
    num_genus_in_fam = 0

    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

    # The ID and range of spreadsheets.     

    # SPREADSHEET_DICT = {
    #     'Acanthaceae': '1vbkdYUAIzmHhqRZCPx_wvImylWM_BqxcuhY2aIKZfuw', 
    #     'Aceraceae'  : '1RqlxSLZs8Uhz2xyCFRq-541jyIqZRUejcGVX_WIPblw',
    #     'Agavaceae'  : '1IadRjWtV_dEsMEgmNhAFY2-viQ0Ug7fUmSyuh4km2Uk',
    #     'Aizoiceae'  : '1j_GgOSlBSEuzgbUOFU5p9eS8iixgbG-iASnL7u0g718',  
    #     'Alangiaceae': '1Z9bLIm1q21cLek5cq6_dv9eAmCjrlLhekkWxxDPLmhE',
    #     'Alismataceae': '1Vq-Z6vmNsLbQzu3ISfae3vmG3xMPg3HcAeH7dZsSA_8',
    #     'Amaranthaceae': '1UpAvdWhzjti04YIXxa5_FWbbfCQC2Z3hVcryn-VA9xQ',
    #     'Amaryllidaceae': '1tbM4IdBSmJRT2NN0AThbW5WNW0eVYHJWOFL0TvI5iYQ',
    #     'Anacardiaceae': '1zCHts6_bkNaD7P-m3MDcGAEzLC9Df_CuvYxzi4amYN0',
    #     'Annonaceae': '1bN4I6az_ISWVTPD3qEu6Xxm6m07dLhNonnWgTuiaKko',
    #     'Apiaceae': '1oI_jKwBDmhcRRuQey3YNAEDDKgQbGY6-qStlGN_WkcI',
    #     'Apocynaceae': '1PHe5lXT6eR6KkMnb0iAXo1_HjQJD8k2yiRashA3uMX8',
    #     'Aponogetonaceae': '1-UZdVUrah1ZgOXHyUKz3iBvKCgPRVzalI2NxHYlbGdM',
    #     'Aquifoliaceae': '1TkEFy28X1iCL0fbb4JuvNeFdUjyeG4wGhcXDfHj8J5Q',
    #     'Aracaceae': '1JwrLcL5oJQQJFPxXY-y-rNOrqrLic1Zb7iGRslLeVf4',
    #     'Araceae': '1bwrFv_iPJ89UGx115ZoRSqjGRY_m1_p1PifbHRiuPtA',
    #     'Araliaceae': '18eVtHUVzH9_X-uBAgCUoDVOeLlEHOmjJdYNzxZEvIUQ',
    #     'Aristrolochiaceae': '1eWGC74p0g-hw9ctUqxYaJExlsUUlS9w_TdMYG7aPfR4',
    #     'Asclepiadaceae': '1It_JAnjSrSl6qDXckqy67JldjgzqXndA7JUZu-h3Rc0',
    #     'Asteraceae': '1R26HJFoGIvVyQDebvN0T_lUZLxP07YHQtl-yt1cinJI',
    #     'Balsaminaceae': '1swLGYE7r6xcO_2RBXC8Bk7-urWk4CL9c5CmAwlrKpZE',
    #     'Basellaceae': '1B-TLV6aKrp3eyqSvdHuG6z-YoHjvMI1JrC-aRji76ao',
    #     'Begoniaceae': '1v-X3D708YPf5mcwaNMhQ6GOazG2UjWKJfZsUSic2omQ',
    #     'Berberidaceae':'1WwCvMDnWxNF58cgKR-plJmF_fgnxidTC_XSmBb4UFfA',
    #     'Betulaceae':'12dpTJwd0ymeb2ssCFB9g1IzkiHTdhZZ-wMtX0rgmYI0',
    #     'Bignoniaceae':'1zzZ7XG4Alxwf5RX6mNPT3K6gTGM5xegF2xhidmsn6Bo',
    #     'Bombacaceae':'1ICUvGYuTzUEwFGfzVpqX2l6dZ22GRePWMLEIIIuU4nI',
    #     'Boraginaceae':'1ICLaRsV4LUvwSUQLSwbrJQSgrDiGa8-20aFujs9UogI',
    #     'Brassicaceae':'1TKt9hILyc7Iapfp9T_jQo0whcPbFffQySTqrN1qspm0',
    #     'Bromelliaceae':'1_Vu4eUkaknzNT8C4d7zVKJCVE_qdljOPP8gkdHoaZH4',
    #     'Burseraceae':'1zVgTT8fOYECUhUN0tqmKgIgUv5-_C95CYQBWkAfCgtU',
    #     'Callistricaceae':'11vu_Od9dwv9yDFPs4TI4NuUhn2iZu86Not1KpbMD0Ck',
    #     'Campanulaceae':'1_bS45r9lEXeN9GkMT8s0C6byOjoM9VNiausNUUlKqsg',
    #     'Cannabaceae':'1EUf_M38fr2Fa6J20OqS1jQqtHHgcUnLm7AvgJQW3ghA',
    #     'Caprifoliaceae':'1rrH8RnMypK7Rgyg0kcrSOiu0kojkBfycfFNHDn32J7g',
    #     'Caricaceae':'1jfuUUy74rPzWm4Zl9E7DzFghSF2PzraMw0vMPDrM1js',
    #     }

    SPREADSHEET_DICT = {
        "Caryophyllaceae": ["1ZteEsKR5j3DUBfd05XMr0VDpJHusK252muqecmIGRTc", False],
        "Caricaceae": ["1jfuUUy74rPzWm4Zl9E7DzFghSF2PzraMw0vMPDrM1js", False],
        "Caprifoliaceae": ["1rrH8RnMypK7Rgyg0kcrSOiu0kojkBfycfFNHDn32J7g", False],
        "Cannabaceae": ["1EUf_M38fr2Fa6J20OqS1jQqtHHgcUnLm7AvgJQW3ghA", False],
        "Campanulaceae": ["1_bS45r9lEXeN9GkMT8s0C6byOjoM9VNiausNUUlKqsg", False],
        "Basellaceae": ["1B-TLV6aKrp3eyqSvdHuG6z-YoHjvMI1JrC-aRji76ao", False],
        "Capparaceae": ["1ViObgOHXYTKCHHf_yRa84UxDK34dRiiZrpZr4CgWEZc", False],
        "Cannaceae": ["1_plRcrI3NLxZldyMMYfI6WOzVkj541R4Lu0_dbEtjKc", False],
        "Callistricaceae": ["11vu_Od9dwv9yDFPs4TI4NuUhn2iZu86Not1KpbMD0Ck", False],
        "Burseraceae": ["1zVgTT8fOYECUhUN0tqmKgIgUv5-_C95CYQBWkAfCgtU", False],
        "Boraginaceae": ["1ICLaRsV4LUvwSUQLSwbrJQSgrDiGa8-20aFujs9UogI", False],
        "Bromelliaceae": ["1_Vu4eUkaknzNT8C4d7zVKJCVE_qdljOPP8gkdHoaZH4", False],
        "Brassicaceae": ["1TKt9hILyc7Iapfp9T_jQo0whcPbFffQySTqrN1qspm0", False],
        "Bombacaceae": ["1ICUvGYuTzUEwFGfzVpqX2l6dZ22GRePWMLEIIIuU4nI", False],
        "Asteraceae": ["1R26HJFoGIvVyQDebvN0T_lUZLxP07YHQtl-yt1cinJI", False],
        "Berberidaceae": ["1WwCvMDnWxNF58cgKR-plJmF_fgnxidTC_XSmBb4UFfA", False],
        "Betulaceae": ["12dpTJwd0ymeb2ssCFB9g1IzkiHTdhZZ-wMtX0rgmYI0", False],
        "Begoniaceae": ["1v-X3D708YPf5mcwaNMhQ6GOazG2UjWKJfZsUSic2omQ", False],
        "Balsaminaceae": ["1swLGYE7r6xcO_2RBXC8Bk7-urWk4CL9c5CmAwlrKpZE", False],
        "Aquifoliaceae": ["1TkEFy28X1iCL0fbb4JuvNeFdUjyeG4wGhcXDfHj8J5Q", False],
        "Asclepiadaceae": ["1It_JAnjSrSl6qDXckqy67JldjgzqXndA7JUZu-h3Rc0", False],
        "Aristrolochiaceae": ["1eWGC74p0g-hw9ctUqxYaJExlsUUlS9w_TdMYG7aPfR4", False],
        "Araliaceae": ["18eVtHUVzH9_X-uBAgCUoDVOeLlEHOmjJdYNzxZEvIUQ", False],
        "Araceae": ["1bwrFv_iPJ89UGx115ZoRSqjGRY_m1_p1PifbHRiuPtA", False],
        "Aracaceae": ["1JwrLcL5oJQQJFPxXY-y-rNOrqrLic1Zb7iGRslLeVf4", False],
        "Verbenaceae": ["1iMwW2H5y1yEPp6TfjiyxcUwbZP6MInqPbeYym8hg1aI", False],
        "Chenopodiaceae": ["1qkqO5DL8FM4I9dZuJcMF89X4ZXmuU6wi73Y2K3vx3xQ", False],
        "Bignoniaceae": ["1zzZ7XG4Alxwf5RX6mNPT3K6gTGM5xegF2xhidmsn6Bo", False],
        "Amaryllidaceae": ["1tbM4IdBSmJRT2NN0AThbW5WNW0eVYHJWOFL0TvI5iYQ", False],
        "Nymphaeaceae": ["1xvLM34YgiU2jw-zxdbfEm9r3egZ-fPk9Of2rAxUip1k", False],
        "Anacardiaceae": ["1zCHts6_bkNaD7P-m3MDcGAEzLC9Df_CuvYxzi4amYN0", False],
        "Violaceae": ["1ImPm9KK0yCDofc-k8dPkWn2Sk02YrmBDj5S9ZshRZEw", False],
        "Combretaceae": ["1omT4FKB7wyZ0h6KF-Tc1RtxPi2qBlmpn7hBFLM88IfI", False],
        "Apiaceae": ["1oI_jKwBDmhcRRuQey3YNAEDDKgQbGY6-qStlGN_WkcI", False],
        "Amaranthaceae": ["1UpAvdWhzjti04YIXxa5_FWbbfCQC2Z3hVcryn-VA9xQ", False],
        "Fabaceae": ["11La7RwBy_D-10_sDPD5SSyJFKvSnRiJpDmt1r_XeYZQ", True],
        "Apocynaceae": ["1PHe5lXT6eR6KkMnb0iAXo1_HjQJD8k2yiRashA3uMX8", False],
        "Aponogetonaceae": ["1-UZdVUrah1ZgOXHyUKz3iBvKCgPRVzalI2NxHYlbGdM", False],
        "Alangiaceae": ["1Z9bLIm1q21cLek5cq6_dv9eAmCjrlLhekkWxxDPLmhE", False],
        "Agavaceae": ["1IadRjWtV_dEsMEgmNhAFY2-viQ0Ug7fUmSyuh4km2Uk", False],
        "Annonaceae": ["1bN4I6az_ISWVTPD3qEu6Xxm6m07dLhNonnWgTuiaKko", False],
        "Moraceae": ["1R_fjHIXjydqBaPZBFNMbJ6spxy9UzDXI2Lo0hjeor6k", False],
        "Aceraceae": ["1RqlxSLZs8Uhz2xyCFRq-541jyIqZRUejcGVX_WIPblw", False],
        "Alismataceae": ["1Vq-Z6vmNsLbQzu3ISfae3vmG3xMPg3HcAeH7dZsSA_8", False],
        "Acanthaceae": ["1vbkdYUAIzmHhqRZCPx_wvImylWM_BqxcuhY2aIKZfuw", False],
        "Aizoiceae": ["1j_GgOSlBSEuzgbUOFU5p9eS8iixgbG-iASnL7u0g718", False],
        "Lauraceae": ["1VsMTlVAueUgHgIN2WtUbf7wceLs-F9kNe7M6IGvMiEM", False],
        "Cucurbitaceae": ["1q0DyiSzb7-CxA_uiK27Hf1Oy7CcjASRI_jjT0Msib8c", False],
        "Oxalidaceae": ["1wP95w2sYahsU_LVnaXTDR0rGSM3PWgMsU5-5W-XKSZI", False],
        "Datiscaceae": ["1bMuTJ-13e3ImBt-0-rITpowW2qxHROs31yJtOtEL9TQ", False],
        "Euphorbiaceae": ["1PpIfiJimzCl3r_ZRM0ESy60hPTQjwoLXk57vyXjCwB4", False],
        "Dipsacaceae": ["1KNDoeE3Qb3XI5uzRQmkSVy-sa0TY01SUOOkvP4Guwv4", False],
        "Ebenaceae": ["1iJdlRBqJfh1wSAlbcRpDv0gutmrEgFKdJHS9GfRyLCc", False],
        "Punicaceae": ["1OPv1OJVtxB92QJqIkQrTfoWGuo-hEgq7a0_6wkfBLx4", False],
        "Ranunculaceae": ["1LwCKgWaOAyH3nz1o65_JmkvyuA6-bZbtl3TZKBHnbRg", False],
        "Onagraceae": ["1SsTfFslaB3NypSIlTLx_xeAdIYa_Ru0fXAZ98jO9RIE", False],
        "Hypericaceae": ["1gwqRXRxQPvk1VeTwlM6Yma5_zQIBNzLw3r5zAYExNSI", False],
        "Geraniaceae": ["1Bz8U9N8j-6IA4eZhirPuaK07UDwsVFx50tR48VOCADQ", False],
        "Malvaceae": ["1mcsOGRWQrhGYT8lCb7XCcmAboZNJwVjIJV32ZyawE_s", False],
        "Rosaceae": ["1b1oiHVok83hrr3lRdm5ZIPkl-a3V8l32NbU_ZrW1Lrk", False],
        "Primulaceae": ["1JBUT0Dv4uZUDHhUQ-a506YsoNECo4F_CONMncL3q5GI", False],
        "Crassulaceae": ["1inRLht4bZKpOoh6vcRp9D0jW8Ay1cm-Ez-arpHDtc3o", False],
        "Zygophyllaceae": ["1in1Si3aOLMbXlR1PMTV2Dx_6dEiNN54GG2uR5itkMws", False],
        "Fumariaceae": ["1sreIkDQdI5qje3xosxS4l9Kn9zyBcdEdjHx5T5HX8uQ", False],
        "Liliaceae": ["1OfUprilynnynmRt1OHGRVcUZu6KQ5YAUg0Wer1nrPLQ", False],
        "Convolvulaceae": ["1K6thfNrWFKgduaVnZfIIS6jWVKEOxiFYQaXkPIJt3-E", False],
        "Papaveraceae": ["1ibRIKXKuq3fIDuIB_noHLVWn6IGFKXF5MJ5-C0x2N1E", False],
        "Ceratophyllaceae": ["1mjgpjXj0Ab0gb-BAGlMCT_KbFRnPOUCCpD47vBTPHuU", False],
        "Portulacaceae": ["1AM3ReBe83slvM7A310ITueBzhgoQOLMtG_JtcLyj45Y", False],
        "Urticaceae": ["16fHAU-v6J9f2boMDoEXaydNM1JkIr61LfXQC3BkVNjQ", False],
        "Rubiaceae": ["1T1lpbLcaRJIxUdOPGQ7hINGqSvbm8UIbFtjSXLgODb4", False],
        "Solanaceae": ["1IRVq5z9tcaHjhrUaLO4RxyL4W1kw6jJqC7t4keVnki0", False],
        "Ulmaceae": ["1CVIMRZDRSdHxzECL78jIHyWZzQ3KQ2qqAj_bL9YpDjs", False],
        "Valerianaceae": ["14fuPJiT7I5NuteLHHIUGsYVv4PZnoTg2dnTrDNfA3Wo", False],
        "Vitaceae": ["1rmsV6Z63_z_o40ZlDMY2XUykGe_Jbr9OX73bkS5GwUg", False],
        "Zingiberaceae": ["1fioMKPZvf5yTzCltrJgI4M1nRHQ1MzktFuyeR-nltcI", False],
        "Iridaceae": ["1OmMboJvHSGEDrVB3FeNqhF81vPjQ6FFKMlJ9T52UX5c", False],
        "Symplocaceae": ["1MWS2_f1BKz5yW2256DdYoGHlUYJ61io-4qdOfieEMq0", False],
        "Sterculiaceae": ["1ZLu75Mgdsfs8nJnMnj0uMVW_ecK83OZN1dz8VW6hYXQ", False],
        "Sphenucleaceae": ["10cYW2tK38A0PRUIbqjRECn_ejGuWMns-0DUkLz3mogk", False],
        "Schizandraceae": ["1nFr6x-u2w5dAnnZo8lBUzIRqpP6hxGBP7n1wBFtrxS8", False],
        "Sapotaceae": ["1R98eeZ1k2x2L-_rPYmvUhjcm1GlyvdcohjpM5UmHlmU", False],
        "Sapindaceae": ["14bsCNMYYcr_RVzT2KcIJJPh7B4vBCnE959jY0Zhw_hQ", False],
        "Salicaceae": ["1WtMJA1Smj2FhAJjjHEj0aytbX1vsRLr4UeDsxFFYvjk", False],
        "Sabiaceae": ["1CE-S0fT4s7mIZt0RJpQBn7mHKEI4qQphlDu_gq8DfPY", False],
        "Rutaceae": ["1qTOQDH2Cl2995_3H5HSieB8nUzyiCtS6A_IZ_NyZTXg", False],
        "Typhaceae": ["1PH6VHK39b6llcHEKxKLu7c34eHTOvPwejqjzC3I8QNE", False],
        "Toricelliaceae": ["1_zR4D8eUefd_eo0AfCWoTi9XdtTXimR_rdg_ViXR0zE", False],
        "Thymalaeaceae": ["1UkDRZt0Q1xwdu7LGWKVOUh1uD-594RPsp-BR2OKwUzo", False],
        "Theaceae": ["1sLYsIvwFcPWAk5zVnk4viRLZoa-Qv7_gNd3c6DHpvi8", False],
        "Orchidaceae": ["1VB6t0N0tTDuv-FJZnbb-7AOycLWt8smYw00EWmOreIc", False],
        "Myrsinaceae": ["1IdqUQ0HWy0zG5_Yw0nHUUuh3GVR34KWA3-Ld_l5T-N8", False],
        "Lamiaceae": ["1ERHYCelqy4-ne5HUvVwV8G-D2R-cgbV1-Uy8QSlm5fM", False],
        "Hypoxidaceae": ["10rw45TEDPvM_56qNf2qqdWKGAhAKdsEwcryzREKKpQM", False],
        "Tropeolaceae": ["1A1QG6D3P9kGxjPec6A5Sf-nO77avwAKGYlpmikX4oNQ", False],
        "Saxifragaceae": ["1VJt7UHa5CM7WBECrfvP7Ug2fyI60hJH-EhlNBC-CPr8", False],
        "Cyperaceae": ["1Bdx01EW23p27t9PcMq2ANzXQvwkckDV58ZMY8K5XOio", True],
        "Chloranthaceae": ["1DwjDVtjZlfjcp8_2AkyzVb11cIPn5hCt2FFQVAfcxmI", False],
        "Cornaceae": ["1wvbABJ0X9lHr4lbpn7gy7Oyv8byVSUUYKvufS8EnIH8", False],
        "Commelinaceae": ["1zW6bGIvVNPUFCW33AtKZpvAa_JyRJ4p-pvuy0J78bG4", False],
        "Coriariaceae": ["1kF8zAixh4WZJj9QDmB9E5guJ4zOAwTiwQyh6Kizryko", False],
        "Circaeasteraceae": ["14CjFN4Dg9110KNHnbH0RRCAlEA_1sX20nyjaKrlfzh8", False],
        "Clausiaceae": ["1IA7QHJ2osLs-71eKDgLs0pFy8FrBu0O1qQnh3kqUjqU", False],
        "Nyctaginaceae": ["1-ZjpMSUYJuc_Z2mT9eeVLs47GHIVYn5mLyJGv6uLWEw", False],
        "Dipterocarpaceae": ["1aQVBWtT41QAAQYdVt-Dva-PUWE2WBegWVjojq2asK-M", False],
        "Dioscoriaceae": ["1rHedzPz0HypQa3fTDQyvTW5IZSuMDVHJ_PHbqwuD6FY", False],
        "Daphniphyllaceae": ["1OuvG7KQoqSgZ8OQJRqMIkbClUR5h6XuXuAYcZLPTeR4", False],
        "Drosaraceae": ["1EtQ8Zo0a7xo6uccacBBrFKDn84YNx4bPFJHlyrjoqQ0", False],
        "Ericaceae": ["1Dsymu_gF0UYvVe-WEZburXi1LM7_JGFnWjavi-MuqXU", False],
        "Tetramelaceae": ["1BLe2XejujQsZSa8JJ6vlBisp9AKTOZZc4tLiGuLGyLc", False],
        "Elaeocarpaceae": ["1OzF_0FuQyixtRYgnlO9Jy98yvoog8IV4WTosp6h2GeM", False],
        "Elatinaceae": ["1NKK5Oo75h7yb64DeX6296vzXseOgG_I1k6KUgEI3NYk", False],
        "Elaeagnaceae": ["1yMhIW05mRD3oyVhikXyb9mTL4oIxv6GVUYeuzWIkVWU", False],
        "Fagaceae": ["11XO-FhNLzfrJ64Xgen0rQME_J_bz_BEM-kjt3dHPJqE", False],
        "Gentianaceae": ["1WXEBMGmEdkKR99BHUmnND-1vXThBg8vPKqUVmRrjqNU", False],
        "Flacourtiaceae": ["1YOT_kQUNtTxGuGt4T2vogtS0zo8VkJakwco-2bqmquM", False],
        "Gesnereaceae": ["1Z2On-7lOPadRVv1DhvputENQ9ttgFZTJfuP8r8OY05c", False],
        "Guttiferae": ["1BLSqfka9i3ArcdqMNrpD36z3qkF1Hb3ozKavenGWHfA", False],
        "Haloragaceae": ["1vESINRAcTLxM8OQx14Ti0_27i9wG4_CcmWXUDIbjiVs", False],
        "Hippocastenaceae": ["1ogALHCYp0Nc-kf5_PLIbUzg4KLBKTzjSKPhSEcJUUyY", False],
        "Hippuridaceae": ["1ITu4EnwbilKhgDSlPiWuMEXL33PA8sg-wDc5rP5mF1w", False],
        "Hydrangeaceae": ["17qCC8sjbqew1FM9wI4EgXi8yHRAeEOeBVee5BcT5uSI", False],
        "Hydrocharitaceae": ["1ZsjVipwX6DWphJVRPMaFXGyRMPqSCHSBOHujPOBb6EU", False],
        "Juncaceae": ["1nUbL4n26pucD-NeEy-iuL6BZ_F_RQdO1qp0svQT0618", False],
        "Juglandaceae": ["1apv4FYDKml-trgxt66a08WFl89YbpmMFWh-bC6Oyu94", False],
        "Linaceae": ["1X9glN6PmT6xC_oTnxAEC3dwXDPvxWQjTHpRKw1_UjUw", False],
        "Juncaginaceae": ["1NM3dmImvPx87ugzSthqJ5s4uhUtaP8ya_95EbJn7B0E", False],
        "Lardizabalaceae": ["1HZpOhKUM3klaQFPwh5rNSd4LmaeCB0TvFjwXhp2FeJw", False],
        "Lecythidaceae": ["1XuTvO2AVrcjoiHOvSD9tUdlpYPelezOlwiIfmt8h1xY", False],
        "Lentibulariaceae": ["1ljteqUg9cHX5KQi4jv9Yr8hxN8ok8MTFSk_T__k2YDw", False],
        "Myrtaceae": ["1AWSQzNLfVpOJxEu--E_T55npvu7KuKkNRh-dxeK3kF0", False],
        "Lobeliaceae": ["1UEPzIsIhLUuSK15SFXmLPwCg40k49LNwSH8NPaRbvYw", False],
        "Loranthaceae": ["1AZI-d_cnUQuTrCAK_Fpe3ZBonuuGWrhG_fle986P_7w", False],
        "Lythraceae": ["1vnalcMvMzPTxK-3ZHgFhUQcoQ_gaLsMPvrFHpy5vPmU", False],
        "Myricaceae": ["1Qj_g0ByuZeJvyAup4EUKvKZ9NXVkp80VdgGOtdVd-0Q", False],
        "Musaceae": ["1woYG52xedKw9A1ccBfoDXoNnx3qlxNnaq-ZQTdtzSfk", False],
        "Moringaceae": ["1Mbfi5RQJcOfAX2SLSGYSSSu2ztOfB6hU3rkU0uhh078", False],
        "Menispermaceae": ["1DdEZ4TVivXiQR0nPo-PeNnKxnc7aI-Z2dfHrhllmEzk", False],
        "Meliaceae": ["1fsl4QKf7Uk1kqti6J6HIMnlQH2nk5g-PAp2vC8zT7AM", False],
        "Melastomaceae": ["1dIz0cRbBPhsVrk67AXjQpUzImpoa8PJsem2-PUohXXM", False],
        "Malpighiaceae": ["1t7yk3b_l1qgK0WXBzKscTzzHK0AdooH4h2u3t9-A-t8", False],
        "Magnoliaceae": ["1hJy1z-NERy-hhNiYGpv3MTkNg823tPT7He6qXqze_Ug", False],
        "Orobancaceae": ["1cmjTo8CVTfHR4XOrYqXTRZZipNz47OVWYWEKAGnBZAw", False],
        "Oleaceae": ["1w7X3xA16-XQL44_gBC_1ypYegCefDMlHmHz7WsYYKVc", False],
        "Poaceae": ["1zDtjVM4U5I5BfRTED5GTel2kIuKypv9PpKi8o2k0Ow4", False],
        "Paeonaceae": ["1EbafHGtwlj9rKGKJFJ00Xr31O7V4M21iH2otUcz3lyg", False],
        "Parnassiaceae": ["1vDRGpCKGqmhEOruVzYLb079_et57hDZiHYBydPq81-I", False],
        "Polygonaceae": ["1tx49tI7k7m_iAn3PQR3krRmLZzJOaAs2JaHuweJfxBc", False],
        "Phrymaceae": ["1_zhdNyI3AdFiCgDCY61woGieen-VFnPPK3d7fMujv58", False],
        "Plumbaginaceae": ["1D1x9R-EHNRW8NdxH8NW2uFZjRkzdD5nxldCxL6IW6pk", False],
        "Pedaliaceae": ["1aaRfwbaucX8S3Ae8lv_XJGLPT9ibNXapVeu63eHvklA", False],
        "Phytolaccaceae": ["1iL6-wejSoo8fF8mnUnAtKkk3BCfH_BqIcOSRaVnZ2yY", False],
        "Polygalaceae": ["1mEGbDNfCqFD_LFvp80eLdfgr9bKOPX-dhtvCXtOENG4", False],
        "Potamogetonaceae": ["1ReOIMlqQizBD3bMeEJro0KDCPpcRhQZQdGg2L_1i5Ww", False],
        "Rhizophoraceae": ["1DxI4oqm4HxW0AkOdGh8j8_qYrN_CY865i_tfHe8g5ws", False],
        "Passifloraceae": ["1wEymc-tslLpu-4tu_2TrVI6xGifmBWbwqXqSRhAC9_I", False],
        "Rhamnaceae": ["1MX_XJkQdcYdl6yjSOWWnrGXWkbMmEYrtlNnYmfKockw", False],
        "Scrophulariaceae": ["16Wre7oF75QDzPWk6KqinTOZZqR4DV9iAnAUF9QlXiDw", False],
        "Santalaceae": ["1jNTE2Z_NB1mwo00YSKh39ccR84uUfAztt_W7fovfB2Q", False],
        "Saururaceae": ["1wuSBgu9MqJdvMvqiIPKetK21tl5dnVOc-mmFUYfO-hA", False],
        "Simaroubaceae": ["1ZuemiyfWxwbzhy5kJcyY_x3hptyhxEoHmRiI8o7qCcg", False],
        "Stachyuraceae": ["1Sch_FW5BcVDa80n8b9tZsjJ1Ky1zE6zQHUQWNHD06q4", False],
        "Tamaricaceae": ["1XzFevAaxT2jvSxxIDmrBSt9NO-kzWTRjJCBfKRyvPZ4", False],
    }

    RANGE_ALL  = 'Sheet1!A1:R'
    RANGE_NAME = 'Sheet1!A2:L'

    SPECIES_INDEX = 0
    NEPAL_NAMES_INDEX = 1
    NEPAL_NAMES_BIB_INDEX = 2
    ENGLISH_NAMES_INDEX = 3
    ENGLISH_NAMES_BIB_INDEX = 4
    USE_CODE_INDEX = 5
    USE_CODE_BIB_INDEX = 6
    CHR_NUM_INDEX = 7
    CITATION_INDEX = 8
    NEPAL_DIST_INDEX = 9
    NEPAL_DIST_BIB_INDEX = 10
    
    NEPAL_SEARCH_WORDS = ['Godawari', 'Patan', 'Kuleswor']

    def normalize_row(self, row):
        TOTAL_COLS = 12
        for _ in range(len(row), TOTAL_COLS):
            row.append('')
        row[0] = row[0].strip(' ')
        return row

    def output_latex_string(self, str):
        strout = str
        strout = strout.replace('&', '\\&')
        strout = strout.replace('%', '\\%')
        strout = strout.replace(',', ', ')
        self.latex_file.write(strout)

    def is_heading_row(self, row):
        return (row[self.SPECIES_INDEX] != '')

    def output_latex_string_noreplace(self, str):
        self.latex_file.write(str)

    def output_citations(self, cite_string):
        cite_string = ''.join(cite_string.split())
        out_str = '\\citet{' + cite_string + '}\n\n'
        self.output_latex_string_noreplace(out_str)

    def output_citations_p(self, cite_string):
        cite_string = ''.join(cite_string.split())
        out_str = '\\citep{' + cite_string + '}\n'
        self.output_latex_string_noreplace(out_str)

    def format_scientific_name_list(self, in_str):
        in_str = in_str.replace('\n', ' ')
        in_str = in_str.strip(' ,')
        str_lst = in_str.split(',')
        for i in range(0, len(str_lst)):
            str_lst[i] = self.format_scientific_name(str_lst[i])
        return ','.join(str_lst)
                
    def __emphasis_first_word(self, in_str):
        if in_str == '':
            raise Exception("Expecting non-empty string")

        m = re.match(r"\s*(\w+)(.*)", in_str, re.I)
        if m:
            # print(in_str)
            # print(m.groups())
            return '{\\em ' + m.group(1) + '}' +  self.__format_sc_post_str(m.group(2))
        else:
            return in_str

    def __format_var_sep(self, sep_str, split_str):
        out_str = split_str[0]
        for i in range(1, len(split_str)):
            out_str += sep_str + ' ' + self.__emphasis_first_word (split_str[i]) 
        return out_str

    def __format_sc_post_str(self, in_str):
        if in_str == '':
            return in_str
        # see if we can match subsp.
        split_str = in_str.split('subsp.')
        if len(split_str) > 1: 
            return self.__format_var_sep('subsp.', split_str)
        # see if we can match ssp.
        split_str = in_str.split('ssp.')
        if len(split_str) > 1: 
            return self.__format_var_sep('ssp.', split_str)
        # see if we can match var.
        split_str = in_str.split('var.')
        if len(split_str) > 1: 
            return self.__format_var_sep('var.', split_str)
        
        return in_str

    def get_genus(self, in_str):
        print(f'get_genus({in_str})')
        in_str = in_str.replace('\n', ' ')
        in_str = in_str.strip(' ,')
        return in_str.partition(' ')[0]

    def format_scientific_name(self, in_str):
        in_str = in_str.replace('\n', ' ')
        in_str = in_str.strip(' ,')
        print(f'format_scientific_name({in_str})')
        m = re.match(r'\s*(\w+\.?\s+[-\w]+)(.*)', in_str, re.I) # match first two words
        if m:
            out_str = '{\\em ' + m.group(1) + '}' + self.__format_sc_post_str(m.group(2))
            return out_str
        else:
            raise Exception(f'Scientific name {in_str} does not seem to be in correct format')

    def generate_latex_row_chr_num(self, row):
        # output chromosome numbers and citation as a separate row
        chr_num = row[self.CHR_NUM_INDEX].strip(',. ')
        citations = row[self.CITATION_INDEX].strip(',. ')
        if len(chr_num) == 0:
            chr_num = 'Missing-Data'
        self.output_latex_string('\\begin{hangparas}{0.5cm}{1}\\noindent \\textbf{$' + chr_num + '$} ')
        self.output_citations_p(citations)
        self.output_latex_string('\\end{hangparas}\n')

    def generate_latex_subheading(
            self, row, str_heading, content, bib_index, capstyle):
        if (capstyle == CapStyle.CAP_WORDS):
            content = string.capwords(content)
        elif (capstyle == CapStyle.LOWER):
            content = content.lower()
        self.output_latex_string(
                    '\\begin{hangparas}{0.5cm}{1}\n'
                    f'\\noindent \\textbf{{\\small {str_heading}}}: ' \
                    + '\\begin{otherlanguage}{hindi} ' \
                    + '{' \
                    + content + '} \\end{otherlanguage}\n')
        bib = row[bib_index].strip(',. ')
        self.output_latex_string('{\\small ')
        self.output_citations_p(bib + '\n\n')
        self.output_latex_string('}\\end{hangparas}\n\n\\vspace{2mm}')
    
    def generate_latex_row(self, row):
        # print(f'generate_latex_row({row})')
        if self.is_heading_row(row):
            self.output_latex_string('\\vspace{5mm}')
            self.output_latex_string(
                '\\section{' + self.format_scientific_name(row[self.SPECIES_INDEX]) + '}\n')
            if row[self.NEPAL_NAMES_INDEX] != '':
                self.generate_latex_subheading(
                    row, 
                    "Common Name(s) in use in Nepal",
                    row[self.NEPAL_NAMES_INDEX], self.NEPAL_NAMES_BIB_INDEX,
                    CapStyle.LOWER)
                
            if row[self.ENGLISH_NAMES_INDEX] != '':
                self.generate_latex_subheading(
                    row, 
                    "Common Name(s) in English",
                    row[self.ENGLISH_NAMES_INDEX], self.ENGLISH_NAMES_BIB_INDEX,
                    CapStyle.CAP_WORDS)

            if row[self.USE_CODE_INDEX] != '':
                self.generate_latex_subheading(
                    row, 
                    "Uses",
                    row[self.USE_CODE_INDEX], self.USE_CODE_BIB_INDEX,
                    CapStyle.AS_IS)
            
            if row[self.NEPAL_DIST_INDEX] != '':
                self.generate_latex_subheading(
                    row, 
                    "Distribution in Nepal",
                    self.add_msl(row[self.NEPAL_DIST_INDEX]), 
                    self.NEPAL_DIST_BIB_INDEX,
                    CapStyle.AS_IS)
            
            self.output_latex_string('\\vspace{4mm}\n\n') 
            
        # output chromosome numbers and citation as a separate row
        self.generate_latex_row_chr_num(row)
        
    def add_msl(self, in_str):
       return re.sub(r'([0-9]+)', r'\1 msl', in_str)

    def generate_latex(self, family_name):
        fn_utf = family_name.encode('utf8')
        print(f'\t\t\tgenerate_latex({fn_utf})')
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret_563563514748-486lji2ouvg2svb016j2gbe65135ks9r.apps.googleusercontent.com.json', self.SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))

        # Call the Sheets API
        sheet = service.spreadsheets()
        sheet_id = self.SPREADSHEET_DICT[family_name][0]
        # result = sheet.values().get(spreadsheetId=sheet_id,
        #                             range=self.RANGE_NAME).execute()
        result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=self.RANGE_ALL).execute()
                                    
        val_all = result.get('values', [])

        #print(val_all[0])
        if (val_all[0][0] != 'Taxon'):
            # remove first row and column from result
            values = [val_all[i][1:] for i in range(1, len(val_all))]
        else:
            # remove first row and 9th column from result
            values = [val_all[i][:9] + val_all[i][10:] for i in range(1, len(val_all))]
        print(values[0])

        self.latex_file = open('output/' + family_name + '.table.tex', 'w', encoding="utf-8")
        for i in range(0, len(values)):
            row = values[i]
            if (len(row) == 0): # skip if empty row
                continue
            row = self.normalize_row(row)
            if (self.is_heading_row(row)):
                self.num_species_in_fam += 1
                row_genus = self.get_genus(row[self.SPECIES_INDEX])
                if row_genus != self.current_genus:
                    self.num_genus_in_fam += 1
                    self.current_genus = row_genus
            self.generate_latex_row(row)
        self.latex_file.close()

    def move_dist_data(self, row, move_str):
        if not (row[self.NEPAL_DIST_INDEX].isspace()):
            row[self.NEPAL_DIST_INDEX] += ', '
        row[self.NEPAL_DIST_INDEX] += move_str
        row[self.NEPAL_DIST_INDEX] = row[self.NEPAL_DIST_INDEX].strip(',. ')

    def generate_latex_all_families(self):
        all_families_file = open('output/families.tex', 'w')
        for family in sorted(self.SPREADSHEET_DICT):
            need_processing = self.SPREADSHEET_DICT[family][1]

            self.current_genus = ''
            self.num_genus_in_fam = 0
            self.num_species_in_fam = 0
            
            all_families_file.write('\\include{' + family + '}\n')
            
            if need_processing:
                self.generate_latex(family)
                family_tex_file = open('output/' + family + '.tex', 'w')
                family_tex_file.write('\\chapter{' + family + '}\n\n' +
                    '\\input{' + family + '.count.tex}\n\n' +   
                    '\\input{' + family + '.table.tex}\n\n' + 
                    '\\vspace{5mm}'
                                    '\\bibliographystyle{plainnat}\n' + 
                                    '\\bibliography{Bibliography}\n')
                family_tex_file.close()
                family_count_file = open('output/' + family + '.count.tex', 'w')
        
                if self.num_genus_in_fam == 1:
                    genus_article = 'is a single'
                    genus_word = 'genus'
                    
                else:
                    genus_article = f'are {self.num_genus_in_fam}'
                    genus_word = 'genera'

                if self.num_species_in_fam == 1:
                    fam_article = 'a single'
                else:
                    fam_article = f'{self.num_species_in_fam}'

                family_count_file.write(
                    'There %s %s and %s species reported with chromosome counts  '
                    'of plants found in Nepal in this family.\\vspace{-5mm}'%
                        (genus_article, genus_word, fam_article)
                )
                family_count_file.close()
                time.sleep(2)
        all_families_file.close()
            

if __name__ == '__main__':
    lgen = LatexGenerator()
    lgen.generate_latex_all_families()
