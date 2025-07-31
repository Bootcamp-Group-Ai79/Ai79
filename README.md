# Ai79
🎉 Mini Matematik Chatbot

📚 Proje Özeti
Bu proje, ilkokul çağındaki çocukların temel matematik işlemlerini eğlenceli ve etkileşimli şekilde öğrenmelerini sağlayan bir chatbot uygulamasıdır.
Çocuklar, soruları doğal Türkçe ifadelerle yazılı olarak ya da çizerek yanıtlayabilirler. 📝✍️

🤖 Kullanılan Teknolojiler ve Yapay Zeka Yöntemleri

💬 Doğal Dil İşleme (NLP)
Temel seviyede, kural tabanlı (rule-based) NLP teknikleri kullanılır.
Kullanıcının doğal dilde yazdığı "dört artı beş" gibi ifadeler, rakamlara ve işlemlere dönüştürülür ve sonuç hesaplanır.

🖌️ Derin Öğrenme ile El Yazısı Rakam Tanıma
Kullanıcıların çizdiği rakamlar, MNIST veri seti ile eğitilmiş bir Convolutional Neural Network (CNN) modeli tarafından tanınır.
MNIST veri seti yaklaşık 60.000 eğitim ve 10.000 test örneği içerir.
Modelimizin doğruluk oranı: %98 ✅


🎯 Projenin Amacı

Eskiden çocuklar matematiği kağıt ve kalemle öğrenirdi. Bu proje, o nostaljik deneyimi dijital ortama taşıyarak, çocukların hem yazılı hem de çizimle matematik öğrenmesini sağlar. Böylece öğrenme süreci çok daha eğlenceli ve interaktif hale gelir. 🎈🎉


👧👦 Hedef Kitle
6–10 yaş arası çocuklar
Matematiğe yeni başlayanlar
Oyun yoluyla öğrenmeyi seven öğrenciler 🎮📖


🚀 Kurulum ve Çalıştırma

📦 Gerekli Kütüphaneler
Projeyi çalıştırmak için terminalde aşağıdaki komutu kullanarak gerekli Python paketlerini kurun:
Projeyi çalıştırmak için aşağıdaki Python paketlerini kurmanız gerekiyor:
pip install torch flask opencv-python pytesseract

▶️ Uygulamayı Başlatmak
Terminal veya komut istemcisinde projenin bulunduğu dizine gidin.

Flask uygulamasını başlatmak için(terminale):
python app.py

Uygulama çalışmaya başladıktan sonra tarayıcınızı açın ve şu adresi ziyaret edin:
http://127.0.0.1:5000 ya da
HTML dosyasını doğrudan açmak için, proje klasöründeki .html uzantılı dosyaya çift tıklayabilir veya tarayıcınızda açabilirsiniz.
