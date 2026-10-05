import streamlit as st
import pandas as pd
from datetime import date, time

st.set_page_config(page_title="Study-Spot | Conversano", page_icon="📚", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.block-container{max-width:1180px;padding-top:1.2rem;padding-bottom:3rem}
.hero{background:linear-gradient(135deg,#eaf6ef 0%,#f8fbf9 55%,#fff 100%);border:1px solid #d7eadf;border-radius:24px;padding:30px}
.badge{display:inline-block;padding:6px 11px;border-radius:999px;background:#dff2e7;color:#246145;font-weight:700;font-size:.82rem}
.hero h1{font-size:3.2rem;margin:.35rem 0 .4rem;color:#18352a}.hero p{font-size:1.08rem;color:#52665c}
.card{border:1px solid #e2e8f0;border-radius:18px;padding:18px;background:#fff;min-height:145px}
.available{color:#1f8a50;font-weight:800}.busy{color:#d34d4d;font-weight:800}.small{color:#64748b;font-size:.88rem}
.section-title{font-size:1.65rem;font-weight:800;color:#18352a;margin-top:1.4rem}
.footer{text-align:center;color:#718096;padding:30px 0 5px}
</style>
""", unsafe_allow_html=True)

if "seats" not in st.session_state:
    st.session_state.seats = {
        "Biblioteca Comunale": 12,
        "Sala Studio Centro": 7,
        "Biblioteca Universitaria": 18,
        "Spazio Studio Conversano": 0,
    }
if "booking" not in st.session_state:
    st.session_state.booking = None
if "notifications" not in st.session_state:
    st.session_state.notifications = False

libraries = pd.DataFrame([
    ["Biblioteca Comunale","Centro",12,40.9522,17.1137],
    ["Sala Studio Centro","Centro",7,40.9532,17.1146],
    ["Biblioteca Universitaria","Zona Università",18,40.9564,17.1178],
    ["Spazio Studio Conversano","Periferia",0,40.9489,17.1089],
], columns=["Nome","Zona","Posti","lat","lon"])
libraries["Posti"] = libraries["Nome"].map(st.session_state.seats)

st.markdown("""
<div class="hero">
<span class="badge">MVP • DEMO SENZA REGISTRAZIONE</span>
<h1>📚 Study-Spot</h1>
<p><b>Trova il tuo posto. Inizia a studiare.</b><br>
Disponibilità delle postazioni e prenotazione rapida a Conversano.</p>
</div>
""", unsafe_allow_html=True)

st.write("")
c1,c2,c3,c4 = st.columns(4)
c1.metric("Posti disponibili", int(libraries["Posti"].sum()))
c2.metric("Biblioteche", len(libraries))
c3.metric("Accesso", "Immediato")
c4.metric("Registrazione", "Non richiesta")

st.markdown('<div class="section-title">📍 Disponibilità a Conversano</div>', unsafe_allow_html=True)
st.caption("Dati simulati per la demo — non rappresentano disponibilità reali.")

search = st.text_input("🔎 Cerca una biblioteca", placeholder="Es. Biblioteca Comunale")
view = libraries[libraries["Nome"].str.contains(search, case=False, na=False)] if search else libraries

cols = st.columns(2)
for idx, (_, row) in enumerate(view.iterrows()):
    with cols[idx % 2]:
        n = int(st.session_state.seats[row["Nome"]])
        cls = "available" if n > 0 else "busy"
        status = f"🟢 {n} posti disponibili" if n > 0 else "🔴 Nessun posto disponibile"
        st.markdown(f'<div class="card"><div style="font-size:1.25rem;font-weight:800;">{row["Nome"]}</div><div class="small">📍 {row["Zona"]}, Conversano</div><p class="{cls}">{status}</p></div>', unsafe_allow_html=True)
        if n > 0:
            if st.button(f"Prenota → {row['Nome']}", key=f"book_{row['Nome']}", use_container_width=True):
                st.session_state.selected = row["Nome"]
                st.rerun()
        else:
            st.button("Posti esauriti", key=f"full_{row['Nome']}", disabled=True, use_container_width=True)

st.markdown('<div class="section-title">🗺️ Mappa delle postazioni</div>', unsafe_allow_html=True)
st.map(libraries[["lat","lon"]], latitude=40.9522, longitude=17.1137, zoom=14, height=380)

if "selected" in st.session_state:
    selected = st.session_state.selected
    st.markdown('<div class="section-title">🎟️ Prenota una postazione</div>', unsafe_allow_html=True)
    st.info(f"Hai selezionato **{selected}**. Nessun account è necessario: è una simulazione del flusso MVP.")
    with st.form("booking_form"):
        a,b,c = st.columns(3)
        with a: booking_date = st.date_input("Data", value=date.today())
        with b: booking_time = st.time_input("Ora", value=time(10,0))
        with c: duration = st.selectbox("Durata", ["1 ora","2 ore","3 ore"])
        if st.form_submit_button("✅ Conferma prenotazione", use_container_width=True):
            if st.session_state.seats[selected] > 0:
                st.session_state.seats[selected] -= 1
                st.session_state.booking = {"luogo":selected,"data":booking_date.strftime("%d/%m/%Y"),"ora":booking_time.strftime("%H:%M"),"durata":duration}
                del st.session_state.selected
                st.rerun()

if st.session_state.booking:
    b = st.session_state.booking
    st.success(f"Prenotazione confermata! 📚 **{b['luogo']}** — {b['data']} alle {b['ora']} — {b['durata']}. Questa prenotazione è dimostrativa e non è reale.")

st.markdown('<div class="section-title">🔔 Notifiche</div>', unsafe_allow_html=True)
n1,n2 = st.columns([2,1])
with n1:
    st.write("Vuoi sapere quando si libera una postazione?")
    email = st.text_input("Email (solo per la demo)", placeholder="nome@email.it")
with n2:
    st.write("")
    if st.button("Attiva notifiche", use_container_width=True):
        if "@" in email and "." in email:
            st.session_state.notifications = True
            st.success("Notifiche attivate (demo).")
        else:
            st.warning("Inserisci un'email valida per simulare l'attivazione.")
if st.session_state.notifications:
    st.caption("🔔 Stato: notifiche attive per la demo.")

with st.expander("💡 Perché questo è un MVP?"):
    st.write("La demo testa l'ipotesi del workshop concentrandosi sulle funzioni essenziali: disponibilità, mappa e prenotazione. Non serve sviluppare subito un sistema completo.")
    st.write("**Build → Measure → Learn**: costruire una versione minima, osservare l'utilizzo, imparare dai dati e adattare la soluzione.")

st.markdown('<div class="section-title">📱 QR per la presentazione</div>', unsafe_allow_html=True)
st.write("Dopo il deploy, incolla qui l'URL pubblico dell'app: il QR viene generato automaticamente.")
public_url = st.text_input("URL pubblico Study-Spot", placeholder="https://nome-app.streamlit.app")
if public_url.startswith("http"):
    import qrcode
    from io import BytesIO
    qr = qrcode.make(public_url)
    buf = BytesIO(); qr.save(buf, format="PNG")
    st.image(buf.getvalue(), width=220, caption="Scansiona per aprire Study-Spot")
    st.code(public_url)

st.markdown('<div class="footer">Study-Spot • Workshop 04 • Lean Startup • Demo didattica</div>', unsafe_allow_html=True)
