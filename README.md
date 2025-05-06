# TCDD Ticket Bot

Bu bot, TCDD (Türkiye Cumhuriyeti Devlet Demiryolları) bilet sisteminde belirli bir rota için boş kuşetli yatak arayan ve bulduğunda e-posta ile bildirim gönderen bir otomasyon aracıdır.

## Özellikler

- Belirli bir rota için otomatik bilet arama
- Boş kuşetli yatak kontrolü
- E-posta bildirimleri
- Kullanıcı dostu arayüz
- Gerçek zamanlı durum takibi

## Gereksinimler

- Python 3.7+
- Chrome WebDriver
- Gmail hesabı (e-posta bildirimleri için)

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/zubeyralmaho/tcdd-ticket-bot.git
cd tcdd-ticket-bot
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Chrome WebDriver'ı yükleyin:
- [Chrome WebDriver'ı indirin](https://sites.google.com/chromium.org/driver/)
- İndirdiğiniz dosyayı sistem PATH'inize ekleyin

## Kullanım

1. Programı başlatın:
```bash
python tcdd_bot_ui.py
```

2. Arayüzde:
   - Kalkış ve varış şehirlerini girin
   - E-posta ayarlarını yapılandırın
   - "Start Bot" düğmesine tıklayın

## E-posta Ayarları

Gmail kullanıyorsanız:
1. Gmail hesabınızda "2 Adımlı Doğrulama"yı etkinleştirin
2. "Uygulama Şifreleri" bölümünden yeni bir şifre oluşturun
3. Bu şifreyi bot arayüzünde "App Password" alanına girin

## Güvenlik

- E-posta şifrelerinizi güvenli bir şekilde saklayın
- `.env` dosyasını asla GitHub'a yüklemeyin
- Hassas bilgileri kod içinde saklamayın

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir özellik dalı oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Dalınıza push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request açın 