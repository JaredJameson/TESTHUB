# 📋 PRD: Platforma Testowa AI w Marketingu
## Product Requirements Document v1.0

---

## 🎯 EXECUTIVE SUMMARY

**Nazwa produktu:** AI Marketing Test Platform  
**Właściciel:** AI NETWORK (Jarek - ARTECH CONSULT)  
**Cel biznesowy:** Automatyzacja procesu egzaminowania studentów na studiach podyplomowych UKEN z zakresu AI w Marketingu  
**Technologia:** Python + Streamlit  
**Timeline:** 2-3 dni development, 1 dzień testów  
**Status:** Ready for Implementation

---

## 📊 PROBLEM STATEMENT

### Obecna sytuacja (pain points):
- ❌ Manualne sprawdzanie testów przez prowadzącą (Tina)
- ❌ Brak natychmiastowego feedbacku dla studentów
- ❌ Brak centralnej bazy wyników
- ❌ Trudność w śledzeniu statystyk grupy
- ❌ Ryzyko błędów przy ręcznym zliczaniu punktów

### Rozwiązanie:
✅ Zautomatyzowana platforma testowa z instant feedback  
✅ Dashboard administracyjny dla prowadzącej  
✅ Centralna baza danych z historią wszystkich testów  
✅ Automatyczna notyfikacja email po zakończeniu testu  
✅ Analityka i statystyki w czasie rzeczywistym

---

## 👥 USER PERSONAS

### 1. STUDENT (Primary User)
**Nazwa:** Anna Kowalska  
**Rola:** Uczestniczka studiów podyplomowych UKEN  
**Potrzeby:**
- Wypełnić test w określonym czasie (30 min)
- Dostać natychmiastowy wynik
- Zobaczyć swoje błędy i poprawne odpowiedzi
- Otrzymać potwierdzenie email

**User Journey:**
1. Otrzymuje link do testu od prowadzącej
2. Loguje się (email + imię + nazwisko)
3. Wypełnia 27 pytań w 30 minut
4. Wysyła test
5. Natychmiast widzi wynik i ocenę
6. Otrzymuje email z podsumowaniem

---

### 2. NAUCZYCIEL (Admin User)
**Nazwa:** Tina Nawrocka  
**Rola:** Prowadząca zajęcia - Social Media & AI Marketing  
**Potrzeby:**
- Widzieć kto wypełnił test (real-time)
- Monitorować statystyki grupy
- Przeglądać szczegóły każdego testu
- Identyfikować trudne pytania (często błędne)
- Eksportować wyniki do raportowania

**User Journey:**
1. Loguje się do dashboardu administracyjnego
2. Widzi listę wszystkich studentów i ich wyniki
3. Klika na konkretnego studenta → widzi szczegóły testu
4. Analizuje statystyki grupy (średnia, rozkład ocen)
5. Eksportuje dane do CSV/Excel (opcjonalnie)

---

## 🎨 PRODUCT ARCHITECTURE

### **Multi-Page Streamlit Application**

```
┌─────────────────────────────────────────────┐
│         LANDING PAGE (login)                 │
│  - Wybór: Student / Nauczyciel              │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌─────────────┐  ┌──────────────┐
│   STUDENT   │  │  NAUCZYCIEL  │
│    PANEL    │  │  DASHBOARD   │
└─────────────┘  └──────────────┘
```

---

## 🏗️ FUNCTIONAL REQUIREMENTS

### **MODULE 1: AUTHENTICATION & LANDING**

#### 1.1 Landing Page
**URL:** `https://aitest.streamlit.app` (przykład)

**Elementy:**
- Logo AI NETWORK / UKEN
- Tytuł: "Test Zaliczeniowy - AI w Marketingu"
- Przycisk: "Jestem Studentem" → Student Login
- Przycisk: "Jestem Nauczycielem" → Admin Login
- Informacje:
  - Czas trwania: 30 minut
  - Liczba pytań: 27
  - Próg zaliczenia: 48% (13 punktów)

