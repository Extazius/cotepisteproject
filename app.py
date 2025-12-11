# Fichier: app.py
from flask import Flask, render_template
from flask_compress import Compress

app = Flask(__name__)

# OPTIMISATION SEO TECHNIQUE : Activation de la compression Gzip/Brotli
# Réduit la taille des fichiers envoyés au navigateur jusqu'à 70%
Compress(app)

@app.route('/')
def home():
    # Données dynamiques pour le SEO (Simulées pour l'instant)
    seo_data = {
        "title": "Boutique en Ligne Optimisée | Cote Piste Project",
        "description": "Découvrez nos produits exclusifs. Livraison rapide et qualité supérieure. Le meilleur équipement pour...",
        "canonical": "https://cotepisteproject-shop.herokuapp.com/",
        "json_ld": {
            "@context": "https://schema.org",
            "@type": "Store",
            "name": "Cote Piste Project",
            "url": "https://cotepisteproject-shop.herokuapp.com/",
            "description": "La référence pour vos équipements."
        }
    }
    return render_template('index.html', seo=seo_data)

if __name__ == '__main__':
    app.run(debug=True)
