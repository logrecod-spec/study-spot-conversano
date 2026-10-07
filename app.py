"""Study-Spot V2 — prototipo didattico per biblioteche dell'area metropolitana di Bari."""

from datetime import date, time
from io import BytesIO
from urllib.parse import quote

import pandas as pd
import qrcode
import streamlit as st


st.set_page_config(
    page_title="Study-Spot | Biblioteche area di Bari",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
:root{--navy:#0b1c34;--navy-2:#142c4a;--green:#15966f;--green-bright:#39d6a2;--ink:#14243a;--muted:#6d7b8e;--line:#e6ecf2;--paper:#fff;--canvas:#f3f6f9}
html{scroll-behavior:smooth;scroll-padding-top:100px}*{box-sizing:border-box}
#MainMenu,footer,header{visibility:hidden;height:0}
.stApp{background:radial-gradient(ellipse at 7% 0%,#e7f5ee 0,transparent 28%),var(--canvas);color:var(--ink);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.block-container{max-width:1240px;padding:0 1.4rem 4rem}
[data-testid="stVerticalBlockBorderWrapper"]{border-color:var(--line)!important;border-radius:22px!important;background:rgba(255,255,255,.92);box-shadow:0 8px 28px rgba(11,28,52,.055);transition:transform .18s ease,box-shadow .18s ease}
[data-testid="stVerticalBlockBorderWrapper"]:hover{box-shadow:0 14px 34px rgba(11,28,52,.09)}
.topbar{position:sticky;top:0;z-index:999;display:flex;align-items:center;justify-content:space-between;gap:1rem;margin:0 -1.4rem 1.7rem;padding:14px clamp(1rem,4vw,3rem);border-bottom:1px solid rgba(222,231,239,.85);background:rgba(255,255,255,.88);backdrop-filter:blur(18px)}
.brand{display:flex;align-items:center;gap:10px;color:var(--navy);text-decoration:none;font-weight:850;letter-spacing:-.04em;font-size:1.16rem}.brand-mark{display:grid;place-items:center;width:36px;height:36px;border-radius:12px;background:var(--navy);color:#fff;font-size:1.05rem;box-shadow:0 5px 12px #0b1c3429}
.navlinks{display:flex;align-items:center;gap:clamp(12px,2.5vw,30px)}.navlinks a{color:#536279;text-decoration:none;font-size:.9rem;font-weight:650;transition:color .15s}.navlinks a:hover{color:var(--green)}
.live-chip{display:flex;align-items:center;gap:8px;border:1px solid #dcefe6;border-radius:999px;background:#f2fbf6;padding:7px 12px;color:#197753;font-size:.76rem;font-weight:750;white-space:nowrap}.live-dot{width:7px;height:7px;border-radius:50%;background:#1db77d;box-shadow:0 0 0 4px #1db77d20}
.hero{position:relative;isolation:isolate;overflow:hidden;display:grid;grid-template-columns:minmax(0,1.4fr) minmax(200px,.6fr);align-items:center;gap:1.5rem;min-height:280px;padding:clamp(26px,5vw,58px);border:1px solid #24415f;border-radius:30px;background:linear-gradient(120deg,#0b1c34 4%,#102a47 64%,#123b4a);box-shadow:0 24px 55px rgba(11,28,52,.17);color:#fff}
.hero:before,.hero:after{position:absolute;z-index:-1;content:"";border-radius:50%;pointer-events:none}.hero:before{width:360px;height:360px;right:5%;top:-210px;border:1px solid #ffffff17;box-shadow:0 0 0 32px #ffffff08,0 0 0 68px #ffffff06}.hero:after{width:240px;height:240px;right:22%;bottom:-190px;background:radial-gradient(circle,#37d6a222,transparent 70%)}
.hero-copy{max-width:650px}.hero .badge{display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border:1px solid #b6f2da32;border-radius:999px;background:#1bd19315;color:#a5f0d0;font-weight:750;font-size:.73rem;letter-spacing:.09em;text-transform:uppercase}.hero h1{margin:17px 0 10px;color:#fff;font-size:clamp(2.25rem,6vw,4.25rem);line-height:1.02;letter-spacing:-.065em}.hero p{max-width:560px;margin:0;color:#c5d2df;font-size:clamp(1rem,2vw,1.13rem);line-height:1.65}.hero b{color:#fff}.hero-art{justify-self:end;display:grid;place-items:center;width:min(100%,230px);aspect-ratio:1;border:1px solid #ffffff20;border-radius:34px;background:linear-gradient(145deg,#ffffff11,#ffffff04);box-shadow:inset 0 1px #ffffff17,0 25px 45px #06172c45;transform:rotate(3deg)}.hero-icon{font-size:5.1rem;filter:drop-shadow(0 10px 18px #07182c80)}.hero-art-label{margin-top:-22px;border:1px solid #ffffff21;border-radius:999px;background:#0b1c34c9;padding:8px 13px;color:#d5e2ee;font-size:.72rem;font-weight:700;letter-spacing:.05em}
.section-title{display:flex;align-items:center;gap:12px;margin:2.2rem 0 1rem;color:var(--navy);font-size:clamp(1.25rem,3vw,1.65rem);font-weight:820;letter-spacing:-.035em}.section-title span{display:grid;place-items:center;width:31px;height:31px;border-radius:10px;background:#e4f5ed;color:#18815f;font-size:.78rem;letter-spacing:0}
.pill{display:inline-flex;align-items:center;border:1px solid #e7edf2;border-radius:999px;padding:5px 10px;background:#f7f9fb;color:#43546a;font-size:.76rem;font-weight:650;margin:4px 4px 0 0}
.stCaption,.stCaption p,[data-testid="stCaptionContainer"]{color:var(--muted)!important;font-size:.86rem}
[data-testid="stMetric"]{min-height:112px;padding:18px 20px;border:1px solid #e6ecf2;border-radius:20px;background:linear-gradient(145deg,#fff,#f9fbfc);box-shadow:0 7px 18px #0b1c3409}
[data-testid="stMetricLabel"]{color:#718197!important;font-weight:650}[data-testid="stMetricValue"]{color:var(--navy)!important;font-size:clamp(1.4rem,3vw,2rem);font-weight:820;letter-spacing:-.04em}
[data-testid="stProgressBar"]>div{height:9px;border-radius:999px;background:#eaf0f3}[data-testid="stProgressBar"]>div>div{border-radius:999px;background:linear-gradient(90deg,#24b982,#61d99a)}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div,div[data-baseweb="textarea"]>div{border-color:#dfe7ed!important;border-radius:13px!important;background:#fff!important;box-shadow:0 2px 5px #0b1c3406}div[data-baseweb="select"]>div:focus-within,div[data-baseweb="input"]>div:focus-within{border-color:#34aa7b!important;box-shadow:0 0 0 3px #34aa7b20!important}
input,textarea{color:var(--ink)!important}label{color:#34465d!important;font-weight:650!important}
.stButton>button,.stLinkButton>a{min-height:42px;border:1px solid #e2e9ef;border-radius:13px;background:#fff;color:#233850;font-weight:700;transition:all .16s ease;box-shadow:0 3px 8px #0b1c3408}.stButton>button:hover,.stLinkButton>a:hover{border-color:#a8dcca;background:#f5fcf8;color:#126d50;transform:translateY(-1px)}.stButton>button[kind="primary"]{border-color:var(--green);background:linear-gradient(135deg,#15966f,#21b17d);color:#fff;box-shadow:0 7px 16px #15966f30}.stButton>button[kind="primary"]:hover{background:linear-gradient(135deg,#117d5d,#15966f);color:#fff}
[data-testid="stForm"]{padding:clamp(16px,3vw,26px);border:1px solid var(--line);border-radius:22px;background:#fff;box-shadow:0 12px 32px #0b1c340b}
[data-testid="stAlert"]{border-radius:16px;border:1px solid #dfeee7}
[data-testid="stImage"] img{border-radius:18px;box-shadow:0 12px 24px #0b1c3417}
[data-testid="stMap"]{overflow:hidden;border:1px solid #dfe7ed;border-radius:22px;box-shadow:0 12px 30px #0b1c3410}
[data-testid="stExpander"]{border:1px solid var(--line);border-radius:18px;background:#fff}
.footer{text-align:center;color:#8491a1;padding:34px 0 8px;font-size:.85rem}
@media(max-width:760px){.block-container{padding:0 .9rem 3rem}.topbar{margin:0 -.9rem 1rem;padding:11px .9rem}.navlinks{gap:12px}.navlinks a{font-size:.78rem}.live-chip{display:none}.hero{grid-template-columns:1fr;min-height:0;padding:27px 22px;border-radius:24px}.hero-art{display:none}.section-title{margin-top:1.7rem}[data-testid="stMetric"]{padding:13px 14px;min-height:94px}[data-testid="stMetricLabel"]{font-size:.72rem}}
@media(max-width:430px){.brand{font-size:1rem}.brand-mark{width:32px;height:32px}.navlinks{gap:9px}.navlinks a{font-size:.72rem}.hero h1{font-size:2.45rem}.hero{padding:23px 19px}}
</style>
""", unsafe_allow_html=True)

# Dataset locale trascritto da fonti pubbliche ufficiali. I posti sono SEMPRE
# valori demo, modificabili qui; le coordinate restano nulle se non verificate.
REGION_URL = "https://dati.puglia.it/ckan/dataset/biblioteche-del-polo-pug-biblioteche-di-puglia"
COLIBRI_URL = "https://dati.puglia.it/v2/dataset/biblioteche-colibri"
COLIBRI_CATALOG_URL = "https://biblioteche.comune.bari.it/SebinaOpac/article/c-biblioteche"
ICCU_URL = "https://www.iccu.sbn.it/it/SBN/poli-e-biblioteche/polo/BA1-Polo-Terra-di-Bari/"
REGIONAL_RECORDS = [
    ("87","BA0542","Biblioteca Marco Polo","Bari","Viale Bartolo, 4/6","biblioteca@marcopolobari.it",16.85786402598167,41.094982913252764),
    ("81","BA0535","Biblioteca Mazzini","Bari","Via Suppa, 7","baic847001@istruzione.it",16.867342955203963,41.11922138178748),
    ("75","BA0533","Biblioteca Lombardi","Bari","Via Lombardia, 2","ibambiniditruffaut@gmail.com",16.789071453357685,41.119807457638046),
    ("76","BA0531","Biblioteca Duse","Bari","Via San Girolamo, 38","Bibliotecadusebari@gmail.com",16.816252324523,41.13672214872098),
    ("96","BA0083","Biblioteca Francescana Provinciale Madonna della Vetrana","Castellana Grotte","Convento Madonna della Vetrana, Largo S. Francesco, 1","info@santuariodellavetrana.it",17.17685309636259,40.875009658879165),
    ("84","BA0526","Biblioteca Cagnazzi","Bari","Via Colella, 13","bibliotecamunicipio2bari@gmail.com",16.868659324521936,41.104455487338754),
    ("MR","IT-BA0441","Mediateca Regionale Pugliese","Bari","Parco Rossani, Via Vitantonio De Bellis, 47","info@mediatecapuglia.it",16.870706,41.115523),
    ("77","BA0530","Biblioteca G. Marconi","Bari","Via Skanderbeg, 35","bibliotecamarconibari@gmail.com",16.844063255204674,41.137357466323884),
    ("78","BA0532","Biblioteca Maurogiovanni","Bari","Via Nicola Colonna, 1","bibliotecamaurogiovanni@gmail.com",16.872197836169008,41.07821394271681),
    ("70",None,"Biblioteca Accademia Pugliese delle Scienze","Bari","Villa La Rocca, Via Celso Ulpiani, 27","segreteria@accademiapugliesescienze.it",16.88077726347481,41.11177503108767),
    ("79","BA0534","Biblioteca Iurlo","Bari","Via Luigi Gurakuqi, 2","bibliotecaiurlo@gmail.com",16.89537363067814,41.10782389233605),
    ("82","BA0033","Biblioteca di quartiere Don Bosco","Bari","Via Martiri d'Otranto, 69","bibliotecadiquartieredonbosco@gmail.com",16.85532434170953,41.11814306668666),
    ("83","BA0012","Biblioteca Museo Civico","Bari","Strada Sagges, 13","info@museocivicobari.it",16.86922668588591,41.12751119038879),
]
COLIBRI_RECORDS = [
    ("Biblioteca Catino","Via dei Narcisi","municipio5@comunebari.it","0805776046"),
    ("Biblioteca dei Ragazzi[e]","Parco 2 Giugno, ingresso Viale della Resistenza s.n.","biblioteca@progettocitta.org","0809262102"),
]
ICCU_RECORDS = [
    ("BA0018","Biblioteca Nazionale Sagarriga Visconti Volpi","Bari","Via Pietro Oreste, 45 - 70123", "080/2173111","bn-ba@cultura.gov.it","Pubblico","nazionale"),
    ("BA0020","Biblioteca della Fondazione Gaetano Ricchetti","Bari","Via Sparano, 145 - 70121","080/5212145","info@bibliotecaricchetti.it","Da verificare","fondazione"),
    ("BA0136","Biblioteca Santa Teresa dei Maschi De Gemmis","Bari","Strada Lamberti, 4 - 70122","080/5412596","direzione@bibliotecametropolitana.bari.it","Da verificare","metropolitana"),
    ("BA0232","Biblioteca comunale Monsignor Amatulli","Noci","Via Cappuccini, 4 - 70015","080/4977304","biblionoci@libero.it","Da verificare","comunale"),
    ("BA0112","Biblioteca comunale De Miccolis Angelini","Putignano","Via Castello, 26 - 70017","080/4911626","biblioteca@comune.putignano.ba.it","Da verificare","comunale"),
    ("BA0078","Biblioteca comunale Eustachio Rogadeo","Bitonto","Via G. D. Rogadeo, 52 - 70032","080/3751877",None,"Da verificare","comunale"),
    ("BA0111","Biblioteca comunale Raffaele Chiantera","Polignano a Mare","Via Mulini, 9 - 70044","080/4248342","biblioteca@comune.polignanoamare.ba.it","Da verificare","comunale"),
    ("BA0113","Biblioteca comunale di Rutigliano","Rutigliano","Via Leopoldo Tarantini, 28 - 70018","080/4769062","biblioteca@comune.rutigliano.ba.it","Da verificare","comunale"),
    ("BA0359","Biblioteca della Fondazione Giuseppe Di Vagno","Conversano","Via San Benedetto, 118 - 70014","080/4959372","info@fondazione.divagno.it","Da verificare","fondazione"),
    ("BA0091","Biblioteca comunale Don Vincenzo Angelilli","Gioia del Colle","Piazza Umberto I, 19 - 70023","080/8419468","biblioteca@comune.gioiadelcolle.ba.it","Da verificare","comunale"),
    ("BA0098","Biblioteca comunale G. De Santis","Mola di Bari","Piazza XX Settembre, 58 - 70042","080/4741449","bibliotecacomunale@comune.moladibari.ba.it","Da verificare","comunale"),
    ("BA0004","Archivio Biblioteca Museo Civico (A.B.M.C.) di Altamura","Altamura","Piazza Zanardelli, 30 - 70022","080/3111708","abmc_a@libero.it","Da verificare","civica"),
    ("BA0104","Biblioteca civica Prospero Rendella","Monopoli","Piazza Garibaldi, 24 - 70043","080/4140709","info@larendella.it","Da verificare","civica"),
    ("BA0086","Biblioteca civica Giacomo Tauro","Castellana Grotte","Via Risorgimento, 9 - 70013","080/4900228","biblioteca@comune.castellanagrotte.ba.it","Da verificare","civica"),
    ("BA0234","Biblioteca comunale di Casamassima","Casamassima","Via Chiasso Elia - 70010","080/530174",None,"Da verificare","comunale"),
    ("BA0349","Biblioteca Interdipartimentale Università LUM Giuseppe Degennaro","Casamassima","S.S. 100 km 18 - 70010","080/9021423","biblioteca@lum.it","Universitaria","universitaria"),
    ("BA0340","Biblioteca della Soprintendenza Archeologia, belle arti e paesaggio","Bari","Via Pier l'Eremita, 25/B - 70122","080/5286223","sabap-ba@cultura.gov.it","Specialistica","specialistica"),
    ("BA0363","Biblioteca d'Arte Michele d'Elia della Pinacoteca Metropolitana","Bari","Lungomare Nazario Sauro, 27 / Via Spalato, 19 - 70121","080/5412208","bibliotecapinacoteca@cittametropolitana.ba.it","Specialistica","specialistica"),
    ("BA0090","Biblioteca comunale Matteo Renato Imbriani","Corato","Largo Plebiscito, 21 - 70033","080/9592309","biblioteca@comune.corato.ba.it","Da verificare","comunale"),
    ("BA0088","Biblioteca civica Maria Marangelli","Conversano","Via San Giuseppe, 12 - 70014","080/4953428","bibliotecacomunale@comune.conversano.ba.it","Da verificare","civica"),
    ("BA0230","Biblioteca comunale G. D'Addosio","Capurso","Piazza Matteotti, 1 - 70010","331/2307304","bibliotecacapurso@gmail.com","Da verificare","comunale"),
    ("BA0141","Biblioteca comunale di Modugno","Modugno","Corso Umberto I, Palazzo della Cultura - 70026","080/5865802","biblioteca@comune.modugno.ba.it","Da verificare","comunale"),
    ("BA0081","Biblioteca comunale di Bitritto","Bitritto","Via Bonghi, 2 - 70020","080/385814","bibliotecabitritto@hotmail.it","Da verificare","comunale"),
    ("BA0128","Biblioteca comunale di Triggiano","Triggiano","Via A. Nitti - 70019","080/4628296","cultura@comune.triggiano.bari.it","Da verificare","comunale"),
    ("BA0117","Biblioteca comunale di Sammichele di Bari","Sammichele di Bari","Piazza Leonardo Netti, Palazzo Pinto - 70010","080/8917297","biblioteca@comune.sammicheledibari.ba.it","Da verificare","comunale"),
    ("BA0364","Biblioteca comunale Vito Bavaro","Sannicandro di Bari","Piazza Castello, 1 - 70028","080/9936312","info@bibliotecavitobavaro.it","Da verificare","comunale"),
    ("BA0118","Biblioteca comunale Giovanni Colonna","Santeramo in Colle","Piazza Giuseppe Di Vagno - 70029","080/3036907",None,"Da verificare","comunale"),
    ("BA0082","Biblioteca comunale Armando Perotti","Cassano delle Murge","Via Miani, 15 - 70020","080/3211606","biblioteca@comune.cassanodellemurge.ba.it","Da verificare","comunale"),
    ("BA0001","Biblioteca comunale Giuseppe Maselli Campagna","Acquaviva delle Fonti","Via Palmiro Togliatti, 2 - 70021","080/761134","biblioteca@comune.acquaviva.ba.it","Da verificare","comunale"),
]
LIBRARY_DATA = []
public_colibri = {"Biblioteca Mazzini", "Biblioteca Lombardi", "Biblioteca Duse", "Biblioteca Cagnazzi", "Biblioteca G. Marconi", "Biblioteca Maurogiovanni", "Biblioteca Iurlo", "Biblioteca di quartiere Don Bosco", "Biblioteca Museo Civico"}
phone_by_email = {"Bibliotecadusebari@gmail.com":"3397953237","bibliotecamarconibari@gmail.com":"080 5344868","bibliotecamaurogiovanni@gmail.com":"3773248236","bibliotecaiurlo@gmail.com":"3534491921","ibambiniditruffaut@gmail.com":"3284071538","bibliotecamunicipio2bari@gmail.com":"0805775464","baic847001@istruzione.it":"0805211367","municipio5@comunebari.it":"0805776046","info@museocivicobari.it":"0805772362","bibliotecadiquartieredonbosco@gmail.com":"0805750006"}
for index, (polo_code, isil, name, city, address, email, lon, lat) in enumerate(REGIONAL_RECORDS, start=1):
    is_colibri = name in public_colibri
    LIBRARY_DATA.append({"id":f"pug-{polo_code.lower()}","name":name,"city":city,"address":address,"phone":phone_by_email.get(email),"email":email,"source":"Regione Puglia – Biblioteche del Polo PUG" + ("; Comune di Bari – rete COLIBRÌ" if is_colibri else ""),"source_url":REGION_URL,"sbn_code":None,"polo_code":polo_code,"isil_code":isil,"access":"Pubblico" if is_colibri else "Da verificare","type":"biblioteca di quartiere" if is_colibri else ("specialistica" if "Accademia" in name else ("mediateca" if "Mediateca" in name else "Da verificare")),"study":"Da verificare","lat":lat,"lon":lon,"total_seats":25,"available_seats":10})
for index, (name, address, email, phone) in enumerate(COLIBRI_RECORDS, start=1):
    LIBRARY_DATA.append({"id":f"colibri-extra-{index}","name":name,"city":"Bari","address":address,"phone":phone,"email":email,"source":"Regione Puglia – Biblioteche Colibrì","source_url":COLIBRI_URL,"sbn_code":None,"polo_code":None,"isil_code":None,"access":"Pubblico","type":"biblioteca di quartiere","study":"Da verificare","lat":None,"lon":None,"total_seats":25,"available_seats":10})
for code, name, city, address, phone, email, access, kind in ICCU_RECORDS:
    LIBRARY_DATA.append({"id":code.lower(),"name":name,"city":city,"address":address,"phone":phone,"email":email,"source":"ICCU – SBN Polo Terra di Bari (BA1)","source_url":ICCU_URL,"sbn_code":None,"polo_code":None,"isil_code":None,"catalogue_code":code,"access":access,"type":kind,"study":"Da verificare","lat":None,"lon":None,"total_seats":25,"available_seats":10})
libraries = pd.DataFrame(LIBRARY_DATA).drop_duplicates(subset="id").reset_index(drop=True)

demo_seats = {item["id"]: item["available_seats"] for item in LIBRARY_DATA}
if "seats" not in st.session_state:
    st.session_state.seats = demo_seats.copy()
else:
    # During a hot reload keep current session values where ids still match,
    # and initialize newly added records without producing NaN seat counts.
    st.session_state.seats = {library_id: st.session_state.seats.get(library_id, default) for library_id, default in demo_seats.items()}
if "selected_library" not in st.session_state:
    st.session_state.selected_library = None
if "booking" not in st.session_state:
    st.session_state.booking = None
if "notifications" not in st.session_state:
    st.session_state.notifications = False
if "checked_in" not in st.session_state:
    st.session_state.checked_in = False
if st.session_state.selected_library and st.session_state.selected_library not in libraries["id"].values:
    st.session_state.selected_library = None
if st.session_state.get("booking") and st.session_state.booking.get("id") not in libraries["id"].values:
    st.session_state.booking = None

libraries["available_seats"] = libraries["id"].map(st.session_state.seats)
libraries["occupied"] = libraries["total_seats"] - libraries["available_seats"]
libraries["occupancy_pct"] = (libraries["occupied"] / libraries["total_seats"] * 100).round().astype(int)
libraries["availability_pct"] = (libraries["available_seats"] / libraries["total_seats"] * 100).round().astype(int)
libraries["status"] = libraries["availability_pct"].apply(lambda value: "Alta" if value >= 60 else ("Media" if value >= 30 else "Bassa"))

st.markdown("""
<nav class="topbar">
  <a class="brand" href="#top"><span class="brand-mark">S</span>Study-Spot</a>
  <div class="navlinks"><a href="#explore">Esplora</a><a href="#map">Mappa</a><a href="#checkin">QR check-in</a></div>
  <div class="live-chip"><span class="live-dot"></span>Prototipo · dati demo</div>
</nav>
<div id="top"></div>
<div class="hero">
  <div class="hero-copy">
    <span class="badge"><span class="live-dot"></span> Study-Spot · MVP V2</span>
    <h1>Il tuo prossimo<br>posto di studio.</h1>
    <p><b>Trova una biblioteca, scegli il posto e mettiti al lavoro.</b><br>Esplora le sedi dell’area di Bari con disponibilità demo e prova prenotazione e QR Check-in.</p>
  </div>
  <div class="hero-art"><span class="hero-icon">📚</span><span class="hero-art-label">STUDIA · ESPLORA · RIPETI</span></div>
</div>
""", unsafe_allow_html=True)
st.caption("Dati territoriali da fonti ufficiali quando disponibili · disponibilità, prenotazioni e check-in sono simulazioni demo.")

st.markdown('<div id="explore"></div><div class="section-title"><span>01</span>Trova il tuo spazio</div>', unsafe_allow_html=True)
f1, f2 = st.columns([1, 1.5])
with f1:
    city_options = ["Tutta l'area"] + sorted(libraries["city"].dropna().unique().tolist())
    selected_city = st.selectbox("Città", city_options)
with f2:
    search = st.text_input("Cerca biblioteca", placeholder="Nome o città")
only_available = st.checkbox("Mostra solo biblioteche con posti disponibili")

view = libraries.copy()
if selected_city != "Tutta l'area":
    city_match = view["city"].eq(selected_city)
    if selected_city == "Bari":
        city_match |= view["city"].eq("Bari-Carbonara")
    view = view[city_match]
if search:
    terms = view["name"].str.contains(search, case=False, na=False) | view["city"].str.contains(search, case=False, na=False)
    view = view[terms]
if only_available:
    view = view[view["available_seats"] > 0]

metric_cols = st.columns(3)
metric_cols[0].metric("Biblioteche nel filtro", len(view))
metric_cols[1].metric("Posti disponibili · demo", int(view["available_seats"].sum()))
metric_cols[2].metric("Occupazione · demo", f"{int(view['occupied'].sum())}/{int(view['total_seats'].sum())}" if len(view) else "—")

st.markdown('<div class="section-title"><span>02</span>Biblioteche vicino a te</div>', unsafe_allow_html=True)
st.caption("Disponibilità demo: valori iniziali stabili, aggiornati solo nella sessione corrente.")

if view.empty:
    st.info("Nessuna biblioteca verificata nel dataset per questa città o ricerca. Il catalogo ufficiale viene ampliato progressivamente.")
else:
    for _, row in view.iterrows():
        with st.container(border=True):
            st.markdown(f"### {row['name']}")
            st.write(f"📍 {row['city']} · {row['address']}")
            st.markdown(f"<span class='pill'>Disponibilità demo</span><span class='pill'>{int(row['available_seats'])} / {int(row['total_seats'])} posti</span><span class='pill'>Occupazione {int(row['occupancy_pct'])}%</span><span class='pill'>Disponibilità {row['status']}</span><span class='pill'>{row['access']}</span>", unsafe_allow_html=True)
            st.progress(float(row["availability_pct"]) / 100, text=f"{row['status']} disponibilità · {int(row['available_seats'])}/{int(row['total_seats'])} posti demo")
            maps_url = "https://www.google.com/maps/search/?api=1&query=" + quote(f"{row['name']}, {row['address']}, {row['city']}")
            left, right = st.columns([1, 2])
            with left:
                if st.button("Apri scheda" if st.session_state.selected_library != row["id"] else "Scheda aperta", key=f"open_{row['id']}", use_container_width=True):
                    st.session_state.selected_library = row["id"]
                    st.rerun()
            with right:
                st.link_button("Posizione su Google Maps", maps_url, use_container_width=True)

st.markdown('<div id="map"></div><div class="section-title"><span>03</span>Mappa delle sedi</div>', unsafe_allow_html=True)
st.caption("I marker usano le coordinate del dataset ufficiale regionale; per le altre sedi trovi il collegamento alla posizione su Maps.")
if view.empty:
    st.info("Nessuna posizione da mostrare con i filtri attuali.")
else:
    for _, row in view.iterrows():
        maps_url = "https://www.google.com/maps/search/?api=1&query=" + quote(f"{row['name']}, {row['address']}, {row['city']}")
        st.markdown(f"- **{row['name']}** — {row['address']}, {row['city']} · [Apri posizione]({maps_url})")
    mapped = view.dropna(subset=["lat", "lon"])
    if not mapped.empty:
        st.map(mapped[["lat", "lon"]], latitude=float(mapped.iloc[0]["lat"]), longitude=float(mapped.iloc[0]["lon"]), zoom=10 if selected_city == "Tutta l'area" else 13, height=380)

# Scheda dettagliata e selezione per prenotazione.
if st.session_state.selected_library:
    selected_rows = libraries[libraries["id"] == st.session_state.selected_library]
    if selected_rows.empty:
        st.session_state.selected_library = None
    else:
        row = selected_rows.iloc[0]
        st.markdown('<div class="section-title"><span>04</span>Dettagli biblioteca</div>', unsafe_allow_html=True)
        st.subheader(row["name"])
        st.write(f"**Città:** {row['city']}  ·  **Indirizzo:** {row['address']}")
        st.write(f"**Accesso:** {row['access']}  ·  **Stato disponibilità:** {row['status']}")
        st.write(f"**Posti disponibili / totali (demo):** {int(row['available_seats'])} / {int(row['total_seats'])}  ·  **Occupazione demo:** {int(row['occupancy_pct'])}%")
        st.write(f"**Tipo:** {row['type']}  ·  **Studio:** {row['study']}")
        st.write(f"**Codice SBN:** {row['sbn_code'] or 'Da verificare'}")
        if row.get("polo_code"):
            st.write(f"**Codice biblioteca Polo PUG:** {row['polo_code']}  ·  **ISIL:** {row['isil_code'] or 'Da verificare'}")
        elif row.get("catalogue_code"):
            st.write(f"**Codice anagrafe ICCU:** {row['catalogue_code']}")
        if row["phone"]:
            st.write(f"**Telefono:** {row['phone']}")
        if row["email"]:
            st.write(f"**Email:** {row['email']}")
        if "Polo PUG" in row["source"]:
            source_text = f"[Regione Puglia – Biblioteche del Polo PUG]({REGION_URL})"
            if "COLIBRÌ" in row["source"]:
                source_text += f" · [Regione Puglia – dataset COLIBRÌ]({COLIBRI_URL}) · [catalogo ufficiale COLIBRÌ]({COLIBRI_CATALOG_URL})"
        elif "COLIBRÌ" in row["source"]:
            source_text = f"[Regione Puglia – Biblioteche Colibrì]({COLIBRI_URL}) · [catalogo ufficiale COLIBRÌ]({COLIBRI_CATALOG_URL})"
        else:
            source_text = f"[ICCU – SBN Polo Terra di Bari (BA1)]({row['source_url']})"
        st.markdown(f"**Fonte dati:** {source_text}")
        st.caption("Posti, occupazione e stato di disponibilità sono dati demo, non comunicati dalla biblioteca.")
        maps_url = "https://www.google.com/maps/search/?api=1&query=" + quote(f"{row['name']}, {row['address']}, {row['city']}")
        st.link_button("Apri mappa / posizione", maps_url)
        if row["available_seats"] > 0 and st.button("Prenota posto", type="primary", key="detail_book"):
            st.session_state.booking_target = row["id"]
            st.rerun()
        elif row["available_seats"] <= 0:
            st.warning("Nessun posto disponibile nella simulazione.")

if st.session_state.get("booking_target"):
    target_rows = libraries[libraries["id"] == st.session_state.booking_target]
    if target_rows.empty:
        st.session_state.booking_target = None
    else:
        target = target_rows.iloc[0]
        st.markdown('<div id="booking"></div><div class="section-title"><span>05</span>Blocca il tuo posto</div>', unsafe_allow_html=True)
        st.info(f"Prenotazione demo — non collegata alla biblioteca reale. **{target['name']}**, {target['city']}.")
        with st.form("booking_form"):
            a, b, c = st.columns(3)
            with a:
                booking_date = st.date_input("Data", value=date.today())
            with b:
                booking_time = st.time_input("Ora", value=time(10, 0))
            with c:
                duration = st.selectbox("Durata", ["1 ora", "2 ore", "3 ore"])
            confirm_col, cancel_col = st.columns(2)
            with confirm_col:
                confirm = st.form_submit_button("Conferma prenotazione demo", use_container_width=True)
            with cancel_col:
                cancel = st.form_submit_button("Annulla", use_container_width=True)
        if cancel:
            st.session_state.booking_target = None
            st.rerun()
        if confirm:
            if st.session_state.seats[target["id"]] > 0:
                st.session_state.seats[target["id"]] -= 1
                st.session_state.booking = {"id": target["id"], "name": target["name"], "city": target["city"], "date": booking_date.strftime("%d/%m/%Y"), "time": booking_time.strftime("%H:%M"), "duration": duration}
                st.session_state.checked_in = False
                st.session_state.booking_target = None
                st.rerun()
            st.error("Posti demo esauriti: aggiorna la selezione.")

if st.session_state.booking:
    booking = st.session_state.booking
    st.markdown('<div class="section-title">La tua prenotazione demo</div>', unsafe_allow_html=True)
    st.success(f"{booking['name']} ({booking['city']}) · {booking['date']} alle {booking['time']} · {booking['duration']}")
    st.caption("Prenotazione demo — non collegata alla biblioteca reale.")

# QR concept for the active booking (or a chosen library if no reservation exists).
st.markdown('<div id="checkin"></div><div class="section-title"><span>06</span>Arriva. Scansiona. Studia.</div>', unsafe_allow_html=True)
st.write("Nel prototipo il QR simula il passaggio di presenza; non comunica con la biblioteca.")
st.info("Scansiona il QR per simulare il check-in presso questa biblioteca. Il check-in è demo e non persistente tra dispositivi.")
st.markdown("**Prenotazione → Arrivo → Scansione QR → Check-in → Posto occupato → Disponibilità aggiornata**  \n**Check-out → Posto liberato → Disponibilità aggiornata**")
qr_rows = libraries[libraries["id"] == st.session_state.booking["id"]] if st.session_state.booking else libraries
if st.session_state.booking:
    qr_library = st.session_state.booking["id"]
    st.caption(f"QR collegato alla prenotazione di {st.session_state.booking['name']}.")
else:
    qr_library = st.selectbox("Biblioteca per il QR demo", qr_rows["id"].tolist(), format_func=lambda library_id: libraries.loc[libraries["id"] == library_id, "name"].iloc[0])
public_url = st.text_input("URL pubblico Study-Spot", value="https://study-spot-conversano.streamlit.app", key="public_url")
qr_name = libraries.loc[libraries["id"] == qr_library, "name"].iloc[0]
qr_url = f"{public_url.rstrip('/')}?checkin={quote(qr_library)}" if public_url.startswith("http") else ""
if qr_url:
    qr_image = qrcode.make(qr_url)
    qr_buffer = BytesIO()
    qr_image.save(qr_buffer, format="PNG")
    col_qr, col_url = st.columns([1, 2])
    with col_qr:
        st.image(qr_buffer.getvalue(), width=200, caption=f"QR demo · {qr_name}")
    with col_url:
        st.write("Questo QR apre il punto di ingresso demo del check-in.")
        st.code(qr_url)

query_library = st.query_params.get("checkin") if hasattr(st, "query_params") else None
if query_library:
    query_rows = libraries[libraries["id"] == query_library]
    if not query_rows.empty:
        st.markdown('<div class="section-title">Check-in demo</div>', unsafe_allow_html=True)
        st.info(f"QR riconosciuto per **{query_rows.iloc[0]['name']}**. Simulazione non collegata alla biblioteca reale.")
        if st.session_state.booking and st.session_state.booking["id"] == query_library:
            if not st.session_state.checked_in and st.button("Conferma check-in demo", type="primary"):
                st.session_state.checked_in = True
                st.rerun()
            elif st.session_state.checked_in and st.button("Conferma check-out demo"):
                st.session_state.seats[query_library] += 1
                st.session_state.checked_in = False
                st.session_state.booking = None
                st.rerun()
            st.caption("Check-in attivo solo nella sessione corrente: il posto resta occupato; il check-out lo libera e aggiorna la disponibilità demo. Nessuna persistenza tra dispositivi.")
        else:
            st.caption("Per simulare check-in e check-out serve una prenotazione demo per questa biblioteca.")

st.markdown('<div id="notifications"></div><div class="section-title"><span>07</span>Avvisami quando si libera un posto</div>', unsafe_allow_html=True)
email_col, action_col = st.columns([2, 1])
with email_col:
    email = st.text_input("Email (non salvata)", placeholder="nome@email.it", key="notification_email")
with action_col:
    st.write("")
    if st.button("Attiva notifica demo", use_container_width=True):
        if "@" in email and "." in email:
            st.session_state.notifications = True
        else:
            st.warning("Inserisci un indirizzo email valido per la simulazione.")
if st.session_state.notifications:
    st.caption("Notifica attiva solo per questa sessione demo; nessuna email verrà inviata.")

with st.expander("MVP / Come funziona"):
    st.write("Nel prototipo la disponibilità delle postazioni è simulata. In una versione reale Study-Spot potrà utilizzare QR Check-in/Check-out per aggiornare l'occupazione delle postazioni.")
    st.write("I dati territoriali mostrati provengono dal catalogo Biblioteche di Puglia; le voci prive di informazioni verificate sull'accesso sono contrassegnate **Accesso da verificare**.")
    st.write("Build → Measure → Learn: il prototipo serve a verificare il bisogno prima di realizzare infrastruttura e integrazioni reali.")
    st.markdown(f"Fonte primaria: [Regione Puglia – Biblioteche del Polo PUG]({REGION_URL})")
    st.markdown(f"Integrazione Bari: [Regione Puglia – Biblioteche Colibrì]({COLIBRI_URL})")
    st.markdown(f"Verifica catalografica: [ICCU – SBN Polo Terra di Bari (BA1)]({ICCU_URL})")

st.markdown('<div class="footer">Study-Spot · Workshop 04 · Lean Startup · MVP didattico</div>', unsafe_allow_html=True)
