# ⚙️ CiberActuar — Backend API

> **Microservicios de ciberseguridad y modelos actuariales** para la plataforma CiberActuar.

![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis)
![NumPy](https://img.shields.io/badge/NumPy-1.26-013243?style=flat-square&logo=numpy)

---

## 🎯 ¿Qué hace este backend?

Este servicio provee la inteligencia matemática detrás de CiberActuar:

1. **Escanea** el dominio de la empresa buscando vulnerabilidades
2. **Calcula** el Cyber Score usando un algoritmo de scoring
3. **Ejecuta** el modelo actuarial (Poisson + Monte Carlo) para calcular pérdidas esperadas
4. **Genera** la cotización óptima del ciberseguro

---

## 🏗️ Arquitectura

```
app/
├── main.py                    # FastAPI app + CORS + routers
├── core/
│   └── config.py              # Configuración (Pydantic Settings)
├── models/
│   └── actuarial.py           # Modelos matemáticos (Poisson + Monte Carlo)
└── api/
    └── v1/
        ├── scan.py            # POST /api/v1/scan
        ├── quote.py           # GET /api/v1/quote/{domain}
        └── recalculate.py     # POST /api/v1/recalculate
```

---

## 🧮 Modelos Matemáticos

### Modelo de Frecuencia — Distribución de Poisson
Calcula cuántos ataques por año puede esperar la empresa:

```
λ = λ_base × factor_sector × (1 + (1 - score/100) × 2)
```

### Modelo de Severidad — Log-Normal
Modela el tamaño de cada pérdida:

```
X ~ LogNormal(μ, σ)
μ = log(pérdida_base) - σ²/2
```

### Simulación Monte Carlo
- 10.000 simulaciones de años de negocio
- Para cada año: n_ataques ~ Poisson(λ)
- Para cada ataque: pérdida ~ LogNormal(μ, σ)
- Resultado: distribución completa de pérdidas posibles

### Cálculo de Prima
```
Prima_mensual = E[Pérdida_anual] / Loss_Ratio / 12
Loss_Ratio = 0.60 (estándar de industria aseguradora)
```

---

## 🚀 Cómo levantar el backend

### Opción 1: Docker Compose (Recomendado)

```bash
git clone https://github.com/dantepiemontesi/ciberactuar-backend.git
cd ciberactuar-backend
docker-compose up
```

La API estará disponible en `http://localhost:8000`

### Opción 2: Local

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Copiar variables de entorno
cp .env.example .env

# 4. Levantar Redis
docker run -d -p 6379:6379 redis:7-alpine

# 5. Iniciar la API
uvicorn app.main:app --reload --port 8000
```

---

## 📡 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v1/scan` | Escanea un dominio |
| `GET`  | `/api/v1/quote/{domain}` | Obtiene cotización |
| `POST` | `/api/v1/recalculate` | Recalcula con mejoras |
| `GET`  | `/docs` | Documentación interactiva (Swagger) |
| `GET`  | `/health` | Health check |

### Ejemplo: POST /api/v1/scan

```json
// Request
{ "domain": "miempresa.com" }

// Response
{
  "domain": "miempresa.com",
  "cyberScore": 45,
  "expectedAnnualLoss": 12500,
  "recommendedPremium": 45,
  "coverageAmount": 100000,
  "vulnerabilities": [...],
  "monteCarloData": [...],
  "sectorComparison": 65
}
```

---

## 🔗 Repositorios del Proyecto

| Repo | Descripción |
|------|-------------|
| [ciberactuar-frontend](https://github.com/dantepiemontesi/ciberactuar-frontend) | Next.js SPA Dashboard |
| [ciberactuar-backend](https://github.com/dantepiemontesi/ciberactuar-backend) | Este repo — FastAPI + Redis |

---

## 📄 Licencia

MIT — Desarrollado con ❤️ para el ecosistema PyME
