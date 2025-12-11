import os
from flask import Flask, render_template
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1. CONFIGURATION DE LA BDD
# On récupère l'URL de la base de données fournie par Heroku
# Si on est en local, on utilisera une base SQLite temporaire pour tester
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local_shop.db')
# Petit fix car Heroku utilise "postgres://" et SQLAlchemy veut "postgresql://"
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation des extensions
Compress(app)
db = SQLAlchemy(app)

# 2. LE MODÈLE DE DONNÉES (Table Produits)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)     # Nom du produit (H1)
    slug = db.Column(db.String(100), unique=True, nullable=False) # L'URL SEO (ex: mon-produit)
    price = db.Column(db.Float, nullable=False)          # Prix pour Google Schema
    description = db.Column(db.Text, nullable=True)      # Description longue
    image_url = db.Column(db.String(200), nullable=True) # Image principale

    def __repr__(self):
        return f'<Product {self.name}>'

# 3. CRÉATION DE LA BDD (Une seule fois au démarrage si elle n'existe pas)
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def home():
    # On récupère tous les produits de la base de données
    products = Product.query.all()
    
    seo_data = {
        "title": "Boutique Cote Piste | Accueil",
        "description": "Les meilleurs produits...",
        "canonical": "https://cotepisteproject-shop.herokuapp.com/",
        # VOICI LA PARTIE QUI MANQUAIT :
        "json_ld": {
            "@context": "https://schema.org",
            "@type": "Store",
            "name": "Cote Piste Project",
            "url": "https://cotepisteproject-shop.herokuapp.com/",
            "description": "La référence pour vos équipements."
        }
    }
    # On passe la liste des produits au HTML
    return render_template('index.html', seo=seo_data, products=products)

# Route Produit (SEO Friendly)
@app.route('/produit/<slug>')
def product_detail(slug):
    # On cherche le produit qui correspond au "slug" dans l'URL
    product = Product.query.filter_by(slug=slug).first_or_404()
    
    seo_data = {
        "title": f"{product.name} | Cote Piste", # Titre dynamique
        "description": product.description[:160], # Meta description (160 premiers caractères)
        "canonical": f"https://cotepisteproject-shop.herokuapp.com/produit/{slug}"
    }
    return render_template('product.html', seo=seo_data, product=product)

if __name__ == '__main__':
    app.run(debug=True)
