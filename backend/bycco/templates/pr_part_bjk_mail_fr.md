## CBJ 2024: Demande de paiement pour l'enregistrement 

### Enregistrement

| Description | Nombre | Prix un. | Total |
|:-------------|:------:|--------:|--------:|
{% for d in details %}
| {{ d.description }} | {{ d.quantity or "" }} | {{ d. unitprice + " €" if d.unitprice }} | {{ d.totalprice }} € |
{% endfor %}

### Paiement

Veuillez virer le montant de {{ totalprice }} € sur le compte de Bycco
BE33 0017 5924 5146 avec la communication structurée {{ paymessage }} dans les 7 jours.

Si vous souhaitez une facture au nom d'un assujetti à la TVA, merci de nous 
contacter au plus vite pour répondre à cet e-mail en indiquant les coordonnées 
TVA de l'assujetti :

  - Nom
  - adresse
  - e-mail
  - Numéro de TVA

Cordialement

_L'équipe Bycco_