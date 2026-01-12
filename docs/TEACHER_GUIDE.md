# Teacher User Guide - AI Marketing Test Platform

**Panel Nauczyciela - Dashboard & Analytics**

---

## Quick Start

### Logowanie
1. Otwórz aplikację
2. Kliknij **"Panel Nauczyciela"**
3. Wprowadź dane logowania:
   - Email (skonfigurowany w Google Sheets)
   - Hasło
4. Kliknij **"Zaloguj się"**

**Uwaga:** Hasła są hashowane (SHA256) i przechowywane w Google Sheets.

---

## Dashboard - Przegląd

### Statystyki Globalne (4 karty)

1. **Wszystkie Testy**
   - Całkowita liczba ukończonych testów
   - Wszystkie próby wszystkich studentów

2. **Wskaźnik Zdawalności**
   - Procent testów zaliczonych
   - **Kolor:**
     - Zielony: ≥70%
     - Żółty: 50-69%
     - Czerwony: <50%

3. **Średni Wynik**
   - Średni procent ze wszystkich testów
   - Obliczany jako (suma % / liczba testów)

4. **Średnia Ocena**
   - Średnia ocena numeryczna (2.0 - 5.0)
   - Obliczana ze wszystkich wyników

### Wyniki według Kategorii

Pokazuje średnią wydajność w każdej z 5 kategorii:
- Podstawy AI w Marketingu
- Modele LLM i ich zastosowania
- Strategia i praktyczne zastosowania
- Nowa era marketingu
- Zaawansowane koncepcje AI

**Dla każdej kategorii:**
- Pasek postępu (wizualizacja)
- Średnia poprawnych/wszystkich
- Procent średni
- Liczba analizowanych studentów

**Kolory:**
- 🟢 Zielony: ≥80%
- 🟡 Żółty: ≥60%
- 🔴 Czerwony: <60%

### Najtrudniejsze Pytania

Top 5 pytań z najniższym wskaźnikiem poprawnych odpowiedzi:
- Numer pytania
- Kategoria
- Liczba poprawnych/wszystkich prób
- Procent poprawnych
- Kolorowanie jak wyżej

**Użycie:** Zidentyfikuj tematy wymagające dodatkowego omówienia.

---

## Lista Wyników Studentów

### Filtry

**Status:**
- Wszystkie
- Zaliczeni (≥48%)
- Niezaliczeni (<48%)

**Sortowanie:**
- Data (najnowsze/najstarsze)
- Wynik (najwyższy/najniższy)
- Nazwisko (A-Z/Z-A)

**Limit:**
- 10, 25, 50, 100, Wszystkie

**Odśwież:** Czyści cache i pobiera najnowsze dane z Google Sheets

### Karty Wyników

Każda karta pokazuje:
- ✅/❌ Status (zaliczony/niezaliczony)
- Imię i nazwisko studenta
- Email i ID studenta (jeśli podany)
- Data i czas testu
- Duży procent wyniku
- Ocena i opis
- Poprawne odpowiedzi (X/27)
- Czas rozwiązywania
- ⏰ Indicator auto-submit (jeśli dotyczy)

**Kolory:**
- Zielona ramka: Zaliczony
- Czerwona ramka: Niezaliczony

---

## Eksport Danych

### CSV Export

Kliknij **"📥 Pobierz CSV"** aby wyeksportować:
- Wszystkie dane z widoku (z zastosowanymi filtrami)
- Wszystkie kolumny z Google Sheets
- Nazwa pliku: `wyniki_testow_YYYYMMDD_HHMMSS.csv`

**Użycie:**
- Analiza w Excel/Google Sheets
- Tworzenie raportów
- Archiwizacja wyników
- Import do innych systemów

---

## Szczegóły Studenta

### Wyszukiwanie

1. W dashboardzie przewiń do góry
2. Kliknij przycisk lub przejdź do "Szczegóły Studenta" (zależy od nawigacji)
3. Wprowadź email studenta
4. Kliknij **"Wyszukaj"**

### Widok Szczegółowy

**Główna Karta:**
- Duża karta ze statusem (zaliczony/niezaliczony)
- Procent, ocena, poprawne odpowiedzi
- Czas rozwiązywania
- Info o auto-submit (jeśli dotyczy)

**Wyniki według Kategorii:**
- Wszystkie 5 kategorii z paskami postępu
- Dokładne wyniki per kategoria

**Szczegółowe Odpowiedzi:**
- Wszystkie 27 pytań po kolei
- Treść pytania i kategoria
- Odpowiedź studenta (podświetlona)
- Poprawna odpowiedź (podświetlona)
- Wyjaśnienie do każdego pytania
- Ikony ✅/❌ przy każdym pytaniu

**Metadata:**
- Czas rozpoczęcia testu
- Czas zakończenia testu
- Auto-save checkpointy (5, 10, 15, 20, 25)
- Informacje o przeglądarce
- Numer próby
- Wersja testu

---

## Email Notifications

System automatycznie wysyła emaile:

### Email do Studenta
**Gdy:** Po zakończeniu testu
**Zawiera:**
- Status (zaliczony/niezaliczony)
- Procent i ocena
- Wyniki według kategorii
- Czas rozwiązywania

### Email do Nauczyciela
**Gdy:** Po zakończeniu testu przez studenta
**Zawiera:**
- Dane studenta (imię, nazwisko, email)
- Status wyniku
- Procent, ocena, poprawne odpowiedzi
- Wyniki kategorii
- Data i czas testu
- Info o auto-submit

