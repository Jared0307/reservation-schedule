from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, jsonify
from flask_sqlalchemy import SQLAlchemy#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import func
from datetime import datetime#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
from flask_mail import Mail, Message

import os
#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com

app.config['MAIL_SERVER'] = 'smtp-jared.com'  # Cambia según el servidor de correo
app.config['MAIL_PORT'] = 587  #Cambia según el puertp
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'jared@jared.com'  # Tu correo electrónico
app.config['MAIL_PASSWORD'] = 'jared123456789'  # Tu contraseña o token
app.config['MAIL_DEFAULT_SENDER'] = 'jared@jared.com'  # Remitente por defecto
mail = Mail(app)

login_manager = LoginManager(app)#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
    is_admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    def __repr__(self):
        return f'<User {self.username}>'
#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 
    approved_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='reservations', foreign_keys=[user_id])
    approved_by = db.relationship('User', foreign_keys=[approved_by_id])#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com

    def __repr__(self):
        return f'<Reservation {self.id} - {self.date} {self.time}>'


@login_manager.user_loader#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com

        if user and user.password == password:
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin'))
            else:#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
                return redirect(url_for('calendar'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/admin')#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
@login_required
def admin():#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
    if not current_user.is_admin:
        return redirect(url_for('calendar'))
    return render_template('admin.html')

@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        return redirect(url_for('calendar'))#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = 'is_admin' in request.form
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
            flash('El usuario ya existe', 'danger')
            return redirect(url_for('create_user'))
        new_user = User(username=username, password=password, is_admin=is_admin)
        db.session.add(new_user)#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
        db.session.commit()

        flash(f"Usuario '{username}' creado exitosamente.", 'success')
        return redirect(url_for('admin'))#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
    return render_template('create_user.html')

@app.route('/calendar')#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
@login_required
def calendar():
    if current_user.is_admin:
        return redirect(url_for('admin'))#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
    return render_template('calendar.html')
#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
@app.route('/get_reservations/<date>', methods=['GET'])
def get_reservations(date):
    reservations = Reservation.query.filter_by(date=date, approved=True).all()
    print(f"Fecha recibida: {date}")
    print(f"Reservas encontradas: {len(reservations)}")#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
    return jsonify([{
        'time': reservation.time,
        'user': {'username': reservation.user.username}
    } for reservation in reservations])
#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
@app.route('/reserve', methods=['POST'])
@login_required
def reserve():
    data = request.get_json()
    date = data.get('date')
    time = data.get('time')
    existing_reservation = Reservation.query.filter_by(date=date, time=time, approved=True).first()
    if existing_reservation:#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
        return jsonify({'success': False, 'message': 'La hora ya está reservada.'})
    new_reservation = Reservation(user_id=current_user.id, date=date, time=time, approved=False)#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
    db.session.add(new_reservation)
    db.session.commit()
    user = User.query.get(current_user.id)
    msg_user = Message("Confirmación de Solicitud de Reserva",
                       recipients=[user.email])
    msg_user.body = f"Hola {user.username},\n\nTu solicitud de reserva para el {date} a las {time} ha sido recibida. Estaremos revisando tu solicitud pronto.\n\n¡Gracias!"
    mail.send(msg_user)
    admin_users = User.query.filter_by(is_admin=True).all()
    for admin in admin_users:#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
        msg_admin = Message("Nueva Solicitud de Reserva",
                            recipients=[admin.email])
        msg_admin.body = f"Hola {admin.username},\n\nSe ha solicitado una nueva reserva para el {date} a las {time}.\n\nRevisa el sistema para más detalles."
        mail.send(msg_admin)
    return jsonify({'success': True, 'message': 'Reserva solicitada con éxito, se ha enviado un correo de confirmación.'})
#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com

@app.route('/logout')
@login_required
def logout():
    logout_user()#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('index.html')#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com

@app.route('/manage_reservations')
@login_required
def manage_reservations():
    if not current_user.is_admin:
        return redirect(url_for('calendar'))
    
    today = datetime.today().strftime('%Y-%m-%d')#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
    print(f"Fecha de hoy: {today}")
    today_formatted = datetime.today().strftime('%Y-%m-%d').replace('-0', '-')
    latest_date = db.session.query(func.max(Reservation.date)).filter(Reservation.approved == True).scalar()
    print(f"Fecha más reciente de reservas aprobadas: {latest_date}")
    approved_today = Reservation.query.filter(
        Reservation.approved == True,
        Reservation.date == today_formatted
    ).all()#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
    print(f"Reservas aprobadas hoy: {approved_today}")
    pending_reservations = Reservation.query.filter_by(approved=False).all()
    return render_template('manage_reservations.html', 
                           reservations=pending_reservations,
                           approved_today=approved_today)
#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
@app.route('/approve_reservation/<int:id>')
@login_required
def approve_reservation(id):#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
    if not current_user.is_admin:
        return redirect(url_for('calendar'))
    reservation = Reservation.query.get_or_404(id)
    reservation.approved = True
    reservation.approved_by_id = current_user.id
    db.session.commit()
    user = reservation.user#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
    msg_user = Message("Reserva Aprobada",
                       recipients=[user.email])
    msg_user.body = f"Hola {user.username},\n\nTu reserva para el {reservation.date} a las {reservation.time} ha sido aprobada. ¡Nos vemos pronto!\n\n¡Gracias!"
    mail.send(msg_user)
    flash('Reserva aprobada correctamente.', 'success')
    return redirect(url_for('manage_reservations'))#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com

@app.route('/deny_reservation/<int:id>')
@login_required
def deny_reservation(id):
    if not current_user.is_admin:
        return redirect(url_for('calendar'))
    reservation = Reservation.query.get_or_404(id)
    user = reservation.user
    db.session.delete(reservation)#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
    db.session.commit()
    msg_user = Message("Reserva Denegada",
                       recipients=[user.email])
    msg_user.body = f"Hola {user.username},\n\nLamentablemente, tu solicitud de reserva para el {reservation.date} a las {reservation.time} ha sido denegada. Por favor, intenta con otro horario.\n\n¡Gracias!"
    mail.send(msg_user)
    flash('Reserva denegada y eliminada correctamente.', 'success')
    return redirect(url_for('manage_reservations'))
#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
#Hecho por Jared0307 jaredrodriguez0307@gmail.com jar3d.atwebpages.com