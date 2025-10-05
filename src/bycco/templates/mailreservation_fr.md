## Confirmation de réservation pour le séjour CBJ 2026   

Cet e-mail a été envoyé automatiquement.

Nous confirmons votre demande de séjour pendant le CBJ 2026.

S'il y a des erreurs dans les détails énumérés ci-dessous, veuillez nous contacter à <floreal@bycco.be> en indiquant votre numéro de GSM.

Nous vous enverrons le prix par e-mail après l'attribution du logement. Ce n'est qu'après paiement du montant indiqué que l'hébergement est définitivement confirmé

_L'équipe Bycco_

### Détails personne responsable

- Nom: {{ first_name }} {{ last_name }}
- E-mail: {{ email }}
- GSM: {{ mobile }}
- Adresse: <br>{{ address | replace("\n", "<br>")}}

### Détails des invités

{% for g in guestlist %}

- Nom: {{ g.first_name }} {{ g.last_name }} <br>
    Date de naissance: {{ g.birthdate }} <br>
    Joueur: {{ "Oui" if g.player else "Non" }} <br>
    Catégorie d'âge : {{ g.age_category }} <br>
{%endfor%}

### Détails hébergement et restauration

- Type : {{ stay }}
- Date d'arrivée : {{ checkindate[0:10] }}
- Date de départ : {{ checkoutdate[0:10] }}
- Repas : {{ meals }}

### Remarques

{{ (remarks if remarks else "Pas de remarques") | replace("\n", "<br>")}}
