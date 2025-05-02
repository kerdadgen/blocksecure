from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
import pandas as pd
import pickle
import os
from werkzeug.utils import secure_filename
from sklearn.preprocessing import PowerTransformer


# --- Initialisation ---
app = Flask(__name__, template_folder='../templates')
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# --- Connexion MongoDB ---
client = MongoClient("mongodb://localhost:27017/")
db = client["blocksecure_db"]
prod_collection = db["prod"]

# --- Charger modèle ---
with open('models/XGB_FRAUD.pickle', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_predict', methods=['POST'])
def upload_predict():
    if 'file' not in request.files:
        return jsonify({"message": "Aucun fichier trouvé"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "Nom de fichier vide"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        # Lire CSV
        df = pd.read_csv(filepath)
        x = df['Index']
        # Supprimer anciens documents et insérer nouveaux
        db.prod.delete_many({})
        db.prod.insert_many(df.to_dict(orient='records'))

        # Lire depuis MongoDB
        cursor = db.prod.find()
        df_prod = pd.DataFrame(list(cursor)).drop(columns=['_id'])
        df_prod = df_prod.iloc[:,3:]

        # Pré-traitement
        

        drop_columns = ['total transactions (including tnx to create contract', 'total ether sent contracts', 'max val sent to contract', ' ERC20 avg val rec',
                ' ERC20 avg val rec',' ERC20 max val rec', ' ERC20 min val rec', ' ERC20 uniq rec contract addr', 'max val sent', ' ERC20 avg val sent',
                ' ERC20 min val sent', ' ERC20 max val sent', ' Total ERC20 tnxs', 'avg value sent to contract', 'Unique Sent To Addresses',
                'Unique Received From Addresses', 'total ether received', ' ERC20 uniq sent token name', 'min value received', 'min val sent', ' ERC20 uniq rec addr' ]


        df_prod.drop(columns=[col for col in drop_columns if col in df_prod.columns], inplace=True, errors='ignore')
        drops = ['min value sent to contract', ' ERC20 uniq sent addr.1']
        df_prod.drop(drops, axis=1, inplace=True)
        drops = [' ERC20 avg time between sent tnx', ' ERC20 avg time between rec tnx', ' ERC20 avg time between rec 2 tnx', ' ERC20 avg time between contract tnx', ' ERC20 min val sent contract', ' ERC20 max val sent contract', ' ERC20 avg val sent contract', ' ERC20 most sent token type', ' ERC20_most_rec_token_type']
        df_prod.drop(drops, axis=1, inplace=True)
        # Remplir les valeurs manquantes
        for col in [' ERC20 uniq rec token name', ' ERC20 uniq sent addr', ' ERC20 total ether sent', ' ERC20 total Ether received', ' ERC20 total Ether sent contract']:
            if col in df_prod.columns:
                df_prod[col] = df_prod[col].fillna(0)
        
        # Préparation des features
        X_prod = df_prod
        # Normalize
        norm = PowerTransformer()
        norm_train_f = norm.fit_transform(X_prod)
        X_prod = pd.DataFrame(norm_train_f, columns=X_prod.columns)
        
        # Prédiction
        predictions = model.predict(X_prod)

        # Ajouter prédictions
        df_prod['prediction'] = predictions
        df_prod['Id'] = df['Index']

        # Convertir en JSON pour affichage
        results = df_prod.to_dict(orient='records')

        return render_template('results.html', tables=[df_prod.to_html(classes='data')], results=results)

    except Exception as e:
        return jsonify({"message": f"Erreur : {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

