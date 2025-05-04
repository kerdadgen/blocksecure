from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
import pandas as pd
import pickle
import os
from werkzeug.utils import secure_filename
from analysis import DataPreprocessor

# initialisation
app = Flask(__name__, template_folder='../templates')
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["blocksecure_db"]
prod_collection = db["prod"]

# charger modèle
with open('models/XGB_FRAUD.pickle', 'rb') as f:
    model = pickle.load(f)

# initialiser pretraitement
preprocessor = DataPreprocessor()

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

        # Nettoyer MongoDB
        db.prod.delete_many({})
        db.prod.insert_many(df.to_dict(orient='records'))

        # Lire depuis MongoDB
        cursor = db.prod.find()
        df_prod = pd.DataFrame(list(cursor)).drop(columns=['_id'])
        df_prod = df_prod.iloc[:, 3:]

        # Prétraitement
        df_cleaned = preprocessor.clean_data(df_prod)
        X_prod = preprocessor.transform(df_cleaned)

        # Prédiction
        predictions = model.predict(X_prod)

        # Ajouter prédictions
        df_cleaned['prediction'] = predictions
        df_cleaned['Id'] = df['Index']

        # Convertir en JSON
        results = df_cleaned.to_dict(orient='records')

        return render_template('results.html', tables=[df_cleaned.to_html(classes='data')], results=results)

    except Exception as e:
        return jsonify({"message": f"Erreur : {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
