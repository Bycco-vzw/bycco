## Betalingsaanvraag inschrijving 2023


### Inschrijvinging

| Omschrijving | Aantal | Eenheid | Totaal |
|:-------------|:------:|--------:|--------:|
{% for d in details %}
| {{ d.description }} | {{ d.quantity or "" }} | {{ d. unitprice + " €" if d.unitprice }} | {{ d.totalprice }} € |
{% endfor %}

### Betaling

Gelieve binnen de 7 dagen het bedrag van {{ totalprice }} € te storten op de rekening van Bycco
BE33 0017 5924 5146  met de gestructureerde mededeling {{ paymessage }}.

Wenst u een factuur op naam van een BTW-plichtige, gelieve dan zo snel mogelijk deze mail te beantwoorden met vermelding van de BTW-gegevens van de betrokken partij:

 - naam
 - adres
 - email
 - BTW-nummer

met vriendelijke groeten

_Het Bycco team_
