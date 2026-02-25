from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.storage import load_json, save_json
import os
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import io
from reportlab.lib.utils import ImageReader
import base64

app = FastAPI(title="GMatrix API")

# ======================================================
# CORS
# ======================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# PATH SETUP
# ======================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

def path(filename: str):
    return os.path.join(DATA_DIR, filename)


# ======================================================
# ROOT
# ======================================================

@app.get("/")
def root():
    return {"status": "GMatrix Backend läuft"}


# ======================================================
# MITARBEITER
# ======================================================

MITARBEITER_FILE = path("mitarbeiter.json")

@app.get("/mitarbeiter")
def get_mitarbeiter():
    return load_json(MITARBEITER_FILE)


@app.post("/mitarbeiter")
def create_mitarbeiter(mitarbeiter: list = Body(...)):
    data = load_json(MITARBEITER_FILE)
    data.append(mitarbeiter)
    save_json(MITARBEITER_FILE, data)
    return {"message": "Mitarbeiter gespeichert"}


@app.put("/mitarbeiter/{index}")
def update_mitarbeiter(index: int, mitarbeiter: list = Body(...)):
    data = load_json(MITARBEITER_FILE)
    if not (0 <= index < len(data)):
        raise HTTPException(status_code=404, detail="Index ungültig")
    data[index] = mitarbeiter
    save_json(MITARBEITER_FILE, data)
    return {"message": "Mitarbeiter aktualisiert"}


@app.delete("/mitarbeiter/{index}")
def delete_mitarbeiter(index: int):
    data = load_json(MITARBEITER_FILE)
    if not (0 <= index < len(data)):
        raise HTTPException(status_code=404, detail="Index ungültig")
    data.pop(index)
    save_json(MITARBEITER_FILE, data)
    return {"message": "Mitarbeiter gelöscht"}


# ======================================================
# FILIALEN
# ======================================================

FILIALEN_FILE = path("filialen.json")

@app.get("/filialen")
def get_filialen():
    return load_json(FILIALEN_FILE)


@app.post("/filialen")
def create_filiale(filiale: list = Body(...)):
    data = load_json(FILIALEN_FILE)
    data.append(filiale)
    save_json(FILIALEN_FILE, data)
    return {"message": "Filiale gespeichert"}


@app.put("/filialen/{index}")
def update_filiale(index: int, filiale: list = Body(...)):
    data = load_json(FILIALEN_FILE)
    if not (0 <= index < len(data)):
        raise HTTPException(status_code=404, detail="Index ungültig")
    data[index] = filiale
    save_json(FILIALEN_FILE, data)
    return {"message": "Filiale aktualisiert"}


@app.delete("/filialen/{index}")
def delete_filiale(index: int):
    data = load_json(FILIALEN_FILE)
    if not (0 <= index < len(data)):
        raise HTTPException(status_code=404, detail="Index ungültig")
    data.pop(index)
    save_json(FILIALEN_FILE, data)
    return {"message": "Filiale gelöscht"}


# ======================================================
# SCHICHTEN
# ======================================================

SCHICHTEN_FILE = path("schichten.json")

@app.get("/schichten")
def get_schichten():
    return load_json(SCHICHTEN_FILE)


@app.post("/schichten")
def create_schicht(schicht: list = Body(...)):
    data = load_json(SCHICHTEN_FILE)
    data.append(schicht)
    save_json(SCHICHTEN_FILE, data)
    return {"message": "Schicht gespeichert"}


@app.put("/schichten/{index}")
def update_schicht(index: int, schicht: list = Body(...)):
    data = load_json(SCHICHTEN_FILE)
    if not (0 <= index < len(data)):
        raise HTTPException(status_code=404, detail="Index ungültig")
    data[index] = schicht
    save_json(SCHICHTEN_FILE, data)
    return {"message": "Schicht aktualisiert"}


@app.delete("/schichten/{index}")
def delete_schicht(index: int):
    data = load_json(SCHICHTEN_FILE)
    if not (0 <= index < len(data)):
        raise HTTPException(status_code=404, detail="Index ungültig")
    data.pop(index)
    save_json(SCHICHTEN_FILE, data)
    return {"message": "Schicht gelöscht"}


# ======================================================
# ÜBERSICHT
# ======================================================

UEBERSICHT_FILE = path("uebersicht.json")

