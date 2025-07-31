# Ai79
Mini Matematik Chatbot
Proje Özeti
Bu proje, ilkokul çağındaki çocukların temel matematik işlemlerini eğlenceli ve etkileşimli bir şekilde öğrenmelerini amaçlayan bir chatbot uygulamasıdır. Kullanıcılar soruları doğal Türkçe ifadelerle yazılı olarak veya çizerek yanıtlayabilirler.

Kullanılan Teknolojiler ve Yapay Zeka Yöntemleri
Doğal Dil İşleme (NLP)
Temel seviyede, kural tabanlı (rule-based) NLP teknikleri kullanılarak, kullanıcının doğal dilde yazdığı matematiksel ifadeler analiz edilir. Örneğin, "dört artı beş" gibi ifadeler rakamsal değerlere dönüştürülür ve doğru işlem sonucu hesaplanır.

Derin Öğrenme ile El Yazısı Rakam Tanıma
Kullanıcıların çizdiği rakamlar, MNIST veri seti kullanılarak eğitilmiş bir Convolutional Neural Network (CNN) modeli tarafından sınıflandırılır. MNIST veri seti yaklaşık 60.000 eğitim ve 10.000 test örneği içerir. Modelimiz %98 doğruluk oranına sahiptir.

Projenin Amacı
Geleneksel yöntemlerde çocuklar kağıt kalemle sayı ve işlemleri öğrenirken, bu proje bu deneyimi dijital ortama taşıyarak, çocukların hem yazılı hem de çizim yoluyla matematik alıştırmaları yapmasını sağlar. Böylece öğrenme süreci daha interaktif ve eğlenceli hale gelir.

Hedef Kitle
6–10 yaş arası çocuklar

Matematiğe yeni başlayanlar

Oyun yoluyla öğrenmeyi seven öğrenciler

Kurulum ve Çalıştırma
Gerekli Kütüphaneler
Projeyi çalıştırmak için aşağıdaki Python paketlerini kurmanız gerekiyor:
pip install torch flask opencv-python pytesseract

Uygulamanın Başlatılması
Terminal veya komut istemcisinde projenin bulunduğu dizine gidin.

Flask uygulamasını başlatmak için(terminale):
python app.py

Uygulama çalışmaya başladıktan sonra tarayıcınızı açın ve şu adresi ziyaret edin:
http://127.0.0.1:5000 ya da
HTML dosyasını doğrudan açmak için, proje klasöründeki .html uzantılı dosyaya çift tıklayabilir veya tarayıcınızda açabilirsiniz.
