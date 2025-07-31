from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import re
import base64
import numpy as np
from io import BytesIO
from PIL import Image
import torch
import torch.nn as nn
import os
from datetime import datetime
# ------------------ MODEL TANIMI ------------------

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 4)
        self.fc1 = nn.Linear(64 * 5 * 5, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.reshape(-1, 64 * 5 * 5)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Model yükleniyor
model = Net()
model.load_state_dict(torch.load("mnist_net.pth", map_location=torch.device('cpu')))
model.eval()

# ------------------ FLASK UYGULAMASI ------------------

app = Flask(__name__)
CORS(app)

# ------------------ Resim Ön İşleme ------------------

image_counter = 0


def preprocess_base64_image(base64_str):
    import re
    from PIL import Image, ImageOps
    import io
    import numpy as np
    import cv2

    # base64'ten decode et
    img_data = re.sub('^data:image/.+;base64,', '', base64_str)
    img_bytes = io.BytesIO(base64.b64decode(img_data))
    img = Image.open(img_bytes).convert("L")  # grayscale


    # NumPy'a çevir
    img_np = np.array(img)

    # Invert: beyaz arka plan/siyah çizim bekleniyor, ters çeviriyoruz
    img_np = 255 - img_np

    # Eşikleme (noise temizliği)
    img_np[img_np < 30] = 0

    # Kontur bul
    contours, _ = cv2.findContours(img_np.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        cropped = img_np[y:y+h, x:x+w]
    else:
        cropped = img_np

    # 20x20’e yeniden boyutlandır
    cropped_img = Image.fromarray(cropped).resize((20, 20), Image.LANCZOS)

    # 28x28 pad’le
    new_img = Image.new('L', (28, 28), 0)
    new_img.paste(cropped_img, ((28 - 20) // 2, (28 - 20) // 2))

    final_img = np.array(new_img).astype("float32") / 255.0  # normalize
    final_img = final_img.reshape(1, 1, 28, 28)

    # Kaydet: kontrol amaçlı
    new_img.save("C:/Users/EdaNurIsik/Desktop/math_chatbot/foto/input_processed.png")

    return torch.tensor(final_img, dtype=torch.float32)


# ------------------ Yardımcı Fonksiyonlar ------------------

def to_turkish_lower(text):
    replacements = {'I': 'ı', 'İ': 'i', 'Ş': 'ş', 'Ğ': 'ğ', 'Ü': 'ü', 'Ö': 'ö', 'Ç': 'ç'}
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.lower()

def text2number_tr(text):
    text = to_turkish_lower(text.strip())
    parts = text.split()
    birler = {'bir': 1, 'iki': 2, 'üç': 3, 'dört': 4, 'beş': 5, 'altı': 6, 'yedi': 7, 'sekiz': 8, 'dokuz': 9}
    onlar = {'on': 10, 'yirmi': 20, 'otuz': 30, 'kırk': 40, 'elli': 50, 'altmış': 60, 'yetmiş': 70, 'seksen': 80, 'doksan': 90}
    if len(parts) == 1:
        if parts[0] in birler: return birler[parts[0]]
        if parts[0] in onlar: return onlar[parts[0]]
    elif len(parts) == 2:
        if parts[0] in onlar and parts[1] in birler:
            return onlar[parts[0]] + birler[parts[1]]
    return None

word_to_number = {'bir': 1, 'iki': 2, 'üç': 3, 'dört': 4, 'beş': 5,
                  'altı': 6, 'yedi': 7, 'sekiz': 8, 'dokuz': 9, 'on': 10}

operations = {'artı': '+', 'topla': '+', '+': '+', 'eksi': '-', 'çıkar': '-', '-': '-',
              'çarpı': '*', 'kere': '*', 'x': '*', '*': '*', 'bölü': '/', 'böl': '/', '/': '/'}

def parse_input(text):
    text = to_turkish_lower(text)
    text = re.sub(r'[^\wçğıöşü+\-*/ ]', '', text)

    # Eğer kullanıcı "hazırım", "soru ver" gibi bir şey dediyse:
    if any(keyword in text for keyword in ['soru', 'hazırım', 'başla', 'bir soru', 'sor']):
        a, b = random.randint(1, 10), random.randint(1, 10)
        op = random.choice(['+', '-'])  # toplama ve çıkarma
        if op == '-' and a < b:
            a, b = b, a  # negatif sonucu önle
        question = f"{a} {op} {b}"
        answer = int(eval(question))
        return f"{question} = ? (Doğru cevap: {answer})"  # veya sadece soruyu döndür

    # Sayısal ifade varsa bunu çöz
    math_expr_match = re.search(r'(\d+)\s*([\+\-\*/])\s*(\d+)', text)
    if math_expr_match:
        try:
            return f"Cevap: {int(eval(math_expr_match.group(0)))}"
        except:
            return "Bu işlemi anlayamadım."

    # Yazılı sayıları işle
    tokens = text.split()
    nums = []
    op = None
    for word in tokens:
        if word.isdigit():
            nums.append(int(word))
        elif word in word_to_number:
            nums.append(word_to_number[word])
        elif word in operations:
            op = operations[word]

    if len(nums) == 2 and op:
        try:
            return f"Cevap: {int(eval(f'{nums[0]} {op} {nums[1]}'))}"
        except:
            return "İşlem sırasında hata oluştu."

    return "İfadeni anlayamadım. Lütfen tekrar yaz."


# ------------------ ROUTES ------------------

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    return jsonify({'reply': parse_input(data.get('message', ''))})

@app.route('/new_question', methods=['GET'])
def new_question():
    a, b = random.randint(1, 10), random.randint(1, 10)
    op = random.choice(['+', '-', '*', '/'])
    question = f"{a} {op} {b}"
    try: answer = int(eval(question))
    except ZeroDivisionError: answer = 0
    return jsonify({'question': f"{question} = ?", 'answer': answer})

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = data.get('answer', '').strip()
    try: correct_answer = int(data.get('correct', 0))
    except: return jsonify({'reply': 'Doğru cevabı alamadım, sistem hatası.', 'correct': False})
    user_answer = to_turkish_lower(re.sub(r'[^\wçğıöşü ]', '', user_answer))
    user_num = int(user_answer) if user_answer.isdigit() else text2number_tr(user_answer)
    if user_num is None:
        return jsonify({'reply': 'Lütfen geçerli bir sayı yaz.', 'correct': False})
    if user_num == correct_answer:
        return jsonify({'reply': 'Tebrikler, doğru cevap!', 'correct': True})
    return jsonify({'reply': f"Yanlış, doğru cevap {correct_answer}.", 'correct': False})

@app.route('/predict_digit', methods=['POST'])
def predict_digit():
    data = request.get_json()
    base64_img = data['image']
    correct = int(data.get('correct', -1))

    img_tensor = preprocess_base64_image(base64_img)  # artık doğru formatta

    with torch.no_grad():
        outputs = model(img_tensor)
        predicted_digit = int(torch.argmax(outputs, dim=1).item())

    if predicted_digit == correct:
        reply = "Tebrikler! Doğru çizim. ✅"
        is_correct = True
    else:
        reply = f"Yanlış çizim. ❌ Model {predicted_digit} tahmin etti, doğru {correct}."
        is_correct = False

    return jsonify({'prediction': predicted_digit, 'reply': reply, 'correct': is_correct})

# ------------------ UYGULAMAYI BAŞLAT ------------------

if __name__ == '__main__':
    app.run(debug=True)
