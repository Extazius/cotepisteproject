from app import app, db, Product

with app.app_context():
    # On vide la table pour éviter les doublons lors des tests
    db.drop_all()
    db.create_all()

    # Création de produits fictifs
    p1 = Product(
        name="Chaussures de Piste Pro",
        slug="chaussures-piste-pro", # IMPORTANT : Pas d'espaces, pas d'accents
        price=129.99,
        description="Les meilleures chaussures pour la compétition. Adhérence maximale."
    )
    p2 = Product(
        name="Casque Aérodynamique",
        slug="casque-aerodynamique-v2",
        price=89.50,
        description="Gagnez de la vitesse avec ce casque ultra-léger."
    )

    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()
    print("Produits ajoutés avec succès !")