#### 1.2 Student Login
**Pola:**
- Email* (walidacja: format email)
- Imię*
- Nazwisko*
- Numer indeksu (opcjonalne)

**Walidacja:**
- Wszystkie pola wymagane (oprócz numeru indeksu)
- Sprawdzenie czy student już nie wypełnił testu (opcjonalne - anti-duplicate)
- Zapisanie danych w session_state

**Przycisk:** "Rozpocznij Test" → przekierowanie do Student Panel

#### 1.3 Teacher Login
**Pola:**
- Email*
- Hasło* (prosty PIN lub hasło - np. "uken2026")

**Walidacja:**
- Sprawdzenie czy credentials są poprawne
- Lista authorized teachers (hard-coded lub z Google Sheets)

**Przycisk:** "Zaloguj się" → przekierowanie do Teacher Dashboard

---

### **MODULE 2: STUDENT PANEL (Test Interface)**

#### 2.1 Test Header (zawsze widoczny)
```
┌─────────────────────────────────────────────┐
│ AI Marketing Test                           │
│ Student: Anna Kowalska                      │
│ Czas pozostały: ⏱️ 28:45                    │
│ Postęp: ████████░░░░░░ 15/27 (56%)        │
└─────────────────────────────────────────────┘
```

**Elementy:**
- Nazwa testu
- Imię i nazwisko studenta
- Timer z countdownem (30 min → 0:00)
- Progress bar (ile pytań wypełniono)
- Ostrzeżenie gdy zostaje < 5 min (czerwony timer)

#### 2.2 Pytania (27 total)
**Format każdego pytania:**

```markdown
### Pytanie 15 / 27

**Główny problem generycznego AI prospectingu, który powoduje jego porażkę to:**

○ a) Zbyt wysokie koszty
○ b) Brak dostępu do najnowszych modeli  
○ c) Generyczny output - wszystkie maile brzmią tak samo
○ d) Wolna szybkość generowania

[Wymagane: zaznacz odpowiedź]
```

**Funkcjonalności:**
- Radio buttons (single choice)
- Obowiązkowe odpowiedzi (nie można zostawić pustego)
- Przycisk "Następne pytanie" (z walidacją)
- Przycisk "Poprzednie pytanie" (można wrócić i zmienić)
- Wizualne oznaczenie wypełnionych vs niewypełnionych pytań

#### 2.3 Podsumowanie przed wysłaniem
**Po wypełnieniu wszystkich 27 pytań:**

```
┌─────────────────────────────────────────────┐
│ ✅ Wszystkie pytania wypełnione!            │
│                                              │
│ Odpowiedziałeś na: 27/27 pytań              │
│ Wykorzystany czas: 27 minut 15 sekund       │
│                                              │
│ ⚠️ Po wysłaniu nie będziesz mógł zmienić    │
│    odpowiedzi. Czy na pewno chcesz wysłać?  │
│                                              │
│ [Sprawdź odpowiedzi] [WYŚLIJ TEST]          │
└─────────────────────────────────────────────┘
```

#### 2.4 Auto-submit
- Jeśli timer dojdzie do 0:00 → automatyczne wysłanie testu
- Popup: "Czas minął! Test został automatycznie wysłany."

#### 2.5 Results Page (natychmiast po wysłaniu)
```
┌─────────────────────────────────────────────┐
│          🎉 TEST ZAKOŃCZONY!                │
│                                              │
│ Twój wynik: 22 / 27 (81%)                   │
│ Ocena: 4.5 - Dobra Plus                     │
│ Status: ✅ ZALICZONY                        │
│                                              │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                              │
│ 📊 SZCZEGÓŁOWE WYNIKI                       │
│                                              │
│ [Tabela z pytaniami]                        │
│ Pytanie | Twoja odp | Poprawna | Status    │
│    1    |     c     |    c     |   ✅      │
│    2    |     a     |    a     |   ✅      │
│    3    |     b     |    a     |   ❌      │
│   ...   |    ...    |   ...    |  ...      │
│                                              │
│ 📧 Email z wynikami został wysłany na:      │
│    anna.kowalska@example.com                │
│                                              │
│ [Pobierz wyniki PDF] [Zamknij]              │
└─────────────────────────────────────────────┘
```

