from flask import Flask, render_template, request, redirect, url_for
import json
import re

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# Vytvořte seznam pro ukládání registračních údajů a set pro ukládání registrovaných společníků
registroavni_ucastnici = []
registered_companions = set()
registered_nicknames = set()
registered_emails = set()

data_file = 'registration_data.json'  # Soubor JSON pro ukládání registračních údajů

# Načtěte existující recenze ze souboru JSON (pokud existuje)
reviews = []
reviews_file = 'reviews.json'

try:
    with open(reviews_file, 'r', encoding='utf-8') as json_file:
        reviews = json.load(json_file)
except FileNotFoundError:
    pass

# Načtěte existující údaje ze souboru JSON (pokud existuje)
try:
    with open(data_file, 'r') as json_file:
        registroavni_ucastnici = json.load(json_file)
        for participant in registroavni_ucastnici:
            registered_nicknames.add(participant['nickname'])
            registered_emails.add(participant['email'])
            registered_companions.add(participant['canoe_companion'])
except FileNotFoundError:
    pass


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', participants=registroavni_ucastnici, reviews=reviews)


def save_data_to_json():
    with open(data_file, 'w') as json_file:
        json.dump(registroavni_ucastnici, json_file)


def save_reviews_to_json():
    with open(reviews_file, 'w', encoding='utf-8') as json_file:
        json.dump(reviews, json_file, ensure_ascii=False, indent=4)


