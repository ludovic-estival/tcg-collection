# An application to manage a card collection

## Description:

The goal of this app is to manage a card collection, no matter the game (YGO, MTG, ...).

## Features:

- Add cards (one by one and in bulk via a CSV file) :white_check_mark:
- Update card information :white_check_mark:
- Delete a card :white_check_mark:
- Calculation of collection value :white_check_mark:
- Show card image
- Sort cards by card attributes in ascending/descending order
- Track price of valuable or selected cards
- Show evolution of prices for the collection and individual cards
- Adapt the app to support all TCG via a settings file

## Usefull commands:
- Install Flask: `pip install Flask`
- Test libraries: `pip install pytest coverage`
- Create database (from `flaskr` folder): `flask --app flaskr init-db`
- Start local server (from `flaskr` folder): `flask --app flaskr run --debug`

## Folders:
- `flask-app`: Flask project
- `price-tracker`: Experimental scripts to track collection price