**Elementy:**
- Duży, wyraźny wynik (punkty + procent)
- Ocena słownie + numerycznie
- Status: ZALICZONY / NIEZALICZONY (kolorystyka)
- Tabela szczegółowa:
  - Każde pytanie z Twoją odpowiedzią vs poprawna
  - Ikona ✅ / ❌
  - Opcjonalnie: pełna treść pytania (expand/collapse)
- Informacja o wysłanym emailu
- Przycisk "Pobierz PDF" (opcjonalny)

---

### **MODULE 3: TEACHER DASHBOARD (Admin Panel)**

#### 3.1 Dashboard Overview (Main Page)
```
┌─────────────────────────────────────────────┐
│  👨‍🏫 DASHBOARD NAUCZYCIELA                   │
│  Witaj, Tina Nawrocka                       │
│                                              │
│  📊 STATYSTYKI OGÓLNE                        │
│                                              │
│  ┌────────┐ ┌────────┐ ┌────────┐          │
│  │   42   │ │  38    │ │  90%   │          │
│  │Studentów│ │Zaliczył│ │Średnia │          │
│  │Łącznie  │ │  Test  │ │ Ocena  │          │
│  └────────┘ └────────┘ └────────┘          │
│                                              │
│  Średni wynik: 19.8 / 27 (73%)              │
│  Najtrudniejsze pytanie: #23 (34% poprawnych)│
│  Najłatwiejsze pytanie: #2 (96% poprawnych) │
│                                              │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                              │
│  📋 LISTA STUDENTÓW                          │
│                                              │
│  [Filtruj: Wszyscy ▼] [Szukaj: ___]        │
│  [Sortuj: Data ▼]                           │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ Anna Kowalska | 22/27 | 4.5 | ✅     │   │
│  │ anna.k@example.com | 12.01 15:30     │   │
│  │ [Zobacz szczegóły] [Email]           │   │
│  ├──────────────────────────────────────┤   │
│  │ Jan Nowak | 18/27 | 3.5 | ✅         │   │
│  │ jan.n@example.com | 12.01 14:45      │   │
│  │ [Zobacz szczegóły] [Email]           │   │
│  ├──────────────────────────────────────┤   │
│  │ Maria Wiśniewska | 12/27 | 2.0 | ❌  │   │
│  │ maria.w@example.com | 11.01 16:20    │   │
│  │ [Zobacz szczegóły] [Email]           │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  [Eksportuj do CSV] [Eksportuj do Excel]   │
└─────────────────────────────────────────────┘
```

**Funkcjonalności:**
- **Statystyki w kartach (cards):**
  - Liczba studentów łącznie
  - Liczba zaliczonych
  - Średnia ocena grupy
  - Procent zdawalności

- **Kluczowe metryki:**
  - Średni wynik punktowy
  - Najtrudniejsze pytanie (najniższy % poprawnych odpowiedzi)
  - Najłatwiejsze pytanie (najwyższy % poprawnych odpowiedzi)

- **Lista studentów (interaktywna tabela):**
  - Imię, nazwisko, email
  - Wynik (punkty + ocena)
  - Status (zaliczony/niezaliczony) - kolorystyka
  - Data i godzina wypełnienia
  - Przyciski akcji:
    - "Zobacz szczegóły" → Student Detail Page
    - "Email" → szybkie wysłanie wiadomości

- **Filtry i sortowanie:**
  - Filtr: Wszyscy / Zaliczeni / Niezaliczeni
  - Szukaj po imieniu/nazwisku/email
  - Sortuj: Data, Wynik, Nazwisko

- **Eksport:**
  - CSV (wszystkie dane)
  - Excel (formatowane z wykresami - opcjonalnie)

