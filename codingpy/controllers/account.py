#!usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request)
from flask.ext.login import login_user, logout_user, \
    login_required

from ..ext import db
from ..models import User
from ..forms import LoginForm, RegistrationForm

bp = Blueprint('account', __name__)


@bp.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            user.ping()
            return redirect(request.args.get('next') or '/')
        redirect('/')
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('/'))


@bp.route('/register/', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # send_email(user.email, 'Confirm Your Account',
        #            'email/confirm', user=user, token=token)
        # flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('account.login'))
    return render_template('register.html', form=form)
