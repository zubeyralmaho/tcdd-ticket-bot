import datetime
import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()

class AppointmentBot:
    def __init__(self, kalkıs, varıs, sender_email, sender_password, receiver_emails, message_subject, message_body):
        self.email_address = kalkıs
        self.password_value = varıs
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_emails = receiver_emails
        self.message_subject = message_subject
        self.message_body = message_body
        self.is_running = True

        self.service = Service()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")  # Run in headless mode
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.get("https://bilet.tcdd.gov.tr/")
        self.wait = WebDriverWait(self.driver, 10)

    def send_mail(self):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["Subject"] = self.message_subject
        message.attach(MIMEText(self.message_body, "plain"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                message["To"] = ", ".join(self.receiver_emails)
                server.sendmail(self.sender_email, self.receiver_emails, message.as_string())
                print("E-posta gönderildi!")
                return True
        except Exception as e:
            print("E-posta gönderilemedi. Hata:", e)
            return False

    def seferara(self):
        try:
            nereden = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="fromTrainInput"]')))
            nereden.click()
            nereden.send_keys(self.email_address)
            time.sleep(1)
            
            ankara = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="gidis-2503"]/div/div')))
            ankara.click()
            time.sleep(1)
            
            nereye = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="buyTicket"]/div[2]/div[2]/div/div[1]/div/input')))
            nereye.click()
            nereye.send_keys(self.password_value)
            print("Gidiş-Dönüş yolu seçildi.")
            time.sleep(1)
            
            kars = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="donus-4594"]/div/div')))
            kars.click()
            time.sleep(1)
            
            tarih = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="buyTicket"]/div[3]/div/div[2]/div/div/div[1]/div')))
            tarih.click()
            time.sleep(1)
            
            # Get tomorrow's date
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            date_str = tomorrow.strftime("%d-%m-%Y")
            
            gun = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="{date_str}"]')))
            gun.click()
            print("Tarih seçildi.")
            time.sleep(2)
            
            sign_in = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="buyTicket"]/div[5]/div/button')))
            time.sleep(1)
            sign_in.click()
            time.sleep(1)
            
            previous = self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/main/section/div[3]/div/div[1]/div/div/div/div/div/button[1]')))
            previous.click()
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Sefer arama hatası: {str(e)}")
            return False

    def koltukcheck(self):
        try:
            print(f"Koltuk sayısı aranıyor")
            empty_seat_element = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                '/html/body/div/main/section/div[3]/div/div[1]/div/div/section/div[2]/div[1]/h5/button/div/div[3]/div/div/span[3]')))
            empty_seat_count = int(empty_seat_element.text.strip('()'))
            
            if empty_seat_count > 0:
                print(f"{empty_seat_count} adet boş koltuk mevcut!")
                self.message_body += f"\n{empty_seat_count} adet boş kuşetli yatak bulundu!!!"
                return self.send_mail()
            else:
                print(f"Koltuk yok tekrar deneniyor")
                return False
                
        except Exception as e:
            print(f"Koltuk kontrolü hatası: {str(e)}")
            return False

    def run(self):
        while self.is_running:
            try:
                if self.seferara():
                    if self.koltukcheck():
                        print("Boş koltuk bulundu ve e-posta gönderildi!")
                        break
                time.sleep(5)  # Wait 5 seconds before next attempt
            except Exception as e:
                print(f"Bot çalışma hatası: {str(e)}")
                time.sleep(5)
        
        self.driver.quit()

    def stop(self):
        self.is_running = False
        self.driver.quit()

if __name__ == "__main__":
    # Get default values from environment variables
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_emails = os.getenv("RECEIVER_EMAILS", "").split(",")
    default_from = os.getenv("DEFAULT_FROM", "Ankara")
    default_to = os.getenv("DEFAULT_TO", "Kars")
    
    appointment_bot = AppointmentBot(
        kalkıs=default_from,
        varıs=default_to,
        sender_email=sender_email,
        sender_password=sender_password,
        receiver_emails=receiver_emails,
        message_subject="Boş Kuşetli Yatak Mevcut! ÇABUUKK!!!",
        message_body=f"https://bilet.tcdd.gov.tr/ adresinde {default_from}-{default_to} Doğu Ekspresi için"
    )

    appointment_bot.run()