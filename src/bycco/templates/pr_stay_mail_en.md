### Payment request stay Floreal 2025

We ask you to verify the data listed and to report any errors to us

### Request

{{ first_name }} {{ last_name }}<br>
{{ address}}<br>
{{ email }}<br>
{{ mobile }}<br>

Checkin date: {{ checkindate }}<br>
Checkout date: {{ checkoutdate}}

{{ guests }}

Comments: {{ reservationremarks or "" }}

Due to a technical error, the comments you provided during the reservation may not have been registered. Please send these comments as a reply to this email

### Reservation

| Description | Quantity | Unit | Total |
|:-------------|:------:|--------:|--------:|
{% for d in details %}
| {{ d.description }} | {{ d.quantity or "" }} | {{ d. unitprice + " €" if d.unitprice }} | {{ d.totalprice }} € |
{% endfor %}

Remark discount: {{ reductionremark or "none" }}

### Payment

Please transfer the amount of {{ totalprice }} € to the account of Bycco
BE33 0017 5924 5146 with the structured communication {{ paymessage }} within 14 days.

After the 15th of February there are cancellation costs.

After payment, the reservation of the stay is definitively confirmed.

If you would like an invoice in the name of a VAT payer, please contact us as soon as possible
to reply to this e-mail stating the VAT details of the party concerned:

- name
- address
- e-mail
- VAT number

Yours sincerely

_The Bycco team_
