### Payment request enrollment BYCC 2025

### Enrollment

| Description | Quantity | Unit | Total |
|:-------------|:------:|--------:|--------:|
{% for d in details %}
| {{ d.description }} | {{ d.quantity or "" }} | {{ d. unitprice + " €" if d.unitprice }} | {{ d.totalprice }} € |
{% endfor %}

### Payment

Please transfer the amount of {{ totalprice }} € to the account of Bycco
BE33 0017 5924 5146 with the structured communication {{ paymessage }} within 7 days.

If you would like an invoice in the name of a VAT payer, please contact us as soon as possible
to reply to this e-mail stating the VAT details of the party concerned:

- name
- address
- e-mail
- VAT number

Yours sincerely

_The Bycco team_
