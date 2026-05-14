from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)

# ── LOAD MODEL ──
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# ── ROUTES ──
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text', '').strip()

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Vectorize and predict
    text_vec     = vectorizer.transform([text])
    prediction   = model.predict(text_vec)[0]
    probability  = model.predict_proba(text_vec)[0]

    label        = 'Real' if prediction == 1 else 'Fake'
    confidence   = round(max(probability) * 100, 2)
    fake_prob    = round(probability[0] * 100, 2)
    real_prob    = round(probability[1] * 100, 2)

    return jsonify({
        'label':      label,
        'confidence': confidence,
        'fake_prob':  fake_prob,
        'real_prob':  real_prob
    })

if __name__ == '__main__':
    app.run(debug=True)