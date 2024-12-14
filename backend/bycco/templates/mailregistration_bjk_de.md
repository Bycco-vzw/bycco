## Bestätigung Registrierung BJLM 2025

### Teilnehmerdetails

- {{ first_name }} {{ last_name }}
- Geburtsjahr: {{ birthyear }}
- ID-Nummer: {{ idbel }}
- Vereinnummer: {{ idclub }}
- FIDE-Nationalität: {{ nationalityfide }}
- Kann belgischer Meister werden: {{ ['Ja', 'Nein', 'zu bestätigen'][natstatus] }}
- Geschlecht: {{ gender }}
- Kategorie: {{ category }}
- Bemerkungen: {{ (remarks if remarks else "Keine Bemerkungen") | replace("\n", "<br>")}}

Mit freundlichen Grüßen.

_Das Bycco-Team_
