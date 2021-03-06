
import re
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import string
from enum import Enum
import time

class ColumnFixer:

    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

    # The ID and range of spreadsheets.     

    SPREADSHEET_DICT = {
        "Caryophyllaceae": "1ZteEsKR5j3DUBfd05XMr0VDpJHusK252muqecmIGRTc",
        "Caricaceae": "1jfuUUy74rPzWm4Zl9E7DzFghSF2PzraMw0vMPDrM1js",
        "Caprifoliaceae": "1rrH8RnMypK7Rgyg0kcrSOiu0kojkBfycfFNHDn32J7g",
        "Cannabaceae": "1EUf_M38fr2Fa6J20OqS1jQqtHHgcUnLm7AvgJQW3ghA",
        "Campanulaceae": "1_bS45r9lEXeN9GkMT8s0C6byOjoM9VNiausNUUlKqsg",
        "Basellaceae": "1B-TLV6aKrp3eyqSvdHuG6z-YoHjvMI1JrC-aRji76ao",
        "Capparaceae": "1ViObgOHXYTKCHHf_yRa84UxDK34dRiiZrpZr4CgWEZc",
        "Cannaceae+‌": "1_plRcrI3NLxZldyMMYfI6WOzVkj541R4Lu0_dbEtjKc",
        "Callistricaceae": "11vu_Od9dwv9yDFPs4TI4NuUhn2iZu86Not1KpbMD0Ck",
        "Burseraceae +‌": "1zVgTT8fOYECUhUN0tqmKgIgUv5-_C95CYQBWkAfCgtU",
        "Boraginaceae‌": "1ICLaRsV4LUvwSUQLSwbrJQSgrDiGa8-20aFujs9UogI",
        "Bromelliaceae": "1_Vu4eUkaknzNT8C4d7zVKJCVE_qdljOPP8gkdHoaZH4",
        "Brassicaceae": "1TKt9hILyc7Iapfp9T_jQo0whcPbFffQySTqrN1qspm0",
        "Bombacaceae": "1ICUvGYuTzUEwFGfzVpqX2l6dZ22GRePWMLEIIIuU4nI",
        "Asteraceae": "1R26HJFoGIvVyQDebvN0T_lUZLxP07YHQtl-yt1cinJI",
        "Berberidaceae": "1WwCvMDnWxNF58cgKR-plJmF_fgnxidTC_XSmBb4UFfA",
        "Betulaceae": "12dpTJwd0ymeb2ssCFB9g1IzkiHTdhZZ-wMtX0rgmYI0",
        "Begoniaceae": "1v-X3D708YPf5mcwaNMhQ6GOazG2UjWKJfZsUSic2omQ",
        "Balsaminaceae": "1swLGYE7r6xcO_2RBXC8Bk7-urWk4CL9c5CmAwlrKpZE",
        "Aquifoliaceae": "1TkEFy28X1iCL0fbb4JuvNeFdUjyeG4wGhcXDfHj8J5Q",
        "Asclepiadaceae": "1It_JAnjSrSl6qDXckqy67JldjgzqXndA7JUZu-h3Rc0",
        "Aristrolochiaceae": "1eWGC74p0g-hw9ctUqxYaJExlsUUlS9w_TdMYG7aPfR4",
        "Araliaceae": "18eVtHUVzH9_X-uBAgCUoDVOeLlEHOmjJdYNzxZEvIUQ",
        "Araceae": "1bwrFv_iPJ89UGx115ZoRSqjGRY_m1_p1PifbHRiuPtA",
        "Aracaceae": "1JwrLcL5oJQQJFPxXY-y-rNOrqrLic1Zb7iGRslLeVf4",
        "Verbenaceae+‌‌‌‍‍‍‌": "1iMwW2H5y1yEPp6TfjiyxcUwbZP6MInqPbeYym8hg1aI",
        "Chenopodiaceae": "1qkqO5DL8FM4I9dZuJcMF89X4ZXmuU6wi73Y2K3vx3xQ",
        "Bignoniaceae": "1zzZ7XG4Alxwf5RX6mNPT3K6gTGM5xegF2xhidmsn6Bo",
        "Amaryllidaceae": "1tbM4IdBSmJRT2NN0AThbW5WNW0eVYHJWOFL0TvI5iYQ",
        "Nymphaeaceae": "1xvLM34YgiU2jw-zxdbfEm9r3egZ-fPk9Of2rAxUip1k",
        "Anacardiaceae": "1zCHts6_bkNaD7P-m3MDcGAEzLC9Df_CuvYxzi4amYN0",
        "Violaceae": "1ImPm9KK0yCDofc-k8dPkWn2Sk02YrmBDj5S9ZshRZEw",
        "Combretaceae": "1omT4FKB7wyZ0h6KF-Tc1RtxPi2qBlmpn7hBFLM88IfI",
        "Apiaceae": "1oI_jKwBDmhcRRuQey3YNAEDDKgQbGY6-qStlGN_WkcI",
        "Amaranthaceae": "1UpAvdWhzjti04YIXxa5_FWbbfCQC2Z3hVcryn-VA9xQ",
        "Fabaceae": "11La7RwBy_D-10_sDPD5SSyJFKvSnRiJpDmt1r_XeYZQ",
        "Apocynaceae": "1PHe5lXT6eR6KkMnb0iAXo1_HjQJD8k2yiRashA3uMX8",
        "Aponogetonaceae": "1-UZdVUrah1ZgOXHyUKz3iBvKCgPRVzalI2NxHYlbGdM",
        "Alangiaceae": "1Z9bLIm1q21cLek5cq6_dv9eAmCjrlLhekkWxxDPLmhE",
        "Agavaceae": "1IadRjWtV_dEsMEgmNhAFY2-viQ0Ug7fUmSyuh4km2Uk",
        "Annonaceae‌": "1bN4I6az_ISWVTPD3qEu6Xxm6m07dLhNonnWgTuiaKko",
        "Moraceae": "1R_fjHIXjydqBaPZBFNMbJ6spxy9UzDXI2Lo0hjeor6k",
        "Aceraceae": "1RqlxSLZs8Uhz2xyCFRq-541jyIqZRUejcGVX_WIPblw",
        "Alismataceae": "1Vq-Z6vmNsLbQzu3ISfae3vmG3xMPg3HcAeH7dZsSA_8",
        "Acanthaceae": "1vbkdYUAIzmHhqRZCPx_wvImylWM_BqxcuhY2aIKZfuw",
        "Aizoiceae": "1j_GgOSlBSEuzgbUOFU5p9eS8iixgbG-iASnL7u0g718",
        "Lauraceae": "1VsMTlVAueUgHgIN2WtUbf7wceLs-F9kNe7M6IGvMiEM",
        "Cucurbitaceae": "1q0DyiSzb7-CxA_uiK27Hf1Oy7CcjASRI_jjT0Msib8c",
        "Oxalidaceae": "1wP95w2sYahsU_LVnaXTDR0rGSM3PWgMsU5-5W-XKSZI",
        "Datiscaceae": "1bMuTJ-13e3ImBt-0-rITpowW2qxHROs31yJtOtEL9TQ",
        "Euphorbiaceae": "1PpIfiJimzCl3r_ZRM0ESy60hPTQjwoLXk57vyXjCwB4",
        "Dipsacaceae": "1KNDoeE3Qb3XI5uzRQmkSVy-sa0TY01SUOOkvP4Guwv4",
        "Ebenaceae": "1iJdlRBqJfh1wSAlbcRpDv0gutmrEgFKdJHS9GfRyLCc",
        "Punicaceae‌‌": "1OPv1OJVtxB92QJqIkQrTfoWGuo-hEgq7a0_6wkfBLx4",
        "Ranunculaceae": "1LwCKgWaOAyH3nz1o65_JmkvyuA6-bZbtl3TZKBHnbRg",
        "Onagraceae": "1SsTfFslaB3NypSIlTLx_xeAdIYa_Ru0fXAZ98jO9RIE",
        "Hypericaceae": "1gwqRXRxQPvk1VeTwlM6Yma5_zQIBNzLw3r5zAYExNSI",
        "Geraniaceae": "1Bz8U9N8j-6IA4eZhirPuaK07UDwsVFx50tR48VOCADQ",
        "Malvaceae": "1mcsOGRWQrhGYT8lCb7XCcmAboZNJwVjIJV32ZyawE_s",
        "Rosaceae": "1b1oiHVok83hrr3lRdm5ZIPkl-a3V8l32NbU_ZrW1Lrk",
        "Primulaceae": "1JBUT0Dv4uZUDHhUQ-a506YsoNECo4F_CONMncL3q5GI",
        "Crassulaceae": "1inRLht4bZKpOoh6vcRp9D0jW8Ay1cm-Ez-arpHDtc3o",
        "Zygophyllaceae": "1in1Si3aOLMbXlR1PMTV2Dx_6dEiNN54GG2uR5itkMws",
        "Fumariaceae": "1sreIkDQdI5qje3xosxS4l9Kn9zyBcdEdjHx5T5HX8uQ",
        "Liliaceae": "1OfUprilynnynmRt1OHGRVcUZu6KQ5YAUg0Wer1nrPLQ",
        "Convolvulaceae": "1K6thfNrWFKgduaVnZfIIS6jWVKEOxiFYQaXkPIJt3-E",
        "Papaveraceae‌‌": "1ibRIKXKuq3fIDuIB_noHLVWn6IGFKXF5MJ5-C0x2N1E",
        "Ceratophyllaceae": "1mjgpjXj0Ab0gb-BAGlMCT_KbFRnPOUCCpD47vBTPHuU",
        "Portulacaceae": "1AM3ReBe83slvM7A310ITueBzhgoQOLMtG_JtcLyj45Y",
        "Urticaceae": "16fHAU-v6J9f2boMDoEXaydNM1JkIr61LfXQC3BkVNjQ",
        "Rubiaceae": "1T1lpbLcaRJIxUdOPGQ7hINGqSvbm8UIbFtjSXLgODb4",
        "Solanaceae": "1IRVq5z9tcaHjhrUaLO4RxyL4W1kw6jJqC7t4keVnki0",
        "Ulmaceae": "1CVIMRZDRSdHxzECL78jIHyWZzQ3KQ2qqAj_bL9YpDjs",
        "Valerianaceae": "14fuPJiT7I5NuteLHHIUGsYVv4PZnoTg2dnTrDNfA3Wo",
        "Vitaceae": "1rmsV6Z63_z_o40ZlDMY2XUykGe_Jbr9OX73bkS5GwUg",
        "Zingiberaceae": "1fioMKPZvf5yTzCltrJgI4M1nRHQ1MzktFuyeR-nltcI",
        "Iridaceae": "1OmMboJvHSGEDrVB3FeNqhF81vPjQ6FFKMlJ9T52UX5c",
        "Symplocaceae‌‌": "1MWS2_f1BKz5yW2256DdYoGHlUYJ61io-4qdOfieEMq0",
        "Sterculiaceae": "1ZLu75Mgdsfs8nJnMnj0uMVW_ecK83OZN1dz8VW6hYXQ",
        "Sphenucleaceae‌": "10cYW2tK38A0PRUIbqjRECn_ejGuWMns-0DUkLz3mogk",
        "Schizandraceae": "1nFr6x-u2w5dAnnZo8lBUzIRqpP6hxGBP7n1wBFtrxS8",
        "Sapotaceae": "1R98eeZ1k2x2L-_rPYmvUhjcm1GlyvdcohjpM5UmHlmU",
        "Sapindaceae‌‌": "14bsCNMYYcr_RVzT2KcIJJPh7B4vBCnE959jY0Zhw_hQ",
        "Salicaceae": "1WtMJA1Smj2FhAJjjHEj0aytbX1vsRLr4UeDsxFFYvjk",
        "Sabiaceae": "1CE-S0fT4s7mIZt0RJpQBn7mHKEI4qQphlDu_gq8DfPY",
        "Rutaceae": "1qTOQDH2Cl2995_3H5HSieB8nUzyiCtS6A_IZ_NyZTXg",
        "Typhaceae": "1PH6VHK39b6llcHEKxKLu7c34eHTOvPwejqjzC3I8QNE",
        "Toricelliaceae": "1_zR4D8eUefd_eo0AfCWoTi9XdtTXimR_rdg_ViXR0zE",
        "Thymalaeaceae‌‌": "1UkDRZt0Q1xwdu7LGWKVOUh1uD-594RPsp-BR2OKwUzo",
        "Theaceae": "1sLYsIvwFcPWAk5zVnk4viRLZoa-Qv7_gNd3c6DHpvi8",
        "Orchidaceae": "1VB6t0N0tTDuv-FJZnbb-7AOycLWt8smYw00EWmOreIc",
        "Myrsinaceae‌": "1IdqUQ0HWy0zG5_Yw0nHUUuh3GVR34KWA3-Ld_l5T-N8",
        "Lamiaceae": "1ERHYCelqy4-ne5HUvVwV8G-D2R-cgbV1-Uy8QSlm5fM",
        "Hypoxidaceae": "10rw45TEDPvM_56qNf2qqdWKGAhAKdsEwcryzREKKpQM",
        "Tropeolaceae": "1A1QG6D3P9kGxjPec6A5Sf-nO77avwAKGYlpmikX4oNQ",
        "Saxifragaceae": "1VJt7UHa5CM7WBECrfvP7Ug2fyI60hJH-EhlNBC-CPr8",
        "Cyperaceae": "1Bdx01EW23p27t9PcMq2ANzXQvwkckDV58ZMY8K5XOio",
        "Chloranthaceae": "1DwjDVtjZlfjcp8_2AkyzVb11cIPn5hCt2FFQVAfcxmI",
        "Cornaceae": "1wvbABJ0X9lHr4lbpn7gy7Oyv8byVSUUYKvufS8EnIH8",
        "Commelinaceae ‌": "1zW6bGIvVNPUFCW33AtKZpvAa_JyRJ4p-pvuy0J78bG4",
        "Coriariaceae": "1kF8zAixh4WZJj9QDmB9E5guJ4zOAwTiwQyh6Kizryko",
        "Circaeasteraceae": "14CjFN4Dg9110KNHnbH0RRCAlEA_1sX20nyjaKrlfzh8",
        "Clausiacece": "1IA7QHJ2osLs-71eKDgLs0pFy8FrBu0O1qQnh3kqUjqU",
        "Nyctaginaceae": "1-ZjpMSUYJuc_Z2mT9eeVLs47GHIVYn5mLyJGv6uLWEw",
        "Dipterocarpaceae": "1aQVBWtT41QAAQYdVt-Dva-PUWE2WBegWVjojq2asK-M",
        "Dioscoriaceae": "1rHedzPz0HypQa3fTDQyvTW5IZSuMDVHJ_PHbqwuD6FY",
        "Daphniphyllaceae": "1OuvG7KQoqSgZ8OQJRqMIkbClUR5h6XuXuAYcZLPTeR4",
        "Drosaraceae": "1EtQ8Zo0a7xo6uccacBBrFKDn84YNx4bPFJHlyrjoqQ0",
        "Ericaceae": "1Dsymu_gF0UYvVe-WEZburXi1LM7_JGFnWjavi-MuqXU",
        "Tetramelaceae": "1BLe2XejujQsZSa8JJ6vlBisp9AKTOZZc4tLiGuLGyLc",
        "Elaeocarpaceae": "1OzF_0FuQyixtRYgnlO9Jy98yvoog8IV4WTosp6h2GeM",
        "Elatinaceae": "1NKK5Oo75h7yb64DeX6296vzXseOgG_I1k6KUgEI3NYk",
        "Elaeagnaceae": "1yMhIW05mRD3oyVhikXyb9mTL4oIxv6GVUYeuzWIkVWU",
        "Fagaceae": "11XO-FhNLzfrJ64Xgen0rQME_J_bz_BEM-kjt3dHPJqE",
        "Gentianaceae": "1WXEBMGmEdkKR99BHUmnND-1vXThBg8vPKqUVmRrjqNU",
        "Flacourtiaceae": "1YOT_kQUNtTxGuGt4T2vogtS0zo8VkJakwco-2bqmquM",
        "Gesnereaceae": "1Z2On-7lOPadRVv1DhvputENQ9ttgFZTJfuP8r8OY05c",
        "Guttiferae": "1BLSqfka9i3ArcdqMNrpD36z3qkF1Hb3ozKavenGWHfA",
        "Haloragaceae": "1vESINRAcTLxM8OQx14Ti0_27i9wG4_CcmWXUDIbjiVs",
        "Hippocastenaceae": "1ogALHCYp0Nc-kf5_PLIbUzg4KLBKTzjSKPhSEcJUUyY",
        "Hippuridaceae": "1ITu4EnwbilKhgDSlPiWuMEXL33PA8sg-wDc5rP5mF1w",
        "Hydrangeaceae": "17qCC8sjbqew1FM9wI4EgXi8yHRAeEOeBVee5BcT5uSI",
        "Hydrocharitaceae": "1ZsjVipwX6DWphJVRPMaFXGyRMPqSCHSBOHujPOBb6EU",
        "Juncaceae": "1nUbL4n26pucD-NeEy-iuL6BZ_F_RQdO1qp0svQT0618",
        "Juglandaceae": "1apv4FYDKml-trgxt66a08WFl89YbpmMFWh-bC6Oyu94",
        "Linaceae": "1X9glN6PmT6xC_oTnxAEC3dwXDPvxWQjTHpRKw1_UjUw",
        "Juncaginaceae": "1NM3dmImvPx87ugzSthqJ5s4uhUtaP8ya_95EbJn7B0E",
        "Lardizabalaceae": "1HZpOhKUM3klaQFPwh5rNSd4LmaeCB0TvFjwXhp2FeJw",
        "Lecythidaceae": "1XuTvO2AVrcjoiHOvSD9tUdlpYPelezOlwiIfmt8h1xY",
        "Lentibulariaceae": "1ljteqUg9cHX5KQi4jv9Yr8hxN8ok8MTFSk_T__k2YDw",
        "Myrtaceae": "1AWSQzNLfVpOJxEu--E_T55npvu7KuKkNRh-dxeK3kF0",
        "Lobeliaceae‌": "1UEPzIsIhLUuSK15SFXmLPwCg40k49LNwSH8NPaRbvYw",
        "Loranthaceae‌": "1AZI-d_cnUQuTrCAK_Fpe3ZBonuuGWrhG_fle986P_7w",
        "Lythraceae‌‌‌": "1vnalcMvMzPTxK-3ZHgFhUQcoQ_gaLsMPvrFHpy5vPmU",
        "Myricaceae": "1Qj_g0ByuZeJvyAup4EUKvKZ9NXVkp80VdgGOtdVd-0Q",
        "Musaceae": "1woYG52xedKw9A1ccBfoDXoNnx3qlxNnaq-ZQTdtzSfk",
        "Moringaceae": "1Mbfi5RQJcOfAX2SLSGYSSSu2ztOfB6hU3rkU0uhh078",
        "Menispermaceae": "1DdEZ4TVivXiQR0nPo-PeNnKxnc7aI-Z2dfHrhllmEzk",
        "Meliaceae": "1fsl4QKf7Uk1kqti6J6HIMnlQH2nk5g-PAp2vC8zT7AM",
        "Melastomaceae": "1dIz0cRbBPhsVrk67AXjQpUzImpoa8PJsem2-PUohXXM",
        "Malpighiaceae": "1t7yk3b_l1qgK0WXBzKscTzzHK0AdooH4h2u3t9-A-t8",
        "Magnoliaceae": "1hJy1z-NERy-hhNiYGpv3MTkNg823tPT7He6qXqze_Ug",
        "Orobancaceae": "1cmjTo8CVTfHR4XOrYqXTRZZipNz47OVWYWEKAGnBZAw",
        "Oleaceae": "1w7X3xA16-XQL44_gBC_1ypYegCefDMlHmHz7WsYYKVc",
        "Poaceae": "1zDtjVM4U5I5BfRTED5GTel2kIuKypv9PpKi8o2k0Ow4",
        "Paeonaceae": "1EbafHGtwlj9rKGKJFJ00Xr31O7V4M21iH2otUcz3lyg",
        "Parnassiaceae": "1vDRGpCKGqmhEOruVzYLb079_et57hDZiHYBydPq81-I",
        "Polygonaceae": "1tx49tI7k7m_iAn3PQR3krRmLZzJOaAs2JaHuweJfxBc",
        "Phrymaceae": "1_zhdNyI3AdFiCgDCY61woGieen-VFnPPK3d7fMujv58",
        "Plumbaginaceae": "1D1x9R-EHNRW8NdxH8NW2uFZjRkzdD5nxldCxL6IW6pk",
        "Pedaliaceae": "1aaRfwbaucX8S3Ae8lv_XJGLPT9ibNXapVeu63eHvklA",
        "Phytolaccaceae": "1iL6-wejSoo8fF8mnUnAtKkk3BCfH_BqIcOSRaVnZ2yY",
        "Polygalaceae": "1mEGbDNfCqFD_LFvp80eLdfgr9bKOPX-dhtvCXtOENG4",
        "Potamogetonaceae": "1ReOIMlqQizBD3bMeEJro0KDCPpcRhQZQdGg2L_1i5Ww",
        "Rhizophoraceae": "1DxI4oqm4HxW0AkOdGh8j8_qYrN_CY865i_tfHe8g5ws",
        "Passifloraceae‌‌‌": "1wEymc-tslLpu-4tu_2TrVI6xGifmBWbwqXqSRhAC9_I",
        "Rhamnaceae": "1MX_XJkQdcYdl6yjSOWWnrGXWkbMmEYrtlNnYmfKockw",
        "Scrophulariaceae": "16Wre7oF75QDzPWk6KqinTOZZqR4DV9iAnAUF9QlXiDw",
        "Santalaceae": "1jNTE2Z_NB1mwo00YSKh39ccR84uUfAztt_W7fovfB2Q",
        "Saururaceae": "1wuSBgu9MqJdvMvqiIPKetK21tl5dnVOc-mmFUYfO-hA",
        "Simaroubaceae": "1ZuemiyfWxwbzhy5kJcyY_x3hptyhxEoHmRiI8o7qCcg",
        "Stachyuraceae": "1Sch_FW5BcVDa80n8b9tZsjJ1Ky1zE6zQHUQWNHD06q4",
        "Tamaricaceae": "1XzFevAaxT2jvSxxIDmrBSt9NO-kzWTRjJCBfKRyvPZ4",
    }

    RANGE_ALL  = 'Sheet1!A1:Z'

    def fix_family(self, family_name):
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
        sheet_id = self.SPREADSHEET_DICT[family_name]
        result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=self.RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('Fixing...')

    def fix_all_families(self):
        for family in sorted(self.SPREADSHEET_DICT):
            self.fix_family(family)
            time.sleep(0.1)

if __name__ == '__main__':
    fixer = ColumnFixer()
    fixer.fix_all_families()
