# 🛡️ NGINX Reverse Proxy with ModSecurity (OWASP CRS) - Dockerized WAF

This project is a **fully containerized Web Application Firewall (WAF)** using **NGINX**, **ModSecurity**, and the **OWASP Core Rule Set (CRS)**.  
It protects a **Flask backend application** running behind a secure reverse proxy, with full request inspection, rate limiting, custom rules, and audit logging.

Everything is deployed automatically using **Docker Compose**, and includes a full suite of **security test cases**.

---

## 🧱 Technologies Used

- **NGINX** (reverse proxy)
- **ModSecurity v3**
- **OWASP Core Rule Set (CRS)**
- **Docker & Docker Compose**
- **Flask + Gunicorn backend**
- **Custom WAF rules + CRS overrides**
- **Audit logging to file system**

---

## 📦 Project Components

### **1. WAF Proxy (`nginx-waf`)**
- Based on `owasp/modsecurity-crs:nginx` official image  
- Full ModSecurity engine enabled (blocking mode)
- OWASP CRS activated with paranoia level 1
- Custom rules included for:
  - SQL injection detection  
  - Scanner User-Agent blocking  
  - Long-URI protection  
  - Logging tags  
- Rate limiting (`limit_req` with burst control)
- Audit logs stored in `waf-logs/`

### **2. Backend App (`demo-app`)**
- Python Flask application
- Served by **Gunicorn** on port `5000`
- Exposed internally only — never to the internet
- Protected by the WAF reverse proxy

### **3. Docker Compose**
- Spins up WAF + backend automatically  
- Ensures clean networking  
- Handles build and runtime dependencies  

---

## 🗂️ Folder Structure

```
nginx-waf-proxy/
│
├─ docker-compose.yml
│
├─ app/
│   ├─ Dockerfile
│   └─ app.py
│
├─ nginx/
│   ├─ Dockerfile
│   ├─ nginx.conf
│   │
│   ├─ rules/
│   │   ├─ crs-setup.conf
│   │   └─ custom-rules.conf
│   │
│   ├─ waf-logs/
│   │   └─ .gitkeep
│   │
│   └─ unicode.mapping
│
└─ README.md
```

---

## 🔗 Architecture Overview

- User → **NGINX WAF** → Flask app  
- All requests pass through:
  - ModSecurity engine  
  - OWASP CRS rule set  
  - Custom rules  
  - Rate limiting  
- Backend is isolated and unreachable without WAF  
- Audit logs stored for every blocked/detected request  

**High-Level Flow:**

```
Client
   ↓
NGINX (ModSecurity + CRS)
   ↓
Security Filters + Rules
   ↓
Flask App (Gunicorn)
```

---

## ⚡ How to Run

1. Clone the repo:
```bash
git clone https://github.com/Mr3bd/nginx-waf-modsecurity-owasp-crs.git
cd nginx-waf-modsecurity-owasp-crs
```

2. Start the environment:
```bash
docker compose up --build
```

3. Access your protected application:
```
http://localhost:8080/
```

You should see:
```
Hello from the backend app (behind NGINX WAF)!
```

---

## 🧪 Security Test Cases (Manual)

Use these tests to verify that your WAF is blocking attacks as expected.

### **1. SQL Injection (custom rule)**  
```bash
curl "http://localhost:8080/echo?q=' OR 1=1--"
```
Expected:
```
403 Forbidden
```

### **2. XSS Attempt (CRS rule)**  
```bash
curl "http://localhost:8080/echo?q=<script>alert(1)</script>"
```
Expected:
```
403 Forbidden
```

### **3. Malicious User-Agent (custom rule)**  
```bash
curl -A "sqlmap/1.0" http://localhost:8080/
```
Expected:
```
403 Forbidden
```

### **4. Long URI (DoS/Fuzzing attempt)**  
```bash
curl "http://localhost:8080/$(head -c 4000 </dev/zero | tr '\0' 'A')"
```
Expected:
```
414 Request-URI Too Long
```

### **5. POST SQL Injection**
```bash
curl -X POST -d "username=a&password=' OR '1'='1" http://localhost:8080/login
```
Expected:
```
403 Forbidden
```

### **6. Rate Limiting Test**
```bash
for i in {1..20}; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/; done
```
Expected:
```
200 (first few)
429 (when rate limit exceeded)
```

---

## 🧪 Automated Test

Run:
```bash
python3 tests/waf_tests.py
```

---

## 📁 Logs

All ModSecurity audit logs are stored here:

```
nginx/waf-logs/access.log
nginx/waf-logs/error.log
```

You can monitor attacks in real-time:

```bash
tail -f nginx/waf-logs/access.log
tail -f nginx/waf-logs/error.log
```

---

## ✅ Key Benefits

- **Production-grade WAF setup** using ModSecurity + OWASP CRS  
- **Reverse proxy architecture** with backend isolation  
- **Custom security rules** for deeper protection  
- **Full audit logging** for every blocked attack  
- **Dockerized environment** — no manual setup  
- **Perfect for DevSecOps, Cloud Security learning, or demos**  
- **SEO-optimized project structure for visibility**  

---

## 🌐 SEO Metadata

**Keywords:**  
NGINX WAF, ModSecurity, OWASP CRS, Docker WAF, Reverse Proxy Security, DevSecOps Demo, Cloud Security Engineer, SQL Injection Protection, XSS Prevention, Containerized WAF, OWASP Top 10 Security, Web Application Firewall Example

**Description:**  
A complete Docker-based NGINX Web Application Firewall (WAF) using ModSecurity and the OWASP Core Rule Set (CRS), featuring custom rules, rate limiting, audit logging, and a protected Flask backend application.

---

## 🌟 Star this repo if you found it useful!

Made with 💻 by a **Cloud Security Engineer**, built for **DevSecOps** and **Cloud Security** enthusiasts.

---

## 👨‍💻 Author

[Abdullrahman Wasfi](https://www.linkedin.com/in/mr3bd)

---

## 🌍 Website

https://mr3bd.com

Made with ❤️ using **NGINX, ModSecurity, OWASP CRS, Docker, and Flask**.
