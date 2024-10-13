## Zahlungsanfrage Aufenthalt Floreal 2025

Wir bitten Sie, die aufgeführten Daten noch einmal zu überprüfen und uns eventuelle Fehler zu melden

### Anfrage

{{ first_name }} {{ last_name }}<br>
{{ address}}<br>
{{ email }}<br>
{{ mobile }}<br>

Check-in Datum: {{ checkindate }}<br>
Check-out Datum: {{ checkoutdate}}

{{ guests }}

Kommentare: {{ reservationremarks or "" }}

Aufgrund eines technischen Fehlers wurden die von Ihnen bei der Reservierung abgegebenen Kommentare möglicherweise nicht registriert. Bitte senden Sie diese Kommentare als Antwort auf diese E-Mail

### Reserverung

| Bezeichnung | Anzahl | Preis | Summe |
|:-------------|:------:|--------:|--------:|
{% for d in details %}
| {{ d.description }} | {{ d.quantity or "" }} | {{ d. unitprice + " €" if d.unitprice }} | {{ d.totalprice }} € |
{% endfor %}

{{ reductionremark or "" }}

### Zahlung

Bitte überweisen Sie innerhalb von 14 Tagen den Betrag von {{ totalprice }} € auf das Konto von Bycco
BE33 0017 5924 5146 mit der strukturierten Kommunikation {{ paymessage }}


Nach der Zahlung ist die Reservierung des Aufenthalts endgültig bestätigt.

Wenn Sie eine Rechnung im Namen eines Mehrwertsteuerzahlers wünschen, kontaktieren Sie uns bitte so schnell wie möglich
um auf diese E-Mail unter Angabe der Umsatzsteuerdaten des Betroffenen zu antworten:

- Name
- Adresse
- Email
- Umsatzsteuer-Identifikationsnummer

Mit freundlichen Grüßen

_Das Bycco-Team_
