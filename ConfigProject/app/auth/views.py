# -*- coding: utf-8 -*-
#! /usr/bin/env python

from flask import  render_template,redirect,request,url_for,flash
from  flask_login import login_user,login_required,logout_user,current_user

from app import db
from  . import auth
from ..email import send_email
from ..models import User
from .forms import LoginForm,RegistrationForm



@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名或密码错误!')
    return render_template('auth/login.html',
                           form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已经成功退出！')
    return redirect(url_for('main.index'))

@auth.route('/secret')
@login_required
def secret():
    return u'您为登陆，请登录！'

@auth.route('/register',methods=['POST','GET'])
def register():
    form = RegistrationForm(csrf_enabled=False)
    if form.validate_on_submit():
       user = User(email=form.eamil.data,
                   username = form.username.data,
                   password = form.password.data)
       db.session.add(user)
       # db.session.commit()
       # token = user.generate_confirmation_token()
       # send_email(user.email,u'请确认是否是您注册的',
       #            'auth/email/confirm',
       #            user=user,
       #            token=token)
       # flash(u'确认邮箱已经发送到您的邮件里面，请查收！')
       # return  redirect(url_for('main.index'))
       flash(u'注册成功可以登陆!')
       return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

# @auth.route('/confirm/<token>')
# @login_required
# def confirm(token):
#     if current_user.confirmed:
#         return redirect(url_for('main.index'))
#     if current_user.confirm(token):
#         flash(u'您的账户已确认，谢谢！')
#     else:
#         flash(u'您的帐号未确认，请重新确认！')
#     return redirect(url_for('mail.index'))

# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         # current_user.ping()
#         if not current_user.confirmed \
#                 and request.endpoint[:5] != 'auth.' \
#                 and request.endpoint != 'static':
#             return redirect(url_for('auth.unconfirmed'))
#
# @auth.route('/unconfirmed')
# def unconfirmed():
#     if current_user.is_anonymous() or current_user.confirmed:
#         return redirect(url_for('main.index'))
#     return render_template('auth/unconfirmed.html')

# @auth.route('/confirm')
# @login_required
# def resend_confirmation():
#     token = current_user.generate_confirmation_token()
#     send_email(current_user.email,u'请确认你的帐号！',
#                'auth/email/confirm',user=current_user,
#                token=token)
#     flash(u'新的确认邮件已经发送的您的邮箱，请您查收下！')
#     return redirect(url_for('main.index'))