@app.get("/uebersicht")
def get_uebersicht():
    return load_json(UEBERSICHT_FILE)


# Komplettes Objekt speichern (nicht append)
@app.post("/uebersicht")
def save_full_uebersicht(payload = Body(...)):
    save_json(UEBERSICHT_FILE, payload)
    return {"message": "Übersicht vollständig gespeichert"}


@app.put("/uebersicht/{index}")
def update_uebersicht(index: int, eintrag: list = Body(...)):
    data = load_json(UEBERSICHT_FILE)
    if not (0 <= index < len(data)):
        raise HTTPException(status_code=404, detail="Index ungültig")
    data[index] = eintrag
    save_json(UEBERSICHT_FILE, data)
    return {"message": "Eintrag aktualisiert"}


@app.delete("/uebersicht/{index}")
def delete_uebersicht(index: int):
    data = load_json(UEBERSICHT_FILE)
    if not (0 <= index < len(data)):
        raise HTTPException(status_code=404, detail="Index ungültig")
    data.pop(index)
    save_json(UEBERSICHT_FILE, data)
    return {"message": "Eintrag gelöscht"}


@app.delete("/uebersicht")
def clear_uebersicht():
    save_json(UEBERSICHT_FILE, [])
    return {"message": "Übersicht vollständig geleert"}


# ======================================================
# KALENDERWOCHEN
# ======================================================

from datetime import datetime, timedelta

KALENDERWOCHEN_FILE = path("kalenderwochen.json")


# ------------------------------------------------------
# Alle gespeicherten Kalenderwochen abrufen
# ------------------------------------------------------

@app.get("/kalenderwochen")
def get_all_calendar_weeks():
    return load_json(KALENDERWOCHEN_FILE)


# ------------------------------------------------------
# Einzelne Kalenderwoche abrufen
# ------------------------------------------------------

@app.get("/kalenderwochen/{kw}/{jahr}")
def get_calendar_week(kw: int, jahr: int):
    data = load_json(KALENDERWOCHEN_FILE)

    for entry in data:
        if entry.get("kalenderwoche") == kw and entry.get("jahr") == jahr:
            return entry

    raise HTTPException(status_code=404, detail="Kalenderwoche nicht gefunden")


# ------------------------------------------------------
# Kalenderwoche erstellen (Snapshot der Übersicht)
# ------------------------------------------------------

@app.post("/kalenderwochen/{kw}/{jahr}")
def create_calendar_week(kw: int, jahr: int):

    # ISO Montag berechnen
    try:
        montag = datetime.fromisocalendar(jahr, kw, 1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Ungültige Kalenderwoche")

    daten = [(montag + timedelta(days=i)).strftime("%d.%m.%Y") for i in range(7)]

    # Übersicht laden (Snapshot)
    uebersicht = load_json(UEBERSICHT_FILE)

    tage_mit_datum = {
        f"{tag} ({daten[i]})": daten[i]
        for i, tag in enumerate(
            ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]
        )
    }

    new_entry = {
        "kalenderwoche": kw,
        "jahr": jahr,
        "tage": tage_mit_datum,
        "uebersicht": uebersicht
    }

    data = load_json(KALENDERWOCHEN_FILE)

    # Replace falls existiert
    replaced = False
    for i, entry in enumerate(data):
        if entry.get("kalenderwoche") == kw and entry.get("jahr") == jahr:
            data[i] = new_entry
            replaced = True
            break

    if not replaced:
        data.append(new_entry)

    save_json(KALENDERWOCHEN_FILE, data)

    return {
        "message": f"Kalenderwoche KW {kw} – {jahr} gespeichert",
        "replaced": replaced
    }


# ------------------------------------------------------
# Kalenderwoche löschen
# ------------------------------------------------------

@app.delete("/kalenderwochen/{kw}/{jahr}")
def delete_calendar_week(kw: int, jahr: int):
    data = load_json(KALENDERWOCHEN_FILE)

    new_data = [
        entry for entry in data
        if not (
            entry.get("kalenderwoche") == kw and entry.get("jahr") == jahr
        )
    ]

    if len(new_data) == len(data):
        raise HTTPException(status_code=404, detail="Kalenderwoche nicht gefunden")

    save_json(KALENDERWOCHEN_FILE, new_data)

    return {"message": f"Kalenderwoche KW {kw} – {jahr} gelöscht"}