#### 3.2 Student Detail Page (kliknięcie "Zobacz szczegóły")
```
┌─────────────────────────────────────────────┐
│  ← Powrót do Dashboard                      │
│                                              │
│  👤 Anna Kowalska                            │
│  📧 anna.kowalska@example.com               │
│  📅 Data testu: 12.01.2026, 15:30           │
│  ⏱️ Czas: 27 minut 15 sekund                │
│                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                              │
│  📊 WYNIK                                    │
│  22 / 27 (81%)                              │
│  Ocena: 4.5 - Dobra Plus                    │
│  Status: ✅ ZALICZONY                       │
│                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                              │
│  📝 SZCZEGÓŁOWA ANALIZA ODPOWIEDZI          │
│                                              │
│  [Pokaż tylko błędne ☐]                     │
│                                              │
│  Pytanie 1: ✅ POPRAWNIE                    │
│  "Kiedy warto stosować szczegółowe prompty?"│
│  Odpowiedź studenta: c) Gdy proste prompty  │
│    nie dają oczekiwanych rezultatów...      │
│  ✓ Poprawna odpowiedź: c)                   │
│                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                              │
│  Pytanie 3: ❌ BŁĘDNIE                      │
│  "Co oznacza pojęcie okno kontekstowe?"     │
│  Odpowiedź studenta: b) Czas przetwarzania  │
│  ✓ Poprawna odpowiedź: a) Ilość danych...   │
│                                              │
│  [... wszystkie 27 pytań ...]               │
│                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                              │
│  📈 ANALIZA WG KATEGORII                    │
│  Podstawy AI: 4/5 (80%) ✅                  │
│  Modele LLM: 3/5 (60%) ⚠️                   │
│  Strategia: 5/5 (100%) ✅                   │
│  Nowa era: 4/5 (80%) ✅                     │
│  Zaawansowane: 6/7 (86%) ✅                 │
│                                              │
│  [Wyślij email do studenta]                 │
│  [Pobierz PDF z wynikami]                   │
└─────────────────────────────────────────────┘
```

**Funkcjonalności:**
- **Nagłówek z informacjami studenta:**
  - Pełne dane (imię, nazwisko, email)
  - Data i czas wypełnienia testu
  - Całkowity czas spędzony na teście

- **Sekcja wyniku:**
  - Punkty + procent
  - Ocena (słownie + numerycznie)
  - Status wizualny (kolor + ikona)

- **Szczegółowa analiza:**
  - Lista wszystkich 27 pytań
  - Dla każdego:
    - Treść pytania
    - Odpowiedź studenta
    - Poprawna odpowiedź
    - Status (✅ / ❌)
  - Checkbox: "Pokaż tylko błędne" (filtr)

- **Analiza kategorii (breakdown):**
  - Wynik w każdej z 5 części testu
  - Wizualna identyfikacja słabszych obszarów

- **Akcje:**
  - Wyślij email do studenta
  - Pobierz PDF z wynikami

#### 3.3 Analytics Page (zaawansowane - opcjonalne)
```
┌─────────────────────────────────────────────┐
│  📊 ANALITYKA I STATYSTYKI                  │
│                                              │
│  [Wykres: Rozkład ocen]                     │
│  Histogram: oś X = ocena, oś Y = liczba     │
│                                              │
│  [Wykres: Procent poprawnych odpowiedzi]    │
│  Dla każdego pytania (1-27)                 │
│                                              │
│  [Tabela: Najtrudniejsze pytania]           │
│  Top 5 pytań z najniższym % poprawnych      │
│                                              │
│  [Timeline: Wypełnienia w czasie]           │
│  Kiedy studenci wypełniali test             │
│                                              │
│  [Heatmap: Błędy wg kategorii]              │
│  Które kategorie sprawiają największe       │
│  trudności?                                  │
└─────────────────────────────────────────────┘
```

---

### **MODULE 4: DATA PERSISTENCE & INTEGRATION**

#### 4.1 Google Sheets Backend
**Arkusz: "Wyniki_Testow"**

**Kolumny:**
| A | B | C | D | E | F | G | H | I | J | K | L |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Timestamp | Email | Imię | Nazwisko | Nr indeksu | Poprawne | Procent | Ocena | Ocena słownie | Status | Czas (min) | Szczegóły (JSON) |

