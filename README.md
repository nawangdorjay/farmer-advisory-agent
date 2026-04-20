# 🌾 Krishi Mitra — Multilingual Farmer Advisory Agent

An AI-powered farming assistant that answers agricultural queries in **Hindi, Tamil, Telugu, Bengali, Marathi, Punjabi, Gujarati, Kannada, Malayalam, and English**.

Built by [Nawang Dorjay](https://github.com/nawangdorjay) — a developer from Ladakh, for **GSSoC 2026** (Agents for India Track).

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🌿 **Crop Advisory** | Sowing times, varieties, fertilizer doses, irrigation schedules |
| 🐛 **Pest & Disease** | Identify problems by symptoms. Get treatment with dosage and timing |
| 🏛️ **Govt Schemes** | PM-KISAN, Fasal Bima, KCC, subsidies — eligibility and how to apply |
| 💰 **Market Prices** | Current mandi prices across states |
| 📅 **Crop Calendar** | Region-specific sowing/harvest calendars for kharif and rabi |
| 🌤️ **Weather Advisory** | Weather-based farming tips using real-time data |
| 🌐 **Multilingual** | Ask in your own language — AI responds in the same language |

---

## 📸 How It Works

```
Farmer: गेहूं की फसल में पीले धब्बे आ रहे हैं, क्या करूं?

Krishi Mitra: 🌾 आपकी गेहूं की फसल में पीले धब्बे होना रतुआ (Rust) 
रोग का लक्षण हो सकता है। यह एक फफूंद जनित रोग है।

उपचार:
1. प्रोपिकोनाजोल 25 EC @ 1ml/L का छिड़काव करें
2. प्रतिरोधी किस्में उगाएं (HD 3226, DBW 187)
3. अतिरिक्त नाइट्रोजन उर्वरक से बचें
4. शीघ्र बुवाई से देर से रतुआ से बचा जा सकता है
```

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **LangChain** — Tool orchestration (function calling)
- **OpenAI / Groq API** — LLM backbone
- **Streamlit** — Interactive chat UI
- **wttr.in** — Free weather API
- **JSON** — Structured agricultural data

---

## 📦 Installation

```bash
# Clone
git clone https://github.com/nawangdorjay/farmer-advisory-agent.git
cd farmer-advisory-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your API key to .env:
# GROQ_API_KEY=gsk_xxxxx  (free at console.groq.com)

# Run
streamlit run app.py
```

### Free API Key (Recommended)

Get a free Groq API key at [console.groq.com](https://console.groq.com) — no credit card needed. It's fast and supports Llama 3.3 70B.

---

## 📁 Project Structure

```
farmer-advisory-agent/
├── app.py                  # Streamlit chat UI
├── agent/
│   ├── __init__.py
│   ├── core.py             # Main agent logic + tool orchestration
│   └── tools.py            # Tool functions (crop info, pest, schemes, etc.)
├── data/
│   ├── crops.json          # Crop database (10 crops with detailed info)
│   ├── pests.json          # Pest/disease database with treatments
│   ├── schemes.json        # Government schemes and subsidies
│   ├── market_prices.json  # Simulated mandi prices by state
│   └── crop_calendar.json  # Regional sowing/harvest calendars
├── utils/
│   ├── __init__.py
│   ├── weather.py          # Weather API wrapper (wttr.in)
│   └── language.py         # Language detection (Unicode script ranges)
├── tests/
│   └── test_tools.py       # Tool validation tests
├── .github/workflows/
│   └── ci.yml              # GitHub Actions CI
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🧪 Testing

```bash
python tests/test_tools.py
```

All 11 tests cover: crop info, pest matching, government schemes, market prices, and crop calendars.

---

## 🌐 Multilingual Support

The agent detects input language using Unicode script ranges and instructs the LLM to respond in the same language.

| Language | Script | Example Query |
|----------|--------|---------------|
| Hindi | Devanagari | "धान की फसल में कीड़ा लगा है" |
| Tamil | Tamil | "நெல் பயிரில் பூச்சி தாக்குதல்" |
| Telugu | Telugu | "వరి పంటలో తెగులు" |
| Bengali | Bengali | "ধানের ক্ষেতে পোকা লেগেছে" |
| Marathi | Devanagari | "भाताच्या पिकावर कीटक" |
| English | Latin | "Best time to sow wheat in Punjab?" |

---

## 📊 Crops Covered

| Crop | Season | States |
|------|--------|--------|
| Rice (चावल) | Kharif/Rabi | Pan-India |
| Wheat (गेहूं) | Rabi | North/Central India |
| Cotton (कपास) | Kharif | West/South/Central |
| Sugarcane (गन्ना) | Year-round | UP, Maharashtra, Karnataka |
| Maize (मक्का) | Kharif/Rabi | Pan-India |
| Mustard (सरसों) | Rabi | North India |
| Tomato (टमाटर) | Year-round | Pan-India |
| Potato (आलू) | Rabi | North/East India |
| Onion (प्याज) | Kharif/Rabi | Maharashtra, Karnataka |
| Chickpea (चना) | Rabi | Central/West India |

---

## 🏛️ Government Schemes Covered

- **PM-KISAN** — ₹6,000/year direct income support
- **PMFBY** — Crop insurance at low premium
- **Kisan Credit Card** — Low-interest farming credit
- **Soil Health Card** — Free soil testing
- **Machinery Subsidies** — 25-50% on farm equipment
- **PM Kusum** — Solar pumps and power
- **eNAM** — Online mandi trading platform
- **NMSA** — Sustainable agriculture mission

---

## 🔮 Future Improvements

- [ ] Integration with live eNAM API for real-time prices
- [ ] Voice input/output for low-literacy users
- [ ] Image-based pest/disease detection (upload leaf photo)
- [ ] WhatsApp bot integration
- [ ] Regional crop varieties for Northeast India
- [ ] Bhashini API integration for better translation

---

## 📄 License

MIT

---

## 👨‍💻 Author

**Nawang Dorjay** — B.Tech CSE (Data Science), MAIT Delhi
From Nubra Valley, Leh, Ladakh 🏔️

- [GitHub](https://github.com/nawangdorjay)
- [Email](mailto:nawangdorjay09@gmail.com)

Built for **GSSoC 2026** — Agents for India Track.

---

## 🤖 AI-Assisted Development

This project was built with AI assistance as part of a transparent human-AI collaboration workflow. AI helped with code generation, structure, and documentation — while domain expertise, data accuracy, and architectural decisions were human-driven.

> **See [BUILDING.md](BUILDING.md) for full transparency on AI usage, roles, and workflow.**

