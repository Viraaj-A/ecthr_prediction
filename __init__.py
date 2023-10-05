import flask
from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, Text, Date
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.dialects.postgresql import TSVECTOR
import openai
import torch
from transformers import RobertaTokenizerFast, RobertaForSequenceClassification
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from cryptography.fernet import Fernet

# Load the encryption key
with open("secret.key", "rb") as key_file:
    key = key_file.read()

# Load the encrypted API key
with open("encrypted_api_key.txt", "rb") as encrypted_file:
    encrypted_api_key = encrypted_file.read()

# Decrypt the API key
cipher_suite = Fernet(key)
decrypted_api_key = cipher_suite.decrypt(encrypted_api_key).decode("utf-8")

# Now set the API key
openai.api_key = decrypted_api_key

# Load tokenizer and classifier model
model_path = 'checkpoint5000/'
tokenizer = RobertaTokenizerFast.from_pretrained(model_path)
model = RobertaForSequenceClassification.from_pretrained(model_path)

# Set the classifer model to evaluation mode
model.eval()

# Global variable for label names
predicted_labels = ["2 - Right to Life", "3 - Prohibition of torture", "5 - Right to liberty and security",
                    "6 - Right to a fair trial", "8 -  Right to respect for private and family life",
                    "9 - Freedom of thought, conscience, and religion", "10 - Freedom of expression",
                    "11 - Freedom of assembly and association", "1 - Prohibition of discrimination",
                    "P1-1 - Protection of property"]

# Load the FAISS index and model
embedding_model = SentenceTransformer("embedding_model/")
faiss_index = faiss.read_index("faiss_index/bert_sentence_transformer.faiss")

def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)

    app.config['SECRET_KEY'] = 'any secret string'

    app.config[
        "SQLALCHEMY_DATABASE_URI"] = 'postgresql://doadmin:AVNS_SbC_UqXYG665R47kxY4@db-postgresql-fra1-kyr-0001-do-user-12476250-0.b.db.ondigitalocean.com:25060/defaultdb'

    app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'


    with app.app_context():

        # db = SQLAlchemy(app)
        # Base = automap_base()
        #
        # class EnglishSearch(Base):
        #     __tablename__ = "english_search"
        #     existing = True
        #
        #     item_id = Column(Text, primary_key=True)
        #     url = Column(Text)
        #     entire_text = Column(Text)
        #     case_title = Column(Text)
        #     importance_number = Column(Text)
        #     judgment_date = Column(Date)
        #     facts = Column(Text)
        #     conclusion = Column(Text)
        #     ecli = Column(Text)
        #     textsearchable_index_col = Column(TSVECTOR)
        #
        # Base.metadata.create_all(db.engine)
        # Session = sessionmaker(bind=db.engine)
        # session = Session()

        def get_prediction(input_text):
            # Preprocess the input text
            inputs = tokenizer(input_text, padding=True, truncation=True, return_tensors='pt')

            # Perform inference
            with torch.no_grad():
                outputs = model(**inputs)
                probs = torch.sigmoid(outputs.logits)

            # Convert probabilities to percentages
            probs_list = probs.squeeze().cpu().tolist()
            probs_percent = [int(round(p * 100)) for p in probs_list]

            # Pair labels with their predicted probabilities
            results = []
            for label, percent in zip(predicted_labels, probs_percent):
                results.append(f"The percentage chance that Article {label} was violated is {percent}%.")

            return results


        # Importing Routes
        @app.route('/')
        def index():
            return render_template('index.html')

        @app.route('/generate-text', methods=['POST'])
        def generate_text():
            user_prompt = request.form['prompt']

            # Create a conversation payload
            conversation = [
                {
                    "role": "system",
                    "content": "Use the following steps to respond to user inputs. \n\nThe user will input their facts that relate to a human rights violation in simple language. \n\nThe output should be just a conversion of their input to legal writing, specifically, a legal formulation of 'facts'.\n\nIn providing the output make no mention to:\nthe date, any conclusion as to a human rights violation, and the reference to the person should always be \"I\"\n"
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]

            print(len(user_prompt))
            # Make API call to OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=conversation,
                temperature=0,
                max_tokens=len(user_prompt)*2,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Extract generated text from API response
            generated_text = response['choices'][0]['message']['content']
            flask.session["generated_text"] = generated_text

            return render_template('index.html', generated_text=generated_text)

        @app.route('/predict', methods=['POST'])
        def predict():
            text = request.form['predict']
            prediction = get_prediction(text)
            flask.session["prediction"] = prediction
            return render_template('index.html', prediction=prediction, generated_text=text)

        # # PostgreSQL search functionality
        # @app.route('/results/', methods=['GET', 'POST'])
        # def results():
        #     if request.method == 'POST':
        #         query = request.form['search']
        #     else:
        #         query = flask.session.get("generated_text", None)
        #     results = search_text2(query, db, EnglishSearch)
        #     generated_text = flask.session.get("generated_text", None)
        #     prediction = flask.session.get("prediction", None)
        #     return render_template('index.html', results=results, generated_text=generated_text, prediction=prediction)

        #FAISS search
        @app.route('/results/', methods=['GET', 'POST'])
        def results():
            # Load the SentenceTransformer model
            embedding_model = SentenceTransformer('embedding_model/')

            # Load the FAISS index
            index = faiss.read_index('faiss_index/bert_sentence_transformer.faiss')

            # Sentence transformer inference
            def search(query_text, top_k=5):
                # Encode the query
                query_vector = embedding_model.encode([query_text])

                # Search the Faiss index
                distances, indices = index.search(query_vector, top_k)

                # Load the all text pickle file
                with open('documents/all_documents_text.pkl', 'rb') as f:
                    results = pickle.load(f)

                # Retrieve the original rows for the closest matches
                closest_rows = [results[i] for i in indices[0]]

                return closest_rows

            # Querying the model
            '''
            Items 1-6 correspond to the following in order - url, entire_text, case_title, importance_number, judgment_date, facts, conclusion
            '''

            query = flask.session.get("generated_text", None)
            top_results = search(query, top_k=5)
            generated_text = flask.session.get("generated_text", None)
            prediction = flask.session.get("prediction", None)
            return render_template('index.html', results=top_results, generated_text=generated_text, prediction=prediction)

        return app