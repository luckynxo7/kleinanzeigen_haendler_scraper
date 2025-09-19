# Kleinanzeigen Händler-Inserate Scraper

Diese Streamlit Anwendung sammelt automatisch die Links zu allen Inseraten eines oder mehrerer Händler auf [kleinanzeigen.de](https://www.kleinanzeigen.de). Geben Sie einfach die URL der Händlerseite(n) ein; die App besucht jede Seite, klickt sich durch alle paginierten Ergebnisse und extrahiert die Links zu den einzelnen Anzeigen. Anschließend können Sie die vollständige Linkliste als Textdatei herunterladen.

## Funktionen

* **Mehrere Händler gleichzeitig**: Fügen Sie mehrere Händler URLs ein (je eine pro Zeile) und die App verarbeitet sie nacheinander.
* **Automatisches Blättern**: Die App nutzt Selenium, um jede Ergebnisseite zu öffnen und durch die Seiten zu navigieren, bis alle Inserate gefunden wurden.
* **Download als TXT**: Nach dem Sammeln der Links können Sie die einzigartige Linkliste als einfache Textdatei herunterladen.

## Einrichtung

1. Clone oder laden Sie dieses Repository herunter.
2. Installieren Sie die Abhängigkeiten (idealerweise in einer virtuellen Umgebung):

   ```bash
   pip install -r requirements.txt
   ```

3. Starten Sie die Streamlit Anwendung:

   ```bash
   streamlit run app.py
   ```

   Gehen Sie anschließend in Ihrem Browser zu `http://localhost:8501`.

## Hinweise zur Nutzung

* **Headless Browser**: Die App verwendet einen headless Chrome Browser über Selenium. In manchen Umgebungen (z.B. Streamlit Cloud) kann der automatische Download des Chrome Drivers durch `webdriver‑manager` erforderlich sein. Die benötigten Pakete sind in `requirements.txt` enthalten.
* **Cookie Banner**: Bei Aufruf einer Händlerseite erscheint in der Regel ein Cookie Banner. Das Skript klickt automatisch auf „Alle akzeptieren“, um fortzufahren.
* **Geschwindigkeit**: Je nach Anzahl der Inserate kann das Sammeln der Links einige Minuten dauern. Während des Vorgangs zeigt eine Fortschrittsanzeige den aktuellen Status.

## Lizenz

Dieser Code steht unter der MIT Lizenz.
