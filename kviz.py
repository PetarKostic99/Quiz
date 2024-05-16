from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:petarkostic123@localhost/testovi_db'
db = SQLAlchemy(app)

# Modeli za sve tabele
class OpsteZnanje(db.Model):
    __tablename__ = 'opste_znanje'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)

class Sport(db.Model):
    __tablename__ = 'sport'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)

class Igre(db.Model):
    __tablename__ = 'igrice'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)

class Filmovi(db.Model):
    __tablename__ = 'filmovi'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)

class Istorija(db.Model):
    __tablename__ = 'istorija'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)

class TacniOdgovori(db.Model):
    __tablename__ = 'tacni_odgovori'
    id = db.Column(db.Integer, primary_key=True)
    pitanje_id = db.Column(db.Integer, nullable=False)
    odgovor = db.Column(db.String(100), nullable=False)

# Početna ruta - izbor oblasti
@app.route('/')
def index():
    return render_template('index.html')

# Ruta za odabir oblasti iz dropdown liste
@app.route('/odabir_oblasti', methods=['GET'])
def odabir_oblasti():
    oblast = request.args.get('oblast')
    return redirect(f'/pitanja/{oblast}')

@app.route('/pitanja/<oblast>')
def pitanja(oblast):
    # Izaberi tabelu na osnovu izabrane oblasti
    tabela = None
    if oblast == 'opste_znanje':
        tabela = OpsteZnanje
    elif oblast == 'sport':
        tabela = Sport
    elif oblast == 'igrice':
        tabela = Igre
    elif oblast == 'filmovi':
        tabela = Filmovi
    elif oblast == 'istorija':
        tabela = Istorija

    # Očisti prethodne odgovore za trenutni pokušaj
    TacniOdgovori.query.delete()

    # Izvuci 3 nasumična pitanja iz odabrane tabele
    if tabela:
        pitanja = tabela.query.order_by(func.rand()).limit(3).all()
        
        # Izračunaj sledeći ID za tabelu TacniOdgovori
        max_id = db.session.query(db.func.max(TacniOdgovori.id)).scalar()
        next_id = (max_id or 0) + 1

        # Upisivanje tacnih odgovora u tabelu TacniOdgovori
        for pitanje in pitanja:
            tacan_odgovor = TacniOdgovori(id=next_id, pitanje_id=pitanje.id, odgovor=pitanje.correct_answer)
            db.session.add(tacan_odgovor)
            next_id += 1
        db.session.commit()

        return render_template('pitanja.html', pitanja=pitanja, oblast=oblast)
    else:
        return 'Oblast nije pronađena'

# Ruta za proveru odgovora
@app.route('/proveri_odgovore', methods=['POST'])
def proveri_odgovore():
    # Dobijanje odgovora od korisnika iz forme
    odgovori = request.form

    # Dobijanje oblasti iz URL-a
    oblast = request.referrer.split('/')[-1]
    niz1=[]
    niz2=[]

    # Prikaz unetih odgovora
    first = True  # Flag za praćenje prvog prolaska kroz petlju
    for pitanje_id, uneti_odgovor in odgovori.items():
        if not first:  # Preskače prvi prolazak kroz petlju
            print(f"Pitanje ID: {pitanje_id}, Uneti odgovor: {uneti_odgovor}")
            niz1.append(uneti_odgovor.lower())
        else:
            first = False


    # Izvlačenje svih tacnih odgovora iz tabele TacniOdgovori
    tacni_odgovori_db = TacniOdgovori.query.all()
    
    # Prikaz svih tacnih odgovora
    for tacan_odgovor in tacni_odgovori_db:
        print(f"Pitanje ID: {tacan_odgovor.pitanje_id}, Tacan odgovor: {tacan_odgovor.odgovor}")
        niz2.append(tacan_odgovor.odgovor)
    niz2 = [( odg.lower()) for odg in niz2]
    print(niz1)
    print(niz2) 
        # Provera odgovora
   # Inicijalizacija brojača za tačne odgovore
    tacni_odgovori = 0

    # Upoređivanje elemenata oba niza
    for odgovor1, odgovor2 in zip(niz1, niz2):
        if odgovor1 == odgovor2:
            tacni_odgovori += 1

    return f'Vaš rezultat je {tacni_odgovori} od 3.'


if __name__ == '__main__':
    app.run(debug=True)
