# app.py
from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Chemin du fichier CSV
data_file = os.path.join(os.path.dirname(__file__), 'data/ProductVendorr.csv')

# Fonction pour analyser les données
def analyse_data():
    # Charger les données
    data = pd.read_csv(data_file, sep=';')

    # Analyse des données par fournisseur
    supplier_stats = data.groupby('VendorID').agg(
        orders_count=('Product_ID', 'count'),
        total_quantity=('Quantity', 'sum'),
        total_price=('Price', 'sum')
    ).reset_index()

    # Ajouter une colonne pour le chiffre d'affaires total (revenu)
    supplier_stats['total_revenue'] = data.groupby('VendorID').apply(lambda x: (x['Price'] * x['Quantity']).sum()).values

    # Créer les graphiques et les sauvegarder dans le dossier 'static'
    save_charts(supplier_stats)
    return supplier_stats

# Fonction pour sauvegarder les graphiques
def save_charts(supplier_stats):
    # Visualisation 1 : Nombre de commandes par fournisseur
    plt.figure(figsize=(10,6))
    plt.bar(supplier_stats['VendorID'], supplier_stats['orders_count'], color='skyblue')
    plt.xlabel('Vendor ID')
    plt.ylabel('Number of Orders')
    plt.title('Number of Orders by Supplier')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join('static', 'number_of_orders_by_supplier.png'))

    # Visualisation 2 : Quantité totale commandée par fournisseur
    plt.figure(figsize=(10,6))
    plt.bar(supplier_stats['VendorID'], supplier_stats['total_quantity'], color='lightgreen')
    plt.xlabel('Vendor ID')
    plt.ylabel('Total Quantity Ordered')
    plt.title('Total Quantity Ordered by Supplier')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join('static', 'total_quantity_by_supplier.png'))

    # Visualisation 3 : Prix total par fournisseur
    plt.figure(figsize=(10,6))
    plt.bar(supplier_stats['VendorID'], supplier_stats['total_price'], color='salmon')
    plt.xlabel('Vendor ID')
    plt.ylabel('Total Price')
    plt.title('Total Price by Supplier')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join('static', 'total_price_by_supplier.png'))

    # Visualisation 4 : Chiffre d'affaires par fournisseur
    plt.figure(figsize=(10,6))
    plt.bar(supplier_stats['VendorID'], supplier_stats['total_revenue'], color='gold')
    plt.xlabel('Vendor ID')
    plt.ylabel('Total Revenue')
    plt.title('Total Revenue by Supplier')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join('static', 'total_revenue_by_supplier.png'))

@app.route('/')
def index():
    # Effectuer l'analyse des données
    supplier_stats = analyse_data()

    # Afficher les résultats dans la page HTML
    return render_template('index.html', supplier_stats=supplier_stats)

if __name__ == '__main__':
    app.run(debug=True)