# ------------------------------------------------------
# Übersicht aus Kalenderwoche wiederherstellen
# ------------------------------------------------------

@app.post("/kalenderwochen/{kw}/{jahr}/restore")
def restore_calendar_week(kw: int, jahr: int):
    data = load_json(KALENDERWOCHEN_FILE)

    for entry in data:
        if entry.get("kalenderwoche") == kw and entry.get("jahr") == jahr:
            save_json(UEBERSICHT_FILE, entry.get("uebersicht", []))
            return {"message": "Übersicht wiederhergestellt"}

    raise HTTPException(status_code=404, detail="Kalenderwoche nicht gefunden")


# ======================================================
# TEAMS
# ======================================================

TEAMS_FILE = path("teams.json")

@app.get("/teams")
def get_teams():
    return load_json(TEAMS_FILE)


@app.post("/teams")
def save_teams(data: list):
    save_json(TEAMS_FILE, data)
    return {"message": "Teams gespeichert"}


# ======================================================
# ARBEITSTÄTIGKEITEN
# ======================================================

ARBEIT_FILE = path("arbeitstaetigkeiten.json")


@app.get("/arbeitstaetigkeiten")
def get_arbeitstaetigkeiten():
    return load_json(ARBEIT_FILE)


@app.post("/arbeitstaetigkeiten")
def create_arbeitstaetigkeit(eintrag: list = Body(...)):
    data = load_json(ARBEIT_FILE)
    data.append(eintrag)
    save_json(ARBEIT_FILE, data)
    return {"message": "Arbeitstätigkeit gespeichert"}


@app.put("/arbeitstaetigkeiten/{index}")
def update_arbeitstaetigkeit(index: int, eintrag: list = Body(...)):
    data = load_json(ARBEIT_FILE)

    if not (0 <= index < len(data)):
        raise HTTPException(status_code=404, detail="Index ungültig")

    data[index] = eintrag
    save_json(ARBEIT_FILE, data)
    return {"message": "Arbeitstätigkeit aktualisiert"}


@app.delete("/arbeitstaetigkeiten/{index}")
def delete_arbeitstaetigkeit(index: int):
    data = load_json(ARBEIT_FILE)

    if not (0 <= index < len(data)):
        raise HTTPException(status_code=404, detail="Index ungültig")

    data.pop(index)
    save_json(ARBEIT_FILE, data)
    return {"message": "Arbeitstätigkeit gelöscht"}


# ======================================================
# RECHNUNG
# ======================================================

