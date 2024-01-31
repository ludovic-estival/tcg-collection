# An application to manage a card collection

## Description:

The goal of this app is to manage a card collection, no matter the game (YGO, MTG, ...).

## Implemented features:

- Add cards (one by one and in bulk via a CSV file)
- Update card information
- Delete a card
- Calculation of collection value

## Next features:

- Show card image
- Sort cards by name, rarity, ... in ascending/descending order

## Usefull commands:
- Install Flask: `pip install Flask`
- Create database (from `flaskr` folder): `flask --app flaskr init-db`
- Start local server (from `flaskr` folder): `flask --app flaskr run --debug`

## Folders:
- `flask-app`: Flask project
- `price-tracker`: Experimental scripts to track collection price
