from datetime import datetime

from flask import abort, flash, make_response, request
from flask import redirect, render_template, session, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    
    return render_template('index.html',
                            current_time=datetime.utcnow(),
                            name=session.get('name'),
                            form=form,
                            known=session.get('known', False))