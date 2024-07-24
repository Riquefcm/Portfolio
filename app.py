from flask import Flask, render_template, request, redirect, url_for
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Carrega os dados dos projetos a partir do arquivo JSON
def load_projects():
    with open('projects.json', 'r') as f:
        projects = json.load(f)
    return projects

# Rota inicial para a página principal
@app.route('/')
def index():
    projects = load_projects()
    return render_template('index.html', projects=projects)

# Rota para enviar e-mail pelo formulário de contato
@app.route('/enviar_email', methods=['POST'])
def enviar_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Configurações para enviar e-mail
    sender_email = 'seu_email@gmail.com'  # substitua pelo seu e-mail
    receiver_email = 'enrique.calza72@gmail.com'  # substitua pelo e-mail do destinatário
    password = 'sua_senha'  # substitua pela senha do seu e-mail

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = receiver_email
    msg['Subject'] = 'Mensagem do formulário de contato'

    body = f'Nome: {name}\nEmail: {email}\nMensagem:\n{message}'
    msg.attach(MIMEText(body, 'plain'))

    # Enviar e-mail usando SMTP
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return redirect(url_for('index') + '#contato')
    except Exception as e:
        return f'Erro ao enviar e-mail: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
