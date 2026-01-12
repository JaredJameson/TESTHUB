# 🎨 UI/UX DESIGN GUIDELINES
## AI Marketing Test Platform - Visual Design System

**Version:** 1.0  
**Date:** 2026-01-12  
**Design Philosophy:** Minimalist, Professional, Functional

---

## TABLE OF CONTENTS

1. [Design Principles](#1-design-principles)
2. [Color Palette](#2-color-palette)
3. [Typography](#3-typography)
4. [Layout & Spacing](#4-layout--spacing)
5. [Components](#5-components)
6. [Page Templates](#6-page-templates)
7. [Responsive Design](#7-responsive-design)
8. [Accessibility](#8-accessibility)
9. [Implementation](#9-implementation)

---

## 1. DESIGN PRINCIPLES

### 1.1 Core Philosophy
```
MINIMALISM: Less is more - only essential elements
CLARITY: Clear hierarchy and purpose of every element
FUNCTIONALITY: Design serves the user's goal
PROFESSIONALISM: Business-appropriate aesthetic
```

### 1.2 Key Rules
- NO emojis anywhere in the interface
- NO decorative icons unless functional
- NO rounded corners (sharp, clean rectangles)
- NO shadows or 3D effects
- NO gradients
- NO animations or transitions (instant state changes)
- NO colorful illustrations

### 1.3 Visual Hierarchy
```
1. Typography size (largest = most important)
2. Black borders to define sections
3. Yellow accents for interactive elements
4. White space for breathing room
```

---

## 2. COLOR PALETTE

### 2.1 Primary Colors

```css
/* Primary Yellow - Interactive elements, accents */
--primary-yellow: #FFD700;
--primary-yellow-hover: #FFC700;
--primary-yellow-active: #E6BE00;

/* Neutral Gray - Backgrounds */
--bg-gray-light: #F5F5F5;
--bg-gray-medium: #E8E8E8;
--bg-white: #FFFFFF;

/* Text & Borders */
--text-black: #000000;
--border-black: #000000;

/* Status Colors - Minimal use */
--status-pass: #2D5016;    /* Dark green for passed */
--status-fail: #8B0000;    /* Dark red for failed */
```

### 2.2 Color Usage Rules

```
BACKGROUNDS:
- Main background: #F5F5F5 (light gray)
- Card/container background: #FFFFFF (white)
- Input field background: #FFFFFF (white)

BORDERS:
- All borders: #000000 (black), 1px solid
- No border radius (0px)

TEXT:
- Primary text: #000000 (black)
- All text is black - no gray text

ACCENTS:
- Buttons: #FFD700 (yellow) background
- Links: #000000 (black) with yellow underline
- Active states: Yellow background
- Focus states: Yellow border

STATUS INDICATORS:
- Passed: #2D5016 (dark green) - text only, no background
- Failed: #8B0000 (dark red) - text only, no background
```

### 2.3 Color Application Examples

```
Primary Button:
  background: #FFD700
  color: #000000
  border: 1px solid #000000

Secondary Button:
  background: #FFFFFF
  color: #000000
  border: 1px solid #000000

Input Field:
  background: #FFFFFF
  color: #000000
  border: 1px solid #000000

Card/Container:
  background: #FFFFFF
  border: 1px solid #000000

Table Header:
  background: #E8E8E8
  color: #000000
  border: 1px solid #000000
```

---

## 3. TYPOGRAPHY

### 3.1 Font Family

```css
/* Primary font for all text */
font-family: 'Poppins', sans-serif;

/* Import from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
```

### 3.2 Font Weights

```css
--font-light: 300;      /* Rarely used */
--font-regular: 400;    /* Body text */
--font-medium: 500;     /* Subheadings */
--font-semibold: 600;   /* Headings */
--font-bold: 700;       /* Page titles, emphasis */
```

### 3.3 Type Scale

```css
/* Headings */
h1: 32px / 600 / black / line-height: 1.2
h2: 24px / 600 / black / line-height: 1.3
h3: 20px / 600 / black / line-height: 1.4
h4: 18px / 500 / black / line-height: 1.4

/* Body text */
body-large: 18px / 400 / black / line-height: 1.6
body-regular: 16px / 400 / black / line-height: 1.6
body-small: 14px / 400 / black / line-height: 1.5

/* UI elements */
button-text: 16px / 600 / black
label-text: 14px / 500 / black
caption-text: 12px / 400 / black
```

### 3.4 Typography Usage

```
PAGE TITLE:
  font-size: 32px
  font-weight: 600
  color: #000000
  margin-bottom: 32px

SECTION HEADING:
  font-size: 24px
  font-weight: 600
  color: #000000
  margin-bottom: 24px

BODY TEXT:
  font-size: 16px
  font-weight: 400
  color: #000000
  line-height: 1.6

BUTTON TEXT:
  font-size: 16px
  font-weight: 600
  color: #000000
  text-transform: none (no uppercase)

LABEL:
  font-size: 14px
  font-weight: 500
  color: #000000
  margin-bottom: 8px
```

### 3.5 Text Formatting Rules

```
- NO text-transform: uppercase (use sentence case)
- NO italic text (use bold for emphasis)
- NO underline except for links
- NO text shadows
- NO letter-spacing adjustments
```

---

## 4. LAYOUT & SPACING

### 4.1 Grid System

```css
/* 12-column grid */
Container max-width: 1200px
Column gap: 24px
Padding: 40px (desktop), 20px (mobile)
```

### 4.2 Spacing Scale

```css
/* 8px base unit */
--space-xs: 8px;
--space-sm: 16px;
--space-md: 24px;
--space-lg: 32px;
--space-xl: 48px;
--space-xxl: 64px;
```

### 4.3 Spacing Usage

```
BETWEEN SECTIONS:
  margin-bottom: 48px (--space-xl)

BETWEEN COMPONENTS:
  margin-bottom: 32px (--space-lg)

BETWEEN ELEMENTS:
  margin-bottom: 24px (--space-md)

INSIDE COMPONENTS:
  padding: 24px (--space-md)

FORM FIELDS:
  margin-bottom: 16px (--space-sm)
  label margin-bottom: 8px (--space-xs)
```

### 4.4 Container Styles

```css
/* Main container */
.main-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px;
  background: #F5F5F5;
}

/* Content card */
.content-card {
  background: #FFFFFF;
  border: 1px solid #000000;
  padding: 32px;
  margin-bottom: 32px;
}

/* Section divider */
.section-divider {
  border-top: 1px solid #000000;
  margin: 48px 0;
}
```

---

## 5. COMPONENTS

### 5.1 Buttons

```css
/* Primary Button */
.btn-primary {
  background: #FFD700;
  color: #000000;
  border: 1px solid #000000;
  padding: 12px 32px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: none;
}

.btn-primary:hover {
  background: #FFC700;
}

.btn-primary:active {
  background: #E6BE00;
}

.btn-primary:disabled {
  background: #E8E8E8;
  cursor: not-allowed;
}

/* Secondary Button */
.btn-secondary {
  background: #FFFFFF;
  color: #000000;
  border: 1px solid #000000;
  padding: 12px 32px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.btn-secondary:hover {
  background: #F5F5F5;
}

/* Button Sizes */
.btn-large {
  padding: 16px 48px;
  font-size: 18px;
}

.btn-small {
  padding: 8px 24px;
  font-size: 14px;
}
```

**Button Examples:**
```
[Rozpocznij Test]     <- Primary, Large
[Wyślij]              <- Primary, Regular
[Anuluj]              <- Secondary, Regular
[Zobacz szczegóły]    <- Secondary, Small
```

### 5.2 Input Fields

```css
/* Text Input */
.input-field {
  background: #FFFFFF;
  color: #000000;
  border: 1px solid #000000;
  padding: 12px 16px;
  font-size: 16px;
  font-family: 'Poppins', sans-serif;
  width: 100%;
}

.input-field:focus {
  border: 2px solid #FFD700;
  outline: none;
}

.input-field:disabled {
  background: #E8E8E8;
  cursor: not-allowed;
}

/* Input with Label */
<div class="input-group">
  <label>Email</label>
  <input type="email" class="input-field" placeholder="jan.kowalski@example.com">
</div>

.input-group {
  margin-bottom: 16px;
}

.input-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #000000;
  margin-bottom: 8px;
}
```

### 5.3 Radio Buttons (Test Questions)

```css
/* Radio button container */
.radio-group {
  margin-bottom: 24px;
}

/* Individual radio option */
.radio-option {
  background: #FFFFFF;
  border: 1px solid #000000;
  padding: 16px;
  margin-bottom: 8px;
  cursor: pointer;
}

.radio-option:hover {
  background: #F5F5F5;
}

.radio-option.selected {
  background: #FFD700;
  border: 2px solid #000000;
}

.radio-option input[type="radio"] {
  margin-right: 12px;
}

.radio-option label {
  font-size: 16px;
  font-weight: 400;
  cursor: pointer;
}
```

**Example:**
```
┌─────────────────────────────────────────────┐
│ ○ a) Zbyt wysokie koszty                    │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│ ● c) Generyczny output                      │  <- Selected (yellow bg)
└─────────────────────────────────────────────┘
```

### 5.4 Tables

```css
/* Table container */
.table-container {
  background: #FFFFFF;
  border: 1px solid #000000;
  overflow-x: auto;
}

/* Table */
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

/* Table header */
thead {
  background: #E8E8E8;
}

th {
  padding: 16px;
  text-align: left;
  font-weight: 600;
  border: 1px solid #000000;
}

/* Table body */
td {
  padding: 16px;
  border: 1px solid #000000;
}

/* Striped rows */
tbody tr:nth-child(even) {
  background: #F5F5F5;
}

/* Hover effect */
tbody tr:hover {
  background: #FFD700;
}
```

**Table Example:**
```
┌────────────┬──────────┬───────┬────────┐
│ Imię       │ Nazwisko │ Wynik │ Status │
├────────────┼──────────┼───────┼────────┤
│ Anna       │ Kowalska │ 22/27 │ ZALICZ │
│ Jan        │ Nowak    │ 18/27 │ ZALICZ │
│ Maria      │ Wiśniews │ 12/27 │ NIEZAL │
└────────────┴──────────┴───────┴────────┘
```

### 5.5 Cards

```css
/* Card container */
.card {
  background: #FFFFFF;
  border: 1px solid #000000;
  padding: 24px;
  margin-bottom: 24px;
}

/* Card header */
.card-header {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #000000;
}

/* Card body */
.card-body {
  font-size: 16px;
  line-height: 1.6;
}

/* Card footer */
.card-footer {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #000000;
}
```

### 5.6 Progress Bar

```css
/* Progress container */
.progress-container {
  background: #FFFFFF;
  border: 1px solid #000000;
  height: 24px;
  margin-bottom: 24px;
}

/* Progress fill */
.progress-fill {
  background: #FFD700;
  height: 100%;
  transition: none;
  border-right: 1px solid #000000;
}

/* Progress text */
.progress-text {
  font-size: 14px;
  font-weight: 600;
  text-align: center;
  line-height: 24px;
}
```

**Example:**
```
┌──────────────────────────────────────┐
│████████████████░░░░░░░░░░│ 15/27 (56%)│
└──────────────────────────────────────┘
```

### 5.7 Timer Display

```css
/* Timer container */
.timer {
  background: #FFFFFF;
  border: 2px solid #000000;
  padding: 16px 32px;
  font-size: 24px;
  font-weight: 600;
  text-align: center;
  display: inline-block;
}

/* Timer warning state (< 5 minutes) */
.timer.warning {
  background: #FFD700;
}
```

**Example:**
```
┌─────────────┐
│ Czas: 28:45 │
└─────────────┘
```

### 5.8 Status Badges

```css
/* Status badge */
.status-badge {
  display: inline-block;
  padding: 4px 12px;
  font-size: 14px;
  font-weight: 600;
  border: 1px solid #000000;
}

.status-badge.passed {
  color: #2D5016;
  background: #FFFFFF;
}

.status-badge.failed {
  color: #8B0000;
  background: #FFFFFF;
}
```

**Example:**
```
┌──────────┐  ┌────────────┐
│ ZALICZONY│  │ NIEZALICZONY│
└──────────┘  └────────────┘
```

### 5.9 Alerts/Messages

```css
/* Alert container */
.alert {
  background: #FFFFFF;
  border: 2px solid #000000;
  padding: 16px 24px;
  margin-bottom: 24px;
  font-size: 16px;
}

.alert.info {
  border-left: 4px solid #000000;
}

.alert.warning {
  border-left: 4px solid #FFD700;
}

.alert.error {
  border-left: 4px solid #8B0000;
}

.alert.success {
  border-left: 4px solid #2D5016;
}
```

### 5.10 Navigation

```css
/* Tab navigation */
.nav-tabs {
  display: flex;
  border-bottom: 1px solid #000000;
  margin-bottom: 32px;
}

.nav-tab {
  padding: 16px 32px;
  font-size: 16px;
  font-weight: 500;
  background: #FFFFFF;
  border: 1px solid #000000;
  border-bottom: none;
  cursor: pointer;
  margin-right: 8px;
}

.nav-tab:hover {
  background: #F5F5F5;
}

.nav-tab.active {
  background: #FFD700;
  font-weight: 600;
}
```

---

## 6. PAGE TEMPLATES

### 6.1 Landing Page Layout

```
┌─────────────────────────────────────────────┐
│                   HEADER                     │
│         AI NETWORK Test Platform             │
│                                              │
│         Test Zaliczeniowy                    │
│         AI w Marketingu                      │
│                                              │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│                                              │
│   Informacje o teście:                      │
│   - Liczba pytań: 27                        │
│   - Czas trwania: 30 minut                  │
│   - Próg zaliczenia: 48%                    │
│                                              │
│   ┌─────────────────┐ ┌──────────────────┐ │
│   │ Jestem Studentem│ │ Jestem Nauczycielem│
│   └─────────────────┘ └──────────────────┘ │
│                                              │
└─────────────────────────────────────────────┘
```

### 6.2 Student Login Layout

```
┌─────────────────────────────────────────────┐
│                   HEADER                     │
│         Logowanie - Student                  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│                                              │
│   Email                                     │
│   ┌──────────────────────────────────────┐ │
│   │ jan.kowalski@example.com             │ │
│   └──────────────────────────────────────┘ │
│                                              │
│   Imię                                      │
│   ┌──────────────────────────────────────┐ │
│   │ Jan                                   │ │
│   └──────────────────────────────────────┘ │
│                                              │
│   Nazwisko                                  │
│   ┌──────────────────────────────────────┐ │
│   │ Kowalski                              │ │
│   └──────────────────────────────────────┘ │
│                                              │
│   Numer indeksu (opcjonalnie)              │
│   ┌──────────────────────────────────────┐ │
│   │ 12345                                 │ │
│   └──────────────────────────────────────┘ │
│                                              │
│   ┌──────────────────┐                     │
│   │ Rozpocznij Test  │                     │
│   └──────────────────┘                     │
│                                              │
└─────────────────────────────────────────────┘
```

### 6.3 Test Interface Layout

```
┌─────────────────────────────────────────────┐
│ AI Marketing Test | Student: Jan Kowalski   │
│ Czas: 28:45 | Postęp: ████░░░░ 15/27       │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│                                              │
│ Pytanie 15 / 27                             │
│                                              │
│ Główny problem generycznego AI prospectingu │
│ który powoduje jego porażkę to:             │
│                                              │
│ ┌─────────────────────────────────────────┐│
│ │ ○ a) Zbyt wysokie koszty                ││
│ └─────────────────────────────────────────┘│
│ ┌─────────────────────────────────────────┐│
│ │ ○ b) Brak dostępu do najnowszych modeli ││
│ └─────────────────────────────────────────┘│
│ ┌─────────────────────────────────────────┐│
│ │ ● c) Generyczny output                  ││ <- Selected
│ └─────────────────────────────────────────┘│
│ ┌─────────────────────────────────────────┐│
│ │ ○ d) Wolna szybkość generowania         ││
│ └─────────────────────────────────────────┘│
│                                              │
│ ┌──────────────┐      ┌──────────────────┐ │
│ │ Poprzednie   │      │ Następne pytanie │ │
│ └──────────────┘      └──────────────────┘ │
│                                              │
└─────────────────────────────────────────────┘
```

### 6.4 Results Display Layout

```
┌─────────────────────────────────────────────┐
│              TEST ZAKOŃCZONY                 │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│                                              │
│ Twój wynik: 22 / 27 (81%)                   │
│ Ocena: 4.5 - Dobra Plus                     │
│ Status: ZALICZONY                           │
│                                              │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ SZCZEGÓŁOWE WYNIKI                          │
│                                              │
│ ┌──┬─────────┬──────────┬────────┬────────┐│
│ │#│ Twoja   │ Poprawna │ Status │ Pytanie││
│ ├──┼─────────┼──────────┼────────┼────────┤│
│ │1 │ c       │ c        │ TAK    │[...] ││
│ │2 │ a       │ a        │ TAK    │[...] ││
│ │3 │ b       │ a        │ NIE    │[...] ││
│ └──┴─────────┴──────────┴────────┴────────┘│
│                                              │
│ Email z wynikami został wysłany              │
│                                              │
│ ┌────────────────┐                          │
│ │ Zamknij        │                          │
│ └────────────────┘                          │
│                                              │
└─────────────────────────────────────────────┘
```

### 6.5 Teacher Dashboard Layout

```
┌─────────────────────────────────────────────┐
│ DASHBOARD NAUCZYCIELA | Witaj, Tina         │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ STATYSTYKI OGÓLNE                           │
│                                              │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│ │   42     │ │   38     │ │   4.2    │    │
│ │ Studentów│ │ Zaliczył │ │ Średnia  │    │
│ └──────────┘ └──────────┘ └──────────┘    │
│                                              │
│ Średni wynik: 19.8 / 27 (73%)               │
│ Najtrudniejsze pytanie: 23 (34%)            │
│ Najłatwiejsze pytanie: 2 (96%)              │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ LISTA STUDENTÓW                             │
│                                              │
│ [Filtr: Wszyscy ▼] [Szukaj: ___________]   │
│                                              │
│ ┌─────────────────────────────────────────┐│
│ │ Anna Kowalska | 22/27 | 4.5 | ZALICZONY ││
│ │ anna.k@example.com | 12.01 15:30        ││
│ │ [Zobacz szczegóły]                      ││
│ ├─────────────────────────────────────────┤│
│ │ Jan Nowak | 18/27 | 3.5 | ZALICZONY     ││
│ │ jan.n@example.com | 12.01 14:45         ││
│ │ [Zobacz szczegóły]                      ││
│ └─────────────────────────────────────────┘│
│                                              │
│ ┌──────────────┐                            │
│ │ Eksportuj CSV│                            │
│ └──────────────┘                            │
│                                              │
└─────────────────────────────────────────────┘
```

### 6.6 Student Detail View Layout

```
┌─────────────────────────────────────────────┐
│ ← Powrót do Dashboard                       │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Anna Kowalska                               │
│ anna.kowalska@example.com                   │
│ Data testu: 12.01.2026, 15:30               │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ WYNIK                                        │
│                                              │
│ 22 / 27 (81%)                               │
│ Ocena: 4.5 - Dobra Plus                     │
│ Status: ZALICZONY                           │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ SZCZEGÓŁOWA ANALIZA                         │
│                                              │
│ [✓] Pokaż tylko błędne                      │
│                                              │
│ Pytanie 1: TAK                              │
│ "Kiedy warto stosować szczegółowe prompty?" │
│ Odpowiedź studenta: c                       │
│ Poprawna odpowiedź: c                       │
│                                              │
│ ────────────────────────────────────────    │
│                                              │
│ Pytanie 3: NIE                              │
│ "Co oznacza pojęcie okno kontekstowe?"      │
│ Odpowiedź studenta: b                       │
│ Poprawna odpowiedź: a                       │
│                                              │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ ANALIZA WG KATEGORII                        │
│                                              │
│ Podstawy AI: 4/5 (80%)                      │
│ Modele LLM: 3/5 (60%)                       │
│ Strategia: 5/5 (100%)                       │
│ Nowa era: 4/5 (80%)                         │
│ Zaawansowane: 6/7 (86%)                     │
└─────────────────────────────────────────────┘
```

---

## 7. RESPONSIVE DESIGN

### 7.1 Breakpoints

```css
/* Mobile First Approach */
--mobile: 320px - 767px
--tablet: 768px - 1023px
--desktop: 1024px+

/* Media queries */
@media (min-width: 768px) { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
```

### 7.2 Mobile Adjustments

```css
/* Mobile (320px - 767px) */
.main-container {
  padding: 20px;  /* Reduced from 40px */
}

.content-card {
  padding: 16px;  /* Reduced from 32px */
}

h1 {
  font-size: 24px;  /* Reduced from 32px */
}

h2 {
  font-size: 20px;  /* Reduced from 24px */
}

.btn-primary, .btn-secondary {
  width: 100%;  /* Full width buttons */
  padding: 16px;  /* Larger touch target */
}

table {
  font-size: 12px;  /* Smaller text */
}

.timer {
  font-size: 20px;  /* Reduced from 24px */
}
```

### 7.3 Touch Targets

```css
/* Minimum 44px x 44px for touch targets (iOS guidelines) */
.btn, .radio-option, .nav-tab {
  min-height: 44px;
  min-width: 44px;
}
```

---

## 8. ACCESSIBILITY

### 8.1 Color Contrast

```
Text on Background:
- Black (#000000) on White (#FFFFFF) = 21:1 (AAA)
- Black (#000000) on Light Gray (#F5F5F5) = 19.8:1 (AAA)
- Black (#000000) on Yellow (#FFD700) = 6.9:1 (AA)

Status Colors:
- Dark Green (#2D5016) on White = 8.3:1 (AAA)
- Dark Red (#8B0000) on White = 9.1:1 (AAA)
```

### 8.2 Keyboard Navigation

```css
/* Focus states for all interactive elements */
*:focus {
  outline: 2px solid #FFD700;
  outline-offset: 2px;
}

/* Skip to content link */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #FFD700;
  color: #000000;
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

### 8.3 Screen Reader Support

```html
<!-- Semantic HTML -->
<header>...</header>
<nav>...</nav>
<main>...</main>
<footer>...</footer>

<!-- ARIA labels -->
<button aria-label="Rozpocznij test">Rozpocznij Test</button>
<input type="email" aria-required="true" aria-describedby="email-help">

<!-- Alt text for images -->
<img src="logo.png" alt="AI NETWORK Logo">

<!-- Status announcements -->
<div role="status" aria-live="polite">
  Test został zapisany
</div>
```

### 8.4 Form Validation

```html
<!-- Clear error messages -->
<div class="input-group error">
  <label for="email">Email</label>
  <input type="email" id="email" aria-invalid="true">
  <span class="error-message" role="alert">
    Wprowadź poprawny adres email
  </span>
</div>
```

---

## 9. IMPLEMENTATION

### 9.1 Streamlit Custom CSS

```python
# Import in main app file
def load_custom_css():
    """Load custom CSS for Streamlit"""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Streamlit overrides */
    .stApp {
        background-color: #F5F5F5;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Button styles */
    .stButton > button {
        background: #FFD700;
        color: #000000;
        border: 1px solid #000000;
        border-radius: 0;
        padding: 12px 32px;
        font-size: 16px;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
    }
    
    .stButton > button:hover {
        background: #FFC700;
        border: 1px solid #000000;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: #FFFFFF;
        color: #000000;
        border: 1px solid #000000;
        border-radius: 0;
        font-family: 'Poppins', sans-serif;
    }
    
    .stTextInput > div > div > input:focus {
        border: 2px solid #FFD700;
        box-shadow: none;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: #FFFFFF;
        border: 1px solid #000000;
        padding: 16px;
        margin-bottom: 8px;
    }
    
    .stRadio > div:hover {
        background: #F5F5F5;
    }
    
    /* Cards */
    .element-container {
        background: #FFFFFF;
        border: 1px solid #000000;
        padding: 24px;
        margin-bottom: 24px;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #000000;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    
    h1 { font-size: 32px; }
    h2 { font-size: 24px; }
    h3 { font-size: 20px; }
    
    /* Text */
    p, div, span {
        color: #000000;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Tables */
    table {
        border-collapse: collapse;
        width: 100%;
        border: 1px solid #000000;
    }
    
    th {
        background: #E8E8E8;
        border: 1px solid #000000;
        padding: 16px;
        text-align: left;
        font-weight: 600;
    }
    
    td {
        border: 1px solid #000000;
        padding: 16px;
    }
    
    tr:nth-child(even) {
        background: #F5F5F5;
    }
    
    tr:hover {
        background: #FFD700;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: #FFFFFF;
        border: 1px solid #000000;
    }
    
    .stProgress > div > div > div {
        background: #FFD700;
        border-right: 1px solid #000000;
    }
    
    /* Alerts */
    .stAlert {
        background: #FFFFFF;
        border: 2px solid #000000;
        border-radius: 0;
    }
    
    /* Remove all border-radius */
    * {
        border-radius: 0 !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
```

### 9.2 Component Examples

```python
# Custom button
def custom_button(label, key=None, type="primary"):
    """Custom styled button"""
    if type == "primary":
        css_class = "btn-primary"
    else:
        css_class = "btn-secondary"
    
    button = st.button(label, key=key)
    return button

# Custom card
def custom_card(title, content):
    """Custom card component"""
    st.markdown(f"""
    <div class="custom-card">
        <div class="card-header">{title}</div>
        <div class="card-body">{content}</div>
    </div>
    """, unsafe_allow_html=True)

# Status badge
def status_badge(passed):
    """Status badge component"""
    if passed:
        badge_class = "status-badge passed"
        text = "ZALICZONY"
    else:
        badge_class = "status-badge failed"
        text = "NIEZALICZONY"
    
    st.markdown(f"""
    <span class="{badge_class}">{text}</span>
    """, unsafe_allow_html=True)
```

### 9.3 Layout Helpers

```python
# Centered container
def centered_container(width="1200px"):
    """Create centered container"""
    st.markdown(f"""
    <div style="max-width: {width}; margin: 0 auto; padding: 40px;">
    """, unsafe_allow_html=True)

# Section divider
def section_divider():
    """Add section divider"""
    st.markdown('<hr style="border-top: 1px solid #000000; margin: 48px 0;">', 
                unsafe_allow_html=True)

# Three column layout
def three_column_stats(stat1, stat2, stat3):
    """Display three statistics in columns"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stat1['value']}</div>
            <div class="stat-label">{stat1['label']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Repeat for col2 and col3
```

---

## 10. DESIGN CHECKLIST

### Before Implementation:
- [ ] Poppins font loaded from Google Fonts
- [ ] All colors defined (#F5F5F5, #FFD700, #000000)
- [ ] No emojis in design files
- [ ] All borders are 1px solid black
- [ ] No border-radius on any element
- [ ] Yellow used only for accents/interactions

### During Development:
- [ ] Test on mobile (320px width minimum)
- [ ] Verify color contrast (WCAG AA minimum)
- [ ] Test keyboard navigation
- [ ] Verify focus states visible
- [ ] Check all text is black (#000000)

### Before Launch:
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Screen reader testing
- [ ] Mobile responsiveness verified
- [ ] All interactive elements have 44px+ touch targets
- [ ] Performance: page load < 2 seconds

---

## 11. DESIGN ASSETS

### 11.1 Logo
```
File: assets/logo.png
Size: 200x200px
Format: PNG with transparency
Colors: Black and yellow only
```

### 11.2 Favicon
```
File: assets/favicon.ico
Size: 32x32px
Format: ICO
Colors: Black and yellow
```

### 11.3 Email Templates
```
Files:
- email_student_pass.html
- email_student_fail.html
- email_teacher.html

Design:
- Same color scheme
- Simple table layout
- No images except logo
- Black text on white background
```

---

## 12. FORBIDDEN ELEMENTS

### NEVER USE:
```
❌ Emojis (anywhere)
❌ Rounded corners
❌ Drop shadows
❌ Gradients
❌ Colorful icons
❌ Animations/transitions
❌ Multiple colors for text
❌ Decorative images
❌ Comic fonts
❌ Italic text (except in rare cases)
```

### ALWAYS USE:
```
✅ Poppins font
✅ Black borders (1px solid)
✅ Yellow for interactive elements
✅ White/light gray backgrounds
✅ Clear hierarchy through size
✅ Plenty of white space
✅ Simple, functional design
```

---

**Design Status:** ✅ APPROVED FOR DEVELOPMENT  
**Design System:** Minimalist Professional  
**Brand:** AI NETWORK  
**Last Updated:** 2026-01-12