**Konfiguracja:** Zobacz DEPLOYMENT_GUIDE.md

---

## Google Sheets Integration

### Arkusz: Wyniki_Testow

**Kolumny:**
- A: Timestamp
- B: Email
- C: First_Name
- D: Last_Name
- E: Student_ID
- F: Correct_Count
- G: Percentage
- H: Grade
- I: Grade_Text
- J: Status
- K: Time_Spent_Minutes
- L: Details_JSON (szczegóły w JSON)
- M: Test_Version
- N: Browser_Info
- O: Attempt_Number
- P: Auto_Submitted
- Q: Zdany (formuła)
- R: Czas_Sekundy (formuła)

**Cache:** Dane cachowane przez 60 sekund. Użyj przycisku "Odśwież" aby wymusić odświeżenie.

---

## Najczęstsze Pytania

### Q: Jak często dane są aktualizowane?
**A:** Dashboard używa cache 60s. Kliknij "Odśwież" aby zaktualizować.

### Q: Czy mogę edytować wyniki w Google Sheets?
**A:** Technicznie tak, ale niezalecane. System może nie odzwierciedlić zmian poprawnie.

### Q: Co oznacza "Auto_Submitted"?
**A:** Test został automatycznie wysłany po upływie 30 minut.

### Q: Jak zmienić hasło?
**A:** Edytuj Google Sheets, zakładka "Teachers", wygeneruj nowy hash SHA256.

### Q: Czy mogę dodać więcej nauczycieli?
**A:** Tak, dodaj wiersz w Google Sheets "Teachers" z emailem i hashem hasła.

### Q: Jak zresetować test studenta?
**A:** Usuń wiersz z wynikami w Google Sheets. Student może podejść ponownie.

### Q: Gdzie są zapisane pytania testowe?
**A:** W pliku `data/questions.json` (27 pytań).

### Q: Czy mogę zmienić pytania?
**A:** Tak, edytuj `data/questions.json` zachowując strukturę JSON.

### Q: Jak zmienić próg zaliczenia?
**A:** Edytuj `data/test_config.json`, pole `pass_threshold_percentage`.

### Q: Jak wydłużyć czas testu?
**A:** Edytuj `data/test_config.json`, pole `duration_minutes`.

---

## Wskazówki

### Analiza Wyników
1. **Identyfikuj słabe punkty:** Sprawdź najtrudniejsze pytania
2. **Trendy kategorii:** Zobacz które kategorie są najtrudniejsze
3. **Wskaźnik zdawalności:** Monitoruj ogólną efektywność
4. **Czas rozwiązywania:** Sprawdź czy studenci mają dość czasu

### Przygotowanie Studentów
1. Poinformuj o zasadach testu (30 min, 27 pytań, 48%)
2. Udostępnij przewodnik studenta
3. Przeprowadź test próbny (opcjonalnie)
4. Upewnij się, że mają link i dane do logowania

### Monitoring Podczas Testu
1. Sprawdzaj emaile o nowych wynikach
2. Monitoruj Google Sheets
3. Bądź dostępny na pytania techniczne

### Po Teście
1. Przeanalizuj wyniki
2. Zidentyfikuj tematy do omówienia
3. Udostępnij feedback studentom
4. Eksportuj wyniki do archiwum

---

## Troubleshooting

### Problem: Brak dostępu do dashboardu
**Rozwiązanie:**
1. Sprawdź dane logowania
2. Zweryfikuj email i hash hasła w Google Sheets
3. Wyloguj i zaloguj ponownie

### Problem: Nie widzę najnowszych wyników
**Rozwiązanie:**
1. Kliknij przycisk "Odśwież"
2. Sprawdź Google Sheets bezpośrednio
3. Wyczyść cache przeglądarki

### Problem: Emaile nie są wysyłane
**Rozwiązanie:**
1. Sprawdź konfigurację SMTP w secrets.toml
2. Zweryfikuj app password Gmail
3. Sprawdź folder SPAM

### Problem: Błąd przy eksporcie CSV
**Rozwiązanie:**
1. Sprawdź czy są dane do eksportu
2. Spróbuj ponownie po odświeżeniu
3. Sprawdź uprawnienia do zapisu plików

---

## Best Practices

### Bezpieczeństwo
- ✅ Nie udostępniaj danych logowania
- ✅ Regularnie zmieniaj hasło
- ✅ Monitoruj nieautoryzowany dostęp
- ✅ Zachowuj kopie zapasowe Google Sheets

### Zarządzanie Testami
- ✅ Zaplanuj testy z wyprzedzeniem
- ✅ Poinformuj studentów o dacie
- ✅ Przygotuj plan B na wypadek problemów
- ✅ Archiwizuj wyniki po zakończeniu semestru

### Komunikacja
- ✅ Jasne instrukcje dla studentów
- ✅ Dostępność podczas testu
- ✅ Szybka odpowiedź na pytania
- ✅ Feedback po teście

---

## Kontakt i Wsparcie

### Problemy Techniczne
1. Sprawdź DEPLOYMENT_GUIDE.md
2. Przejrzyj logi aplikacji
3. Sprawdź Google Sheets API quota
4. Skontaktuj się z administratorem systemu

### Pytania o Funkcjonalność
- Zobacz dokumentację w `/docs`
- Przeczytaj handoff documents
- Sprawdź FAQ

---

**Powodzenia w prowadzeniu testów!** 🎓

**Dokument:** Teacher User Guide v1.0
**Data:** 2026-01-12
**Status:** Gotowy do użytku