**Kolumna L (Szczegóły JSON):**
```json
{
  "answers": {
    "1": "c",
    "2": "a",
    ...
  },
  "details": {
    "1": {"student": "c", "correct": "c", "isCorrect": true},
    "2": {"student": "a", "correct": "a", "isCorrect": true},
    ...
  }
}
```

**Funkcje:**
- `append_row()` - dodanie nowego wyniku
- `get_all_records()` - pobranie wszystkich wyników
- `find_by_email()` - wyszukanie studenta po email

#### 4.2 Teacher Credentials (oddzielny arkusz)
**Arkusz: "Teachers"**

| Email | Hasło (hash) | Imię | Nazwisko | Rola |
|-------|--------------|------|----------|------|
| tina@example.com | hash123 | Tina | Nawrocka | Admin |

---

### **MODULE 5: EMAIL NOTIFICATIONS**

#### 5.1 Email do Studenta (po zakończeniu testu)

**Temat:**
```
{{ "✅ Test zaliczony!" if passed else "❌ Test niezaliczony" }} - AI w Marketingu UKEN
```

**Treść (HTML - skrócona):**
```html
<div style="font-family: Arial, sans-serif;">
  <h2 style="color: {{ '#4CAF50' if passed else '#f44336' }};">
    {{ "Gratulacje!" if passed else "Niestety, tym razem się nie udało" }}
  </h2>
  
  <p>Cześć {{ imię }},</p>
  
  <div style="background: #f9f9f9; padding: 20px; margin: 20px 0;">
    <h3>Twój wynik:</h3>
    <p style="font-size: 24px; font-weight: bold;">
      {{ poprawne }} / 27 ({{ procent }}%)
    </p>
    <p>Ocena: <strong>{{ ocena }}</strong> - {{ ocena_slownie }}</p>
    <p>Status: {{ "✅ ZALICZONY" if passed else "❌ NIEZALICZONY" }}</p>
  </div>
  
  <p>Możesz zobaczyć szczegółowe wyniki i swoje błędy logując się ponownie do platformy testowej.</p>
  
  <p>Pozdrawiam,<br>AI NETWORK Team</p>
</div>
```

#### 5.2 Email do Nauczyciela (notification)

**Temat:**
```
🔔 Nowy test wypełniony: {{ imię }} {{ nazwisko }}
```

**Treść:**
```
Cześć Tina,

Student właśnie zakończył test:

Imię i nazwisko: {{ imię }} {{ nazwisko }}
Email: {{ email }}
Wynik: {{ poprawne }}/27 ({{ procent }}%)
Ocena: {{ ocena }}
Status: {{ "ZALICZONY" if passed else "NIEZALICZONY" }}

Zobacz szczegóły w dashboardzie:
https://aitest.streamlit.app/dashboard

---
AI NETWORK Test Platform
```

---

## 🎯 NON-FUNCTIONAL REQUIREMENTS

### Performance
- ✅ Czas ładowania strony: < 2s
- ✅ Responsive na mobile (320px+) i desktop (1920px)
- ✅ Obsługa 50 równoczesnych użytkowników (Streamlit Community Cloud limit)

### Security
- ✅ Hasła nauczycieli: SHA256 hash (minimum)
- ✅ HTTPS (Streamlit Cloud zapewnia)
- ✅ Session timeout: 60 minut bez aktywności
- ✅ Rate limiting: max 3 próby logowania/5 min (anty-brute force)

### Data Privacy (RODO/GDPR)
- ✅ Dane przechowywane w Google Sheets (EU region)
- ✅ Możliwość usunięcia danych studenta na żądanie
- ✅ Anonimizacja: opcja eksportu bez danych osobowych
- ✅ Polityka prywatności (link w stopce)

### Reliability
- ✅ Backup Google Sheets: automatyczny (Google Drive)
- ✅ Error handling: graceful degradation (jeśli Sheets nie działa → zapis lokalny + retry)
- ✅ Auto-save: zapisywanie odpowiedzi co 5 pytań (session state)

