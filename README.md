# AI Marketing Test Platform

**Test egzaminacyjny z AI w marketingu dla studentów studiów podyplomowych UKEN**

## 📋 Opis projektu

Platforma testowa zbudowana w Streamlit umożliwiająca przeprowadzenie egzaminu końcowego z kursu AI w marketingu. System obsługuje 42 studentów oraz jednego nauczyciela (Tina) z pełnym panelem zarządzania i analizy wyników.

## 🎯 Funkcjonalności

### Dla studentów:
- Test wielokrotnego wyboru (27 pytań, 30 minut)
- Automatyczne zapisywanie postęów co 5 pytań
- Natychmiastowe wyniki po zakończeniu testu
- Wizualizacja wyników według kategorii
- Powiadomienie email z wynikiem

### Dla nauczyciela:
- Panel zarządzania z listą wszystkich studentów
- Szczegółowa analiza odpowiedzi każdego studenta
- Statystyki globalne i wykresy
- Eksport wyników do CSV
- Podgląd najtrudniejszych pytań

## 🛠️ Stack technologiczny

- **Frontend**: Streamlit 1.30+
- **Database**: Google Sheets API v4
- **Email**: Gmail SMTP
- **Wizualizacje**: Plotly 5.18+
- **Style**: Custom CSS (Brutalist Design)

## 📦 Instalacja

1. Sklonuj repozytorium:
```bash
git clone <repository-url>
cd TESTHUB
```

2. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

3. Skonfiguruj zmienne środowiskowe:
```bash
cp .env.example .env
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edytuj oba pliki i uzupełnij dane dostępowe
```

4. Skonfiguruj Google Sheets API:
   - Utwórz projekt w Google Cloud Console
   - Włącz Google Sheets API
   - Stwórz Service Account i pobierz credentials.json
   - Udostępnij arkusz Google Sheets dla service account email

5. Uruchom aplikację:
```bash
streamlit run app.py
```

## 📁 Struktura projektu

```
TESTHUB/
├── app.py                          # Strona główna
├── requirements.txt                # Zależności Python
├── modules/                        # Moduły biznesowe
│   ├── auth.py                     # Autoryzacja użytkowników
│   ├── test_engine.py              # Logika testu
│   ├── sheets_manager.py           # Integracja Google Sheets
│   ├── email_service.py            # Obsługa email
│   ├── analytics.py                # Analiza danych
│   └── ui_components.py            # Komponenty UI
├── pages/                          # Strony Streamlit
│   ├── 1_Student_Login.py          # Logowanie studenta
│   ├── 2_Student_Test.py           # Interfejs testu
│   ├── 3_Student_Results.py        # Wyniki studenta
│   ├── 4_Teacher_Login.py          # Logowanie nauczyciela
│   ├── 5_Teacher_Dashboard.py      # Panel nauczyciela
│   └── 6_Teacher_Details.py        # Szczegóły studenta
├── data/                           # Dane aplikacji
│   ├── questions.json              # Baza pytań
│   └── test_config.json            # Konfiguracja testu
├── .streamlit/                     # Konfiguracja Streamlit
│   └── config.toml                 # Ustawienia tematu i serwera
└── docs/                           # Dokumentacja
    ├── ARCHITECTURE.md             # Architektura systemu
    ├── IMPLEMENTATION_PLAN.md      # Plan implementacji
    └── PROJECT_DOCUMENTATION.md    # Pełna dokumentacja

```

## 🎨 Design System

Projekt wykorzystuje **Brutalist Design System**:
- Brak zaokrąglonych rogów
- Czarne ramki (1px solid #000000)
- Żółte akcenty (#FFD700)
- Font: Poppins
- Brak cieni, gradientów, animacji
- Brak emoji w UI

## 🔒 Bezpieczeństwo

- Hasła przechowywane jako zmienne środowiskowe
- Google Sheets API z Service Account
- XSRF Protection włączone
- Walidacja danych wejściowych
- Session state dla bezpiecznego zarządzania sesją

## 📊 Wymagania biznesowe

- **Próg zdawalności**: 48% (13/27 pytań poprawnych)
- **Czas trwania**: 30 minut
- **Liczba pytań**: 27
- **Liczba użytkowników**: 42 studentów + 1 nauczyciel
- **Auto-save**: Co 5 pytań

## 🚀 Deployment

Aplikacja jest przygotowana do wdrożenia na **Streamlit Cloud**:

1. Połącz repozytorium z Streamlit Cloud
2. Skonfiguruj secrets w panelu Streamlit Cloud
3. Deploy automatyczny po każdym commit

## 📝 Licencja

Ten projekt jest własnością UKEN i jest przeznaczony wyłącznie do użytku edukacyjnego.

## 👥 Autorzy

- **Nauczyciel**: Tina
- **Studenci**: 42 studentów studiów podyplomowych UKEN
- **Deweloper**: [Twoje imię]

## 📞 Wsparcie

W przypadku problemów lub pytań skontaktuj się z [Tina] pod adresem [tina@example.com]
