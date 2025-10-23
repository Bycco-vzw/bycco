## Zahlungsanfrage Anmeldung BJLM 2026


### Anmeldung

| Bezeichnung | Anzahl | Preis | Summe |
|:-------------|:------:|--------:|--------:|
{% for d in details %}
| {{ d.description }} | {{ d.quantity or "" }} | {{ d. unitprice + " €" if d.unitprice }} | {{ d.totalprice }} € |
{% endfor %}

### Zahlung

Bitte überweisen Sie innerhalb von 7 Tagen den Betrag von {{ totalprice }} € auf das Konto von Bycco
BE33 0017 5924 5146 mit der strukturierten Kommunikation {{ paymessage }}


Wenn Sie eine Rechnung im Namen eines Mehrwertsteuerzahlers wünschen, kontaktieren Sie uns bitte so schnell wie möglich
um auf diese E-Mail unter Angabe der Umsatzsteuerdaten des Betroffenen zu antworten:

  - Name
  - Adresse
  - Email
  - Umsatzsteuer-Identifikationsnummer

Mit freundlichen Grüßen

_Das Bycco-Team_