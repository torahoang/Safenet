import json
import torch
from transformers import BertTokenizerFast, BertForTokenClassification
import gradio as gr

# init important things
tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
model = BertForTokenClassification.from_pretrained('ethical-spectacle/social-bias-ner')
model.eval()
model.to('cuda' if torch.cuda.is_available() else 'cpu')
sentence = """Sorry, @Rosi is a mentally sick woman, a bully, a dummy and,
 above all, a loser. Other than that she is just wonderful!"""
# ids to labels we want to display
id2label = {
    0: 'O',
    1: 'B-STEREO',
    2: 'I-STEREO',
    3: 'B-GEN',
    4: 'I-GEN',
    5: 'B-UNFAIR',
    6: 'I-UNFAIR'
}


# predict function you'll want to use if using in your own code
def predict_ner_tags(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=128)
    input_ids = inputs['input_ids'].to(model.device)
    attention_mask = inputs['attention_mask'].to(model.device)

    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        probabilities = torch.sigmoid(logits)
        predicted_labels = (probabilities > 0.5).int()  # remember to try your own threshold

    result = []
    tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    for i, token in enumerate(tokens):
        if token not in tokenizer.all_special_tokens:
            label_indices = (predicted_labels[0][i] == 1).nonzero(as_tuple=False).squeeze(-1)
            labels = [id2label[idx.item()] for idx in label_indices] if label_indices.numel() > 0 else ['O']
            result.append({"token": token, "labels": labels})

    return json.dumps(result, indent=4)


while True:
    sentence = input("Enter a sentence to analyze or type 'exit' to quit: ")
    if sentence.lower() == 'exit':
        break
    print("NER Tags:", predict_ner_tags(sentence))
