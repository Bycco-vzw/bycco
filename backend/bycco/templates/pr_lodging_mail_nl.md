## Betalingsaanvraag verblijf Floreal 2025

Wij vragen je om de vermelde gegevens te verifiëren en eventuele fouten aan ons te melden

### Aanvraag

{{ first_name }} {{ last_name }}<br>
{{ address}}<br>
{{ email }}<br>
{{ mobile }}<br>

Checkindatum: {{ checkindate }}<br>
Checkoutdatum: {{ checkoutdate}}

{{ guests }}

### Reservering

| Omschrijving | Aantal | Eenheid | Totaal |
|:-------------|:------:|--------:|--------:|
{% for d in details %}
| {{ d.description }} | {{ d.quantity or "" }} | {{ d. unitprice + " €" if d.unitprice }} | {{ d.totalprice }} € |
{% endfor %}

### Betaling

Gelieve voor 15 februari 2024 het bedrag van {{ totalprice }} € te storten op de rekening van Bycco
BE33 0017 5924 5146  met de gestructureerde mededeling {{ paymessage }}.

Na 15 februari zijn er annulatiekosten.

Na de betaling is de reservering van het verblijf definitief bevestigd.

Wenst u een factuur op naam van een BTW-plichtige, gelieve dan zo snel mogelijk deze mail te beantwoorden met vermelding van de BTW-gegevens van de betrokken partij:

- naam
- adres
- email
- BTW-nummer

met vriendelijke groeten

_Het Bycco team_
