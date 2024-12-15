## Bevestiging inschrijving BJK 2025

### Details deelnemer

- {{ first_name }} {{ last_name }}
- Geboortejaar: {{ birthyear }}
- Stamnummer: {{ idbel }}
- Clubnummer: {{ idclub }}
- FIDE nationaliteit: {{ nationalityfide }}
- Kan Belgisch kampioen worden: {{ ['Ja', 'Neen', 'Te bevestigen'][natstatus] }}
- Geslacht: {{ gender }}
- Categorie: {{ category }}
- Opmerkingen: {{ (remarks if remarks else "Geen opmerkingen")  | replace("\n", "<br>")}}


met vriendelijke groeten.

_Het Bycco team_
