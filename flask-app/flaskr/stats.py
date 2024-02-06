from flask import (
    Blueprint, render_template
)

from flaskr.db import get_db

bp = Blueprint('stats', __name__)


@bp.route('/stats')
def index():
    rarities = get_db().execute('SELECT code FROM rarity')
    labels = []
    data = []
    
    for rarity in rarities:
        cards_count = get_db().execute('SELECT COUNT(code) as number FROM card WHERE rarity = ?', rarity).fetchone()
        labels.append(rarity["code"])
        data.append(cards_count["number"])
        
    return render_template('stats.html', labels=labels, data=data)