### Accessibility
- ✅ WCAG 2.1 Level AA
- ✅ Keyboard navigation
- ✅ Screen reader friendly
- ✅ Kontrast tekstu minimum 4.5:1

---

## 🌐 HOSTING & DOMAIN

### Option 1: Streamlit Community Cloud (RECOMMENDED)
**URL:** `https://aitest-uken.streamlit.app`

**Zalety:**
- ✅ Darmowy hosting
- ✅ HTTPS z certyfikatem
- ✅ Auto-deployment z GitHub
- ✅ Gotowy w 5 minut

**Wady:**
- ⚠️ Limit 50 równoczesnych użytkowników
- ⚠️ URL: subdomena streamlit.app

**Koszt:** $0/mies

---

### Option 2: Streamlit Cloud + Custom Domain
**URL:** `https://test.ainetwork.pl`

**Setup:**
1. Kup domenę: `ainetwork.pl` (~50 zł/rok)
2. Dodaj subdomenę: `test.ainetwork.pl`
3. CNAME record → `aitest-uken.streamlit.app`

**Zalety:**
- ✅ Profesjonalny URL
- ✅ Branding AI NETWORK
- ✅ Wszystkie zalety Option 1

**Koszt:** ~50 zł/rok (domena)

---

### Option 3: Self-Hosted (VPS)
**URL:** `https://test.ainetwork.pl`

