FROM python:3.12-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinim dosyasını kopyala ve yükle
COPY requirements.txt .

# Gereksinimleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Django uygulamasını başlat
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