@app.post("/rechnung/pdf")
def create_rechnung_pdf(payload: dict = Body(...)):

    rechnung = payload.get("rechnung", {})
    briefkopf = payload.get("briefkopf", {})

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    left = 25 * mm
    right = width - 25 * mm
    y = height - 25 * mm

    def check_page_space(y_pos, needed=20):
        if y_pos < 60:
            c.showPage()
            c.setFont("Helvetica", 10)
            return height - 25 * mm
        return y_pos

    # --------------------------------------------------
    # LOGO (ganz oben rechts – über Absender)
    # --------------------------------------------------

    logo_base64 = briefkopf.get("logo")

    if logo_base64:
        try:
            header, encoded = logo_base64.split(",", 1)
            logo_bytes = base64.b64decode(encoded)
            image = ImageReader(io.BytesIO(logo_bytes))

            logo_width = 120
            logo_height = 60

            # 🔥 Direkt unter dem oberen Seitenrand
            logo_y = height - 5 * mm - logo_height

            c.drawImage(
                image,
                right - logo_width,
                logo_y,
                width=logo_width,
                height=logo_height,
                preserveAspectRatio=True,
                mask='auto'
            )

        except Exception as e:
            print("Logo Fehler:", e)

    # --------------------------------------------------
    # ABSENDER
    # --------------------------------------------------
    c.setFont("Helvetica", 10)

    for line in briefkopf.get("name", "").split("\n"):
        c.drawString(left, y, line)
        y -= 14

    for line in briefkopf.get("adresse", "").split("\n"):
        c.drawString(left, y, line)
        y -= 14

    y -= 20

    # --------------------------------------------------
    # KUNDE
    # --------------------------------------------------
    kunde = rechnung.get("kunde", {})

    for line in kunde.get("firma", "").split("\n"):
        c.drawString(left, y, line)
        y -= 14

    for line in kunde.get("kontakt", "").split("\n"):
        c.drawString(left, y, line)
        y -= 14

    for line in kunde.get("adresse", "").split("\n"):
        c.drawString(left, y, line)
        y -= 14

    y -= 20

    # --------------------------------------------------
    # RECHNUNGSDATEN (rechtsbündig)
    # --------------------------------------------------
    c.drawRightString(right, y, f"Rechnungsnummer: {rechnung.get('nummer', '')}")
    y -= 14
    c.drawRightString(right, y, f"Rechnungsdatum: {rechnung.get('datum', '')}")
    y -= 25
    # --------------------------------------------------
    # TEXTBEREICH NACH TABELLE
    # --------------------------------------------------
    c.setFont("Helvetica", 10)
    y -= 14
    y = check_page_space(y)

    c.drawString(left, y, "Sehr geehrte Damen und Herren,")
    y -= 16

    for line in briefkopf.get("einleitung", "").split("\n"):
        c.drawString(left, y, line)
        y -= 14

    y -= 20
    y = check_page_space(y)


    # --------------------------------------------------
    # TABELLE HEADER
    # --------------------------------------------------
    col_datum = left
    col_text = left + 70
    col_std = right - 90
    col_satz = right - 50
    col_betrag = right

    c.setFont("Helvetica-Bold", 10)
    c.drawString(col_datum, y, "Datum")
    c.drawString(col_text, y, "Beschreibung")
    c.drawRightString(col_std, y, "Std")
    c.drawRightString(col_satz, y, "Satz")
    c.drawRightString(col_betrag, y, "Betrag")
    y -= 12

    c.line(left, y, right, y)
    y -= 12
    c.setFont("Helvetica", 10)

    netto = 0.0

    # --------------------------------------------------
    # POSITIONEN
    # --------------------------------------------------
    for p in rechnung.get("positionen", []):

        y = check_page_space(y)

        stunden = float(p.get("stunden", 0))
        satz = float(p.get("satz", 0))
        betrag = stunden * satz
        netto += betrag

        c.drawString(col_datum, y, p.get("datum", ""))
        c.drawString(col_text, y, p.get("text", ""))
        c.drawRightString(col_std, y, f"{stunden:.2f}")
        c.drawRightString(col_satz, y, f"{satz:.2f}")
        c.drawRightString(col_betrag, y, f"{betrag:.2f}")

        y -= 16



    # --------------------------------------------------
    # SUMMEN
    # --------------------------------------------------
    steuer = 0.0

    if not briefkopf.get("steuer_befreit", True):
        steuer = netto * float(briefkopf.get("steuer_prozent", 19)) / 100

    y -= 20
    y = check_page_space(y)

    c.drawRightString(col_satz, y, "Zwischensumme:")
    c.drawRightString(col_betrag, y, f"{netto:.2f}")
    y -= 14

    if not briefkopf.get("steuer_befreit", True):
        c.drawRightString(col_satz, y, f"MwSt ({briefkopf.get('steuer_prozent', 19)}%):")
        c.drawRightString(col_betrag, y, f"{steuer:.2f}")
        y -= 14
    else:
        for line in briefkopf.get("steuer_text", "").split("\n"):
            c.drawString(left, y, line)
            y -= 14

    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(col_satz, y, "Gesamtbetrag:")
    c.drawRightString(col_betrag, y, f"{netto + steuer:.2f}")

    c.setFont("Helvetica", 10)
    y -= 40
    y = check_page_space(y)


    y -= 20
    y = check_page_space(y)

    for line in briefkopf.get("zahlungs_text", "").split("\n"):
        c.drawString(left, y, line)
        y -= 30

    for line in briefkopf.get("abschluss_text", "").split("\n"):
        c.drawString(left, y, line)
        y -= 14

    y -= 30
    y = check_page_space(y)

    for line in briefkopf.get("gruss", "").split("\n"):
        c.drawString(left, y, line)
        y -= 14

    y -= 20
    c.drawString(left, y, briefkopf.get("name", ""))

    y -= 20

    for line in briefkopf.get("bank", "").split("\n"):
        c.drawString(left, y, line)
        y -= 14

    c.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={rechnung.get('nummer','Rechnung')}.pdf"}
    )
