from flask import (
    Blueprint, render_template
)

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('stats', __name__)


@bp.route('/stats')
@login_required
def index():
    rarities = get_db().execute('SELECT code FROM rarity')
    labels = []
    data = []
    
    for rarity in rarities:
        cards_count = get_db().execute('SELECT COUNT(cardCode) AS number FROM contain WHERE rarity = ?', rarity).fetchone()
        labels.append(rarity["code"])
        data.append(cards_count["number"])
        
    return render_template('stats.html', labels=labels, data=data)
