## Floréal 2024: Demande de paiement pour le séjour

Nous vous demandons de vérifier à nouveau les données répertoriées et de nous signaler toute erreur

### Demande

{{ first_name }} {{ last_name }}<br>
{{ address}}<br>
{{ email }}<br>
{{ mobile }}<br>

Date checkin: {{ checkindate }}<br>
Date checkout: {{ checkoutdate}}

{{ guests }}

### Reservation 2022

| Description | Nombre | Prix un. | Total |
|:-------------|:------:|--------:|--------:|
{% for d in details %}
| {{ d.description }} | {{ d.quantity or "" }} | {{ d. unitprice + " €" if d.unitprice }} | {{ d.totalprice }} € |
{% endfor %}

### Paiement

Veuillez virer le montant de {{ totalprice }} € sur le compte de Bycco
BE33 0017 5924 5146 avec la communication structurée {{ paymessage }} avant le 15 février 2024.

Après le 15 février il y a coûts d'annulation.

Après paiement, la réservation du séjour est définitivement confirmée.

Si vous souhaitez une facture au nom d'un assujetti à la TVA, merci de nous
contacter au plus vite pour répondre à cet e-mail en indiquant les coordonnées
TVA de l'assujetti :

- Nom
- adresse
- e-mail
- Numéro de TVA

Cordialement

_L'équipe Bycco_