def send_email(receiver_email, user_data):
    global server
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Konfigurace e-mailu
    sender_email = 'wolfvodackykurz@gmail.com'
    app_password = 'pucp kzte ttof trhz'
    subject = 'Nový uživatel'
    message = f"""
    Dobrý den,

    Děkujeme vám za registraci do naší události.

    Vaše registrace byla úspěšně zaznamenána. Zde jsou vaše údaje:
    Jméno: {user_data['name']}
    Příjmení: {user_data['last_name']}
    Přezdívka: {user_data['nickname']}
    Třída: {user_data['class_name']}
    Email: {user_data['email']}

    Těšíme se na vaši účast a doufáme, že si událost užijete naplno.

    S pozdravem,
    Tým Wolfvodackykurz
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)

        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email byl úspěšně odeslán!')
    except Exception as e:
        print(f'Chyba: {e}')
    finally:
        server.quit()


@app.route('/classes', methods=['GET', 'POST'])
def users_by_class():
    if request.method == 'POST':
        selected_class = request.form.get('class')

        # Filtrujte účastníky podle vybrané třídy
        filtered_participants = [participant for participant in registroavni_ucastnici if
                                 participant['class_name'] == selected_class]

        return render_template('classes.html', filtered_participants=filtered_participants)
    else:
        # Pokud jde o GET požadavek, prostě zobrazte stránku filtru
        return render_template('classes.html', filtered_participants=[])


@app.route('/check_swimmer', methods=['POST'])
def check_swimmer():
    je_plavec = int(request.form.get('je_plavec'))

    if je_plavec == 0:
        return 'invalid', 200
    else:
        return 'valid', 200

@app.route('/check_companion', methods=['POST'])
def check_companion():
    kanoe_kamarad = request.form.get('kanoe_kamarad')

    # Zkontrolujte, zda zadaná přezdívka je již registrována
    if kanoe_kamarad:
        if kanoe_kamarad in registered_companions:
            return "True", 200  # Vraťte "True" pro "obsazeno"
        elif kanoe_kamarad not in [participant['nickname'] for participant in registroavni_ucastnici]:
            return "False", 200  # Vraťte "False" pro "neplatný"
        else:
            for participant in registroavni_ucastnici:
                if participant['nickname'] == kanoe_kamarad and participant['canoe_companion']:
                    return "Invalid", 200
            return "available", 200

@app.route('/check_last_name', methods=['POST'])
def check_last_name():
    last_name = request.form.get('last_name')

    valid_name_pattern = r"^[A-Za-záčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ ]+$"

    if not re.match(valid_name_pattern, last_name):
        return "invalid", 200

    if len(last_name) < 2:
        return "short", 200

    if len(last_name) > 30:
        return "long", 200

    return "valid", 200

@app.route('/check_name', methods=['POST'])
def check_name():
    name = request.form.get('name')

    # Definujte regulární výraz pro platná jména (pouze písmena a mezery)
    valid_name_pattern = r"^[A-Za-záčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ ]+$"


    # Zkontrolujte, zda jméno a příjmení obsahují speciální znaky
    if not re.match(valid_name_pattern, name):
        return "invalid", 200

    # Zkontrolujte, zda jméno a příjmení mají délku od 2 do 30 znaků
    if len(name) < 2  :
        return "short", 200

    if len(name) > 30:
        return "long", 200

    return "valid", 200

@app.route('/check_nickname', methods=['POST'])
def check_nickname():
    nickname = request.form.get('nickname')

    # Zkontrolujte, zda zadaná přezdívka je již registrována
    if nickname in registered_nicknames:
        return "taken", 200

    # Zkontrolujte, zda přezdívka obsahuje speciální znaky
    if not re.match(r'^[A-Za-z0-9_]+$', nickname):
        return "invalid", 200

    # Zkontrolujte, zda je přezdívka dlouhá 2 až 20 znaků
    if len(nickname) < 2 :
        return "short", 200

    if len(nickname) > 20:
        return "long", 200

    return "available", 200

@app.route('/check_email', methods=['POST'])
def check_email():
    email = request.form.get('email')

    # Zkontrolujte, zda zadaný e-mail je již registrován
    if email in registered_emails:
        return "taken", 200
    else:
        # Ověřte formát e-mailu pomocí regulárního výrazu
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}$'
        if not re.match(email_pattern, email):
            return "invalid", 200
        else:
            return "available", 200

@app.route('/registrace', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        nickname = request.form['nick']
        is_swimmer = request.form['je_plavec']
        canoe_companion = request.form['kanoe_kamarad']
        class_name = request.form['class']
        name = request.form['name']
        last_name = request.form['last_name']
        email = request.form['email']

        # Zkontrolujte, zda zadaná přezdívka je již registrována
        if nickname in registered_nicknames:
            return "Chyba: Tato přezdívka již byla zaregistrována.", 400

        if any(participant['email'] == email for participant in registroavni_ucastnici):
            return "Chyba: Tato emailová adresa již byla zaregistrována.", 400

        # Ověřte pole jména pomocí regulárního výrazu
        name_pattern = r"^[A-Za-záčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ ]+$"
        if not re.match(name_pattern, name):
            return "Chyba: Jméno obsahuje neplatné znaky.", 400

        if not re.match(name_pattern, nickname):
            return "Chyba: Přezdívka obsahuje neplatné znaky.", 400

        if not re.match(name_pattern, last_name):
            return "Chyba: Příjmení obsahuje neplatné znaky.", 400

        # Zkontrolujte, zda zadaný společník v kánoi je registrován
        if canoe_companion:
            if canoe_companion not in [participant['nickname'] for participant in registroavni_ucastnici]:
                return "Chyba: Společník na lodi není registrován.", 400

            if canoe_companion in registered_companions:
                return "Chyba: Společník na lodi byl již vybrán jiným účastníkem.", 400
            else:
                registered_companions.add(canoe_companion)

                # Zkontrolujte, zda vybraný společník již má svého vlastního společníka
        for participant in registroavni_ucastnici:
                if participant['nickname'] == canoe_companion and participant['canoe_companion']:
                    return "Chyba: Tento společník na lodi již má vlastního společníka.", 400

        # Pokud projdou všechny kontroly, uložte registrační údaje do registroavni_ucastnici a aktualizujte registered_nicknames
        registration_data = {
            'name': name,
            'last_name': last_name,
            'nickname': nickname,
            'is_swimmer': is_swimmer,
            'canoe_companion': canoe_companion,
            'class_name': class_name,
            'email': email
        }
        registroavni_ucastnici.append(registration_data)
        registered_nicknames.add(nickname)
        registered_emails.add(email)
        save_data_to_json()  # Uložit data do souboru JSON

        send_email(email, registration_data)

    return render_template('registration.html'), 200

@app.route('/recenze', methods=['POST', 'GET'])
def add_review():
    if request.method == 'POST':
        nickname = request.form.get('nickname')

        if nickname not in registered_nicknames:
            return "Pouze registrovaní uživatelé mohou psát recenze.", 400

        review = request.form.get('review')
        if not review:
            return redirect(url_for('index'))

        # Apply character limit and filter cuss words
        review = review[:200]
        cuss_words = ["kurva", "piča", "píča", "hovno", "prdel", "prdeli", "hovna",
                      "prdele", "kurvy", "debil", "kokot", "kretén"]  # Add your cuss words
        for word in cuss_words:
            review = re.sub(fr'\b{re.escape(word)}\b', '***', review, flags=re.IGNORECASE)

        reviews.append(f"({nickname}): {review}")
        save_reviews_to_json()

    return render_template('feedback.html', reviews=reviews), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030)
