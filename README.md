# GBT-WAF

GBT-WAF, web uygulamalarının önünde çalışan Python/FastAPI tabanlı modüler bir Web Application Firewall'dur.

Gelen HTTP isteklerini analiz eder, saldırıları engeller ve güvenlik olaylarını admin dashboard üzerinden görüntüler.

## Mimari

```text
Internet
   ↓
Nginx :80/443
   ↓
GBT-WAF :8000
   ↓
Kullanıcının Backend'i
```

Backend ve WAF portlarının doğrudan internete açılması gerekmez.

## Özellikler

- SQL Injection, XSS, Path Traversal tespiti
- Command Injection ve SSRF tespiti
- IP Rate Limiting
- Modüler Rule Engine
- SQLite loglama
- Admin Dashboard
- Admin giriş ve brute-force koruması
- Reverse Proxy
- Docker / Docker Compose
- Nginx
- HTTPS
- Security Headers
- Health Check
- Unit Tests

## Kurulum

```bash
git clone https://github.com/melihercen/waf.git
cd waf
```

`.env.example` dosyasını `.env` olarak kopyalayın:


`.env`:

```env
BACKEND_URL=http://host.docker.internal:3000
SECRET_KEY=CHANGE_ME
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=CHANGE_ME
```

`BACKEND_URL` alanını kendi uygulamanızın portuna göre değiştirin.

Örneğin backend `localhost:5000` üzerinde çalışıyorsa:

```env
BACKEND_URL=http://host.docker.internal:5000
```

## Local HTTPS

```powershell
mkdir nginx\certs

docker run --rm -v "${PWD}/nginx/certs:/certs" alpine/openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /certs/server.key -out /certs/server.crt -subj "/CN=localhost"
```

Self-signed sertifika yalnızca local test içindir.

## Çalıştırma

```bash
docker compose up --build -d
```

Kontrol:

```bash
docker ps
```

WAF'ın durumunda `healthy` görünmelidir.

Uygulama:

```text
https://localhost/
```

Admin:

```text
https://localhost/admin/login
```

## Trafik Akışı

```text
Client → Nginx → WAF → Backend
                    │
                    └── Saldırı → Log + Block
```
