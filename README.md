# OSINT-tool---Telegram-Bot-script
# OSINT tool — Telegram Bot script

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🕵️‍♂️ About

This repository contains a **Python-based OSINT Telegram bot** called **SaidSecurity Domain Checker Bot**, accessible [here on Telegram](https://t.me/osint_domain_bot).

The bot allows you to check domain information such as:
- DNS records (A, AAAA, MX, NS, SOA, TXT)
- Subdomain count
- IP addresses

It uses the **SecurityTrails API** for data retrieval and is hosted on an AWS VPS (free tier for up to 1 year).

---

## 🚀 Features

- **Multi-API key rotation:** Automatically switches between multiple SecurityTrails API keys to handle rate limits.
- **Rate limiting per user:** Users are limited to 2 domain checks per day to reduce abuse.
- **Input validation:** Verifies domains before processing, helping prevent misuse and errors.
- **Admin logging:** Logs each domain check request to a specific admin chat for monitoring.
- **Bot commands:**  
  - `/start` — Welcome message and usage instructions  
  - `/check domain.com` — Check domain info  
  - `/contact` — Contact details

---

## 💡 Concepts & security practices

### ✅ API key rotation

The bot rotates through multiple API keys to avoid service disruptions when one key hits a rate limit.

### ✅ Input validation

Domain input is strictly validated using regex before any API call, preventing malicious or malformed requests.

### ✅ User rate limiting

Each user is restricted to **2 checks per day**, limiting excessive or abusive usage.

### ✅ Logging

All checks are reported to an admin (your Telegram ID), so you can monitor usage and potential suspicious activity.

---

## ⚙️ Tech stack

- **Python** (>=3.10)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v20+
- AWS VPS hosting

---

## 🔐 Security considerations

As an **ethical hacker**, I designed this bot following good security practices:
- Avoid exposing sensitive logic and internal structures publicly.
- Validate all external inputs.
- Monitor and limit usage through daily limits and admin logs.
- Use environment variables or secrets to store actual API keys and bot tokens in production.

---

## 🌍 Bot link

Try it live: [@osint_domain_bot](https://t.me/osint_domain_bot)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contact

- LinkedIn: [Nursaid Kamilli](https://www.linkedin.com/in/nursaid-kamilli)
- Telegram: [@elsenoraccount](https://t.me/elsenoraccount)
- Website: [saidsecurity.com](https://saidsecurity.com)

---

### ⭐️ Feel free to star or contribute if you like the project!
