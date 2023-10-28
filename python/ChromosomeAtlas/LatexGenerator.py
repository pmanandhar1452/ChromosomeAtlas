import re
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import string
from enum import Enum
import time


class CapStyle(Enum):
    AS_IS = 0
    LOWER = 1
    CAP_WORDS = 2


class LatexGenerator:
    latex_file = None
    current_genus = ""
    num_species_in_fam = 0
    num_genus_in_fam = 0
    use_acronyms_to_remove = {"Bu", "Wf"}
    use_acronyms_to_replace = {
        "Taxonomy": "Ta",
        "AM": "M",
        "cond": "S",
        "spic": "S",
        "F": "E",
        "V": "E",
        "Oil": "O",
        "Fuel": "Fw",
        "fl": "Fl",
        "FW": "Fw",
        "Mn": "M",
        "PP": "Pp",
        "Ic": "A",
        "Pa": "P",
        "Dr": "M",
        "PO": "Po",
        "Pe": "A",
    }
    all_use_codes = set()

    def replace_use_codes(self, theset, replacement_dict):
        newset = theset.copy()
        for e in theset:
            if e in replacement_dict:
                newset.remove(e)
                newset.add(replacement_dict[e])
        return newset

    def add_str_list_to_set(self, theset, comma_sep_values):
        values_list = comma_sep_values.replace(" ", ",").split(",")
        for value in values_list:
            value_s = value.strip()
            if len(value_s) > 0:
                theset |= set([value_s])

    def set_to_string(self, theset):
        s = ""
        for e in theset:
            s += str(e) + ", "
        s = s.rstrip(", ")
        return s

    # If modifying these scopes, delete the file token.json.
    SCOPES = "https://www.googleapis.com/auth/spreadsheets"

    # The ID and range of spreadsheets.
    SPREADSHEET_DICT = {
        "Acanthaceae": ["1vbkdYUAIzmHhqRZCPx_wvImylWM_BqxcuhY2aIKZfuw", False],
        "Aceraceae": ["1RqlxSLZs8Uhz2xyCFRq-541jyIqZRUejcGVX_WIPblw", False],
        "Actinidiaceae": ["17aMOxkNo4R-9xO4F-iKW_EcLLi1KW4phkPhvmWC8kQM", False],
        "Agavaceae": ["1IadRjWtV_dEsMEgmNhAFY2-viQ0Ug7fUmSyuh4km2Uk", False],
        "Aizoiceae": ["1j_GgOSlBSEuzgbUOFU5p9eS8iixgbG-iASnL7u0g718", False],
        "Alangiaceae": ["1Z9bLIm1q21cLek5cq6_dv9eAmCjrlLhekkWxxDPLmhE", False],
        "Alismataceae": ["1Vq-Z6vmNsLbQzu3ISfae3vmG3xMPg3HcAeH7dZsSA_8", False],
        "Amaranthaceae": ["1UpAvdWhzjti04YIXxa5_FWbbfCQC2Z3hVcryn-VA9xQ", False],
        "Amaryllidaceae": ["1tbM4IdBSmJRT2NN0AThbW5WNW0eVYHJWOFL0TvI5iYQ", False],
        "Anacardiaceae": ["1zCHts6_bkNaD7P-m3MDcGAEzLC9Df_CuvYxzi4amYN0", False],
        "Annonaceae": ["1bN4I6az_ISWVTPD3qEu6Xxm6m07dLhNonnWgTuiaKko", False],
        "Anthericaceae": ["1LcaC_si04LuZKHLkmcYeiNNken7odD721JVYCKluRjE", False],
        "Apiaceae": ["1oI_jKwBDmhcRRuQey3YNAEDDKgQbGY6-qStlGN_WkcI", False],
        "Apocynaceae": ["1PHe5lXT6eR6KkMnb0iAXo1_HjQJD8k2yiRashA3uMX8", False],
        "Aponogetonaceae": ["1-UZdVUrah1ZgOXHyUKz3iBvKCgPRVzalI2NxHYlbGdM", False],
        "Aquifoliaceae": ["1TkEFy28X1iCL0fbb4JuvNeFdUjyeG4wGhcXDfHj8J5Q", False],
        "Aracaceae": ["1JwrLcL5oJQQJFPxXY-y-rNOrqrLic1Zb7iGRslLeVf4", False],
        "Araceae": ["1bwrFv_iPJ89UGx115ZoRSqjGRY_m1_p1PifbHRiuPtA", False],
        "Araliaceae": ["18eVtHUVzH9_X-uBAgCUoDVOeLlEHOmjJdYNzxZEvIUQ", False],
        "Aristrolochiaceae": ["1eWGC74p0g-hw9ctUqxYaJExlsUUlS9w_TdMYG7aPfR4", False],
        "Asclepiadaceae": ["1It_JAnjSrSl6qDXckqy67JldjgzqXndA7JUZu-h3Rc0", False],
        "Asparagaceae": ["1b5lkHpTqm9aj_jT8Jpzgr4AEc8wIKfutAV5WO30d98Q", False],
        "Asphodelaceae": ["1iDX4M16F6bCzjMzlmp044UlMvwltU2xw3-gqgBMyuJU", False],
        "Asteraceae": ["1R26HJFoGIvVyQDebvN0T_lUZLxP07YHQtl-yt1cinJI", False],
        "Balsaminaceae": ["1swLGYE7r6xcO_2RBXC8Bk7-urWk4CL9c5CmAwlrKpZE", False],
        "Basellaceae": ["1B-TLV6aKrp3eyqSvdHuG6z-YoHjvMI1JrC-aRji76ao", False],
        "Begoniaceae": ["1v-X3D708YPf5mcwaNMhQ6GOazG2UjWKJfZsUSic2omQ", False],
        "Berberidaceae": ["1WwCvMDnWxNF58cgKR-plJmF_fgnxidTC_XSmBb4UFfA", False],
        "Betulaceae": ["12dpTJwd0ymeb2ssCFB9g1IzkiHTdhZZ-wMtX0rgmYI0", False],
        "Bignoniaceae": ["1zzZ7XG4Alxwf5RX6mNPT3K6gTGM5xegF2xhidmsn6Bo", False],
        "Bombacaceae": ["1ICUvGYuTzUEwFGfzVpqX2l6dZ22GRePWMLEIIIuU4nI", False],
        "Boraginaceae": ["1ICLaRsV4LUvwSUQLSwbrJQSgrDiGa8-20aFujs9UogI", False],
        "Brassicaceae": ["1TKt9hILyc7Iapfp9T_jQo0whcPbFffQySTqrN1qspm0", False],
        "Bromelliaceae": ["1_Vu4eUkaknzNT8C4d7zVKJCVE_qdljOPP8gkdHoaZH4", False],
        "Burseraceae": ["1zVgTT8fOYECUhUN0tqmKgIgUv5-_C95CYQBWkAfCgtU", False],
        "Buxaceae": ["1t6dP0uO15Lr7KA8AY5nJmCFFSCEUPUIOY0CsYblKH88", False],
        "Callistricaceae": ["11vu_Od9dwv9yDFPs4TI4NuUhn2iZu86Not1KpbMD0Ck", False],
        "Campanulaceae": ["1_bS45r9lEXeN9GkMT8s0C6byOjoM9VNiausNUUlKqsg", False],
        "Cannabaceae": ["1EUf_M38fr2Fa6J20OqS1jQqtHHgcUnLm7AvgJQW3ghA", False],
        "Cannaceae": ["1_plRcrI3NLxZldyMMYfI6WOzVkj541R4Lu0_dbEtjKc", False],
        "Capparaceae": ["1ViObgOHXYTKCHHf_yRa84UxDK34dRiiZrpZr4CgWEZc", False],
        "Caprifoliaceae": ["1rrH8RnMypK7Rgyg0kcrSOiu0kojkBfycfFNHDn32J7g", False],
        "Caricaceae": ["1jfuUUy74rPzWm4Zl9E7DzFghSF2PzraMw0vMPDrM1js", False],
        "Caryophyllaceae": ["1ZteEsKR5j3DUBfd05XMr0VDpJHusK252muqecmIGRTc", False],
        "Casuarinaceae": ["18zCwE60q-bp7lmRY5istJY4qF28nL6eddYbd0wrAcjg", False],
        "Ceratophyllaceae": ["1mjgpjXj0Ab0gb-BAGlMCT_KbFRnPOUCCpD47vBTPHuU", False],
        "Chenopodiaceae": ["1qkqO5DL8FM4I9dZuJcMF89X4ZXmuU6wi73Y2K3vx3xQ", False],
        "Chloranthaceae": ["1DwjDVtjZlfjcp8_2AkyzVb11cIPn5hCt2FFQVAfcxmI", False],
        "Circaeasteraceae": ["14CjFN4Dg9110KNHnbH0RRCAlEA_1sX20nyjaKrlfzh8", False],
        "Clusiacece": ["1IA7QHJ2osLs-71eKDgLs0pFy8FrBu0O1qQnh3kqUjqU", False],
        "Colchicaceae": ["1Ick6F5Atxpne3WY5NKgAuIHNftD2M87ZHPxTmKfHiWw", False],
        "Combretaceae": ["1omT4FKB7wyZ0h6KF-Tc1RtxPi2qBlmpn7hBFLM88IfI", False],
        "Commelinaceae": ["1zW6bGIvVNPUFCW33AtKZpvAa_JyRJ4p-pvuy0J78bG4", False],
        "Convallariaceae": ["1i0OoKI7Mby59H4HjGjO7xCKGGUDwsi3TmXnYsk_ZFYY", False],
        "Convolvulaceae": ["1K6thfNrWFKgduaVnZfIIS6jWVKEOxiFYQaXkPIJt3-E", False],
        "Cordiaceae": ["1c5g-URmuc6rxxYaadkJ8Z5O08Q2ESE5_HJ6DGbdhx60", False],
        "Coriariaceae": ["1kF8zAixh4WZJj9QDmB9E5guJ4zOAwTiwQyh6Kizryko", False],
        "Cornaceae": ["1wvbABJ0X9lHr4lbpn7gy7Oyv8byVSUUYKvufS8EnIH8", False],
        "Corylaceae": ["1ruRLNe7q73ZQC2S2oC4Riv-H6PFlH_y8Xn1A4_lnfOw", False],
        "Costaceae": ["1MxsDsQjOJXZM8V401SYxZ9C10rkQMhEE5neheCq7CGo", False],
        "Crassulaceae": ["1inRLht4bZKpOoh6vcRp9D0jW8Ay1cm-Ez-arpHDtc3o", False],
        "Cucurbitaceae": ["1q0DyiSzb7-CxA_uiK27Hf1Oy7CcjASRI_jjT0Msib8c", False],
        "Cyperaceae": ["1Bdx01EW23p27t9PcMq2ANzXQvwkckDV58ZMY8K5XOio", False],
        "Daphniphyllaceae": ["1OuvG7KQoqSgZ8OQJRqMIkbClUR5h6XuXuAYcZLPTeR4", False],
        "Datiscaceae": ["1bMuTJ-13e3ImBt-0-rITpowW2qxHROs31yJtOtEL9TQ", False],
        "Dilleniaceae": ["1HGa2AP6kHdY9TAgYGoFbs5iU9XQHnp0uMU4LTMPMgVk", False],
        "Dioscoreaceae": ["1rHedzPz0HypQa3fTDQyvTW5IZSuMDVHJ_PHbqwuD6FY", False],
        "Dipsacaceae": ["1KNDoeE3Qb3XI5uzRQmkSVy-sa0TY01SUOOkvP4Guwv4", False],
        "Dipterocarpaceae": ["1aQVBWtT41QAAQYdVt-Dva-PUWE2WBegWVjojq2asK-M", False],
        "Droseraceae": ["1EtQ8Zo0a7xo6uccacBBrFKDn84YNx4bPFJHlyrjoqQ0", False],
        "Ebenaceae": ["1iJdlRBqJfh1wSAlbcRpDv0gutmrEgFKdJHS9GfRyLCc", False],
        "Elaeagnaceae": ["1yMhIW05mRD3oyVhikXyb9mTL4oIxv6GVUYeuzWIkVWU", False],
        "Elaeocarpaceae": ["1OzF_0FuQyixtRYgnlO9Jy98yvoog8IV4WTosp6h2GeM", False],
        "Elatinaceae": ["1NKK5Oo75h7yb64DeX6296vzXseOgG_I1k6KUgEI3NYk", False],
        "Ericaceae": ["1Dsymu_gF0UYvVe-WEZburXi1LM7_JGFnWjavi-MuqXU", False],
        "Eriocaulaceae": ["1CY6LiDQ3CDl0tFDEiEXwFBdJjnA8se3IDOwtPFHvSaI", False],
        "Euphorbiaceae": ["1PpIfiJimzCl3r_ZRM0ESy60hPTQjwoLXk57vyXjCwB4", False],
        "Fabaceae": ["11La7RwBy_D-10_sDPD5SSyJFKvSnRiJpDmt1r_XeYZQ", False],
        "Fagaceae": ["11XO-FhNLzfrJ64Xgen0rQME_J_bz_BEM-kjt3dHPJqE", False],
        "Flacourtiaceae": ["1YOT_kQUNtTxGuGt4T2vogtS0zo8VkJakwco-2bqmquM", False],
        "Fumariaceae": ["1sreIkDQdI5qje3xosxS4l9Kn9zyBcdEdjHx5T5HX8uQ", False],
        "Gentianaceae": ["1WXEBMGmEdkKR99BHUmnND-1vXThBg8vPKqUVmRrjqNU", False],
        "Geraniaceae": ["1Bz8U9N8j-6IA4eZhirPuaK07UDwsVFx50tR48VOCADQ", False],
        "Gesneriaceae": ["1Z2On-7lOPadRVv1DhvputENQ9ttgFZTJfuP8r8OY05c", False],
        "Grossulariaceae": ["1bjPgmSyxlUJe0H46TlpH3ErVAbVfuLv_249T5UGfPe0", False],
        "Haloragaceae": ["1vESINRAcTLxM8OQx14Ti0_27i9wG4_CcmWXUDIbjiVs", False],
        "Hamamelidaceae": ["1kGAFlJL-5coLXgqhX6jhDSMQh2RxW1PhNmqe5kjrLZI", False],
        "Hemerocallidaceae": ["121iYs0iMlXVjFZvJcPGX0lmSh5Zu1x6hg7TXP14OAhM", False],
        "Hippocastanaceae": ["1ogALHCYp0Nc-kf5_PLIbUzg4KLBKTzjSKPhSEcJUUyY", False],
        "Hippuridaceae": ["1ITu4EnwbilKhgDSlPiWuMEXL33PA8sg-wDc5rP5mF1w", False],
        "Hyacinthaceae": ["1Jizk0h9Dfx0qYy9qPUbPib6sVt3jF1zvjFtd8dehFSk", False],
        "Hydrangeaceae": ["17qCC8sjbqew1FM9wI4EgXi8yHRAeEOeBVee5BcT5uSI", False],
        "Hydrocharitaceae": ["1ZsjVipwX6DWphJVRPMaFXGyRMPqSCHSBOHujPOBb6EU", False],
        "Hydrophyllaceae": ["1fqqoi2d3HifwWlHi1zoBInS_dJKAhwgi2804UHnckvE", False],
        "Hypoxidaceae": ["10rw45TEDPvM_56qNf2qqdWKGAhAKdsEwcryzREKKpQM", False],
        "Illiciaceae": ["1vFfEpVwubYBWpiEf_l-yTtfGAPKnK0D6i9V3lNWWXIo", False],
        "Iridaceae": ["1OmMboJvHSGEDrVB3FeNqhF81vPjQ6FFKMlJ9T52UX5c", False],
        "Juglandaceae": ["1apv4FYDKml-trgxt66a08WFl89YbpmMFWh-bC6Oyu94", False],
        "Juncaceae": ["1nUbL4n26pucD-NeEy-iuL6BZ_F_RQdO1qp0svQT0618", False],
        "Juncaginaceae": ["1NM3dmImvPx87ugzSthqJ5s4uhUtaP8ya_95EbJn7B0E", False],
        "Lamiaceae": ["1ERHYCelqy4-ne5HUvVwV8G-D2R-cgbV1-Uy8QSlm5fM", False],
        "Lardizabalaceae": ["1HZpOhKUM3klaQFPwh5rNSd4LmaeCB0TvFjwXhp2FeJw", False],
        "Lauraceae": ["1VsMTlVAueUgHgIN2WtUbf7wceLs-F9kNe7M6IGvMiEM", False],
        "Lecythidaceae": ["1XuTvO2AVrcjoiHOvSD9tUdlpYPelezOlwiIfmt8h1xY", False],
        "Leeaceae": ["1u2RORGOBLpSxFPcUP5-UA0E7vM28mvCDzrms0oPFsus", False],
        "Lentibulariaceae": ["1ljteqUg9cHX5KQi4jv9Yr8hxN8ok8MTFSk_T__k2YDw", False],
        "Liliaceae": ["1OfUprilynnynmRt1OHGRVcUZu6KQ5YAUg0Wer1nrPLQ", False],
        "Linaceae": ["1X9glN6PmT6xC_oTnxAEC3dwXDPvxWQjTHpRKw1_UjUw", False],
        "Loganiaceae": ["1UerAFm81-6ZNrCA8n0OZ4kf7bsihKg5I7vXU413cw-Y", False],
        "Loranthaceae": ["1AZI-d_cnUQuTrCAK_Fpe3ZBonuuGWrhG_fle986P_7w", False],
        "Lythraceae": ["1vnalcMvMzPTxK-3ZHgFhUQcoQ_gaLsMPvrFHpy5vPmU", False],
        "Magnoliaceae": ["1hJy1z-NERy-hhNiYGpv3MTkNg823tPT7He6qXqze_Ug", True],
        "Malpighiaceae": ["1t7yk3b_l1qgK0WXBzKscTzzHK0AdooH4h2u3t9-A-t8", True],
        "Malvaceae": ["1mcsOGRWQrhGYT8lCb7XCcmAboZNJwVjIJV32ZyawE_s", True],
        "Martyniaceae": ["1_eITzIJeJYpQtfotfUk8vplyvuNtWnz3i4unXjU2ygc", True],
        "Melanthiaceae": ["1gC5jRh2hjnxeUsNXzCDM4-uI5-2bJxjMnhaoX2peXlM", True],
        "Melastomaceae": ["1dIz0cRbBPhsVrk67AXjQpUzImpoa8PJsem2-PUohXXM", True],
        "Meliaceae": ["1fsl4QKf7Uk1kqti6J6HIMnlQH2nk5g-PAp2vC8zT7AM", True],
        "Menispermaceae": ["1DdEZ4TVivXiQR0nPo-PeNnKxnc7aI-Z2dfHrhllmEzk", True],
        "Monotropaceae": ["1T28VGvlKTuQiHOIKQ6-J3tZSHzDRc6a5Fxbr2xaZUSs", True],
        "Moraceae": ["1R_fjHIXjydqBaPZBFNMbJ6spxy9UzDXI2Lo0hjeor6k", True],
        "Moringaceae": ["1Mbfi5RQJcOfAX2SLSGYSSSu2ztOfB6hU3rkU0uhh078", True],
        "Musaceae": ["1woYG52xedKw9A1ccBfoDXoNnx3qlxNnaq-ZQTdtzSfk", True],
        "Myricaceae": ["1Qj_g0ByuZeJvyAup4EUKvKZ9NXVkp80VdgGOtdVd-0Q", True],
        "Myrsinaceae": ["1IdqUQ0HWy0zG5_Yw0nHUUuh3GVR34KWA3-Ld_l5T-N8", True],
        "Myrtaceae": ["1AWSQzNLfVpOJxEu--E_T55npvu7KuKkNRh-dxeK3kF0", True],
        "Najadaceae": ["14EmBfbi15JwkJOlifHfc_hMmRb6IBnUo7dzmewItzJU", True],
        "Nyctaginaceae": ["1-ZjpMSUYJuc_Z2mT9eeVLs47GHIVYn5mLyJGv6uLWEw", True],
        "Nymphaeaceae": ["1xvLM34YgiU2jw-zxdbfEm9r3egZ-fPk9Of2rAxUip1k", True],
        "Oleaceae": ["1w7X3xA16-XQL44_gBC_1ypYegCefDMlHmHz7WsYYKVc", True],
        "Onagraceae": ["1SsTfFslaB3NypSIlTLx_xeAdIYa_Ru0fXAZ98jO9RIE", True],
        "Orchidaceae": ["1VB6t0N0tTDuv-FJZnbb-7AOycLWt8smYw00EWmOreIc", True],
        "Orobancaceae": ["1cmjTo8CVTfHR4XOrYqXTRZZipNz47OVWYWEKAGnBZAw", True],
        "Oxalidaceae": ["1wP95w2sYahsU_LVnaXTDR0rGSM3PWgMsU5-5W-XKSZI", True],
        "Paeoniaceae": ["1EbafHGtwlj9rKGKJFJ00Xr31O7V4M21iH2otUcz3lyg", True],
        "Pandanaceae": ["16tPUqaUlhEigc2We1w24w47mtlES1kX79VGRp-5XhUA", True],
        "Papaveraceae": ["1ibRIKXKuq3fIDuIB_noHLVWn6IGFKXF5MJ5-C0x2N1E", True],
        "Parnassiaceae": ["1vDRGpCKGqmhEOruVzYLb079_et57hDZiHYBydPq81-I", True],
        "Passifloraceae": ["1wEymc-tslLpu-4tu_2TrVI6xGifmBWbwqXqSRhAC9_I", True],
        "Pedaliaceae": ["1aaRfwbaucX8S3Ae8lv_XJGLPT9ibNXapVeu63eHvklA", True],
        "Phormiaceae": ["15HEus4RHbx115pXmBVsa4O7JNSvJLbk2jJLmiX1j9Dc", True],
        "Phrymaceae": ["1_zhdNyI3AdFiCgDCY61woGieen-VFnPPK3d7fMujv58", True],
        "Phyllanthaceae": ["1GMrB0pwAQMqTfQfTZ99jwJtr2xhgX0FkQQpO3Zd6mvo", True],
        "Phytolaccaceae": ["1iL6-wejSoo8fF8mnUnAtKkk3BCfH_BqIcOSRaVnZ2yY", True],
        "Plantaginaceae": ["1r5RBu4_iI-zN7d-_5R_xgr_h9mkQEXp-euclA7GG4bg", True],
        "Plumbaginaceae": ["1D1x9R-EHNRW8NdxH8NW2uFZjRkzdD5nxldCxL6IW6pk", True],
        "Poaceae": ["1zDtjVM4U5I5BfRTED5GTel2kIuKypv9PpKi8o2k0Ow4", True],
        "Polemoniaceae": ["1AOVQsnHUPRP8mpYZVRgrYKONmqpVUMHfXhDEKtXfyDE", True],
        "Polygalaceae": ["1mEGbDNfCqFD_LFvp80eLdfgr9bKOPX-dhtvCXtOENG4", True],
        "Polygonaceae": ["1tx49tI7k7m_iAn3PQR3krRmLZzJOaAs2JaHuweJfxBc", True],
        "Pontederiaceae": ["1x75tnamg5uzr5JQLyLnwOEYjX2H2iXuZkQYjh7CLcrU", True],
        "Portulacaceae": ["1AM3ReBe83slvM7A310ITueBzhgoQOLMtG_JtcLyj45Y", True],
        "Potamogetonaceae": ["1ReOIMlqQizBD3bMeEJro0KDCPpcRhQZQdGg2L_1i5Ww", True],
        "Primulaceae": ["1JBUT0Dv4uZUDHhUQ-a506YsoNECo4F_CONMncL3q5GI", True],
        "Proteaceae": ["1FNMDk2fSzHvei4EmJj2wqdc2mLyUZmEG9d22as0A3mI", True],
        "Punicaceae": ["1OPv1OJVtxB92QJqIkQrTfoWGuo-hEgq7a0_6wkfBLx4", True],
        "Ranunculaceae": ["1LwCKgWaOAyH3nz1o65_JmkvyuA6-bZbtl3TZKBHnbRg", False],
        "Rhamnaceae": ["1MX_XJkQdcYdl6yjSOWWnrGXWkbMmEYrtlNnYmfKockw", False],
        "Rhizophoraceae": ["1DxI4oqm4HxW0AkOdGh8j8_qYrN_CY865i_tfHe8g5ws", False],
        "Rosaceae": ["1b1oiHVok83hrr3lRdm5ZIPkl-a3V8l32NbU_ZrW1Lrk", False],
        "Rubiaceae": ["1T1lpbLcaRJIxUdOPGQ7hINGqSvbm8UIbFtjSXLgODb4", False],
        "Rutaceae": ["1qTOQDH2Cl2995_3H5HSieB8nUzyiCtS6A_IZ_NyZTXg", False],
        "Sabiaceae": ["1CE-S0fT4s7mIZt0RJpQBn7mHKEI4qQphlDu_gq8DfPY", False],
        "Salicaceae": ["1WtMJA1Smj2FhAJjjHEj0aytbX1vsRLr4UeDsxFFYvjk", False],
        "Sambucaceae": ["1aEusWA71MAsDvNnAKM-FmE75XGdvMFePC1hRsggzX7E", False],
        "Santalaceae": ["1jNTE2Z_NB1mwo00YSKh39ccR84uUfAztt_W7fovfB2Q", False],
        "Sapindaceae": ["14bsCNMYYcr_RVzT2KcIJJPh7B4vBCnE959jY0Zhw_hQ", False],
        "Sapotaceae": ["1R98eeZ1k2x2L-_rPYmvUhjcm1GlyvdcohjpM5UmHlmU", False],
        "Saururaceae": ["1wuSBgu9MqJdvMvqiIPKetK21tl5dnVOc-mmFUYfO-hA", False],
        "Saxifragaceae": ["1VJt7UHa5CM7WBECrfvP7Ug2fyI60hJH-EhlNBC-CPr8", False],
        "Schisandraceae": ["1nFr6x-u2w5dAnnZo8lBUzIRqpP6hxGBP7n1wBFtrxS8", False],
        "Scrophulariaceae": ["16Wre7oF75QDzPWk6KqinTOZZqR4DV9iAnAUF9QlXiDw", False],
        "Simaroubaceae": ["1ZuemiyfWxwbzhy5kJcyY_x3hptyhxEoHmRiI8o7qCcg", False],
        "Smilacaceae": ["1eHzSfkLEAN2a8Xxzvd8zHZ86yA93t7xOYV1d_Ie6l38", False],
        "Solanaceae": ["1IRVq5z9tcaHjhrUaLO4RxyL4W1kw6jJqC7t4keVnki0", False],
        "Sonneratiaceae": ["1wnF7oqyz2nPJt0vjD2cW3o5dFoK5G5HVs6BTUw5hR7Q", False],
        "Sphenocleaceae": ["10cYW2tK38A0PRUIbqjRECn_ejGuWMns-0DUkLz3mogk", False],
        "Stachyuraceae": ["1Sch_FW5BcVDa80n8b9tZsjJ1Ky1zE6zQHUQWNHD06q4", False],
        "Staphyleaceae": ["1PoOijyFBBwmx_hn7UvXLcEW3nJdC1PJgNjDVRhrY9Vo", False],
        "Sterculiaceae": ["1ZLu75Mgdsfs8nJnMnj0uMVW_ecK83OZN1dz8VW6hYXQ", False],
        "Symplocaceae": ["1MWS2_f1BKz5yW2256DdYoGHlUYJ61io-4qdOfieEMq0", False],
        "Tamaricaceae": ["1XzFevAaxT2jvSxxIDmrBSt9NO-kzWTRjJCBfKRyvPZ4", False],
        "Tetramelaceae": ["1BLe2XejujQsZSa8JJ6vlBisp9AKTOZZc4tLiGuLGyLc", False],
        "Theaceae": ["1sLYsIvwFcPWAk5zVnk4viRLZoa-Qv7_gNd3c6DHpvi8", False],
        "Thymalaeaceae": ["1UkDRZt0Q1xwdu7LGWKVOUh1uD-594RPsp-BR2OKwUzo", False],
        "Tiliaceae": ["1FBQDS_0LjE9ou9q5XiCoPC0Hod4Z1byGgM5i16dCJJQ", False],
        "Toricelliaceae": ["1_zR4D8eUefd_eo0AfCWoTi9XdtTXimR_rdg_ViXR0zE", False],
        "Trapaceae": ["1MwM9sOsbzMs0IE2vTItEocY-D5_fw4YEbMqoSE0fMgQ", False],
        "Trilliaceae": ["1_s1cYoyoyAxlbBgL4PaPNu9NSnQ7Gwxr866xEoqfCxc", False],
        "Tropeolaceae": ["1A1QG6D3P9kGxjPec6A5Sf-nO77avwAKGYlpmikX4oNQ", False],
        "Typhaceae": ["1PH6VHK39b6llcHEKxKLu7c34eHTOvPwejqjzC3I8QNE", False],
        "Ulmaceae": ["1CVIMRZDRSdHxzECL78jIHyWZzQ3KQ2qqAj_bL9YpDjs", False],
        "Urticaceae": ["16fHAU-v6J9f2boMDoEXaydNM1JkIr61LfXQC3BkVNjQ", False],
        "Valerianaceae": ["14fuPJiT7I5NuteLHHIUGsYVv4PZnoTg2dnTrDNfA3Wo", False],
        "Verbenaceae": ["1iMwW2H5y1yEPp6TfjiyxcUwbZP6MInqPbeYym8hg1aI", False],
        "Violaceae": ["1ImPm9KK0yCDofc-k8dPkWn2Sk02YrmBDj5S9ZshRZEw", False],
        "Vitaceae": ["1rmsV6Z63_z_o40ZlDMY2XUykGe_Jbr9OX73bkS5GwUg", False],
        "Zingiberaceae": ["1fioMKPZvf5yTzCltrJgI4M1nRHQ1MzktFuyeR-nltcI", False],
        "Zygophyllaceae": ["1in1Si3aOLMbXlR1PMTV2Dx_6dEiNN54GG2uR5itkMws", False],
    }

    RANGE_ALL = "Sheet1!A1:R"
    RANGE_NAME = "Sheet1!A2:L"

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

    NEPAL_SEARCH_WORDS = ["Godawari", "Patan", "Kuleswor"]

    def normalize_row(self, row):
        TOTAL_COLS = 12
        for _ in range(len(row), TOTAL_COLS):
            row.append("")
        row[0] = row[0].strip(" ")
        return row

    def output_latex_string(self, str):
        strout = str
        strout = strout.replace("&", "\\&")
        strout = strout.replace("%", "\\%")
        strout = strout.replace(",", ", ")
        self.latex_file.write(strout)

    def is_heading_row(self, row):
        return row[self.SPECIES_INDEX] != ""

    def output_latex_string_noreplace(self, str):
        self.latex_file.write(str)

    def output_citations(self, cite_string):
        cite_string = "".join(cite_string.split())
        out_str = "\\citet{" + cite_string + "}\n\n"
        self.output_latex_string_noreplace(out_str)

    def output_citations_p(self, cite_string):
        cite_string = "".join(cite_string.split())
        out_str = "\\citep{" + cite_string + "}\n"
        self.output_latex_string_noreplace(out_str)

    def format_scientific_name_list(self, in_str):
        in_str = in_str.replace("\n", " ")
        in_str = in_str.strip(" ,")
        str_lst = in_str.split(",")
        for i in range(0, len(str_lst)):
            str_lst[i] = self.format_scientific_name(str_lst[i])
        return ",".join(str_lst)

    def __emphasis_first_word(self, in_str):
        if in_str == "":
            raise Exception("Expecting non-empty string")

        m = re.match(r"\s*(\w+)(.*)", in_str, re.I)
        if m:
            # print(in_str)
            # print(m.groups())
            return "{\\em " + m.group(1) + "}" + self.__format_sc_post_str(m.group(2))
        else:
            return in_str

    def __format_var_sep(self, sep_str, split_str):
        out_str = split_str[0]
        for i in range(1, len(split_str)):
            out_str += sep_str + " " + self.__emphasis_first_word(split_str[i])
        return out_str

    def __format_sc_post_str(self, in_str):
        if in_str == "":
            return in_str
        # see if we can match subsp.
        split_str = in_str.split("subsp.")
        if len(split_str) > 1:
            return self.__format_var_sep("subsp.", split_str)
        # see if we can match ssp.
        split_str = in_str.split("ssp.")
        if len(split_str) > 1:
            return self.__format_var_sep("ssp.", split_str)
        # see if we can match var.
        split_str = in_str.split("var.")
        if len(split_str) > 1:
            return self.__format_var_sep("var.", split_str)

        return in_str

    def get_genus(self, in_str):
        print(f"get_genus({in_str})")
        in_str = in_str.replace("\n", " ")
        in_str = in_str.strip(" ,")
        return in_str.partition(" ")[0]

    def format_scientific_name(self, in_str):
        in_str = in_str.replace("\n", " ")
        in_str = in_str.strip(" ,")
        print(f"format_scientific_name({in_str})")
        m = re.match(r"\s*(\w+\.?\s+[-\w]+)(.*)", in_str, re.I)  # match first two words
        if m:
            out_str = (
                "{\\em " + m.group(1) + "}" + self.__format_sc_post_str(m.group(2))
            )
            return out_str
        else:
            raise Exception(
                f"Scientific name {in_str} does not seem to be in correct format"
            )

    def generate_latex_row_chr_num(self, row):
        # output chromosome numbers and citation as a separate row
        chr_num = row[self.CHR_NUM_INDEX].strip(",. ")
        citations = row[self.CITATION_INDEX].strip(",. ")
        if len(chr_num) > 0:
            self.output_latex_string(
                "\\begin{hangparas}{0.5cm}{1}\\noindent \\textbf{$" + chr_num + "$} "
            )
            self.output_citations_p(citations)
            self.output_latex_string("\\end{hangparas}\n")

    def generate_latex_subheading(self, row, str_heading, content, bib_index, capstyle):
        if capstyle == CapStyle.CAP_WORDS:
            content = string.capwords(content)
        elif capstyle == CapStyle.LOWER:
            content = content.lower()
        self.output_latex_string(
            "\\begin{hangparas}{0.5cm}{1}\n"
            f"\\noindent \\textbf{{\\small {str_heading}}}: "
            + "\\begin{otherlanguage}{hindi} "
            + "{"
            + content
            + "} \\end{otherlanguage}\n"
        )
        bib = row[bib_index].strip(",. ")
        self.output_latex_string("{\\small ")
        self.output_citations_p(bib + "\n\n")
        self.output_latex_string("}\\end{hangparas}\n\n\\vspace{2mm}")

    def generate_latex_row(self, row, family_name):
        # print(f'generate_latex_row({row})')

        if self.is_heading_row(row):
            self.output_latex_string("\\vspace{5mm}")
            self.output_latex_string(
                "\\section{"
                + self.format_scientific_name(row[self.SPECIES_INDEX])
                + "}\n"
            )

            if row[self.NEPAL_DIST_INDEX] != "":
                self.generate_latex_subheading(
                    row,
                    "Distribution in Nepal",
                    self.add_msl(row[self.NEPAL_DIST_INDEX]),
                    self.NEPAL_DIST_BIB_INDEX,
                    CapStyle.AS_IS,
                )

            if row[self.USE_CODE_INDEX] != "":
                row_use_codes = set()
                self.add_str_list_to_set(row_use_codes, row[self.USE_CODE_INDEX])
                row_use_codes = row_use_codes - self.use_acronyms_to_remove
                row_use_codes = self.replace_use_codes(
                    row_use_codes, self.use_acronyms_to_replace
                )
                self.all_use_codes |= row_use_codes
                use_codes_str = self.set_to_string(row_use_codes)
                self.generate_latex_subheading(
                    row, "Uses", use_codes_str, self.USE_CODE_BIB_INDEX, CapStyle.AS_IS
                )

            if row[self.NEPAL_NAMES_INDEX] != "":
                self.generate_latex_subheading(
                    row,
                    "Common Name(s) in use in Nepal",
                    row[self.NEPAL_NAMES_INDEX],
                    self.NEPAL_NAMES_BIB_INDEX,
                    CapStyle.LOWER,
                )

            if row[self.ENGLISH_NAMES_INDEX] != "":
                self.generate_latex_subheading(
                    row,
                    "Common Name(s) in English",
                    row[self.ENGLISH_NAMES_INDEX],
                    self.ENGLISH_NAMES_BIB_INDEX,
                    CapStyle.CAP_WORDS,
                )

            self.output_latex_string("\\vspace{4mm}\n\n")

        # output chromosome numbers and citation as a separate row
        self.generate_latex_row_chr_num(row)

    def add_msl(self, in_str):
        return re.sub(r"([0-9]+)", r"\1 msl", in_str)

    def generate_latex(self, family_name):
        fn_utf = family_name.encode("utf8")
        print(f"\t\t\tgenerate_latex({fn_utf})")
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        store = file.Storage("token.json")
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(
                "client_secret_563563514748-486lji2ouvg2svb016j2gbe65135ks9r.apps.googleusercontent.com.json",
                self.SCOPES,
            )
            creds = tools.run_flow(flow, store)
        service = build("sheets", "v4", http=creds.authorize(Http()))

        # Call the Sheets API
        sheet = service.spreadsheets()
        sheet_id = self.SPREADSHEET_DICT[family_name][0]
        # result = sheet.values().get(spreadsheetId=sheet_id,
        #                             range=self.RANGE_NAME).execute()
        retry = 10
        while retry > 0:
            try:
                result = (
                    sheet.values()
                    .get(spreadsheetId=sheet_id, range=self.RANGE_ALL)
                    .execute()
                )
                break
            except:
                print(f"Retrying ...{family_name}")
                retry -= 1
                time.sleep(10)

        val_all = result.get("values", [])

        # print(val_all[0])
        if val_all[0][0] != "Taxon":
            # remove first row and column from result
            values = [val_all[i][1:] for i in range(1, len(val_all))]
        else:
            # remove first row and 9th column from result
            values = [val_all[i][:9] + val_all[i][10:] for i in range(1, len(val_all))]
        print(values[0])

        self.latex_file = open(
            "output/" + family_name + ".table.tex", "w", encoding="utf-8"
        )
        for i in range(0, len(values)):
            row = values[i]
            if len(row) == 0:  # skip if empty row
                continue
            row = self.normalize_row(row)
            if self.is_heading_row(row):
                self.num_species_in_fam += 1
                row_genus = self.get_genus(row[self.SPECIES_INDEX])
                if row_genus != self.current_genus:
                    self.num_genus_in_fam += 1
                    self.current_genus = row_genus
            self.generate_latex_row(row, family_name)
        self.latex_file.close()

    def move_dist_data(self, row, move_str):
        if not (row[self.NEPAL_DIST_INDEX].isspace()):
            row[self.NEPAL_DIST_INDEX] += ", "
        row[self.NEPAL_DIST_INDEX] += move_str
        row[self.NEPAL_DIST_INDEX] = row[self.NEPAL_DIST_INDEX].strip(",. ")

    def generate_latex_all_families(self):
        all_families_fileA = open("output/familiesA.tex", "w")
        all_families_fileB = open("output/familiesB.tex", "w")
        all_families_fileC = open("output/familiesC.tex", "w")
        all_families_fileD = open("output/familiesD.tex", "w")

        species_count_csv_file = open("output/species_count.csv", "w")
        species_count_csv_file.write("Family,Genus Count,Species Count\n")
        for family in sorted(self.SPREADSHEET_DICT):
            need_processing = self.SPREADSHEET_DICT[family][1]

            self.current_genus = ""
            self.num_genus_in_fam = 0
            self.num_species_in_fam = 0

            if re.search(r"^[a-cA-C]", family):
                # mainA -> Book PartA, Part 1
                all_families_fileA.write("\\include{" + family + "}\n")
            elif re.search(r"^[d-lD-L]", family):
                # mainB  -> Book PartB
                all_families_fileB.write("\\include{" + family + "}\n")
            elif re.search(r"^[m-pM-P]", family):
                # mainC  -> Book PartC
                all_families_fileC.write("\\include{" + family + "}\n")
            else:
                # mainD  -> Book PartD
                all_families_fileD.write("\\include{" + family + "}\n")

            if need_processing:
                self.generate_latex(family)
                family_tex_file = open("output/" + family + ".tex", "w")
                family_tex_file.write(
                    "\\chapter{"
                    + family
                    + "}\n\n"
                    + "\\input{"
                    + family
                    + ".count.tex}\n\n"
                    + "\\input{"
                    + family
                    + ".table.tex}\n\n"
                    + "\\vspace{5mm}"
                    "\\bibliographystyle{plainnat}\n" + "\\bibliography{Bibliography}\n"
                )
                family_tex_file.close()
                family_count_file = open("output/" + family + ".count.tex", "w")

                if self.num_genus_in_fam == 1:
                    genus_article = "is a single"
                    genus_word = "genus"

                else:
                    genus_article = f"are {self.num_genus_in_fam}"
                    genus_word = "genera"

                if self.num_species_in_fam == 1:
                    fam_article = "a single"
                else:
                    fam_article = f"{self.num_species_in_fam}"

                family_count_file.write(
                    "There %s %s and %s species reported with chromosome counts  "
                    "of plants found in Nepal in this family.\\vspace{-5mm}"
                    % (genus_article, genus_word, fam_article)
                )
                family_count_file.close()
                species_count_csv_file.write(
                    f"{family},{self.num_genus_in_fam},{self.num_species_in_fam}\n"
                )
                time.sleep(2)
        all_families_fileA.close()
        all_families_fileB.close()
        all_families_fileC.close()
        all_families_fileD.close()
        species_count_csv_file.close()

        use_codes_file = open("output/all_use_codes.csv", "w", encoding="utf-8")
        use_codes_file.write(self.set_to_string(self.all_use_codes))
        use_codes_file.close()


if __name__ == "__main__":
    lgen = LatexGenerator()
    lgen.generate_latex_all_families()
