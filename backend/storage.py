import json
import os
import shutil
from typing import Any


# ======================================================
# BASIS FUNKTIONEN
# ======================================================

def ensure_directory(path: str):
    """
    Stellt sicher, dass das Zielverzeichnis existiert.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


# ======================================================
# JSON LADEN
# ======================================================

def load_json(path: str, default: Any = None):
    """
    Lädt eine JSON-Datei sicher.

    - Wenn Datei nicht existiert → default oder []
    - Wenn Datei leer ist → default oder []
    - Wenn Datei korrupt ist → Backup wird erstellt
    """

    if default is None:
        default = []

    if not os.path.exists(path):
        return default

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return default
            return json.loads(content)

    except json.JSONDecodeError:
        # Datei ist beschädigt → Backup erstellen
        backup_path = path + ".corrupt_backup"
        shutil.copy(path, backup_path)
        return default

    except Exception:
        return default


# ======================================================
# JSON SPEICHERN (ATOMISCH)
# ======================================================

def save_json(path: str, data: Any):
    """
    Speichert JSON atomisch (keine kaputten Dateien bei Absturz).
    """

    ensure_directory(path)

    temp_path = path + ".tmp"

    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    # Atomarer Replace
    os.replace(temp_path, path)


# ======================================================
# APPEND
# ======================================================

def append_json(path: str, item: Any):
    """
    Fügt einen Eintrag zu einer JSON-Liste hinzu.
    """
    data = load_json(path, default=[])
    if not isinstance(data, list):
        data = []
    data.append(item)
    save_json(path, data)


# ======================================================
# UPDATE BY INDEX
# ======================================================

def update_json_index(path: str, index: int, item: Any):
    """
    Aktualisiert einen Eintrag in einer JSON-Liste anhand des Index.
    """
    data = load_json(path, default=[])

    if not isinstance(data, list):
        raise ValueError("JSON ist keine Liste.")

    if not (0 <= index < len(data)):
        raise IndexError("Index außerhalb des Bereichs.")

    data[index] = item
    save_json(path, data)


# ======================================================
# DELETE BY INDEX
# ======================================================

def delete_json_index(path: str, index: int):
    """
    Löscht einen Eintrag anhand des Index.
    """
    data = load_json(path, default=[])

    if not isinstance(data, list):
        raise ValueError("JSON ist keine Liste.")

    if not (0 <= index < len(data)):
        raise IndexError("Index außerhalb des Bereichs.")

    data.pop(index)
    save_json(path, data)


# ======================================================
# CLEAR FILE
# ======================================================

def clear_json(path: str):
    """
    Leert eine JSON-Datei vollständig.
    """
    save_json(path, [])


# ======================================================
# EXISTS
# ======================================================

def file_exists(path: str) -> bool:
    return os.path.exists(path)


# ======================================================
# SAFE MERGE
# ======================================================

def merge_json_dict(path: str, new_data: dict):
    """
    Merged ein Dictionary in bestehende JSON-Datei.
    """
    data = load_json(path, default={})

    if not isinstance(data, dict):
        data = {}

    data.update(new_data)
    save_json(path, data)
