## Zahlungsanfrage Aufenthalt Floreal 2024

Wir bitten Sie, die aufgeführten Daten noch einmal zu überprüfen und uns eventuelle Fehler zu melden

### Anfrage

{{ first_name }} {{ last_name }}<br>
{{ address}}<br>
{{ email }}<br>
{{ mobile }}<br>

Check-in Datum: {{ checkindate }}<br>
Check-out Datum: {{ checkoutdate}}

{{ guests }}

### Reserverung

| Bezeichnung | Anzahl | Preis | Summe |
|:-------------|:------:|--------:|--------:|
{% for d in details %}
| {{ d.description }} | {{ d.quantity or "" }} | {{ d. unitprice + " €" if d.unitprice }} | {{ d.totalprice }} € |
{% endfor %}

### Zahlung

Bitte überweisen Sie vor dem 15. Februar 2024 den Betrag von {{ totalprice }} € auf das Konto von Bycco
BE33 0017 5924 5146 mit der strukturierten Kommunikation {{ paymessage }}

Nach dem 15. Februar fallen Stornokosten an.

Nach der Zahlung ist die Reservierung des Aufenthalts endgültig bestätigt.

Wenn Sie eine Rechnung im Namen eines Mehrwertsteuerzahlers wünschen, kontaktieren Sie uns bitte so schnell wie möglich
um auf diese E-Mail unter Angabe der Umsatzsteuerdaten des Betroffenen zu antworten:

- Name
- Adresse
- Email
- Umsatzsteuer-Identifikationsnummer

Mit freundlichen Grüßen

_Das Bycco-Team_
