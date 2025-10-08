# Product Requirements Document (PRD)
## Food Planning & Cooking App for Families

### 1. Overview
**Product Name:** FamilyMeal (working title)
**Version:** 1.0
**Date:** 2025-10-01
**Owner:** Martin Šimo

**Purpose:** Aplikácia na plánovanie jedál, tvorbu týždenného menu a generovanie nákupných zoznamov pre rodiny.

---

### 2. Product Goals
- Zjednodušiť proces plánovania jedál pre celý týždeň
- Automatizovať tvorbu nákupného zoznamu
- Centralizovať recepty a jedlá na jednom mieste
- Ušetriť čas pri rozhodovaní "čo dnes na obed/večeru"

---

### 3. Target Users
- **Primárni:** Rodičia s deťmi, ktorí plánujú jedlá pre celú rodinu
- **Sekundárni:** Singles/páry, ktorí chcú lepšie organizovať stravovanie

---

### 4. Core Features

#### 4.1 Manažovanie Jedál (Meal Management)
**Funkcionality:**
- Pridanie nového jedla (názov, kategória, doba prípravy, obtiažnosť)
- Editácia existujúcich jedál
- Mazanie jedál
- Vyhľadávanie a filtrovanie jedál (podľa kategórie, ingrediencií, času prípravy)
- Označenie obľúbených jedál

**Data model:**
- ID, názov, kategória (raňajky/obed/večera/polievka), čas prípravy, obtiažnosť, tagy, link na recept

#### 4.2 Týždenné Menu (Weekly Menu Planning)
**Funkcionality:**
- Zobrazenie týždňa v kalendári (Po-Ne)
- Priradenie jedál k dňom a času (raňajky/obed/večera)
- Drag & drop jedál do kalendára
- Kopírovanie menu z predchádzajúcich týždňov
- Náhodný výber jedál ("surprise me")
- Zobrazenie prehľadu celého týždňa

**Data model:**
- Týždeň (dátum od-do), deň, čas jedla (breakfast/lunch/dinner), ID jedla

#### 4.3 Nákupný Zoznam (Shopping List)
**Funkcionality:**
- Automatické generovanie zoznamu na základe vybraných jedál
- Agregácia ingrediencií (ak sa opakujú)
- Kategorizácia podľa typu (zelenina, mäso, mliečne výrobky, atď.)
- Možnosť manuálneho pridania položiek
- Označenie zakúpených položiek (checkbox)
- Export/zdieľanie zoznamu (email, PDF, text)

**Data model:**
- ID, ingrediencia, množstvo, jednotka, kategória, status (kúpené/nekúpené)

#### 4.4 Recepty (Recipes)
**Funkcionalities:**
- Detail receptu (ingrediencie, postup, čas, porcie)
- Príprava ingrediencií s množstvami
- Krok-za-krokom postup
- Fotka jedla (voliteľné)
- Úprava počtu porcií (prepočet ingrediencií)
- Poznámky a tipy

**Data model:**
- ID receptu, názov, ingrediencie (pole objektov: názov, množstvo, jednotka), postup (pole krokov), čas prípravy, počet porcií, fotka URL

---

### 5. Non-Functional Requirements

#### 5.1 Technológie (MVP)
- **Frontend:** Next.js 14 (App Router) + TypeScript
- **Backend:** Next.js API routes
- **Database:** Prisma + SQLite (lokálne) → PostgreSQL (produkcia)
- **UI:** Tailwind CSS + shadcn/ui
- **State Management:** React Context / Zustand
- **Hosting:** Vercel

#### 5.2 Performance
- Načítanie aplikácie < 2s
- Responzívny dizajn (mobile-first)

#### 5.3 Bezpečnosť (V2)
- Autentifikácia používateľov (NextAuth)
- Osobné dáta a recepty sú privátne pre každého používateľa

---

### 6. MVP Scope (V1.0)

**Included:**
- ✅ Základná databáza jedál (import z "Mapa našich chutí")
- ✅ CRUD operácie pre jedlá
- ✅ Týždenný kalendár s priradením jedál
- ✅ Generovanie nákupného zoznamu
- ✅ Detail receptu
- ✅ Vyhľadávanie a filtrovanie jedál
- ✅ Lokálna SQLite databáza

**Excluded (V2+):**
- ❌ Autentifikácia používateľov
- ❌ Drag & drop (použijeme select/dropdown)
- ❌ Upload fotiek (len URL linky)
- ❌ Export PDF
- ❌ Multi-user / rodinné účty
- ❌ Nutričné informácie

---

### 7. Implementation Phases

**Fáza 1 - Setup & Database (2-3 dni):**
- Next.js projekt setup
- Prisma schema (Meal, Recipe, WeeklyMenu, ShoppingList)
- Seed databázy s jedlami z PDF
- Základné API routes

