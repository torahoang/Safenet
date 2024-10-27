import json
import torch
from flask import Flask, request, jsonify
from transformers import BertTokenizerFast, BertForTokenClassification
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Initialize important things
device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
model = BertForTokenClassification.from_pretrained('ethical-spectacle/social-bias-ner')
model.eval()
model.to(device)

# IDs to labels we want to display
id2label = {
    0: 'O',
    1: 'B-STEREO',
    2: 'I-STEREO',
    3: 'B-GEN',
    4: 'I-GEN',
    5: 'B-UNFAIR',
    6: 'I-UNFAIR'
}

# Counters for label occurrences
count_Stereo = 0
count_Gen = 0
count_unfair = 0


@app.route('/predict', methods=['POST'])
def predict():
    global count_Stereo, count_Gen, count_unfair
    count_Stereo = count_Gen = count_unfair = 0  # Reset counts for each request

    data = request.get_json()  # Get JSON data from request
    print(data)
    sentence = data.get('sentence', '')  # Extract the sentence

    if not sentence:
        return jsonify({'error': 'No sentence provided'}), 400

    # Call your prediction function
    response = predict_ner_tags(sentence)

    if count_unfair + count_Stereo > 5:
        # Generate your replacement text
        replacement_text = "Some generated text"
    else:
        replacement_text = "None"  # If no rephrasing is needed

    return jsonify({'replacementText': replacement_text})


def predict_ner_tags(sentence, threshold=0.5):
    global count_Stereo, count_Gen, count_unfair

    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=128)
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        probabilities = torch.sigmoid(logits)
        predicted_labels = (probabilities > threshold).int()

    result = []
    tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    for i, token in enumerate(tokens):
        if token not in tokenizer.all_special_tokens:
            label_indices = (predicted_labels[0][i] == 1).nonzero(as_tuple=False).squeeze(-1)
            labels = [id2label[idx.item()] for idx in label_indices] if label_indices.numel() > 0 else ['O']
            count_label(labels)  # Update the counts
            result.append({"token": token, "labels": labels})

    return result  # Return as a list of dictionaries


def count_label(labels):
    global count_Stereo, count_Gen, count_unfair
    for item in labels:
        if 'STEREO' in item:
            count_Stereo += 1
        elif 'GEN' in item:
            count_Gen += 1
        elif 'UNFAIR' in item:
            count_unfair += 1


if __name__ == '__main__':
    app.run(debug=True)
