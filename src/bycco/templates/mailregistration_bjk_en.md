## Confirmation registration BYCC 2026

### Participant Details

- {{ first_name }} {{ last_name }}
- Birth year: {{ birthyear }}
- ID number: {{ idbel }}
- Club number: {{ idclub }}
- FIDE nationality: {{ nationalityfide }}
- Can become Belgian champion: {{ ['Yes', 'No', 'to be confirmed'][natstatus] }}
- Gender: {{ gender }}
- Category: {{ category }}
- Remarks: {{ (remarks if remarks else "No remarks") | replace("\n", "<br>")}}

Greetings.

_The Bycco team_
