# Changelog

## Non publié

- Choix du **pays** (et d'une subdivision si elle existe) via la bibliothèque Python `holidays`, déjà utilisée par Home Assistant. La France reste le défaut, avec les libellés historiques.
- Option **Alsace-Moselle** conservée pour la France ; les installations existantes sont migrées sans casse (pays absent = France, réglage Alsace-Moselle conservé).
- Sélection facultative de la langue des noms de fêtes lorsque `holidays` la propose (par défaut la langue de Home Assistant si elle est supportée ; français pour la France).
- Dépendance `holidays>=0.50` ajoutée au manifeste, compatible avec Home Assistant 2024.6 (0.50/0.51) jusqu'au pin actuel du noyau (0.107).


## 1.2.9 - 2026-11-20

- Ajout d'une option **Alsace-Moselle** (désactivée par défaut) pour inclure le Vendredi Saint et la Saint Étienne, disponible à l'installation et modifiable ensuite dans les options de l'intégration.
- Précision dans le README : les dates de Pâques, de l'Ascension et de la Pentecôte sont recalculées chaque année.
- Correction : le capteur utilise désormais `get_device_info()` (version et lien du dépôt à jour), au lieu d'informations d'appareil obsolètes.


## 1.2.8 - 2026-11-07

- Nettoyage suite à la revue de Frenck : suppression de la déclaration et de la documentation du service obsolète `jourferier.create_card`, déjà retiré du code.
- README : alignement de la version affichée sur la release actuelle 1.2.7.

## 1.2.6

- fix(i18n): état sensor `aucun` en minuscules (hassfest)
- i18n: compléter en.json et strings.json

## 1.2.5 - 2026-10-31

### Ajouté
- Carte Lovelace native **Jours fériés** (`custom:jour-ferie-card`) livrée avec l'intégration :
  - ressource JS servie sur `/jourferier/jour-ferie-card.js` et enregistrée automatiquement dans Lovelace ;
  - éditeur visuel (`getConfigForm`) : sélecteur de capteur et titre, libellés en français ;
  - affiche le jour férié du jour (ou « Aujourd'hui, pas de jour férié. ») et le prochain jour férié avec le nombre de jours.
- Rectificatif : le service `jourferier.create_card` avait déjà été retiré du code ; utiliser les exemples de cartes ou la carte Lovelace native.

## 1.2.4
- Docs : badge téléchargements cumulés.
