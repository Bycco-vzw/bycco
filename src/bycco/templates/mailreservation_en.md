## Confirmation reservation for a stay during the BYCC 2026

This email was sent automatically.

We will confirm your application for a stay during the BYCC 2026.

If there are any errors in the details listed below, please contact us at <floreal@bycco.be> adding your mobile phone number.

We will send you the price by e-mail after the accommodation has been allocated. Only after payment of the stated amount, the accommodation is definitively confirmed

_The Bycco team_

### Details responsible person

- Name: {{ first_name }} {{ last_name }}
- Email: {{ email }}
- Mobile: {{ mobile }}
- Address: <br>{{ address | replace("\n", "<br>")}}

### Details guests

{% for g in guestlist %}

- Name: {{ g.first_name }} {{ g.last_name }} <br>
    Birthday: {{ g.birthdate }} <br>
    Player: {{ "Yes" if g.player else "No" }} <br>
    Age category: {{ g.age_category }} <br>
{%endfor%}

### Details accommodation and catering

- Type: {{ stay }}
- Arrival date: {{ checkindate[0:10] }}
- Departure date: {{ checkoutdate[0:10] }}
- Meals: {{ meals }}

### Remarks

{{ (remarks if remarks else "No remarks") | replace("\n", "<br>")}}
