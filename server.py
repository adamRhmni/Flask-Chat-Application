# this was made by Adam rhmni
# contect me if you wanna make it better
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)
socketio = SocketIO(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
@login_required
def index():
    return render_template('chat.html')  # Serve the chat HTML file

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # In production, use hashed passwords
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! You can now log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Store connected users and messages
connected_users = {}
messages = []  # List to store chat messages

@socketio.on('join')
def handle_join(data):
    user_name = current_user.username  # Get the username from the current user
    connected_users[request.sid] = user_name  # Store the user with their session ID
    emit('receive_message', {'user': 'System', 'message': f'{user_name} has joined the chat.'}, broadcast=True)

    # Send existing messages to the new user
    for message in messages:
        emit('receive_message', message)  # Send each message to the new user

@socketio.on('send_message')
def handle_message(data):
    messages.append(data)  # Store the message
    emit('receive_message', data, broadcast=True)  # Broadcast the message to all clients

@socketio.on('disconnect')
def handle_disconnect():
    user_name = connected_users.pop(request.sid, None)  # Remove user from connected users
    if user_name:
        emit('receive_message', {'user': 'System', 'message': f'{user_name} has left the chat.'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)  # This line can be ignored when using Gunicorn
#                                   change the port here to use it 