**Fáza 2 - Meal Management (1-2 dni):**
- List jedál s vyhľadávaním
- Formulár na pridanie/editáciu jedla
- Detail receptu

**Fáza 3 - Weekly Planner (2-3 dni):**
- Kalendárny view (Po-Ne)
- Priradenie jedál pomocou select/dropdown
- CRUD operácie pre menu

**Fáza 4 - Shopping List (1-2 dni):**
- Generovanie zoznamu z menu
- Agregácia ingrediencií
- Checkbox UI pre označovanie
- Manuálne pridávanie položiek

**Celkový čas MVP: 7-10 dní**

---

### 8. User Stories

**US1:** Ako rodič chcem pridať nové jedlo do databázy, aby som si ho mohol neskôr naplánovať
**US2:** Ako používateľ chcem vybrať jedlá na celý týždeň, aby som mal prehľad čo budem variť
**US3:** Ako používateľ chcem automaticky vygenerovať nákupný zoznam, aby som nemusel manuálne počítať ingrediencie
**US4:** Ako používateľ chcem vidieť detail receptu s postupom, aby som vedel ako jedlo pripraviť
**US5:** Ako používateľ chcem filtrovať jedlá podľa času prípravy, aby som našiel rýchle recepty na pracovné dni
**US6:** Ako používateľ chcem označiť zakúpené položky v nákupnom zozname, aby som vedel čo mi ešte chýba

---

### 9. Database Schema (Prisma)

```prisma
model Meal {
  id          String   @id @default(cuid())
  name        String
  category    String   // "chicken", "beef", "pork", "vegetarian", "soup", "breakfast", "quick"
  prepTime    Int?     // v minútach
  difficulty  String?  // "easy", "medium", "hard"
  isFavorite  Boolean  @default(false)
  recipe      Recipe?
  weeklyMenus WeeklyMenu[]
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}

model Recipe {
  id           String           @id @default(cuid())
  mealId       String           @unique
  meal         Meal             @relation(fields: [mealId], references: [id], onDelete: Cascade)
  ingredients  RecipeIngredient[]
  instructions String           // JSON nebo text s kroky
  servings     Int              @default(4)
  imageUrl     String?
  notes        String?
  createdAt    DateTime         @default(now())
  updatedAt    DateTime         @updatedAt
}

model RecipeIngredient {
  id         String  @id @default(cuid())
  recipeId   String
  recipe     Recipe  @relation(fields: [recipeId], references: [id], onDelete: Cascade)
  name       String
  amount     Float?
  unit       String?
  category   String? // "meat", "vegetables", "dairy", "spices", etc.
}

model WeeklyMenu {
  id        String   @id @default(cuid())
  weekStart DateTime // Pondelok týždňa
  weekEnd   DateTime // Nedeľa týždňa
  day       String   // "monday", "tuesday", etc.
  mealTime  String   // "breakfast", "lunch", "dinner"
  mealId    String
  meal      Meal     @relation(fields: [mealId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model ShoppingListItem {
  id         String   @id @default(cuid())
  name       String
  amount     Float?
  unit       String?
  category   String?  // "meat", "vegetables", "dairy", etc.
  isPurchased Boolean @default(false)
  weekStart  DateTime // Na ktorý týždeň sa vzťahuje
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt
}
```

---

### 10. Success Metrics
- Počet aktívnych používateľov (V2 - po pridaní auth)
- Počet vytvorených týždenných menu
- Počet vygenerovaných nákupných zoznamov
- User retention rate (% používateľov, ktorí sa vrátia)

---

### 11. Open Questions
1. ✅ Chceme podporovať viacero rodín/domácností pod jedným účtom? → V2
2. ❌ Potrebujeme integráciu s existujúcimi receptovými API? → Nie, máme vlastné jedlá
3. ✅ Aké kategórie jedál definujeme? → Kuracie, Hovädzie, Bravčové, Vegetariánske, Polievky, Raňajky, Rýchle, Všehodruhy
4. ❌ Chceme umožniť import receptov z URL? → V2

---

### 12. Data Source
**"Mapa našich rodinných chutí"** - rodinný jedálny plánovač obsahujúci ~80+ jedál vo kategóriách:
- Hlavné jedlá z kuracieho mäsa (8 jedál)
- Hlavné jedlá z hovädzieho mäsa (8 jedál)
- Hlavné jedlá z bravčového mäsa (6 jedál)
- Všehodruhy (5 jedál)
- Vegetariánske jedlá (16 jedál)
- Polievky (8 polievok)
- Raňajky (6 jedál)
- Rýchle jedlá (8 jedál)

---

## Next Steps
1. ✅ Create this PRD document
2. Initialize Next.js project
3. Setup Prisma + SQLite
4. Create seed script with all meals
5. Build core features iteratively