**Infrastruktura:**
- VPS (np. DigitalOcean, Hetzner): 5€/mies
- Docker container z Streamlit
- Nginx reverse proxy
- SSL cert (Let's Encrypt - darmowy)

**Zalety:**
- ✅ Pełna kontrola
- ✅ Brak limitów użytkowników
- ✅ Możliwość integracji z innymi systemami

**Wady:**
- ⚠️ Wymaga DevOps knowledge
- ⚠️ Maintenance

**Koszt:** ~5€/mies + domena

---

## 💡 RECOMMENDED APPROACH

### Dla AI NETWORK (Twój przypadek):

**Faza 1 - MVP (Teraz):**
- Streamlit Community Cloud (darmowy)
- URL: `https://aitest-uken.streamlit.app`
- Wdrożenie w 2 dni
- Koszt: $0

**Faza 2 - Scale (Za 2-3 miesiące):**
- Kup domenę: `ainetwork.pl`
- Podepnij: `test.ainetwork.pl` → Streamlit Cloud
- Koszt: ~50 zł/rok

**Faza 3 - Enterprise (Jeśli > 100 studentów równocześnie):**
- Self-hosted VPS
- Rozszerzenie o kolejne kursy
- Integracja z innymi systemami AI NETWORK

---

## 📸 UI/UX MOCKUPS (Conceptual)

### Color Palette
```
Primary: #2196F3 (niebieski - edukacja)
Secondary: #4CAF50 (zielony - sukces)
Error: #f44336 (czerwony - błąd)
Warning: #FF9800 (pomarańczowy - ostrzeżenie)
Background: #F5F5F5
Text: #333333
```

### Typography
- Headings: **Poppins Bold**
- Body: **Open Sans Regular**
- Code: **Fira Code**

### Layout
- Max width: 1200px (centered)
- Padding: 20px mobile, 40px desktop
- Card-based design (Material Design inspired)

---

## 🚀 DEVELOPMENT ROADMAP

### **Sprint 1: Core Functionality (2 dni)**
- [ ] Setup projektu (Streamlit + GitHub)
- [ ] Student login + session management
- [ ] Test interface (27 pytań)
- [ ] Timer (30 min countdown)
- [ ] Answer validation
- [ ] Score calculation
- [ ] Results display
- [ ] Google Sheets integration (zapis)

### **Sprint 2: Teacher Dashboard (1 dzień)**
- [ ] Teacher login
- [ ] Dashboard overview (statystyki)
- [ ] Student list (tabela)
- [ ] Student detail page
- [ ] Filters & search
- [ ] Export to CSV

### **Sprint 3: Notifications & Polish (0.5 dnia)**
- [ ] Email notifications (student + teacher)
- [ ] UI polish (kolory, fonty, spacing)
- [ ] Mobile responsiveness
- [ ] Error handling

### **Sprint 4: Testing & Deployment (0.5 dnia)**
- [ ] Test wszystkich funkcji
- [ ] Bug fixes
- [ ] Deployment na Streamlit Cloud
- [ ] Documentation (README)

**TOTAL: 4 dni robocze**

---

## 🧪 TESTING PLAN

### Unit Tests (kod Python)
- [ ] Score calculation (różne scenariusze)
- [ ] Timer logic
- [ ] Email formatting
- [ ] Google Sheets CRUD

### Integration Tests
- [ ] End-to-end: Student wypełnia test → wynik w Sheets
- [ ] Email delivery
- [ ] Dashboard data loading

### User Acceptance Testing (UAT)
- [ ] 5 studentów testowych
- [ ] 1 nauczyciel testowy
- [ ] Feedback loop

---

## 📊 SUCCESS METRICS (KPIs)

### MVP Success Criteria:
- ✅ 95% testów wypełnionych bez błędów technicznych
- ✅ < 1 sec czas obliczania wyniku
- ✅ 100% emaili dostarczonych (no spam)
- ✅ 0 duplikatów w bazie danych
- ✅ Pozytywny feedback od Tiny (nauczyciel)

### Long-term Metrics:
- **Adoption:** Liczba studentów korzystających z platformy
- **Reliability:** Uptime > 99%
- **Performance:** Avg load time < 2s
- **Satisfaction:** NPS > 8/10 (ankieta po teście)

---

## 🔐 DATA SCHEMA (Google Sheets)

### Arkusz: "Wyniki_Testow"
```python
{
  "timestamp": "2026-01-12T15:30:45Z",          # ISO datetime
  "email": "anna.k@example.com",                # string
  "first_name": "Anna",                         # string
  "last_name": "Kowalska",                      # string
  "student_id": "12345",                        # string (optional)
  "correct_count": 22,                          # int (0-27)
  "percentage": 81,                             # int (0-100)
  "grade": 4.5,                                 # float
  "grade_text": "Dobra Plus",                   # string
  "passed": True,                               # boolean
  "time_spent_seconds": 1635,                   # int
  "answers_json": "{...}",                      # JSON string
}
```

### Arkusz: "Teachers"
```python
{
  "email": "tina@example.com",
  "password_hash": "sha256hash...",
  "first_name": "Tina",
  "last_name": "Nawrocka",
  "role": "admin"
}
```

---

## 🛠️ TECH STACK

### Frontend + Backend
- **Streamlit** 1.30+ (Python web framework)
- **Python** 3.11+

### Libraries
```python
streamlit==1.30.0
gspread==5.12.0              # Google Sheets API
oauth2client==4.1.3          # Google auth
pandas==2.1.4                # Data manipulation
plotly==5.18.0               # Charts (opcjonalne)
python-dotenv==1.0.0         # Environment variables
smtplib                      # Email (built-in)
hashlib                      # Password hashing (built-in)
datetime                     # Timestamps (built-in)
```

### External Services
- **Google Sheets API** - database
- **SMTP (Gmail)** - email notifications
- **Streamlit Cloud** - hosting

---

## 💰 COST BREAKDOWN

### MVP (Faza 1):
| Item | Cost |
|------|------|
| Streamlit Cloud | $0/mies |
| Google Sheets API | $0 (free tier) |
| Gmail SMTP | $0 (existing account) |
| Development (Twój czas) | 4 dni |
| **TOTAL** | **$0/mies** |

### Production (Faza 2):
| Item | Cost |
|------|------|
| Domena ainetwork.pl | ~50 zł/rok (~€10) |
| Streamlit Cloud | $0/mies |
| Google Workspace (opcjonalne) | €5/user/mies |
| **TOTAL** | **~€10-70/rok** |

---

## 🎓 FUTURE ENHANCEMENTS (v2.0)

### Phase 2 Features:
- [ ] **Multi-test support** - różne testy dla różnych kursów
- [ ] **Question bank** - losowanie pytań z puli
- [ ] **Analytics dashboard** - zaawansowane wykresy
- [ ] **Certificate generation** - automatyczne certyfikaty PDF
- [ ] **API dla integracji** - webhook do innych systemów
- [ ] **Mobile app** (opcjonalnie - PWA)
- [ ] **AI proctoring** - detekcja oszustw (kamera)
- [ ] **Adaptive testing** - trudność pytań dopasowana do poziomu

### Phase 3 (Scale to AI NETWORK Platform):
- [ ] Multi-tenant (wiele szkół/kursów)
- [ ] Marketplace testów
- [ ] Payment integration (Stripe)
- [ ] White-label dla klientów B2B

---

## 📞 STAKEHOLDERS & ROLES

### Product Owner
**Jarek (ARTECH CONSULT)**
- Decyzje produktowe
- Priorityzacja features
- Feedback loops

### End Users
**Tina Nawrocka** (Nauczyciel)
- UAT testing
- Feedback na dashboard
- Requirements validation

**Studenci UKEN** (42 osoby)
- Beta testing
- UX feedback

### Developer
**Claude + Jarek**
- Implementation
- Testing
- Deployment

---

## ✅ DEFINITION OF DONE

### MVP jest gotowy gdy:
- ✅ Student może wypełnić test (27 pytań w 30 min)
- ✅ Wynik jest obliczany poprawnie
- ✅ Student widzi swoje błędy
- ✅ Nauczyciel widzi dashboard z listą studentów
- ✅ Nauczyciel może zobaczyć szczegóły każdego testu
- ✅ Dane są zapisywane w Google Sheets
- ✅ Email notifications działają (student + nauczyciel)
- ✅ Aplikacja jest wdrożona na Streamlit Cloud
- ✅ Zero critical bugs
- ✅ UAT passed by Tina

---

## 📚 APPENDIX

### A. Sample Test Data (27 pytań)
[Zawarte w: Test_Zaliczeniowy_AI_Marketing_UKEN_Final.md]

### B. Answer Key (JSON)
```json
{
  "1": "c", "2": "a", "3": "a", "4": "c", "5": "b",
  "6": "d", "7": "c", "8": "a", "9": "d", "10": "c",
  "11": "c", "12": "d", "13": "c", "14": "a", "15": "b",
  "16": "b", "17": "b", "18": "a", "19": "b", "20": "b",
  "21": "d", "22": "a", "23": "c", "24": "d", "25": "a",
  "26": "d", "27": "c"
}
```

### C. Environment Variables (.env)
```bash
# Google Sheets
GOOGLE_SHEETS_ID=your_sheet_id_here
GOOGLE_SERVICE_ACCOUNT_JSON=path/to/credentials.json

# Email (SMTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Teacher credentials
TEACHER_PASSWORD_HASH=sha256_hash_here

# App config
SESSION_TIMEOUT_MINUTES=60
TEST_TIME_LIMIT_MINUTES=30
```

---

## 🎯 NEXT STEPS

### Immediate Actions:
1. **Review PRD** - Twoje zatwierdzenie tego dokumentu
2. **Setup GitHub repo** - Nowy projekt
3. **Google Sheets setup** - Utworzenie arkusza + API credentials
4. **Start Sprint 1** - Development

### Questions for You:
- [ ] Czy wszystkie wymagania są jasne?
- [ ] Czy dashboard nauczyciela ma wszystko czego Tina potrzebuje?
- [ ] Czy chcesz zacząć od darmowej subddomeny Streamlit czy od razu kupić domenę?
- [ ] Czy są jakieś dodatkowe features które chcesz w MVP?

---

**Status:** ✅ READY FOR DEVELOPMENT  
**Estimated Timeline:** 4 dni robocze  
**Risk Level:** 🟢 LOW (proven tech stack)

---

**Prepared by:** Claude + Jarek  
**Date:** 12.01.2026  
**Version:** 1.0
