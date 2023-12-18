from flask import Flask, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define the main function for machine learning operations
def main(new_sentences):
    df = pd.read_csv('./data.csv')

    # Assuming your dataset has 'text' and 'label' columns
    X = df['text']
    y = df['label']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a bag-of-words model using CountVectorizer
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Train a logistic regression classifier
    classifier = LogisticRegression()
    classifier.fit(X_train_vec, y_train)

    # Evaluate the model
    y_pred = classifier.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)

    # Vectorize the new sentences using the same vectorizer
    new_sentences_vec = vectorizer.transform(new_sentences)

    # Make predictions
    predictions = classifier.predict(new_sentences_vec)
    
    return predictions, accuracy

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        if not data or 'sentences' not in data:
            return jsonify({'error': 'No sentences provided.'}), 400

        if not isinstance(data['sentences'], list):
            return jsonify({'error': 'Sentences must be a list.'}), 400

        if len(data['sentences']) == 0:
            return jsonify({'predictions': [], 'accuracy': 0})

        predictions, accuracy = main(data['sentences'])
        return jsonify({'predictions': list(predictions), 'accuracy': accuracy})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8001)
