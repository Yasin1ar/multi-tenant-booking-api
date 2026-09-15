# Multi-Tenant Resource & Event Booking API

A high-concurrency RESTful backend API built with Django REST Framework, designed to handle multi-tenant space reservations, race-condition safety, async tasks, and payment processing.

> 🚧 **Status:** Under Active Development

---

## 🛠 Tech Stack
- **Language:** Python 3.12+ (managed with `uv`)
- **Framework:** Django 5.x & Django REST Framework
- **Database:** PostgreSQL
- **Async Queue:** Celery & Redis
- **Testing:** Pytest & Factory Boy
- **Containerization:** Docker & Docker Compose

---

## 📋 Implementation Roadmap

- [x] Phase 1: Environment Setup & Docker Compose
- [x] Phase 2: Multi-Tenant Data Models & Custom Auth
- [ ] Phase 3: Concurrency Control & Row Locking (`select_for_update`)
- [ ] Phase 4: Celery Background Workers & Stripe Webhooks
- [x] Phase 5: Automated Testing Suite (`pytest-django`)
- [ ] Phase 6: CI/CD & Deployment
