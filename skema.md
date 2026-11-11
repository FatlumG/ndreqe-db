# Skema relacionale – Ndreqe

Databaza për platformën **Ndreqe**, ku klientët në Kosovë rezervojnë profesionistë për shtëpinë (hidraulik, elektricist, pastrim etj.).

> Ky dokument është burimi i vetëm i së vërtetës për skemën. Çdo ndryshim bëhet me PR te `dev` dhe aprovohet nga lideri i ekipit.
> **Statusi:** v1.0, skema e ngrirë për Fazën 1.

---

## 1. Konventat

- **Emrat** e tabelave dhe kolonave: pa `ë`/`ç`, pa hapësira (p.sh. `Cmimi_Final`, jo `Çmimi Final`). Kjo na shmang probleme në CSV, RelaX, Datalog dhe MySQL.
- **Vlerat e statuseve** shkruhen me shkronja të vogla, pa `ë` dhe pa hapësira (p.sh. `ne_pritje`, `perfunduar`).
- **PK** = çelës primar, **FK** = çelës i jashtëm, **UQ** = unik, **NN** = jo NULL.
- **Datat** në formatin `YYYY-MM-DD`, **orët** `HH:MM`, **data+ora** `YYYY-MM-DD HH:MM:SS`.
- **Çmimet** në euro, me 2 shifra pas presjes (p.sh. `25.00`).
- Çdo tabelë ka një CSV në `data/` me të njëjtin emër (p.sh. `data/Rezervimi.csv`), UTF-8, me header që përputhet saktë me emrat e kolonave këtu.

## 2. Rregullat e përgjithshme

1. **Asgjë nuk fshihet.** Përdoruesit, kategoritë, rezervimet etj. çaktivizohen përmes kolonës `Statusi` (soft delete).
2. **Të gjitha FK janë `ON DELETE RESTRICT`** (dhe `ON UPDATE CASCADE`), që të mos humbet historiku.
3. Çdo ndryshim i statusit të një rezervimi regjistrohet automatikisht te `Historiku_Statusit` (me trigger, Faza 2).

---

## 3. Tabelat

### 3.1 Qyteti
Qytetet ku funksionon platforma.

| Kolona | Tipi | Kufizime | Përshkrimi |
|---|---|---|---|
| QID | INT | PK | Identifikuesi i qytetit |
| Emri | VARCHAR(50) | NN, UQ | P.sh. Prishtinë, Prizren |
| Rajoni | VARCHAR(50) | NN | P.sh. Prishtina, Mitrovica |

### 3.2 Perdoruesi
Të gjithë përdoruesit: klientë, profesionistë dhe administratorë.

| Kolona | Tipi | Kufizime | Përshkrimi |
|---|---|---|---|
| UID | INT | PK | Identifikuesi i përdoruesit |
| Emri | VARCHAR(50) | NN | |
| Mbiemri | VARCHAR(50) | NN | |
| Email | VARCHAR(100) | NN, UQ | |
| Telefoni | VARCHAR(20) | NN, UQ | Format `+383 4X XXX XXX` |
| QID | INT | NN, FK → Qyteti(QID) | Qyteti ku banon |
| Roli | ENUM | NN, `klient` / `profesionist` / `admin` | |
| Data_Regjistrimit | DATE | NN | |
| Statusi | ENUM | NN, `aktiv` / `joaktiv` / `pezulluar` | Soft delete |

### 3.3 Profesionisti
Të dhënat shtesë vetëm për profesionistët. Lidhje **1:1 (ISA)** me `Perdoruesi`.

| Kolona | Tipi | Kufizime | Përshkrimi |
|---|---|---|---|
| UID | INT | PK, FK → Perdoruesi(UID) | I njëjti UID si te Perdoruesi |
| Bio | TEXT | | Përshkrim i shkurtër |
| Vitet_Pervoje | INT | NN, CHECK ≥ 0 | |
| I_Verifikuar | BOOLEAN | NN, default 0 | 1 = i verifikuar nga admini |
| Data_Verifikimit | DATE | | NULL nëse s'është verifikuar |

Rregull: nëse `I_Verifikuar = 1` atëherë `Data_Verifikimit` nuk është NULL.
Vetëm përdoruesit me `Roli = 'profesionist'` kanë rresht këtu (kontrollohet me trigger në Fazën 2).

### 3.4 Kategoria
Llojet e shërbimeve.

| Kolona | Tipi | Kufizime | Përshkrimi |
|---|---|---|---|
| KID | INT | PK | |
| Emri | VARCHAR(50) | NN, UQ | Elektricist, Hidraulik, Montues, Pastrim, Lyerje, Mekanik |
| Pershkrimi | VARCHAR(255) | | |

### 3.5 Profesionisti_Kategoria
Cilat kategori ofron secili profesionist. Lidhje **M:N**.

| Kolona | Tipi | Kufizime | Përshkrimi |
|---|---|---|---|
| UID_Prof | INT | PK, FK → Profesionisti(UID) | |
| KID | INT | PK, FK → Kategoria(KID) | |
| Cmimi_Fillestar | DECIMAL(8,2) | NN, CHECK > 0 | Çmimi nga i cili nis |
| Data_Shtimit | DATE | NN | |
| Statusi | ENUM | NN, `aktiv` / `joaktiv` | |

PK e përbërë: **(UID_Prof, KID)**.

### 3.6 Zona_Sherbimit
Në cilat qytete punon secili profesionist. Lidhje **M:N**.

| Kolona | Tipi | Kufizime | Përshkrimi |
|---|---|---|---|
| UID_Prof | INT | PK, FK → Profesionisti(UID) | |
| QID | INT | PK, FK → Qyteti(QID) | |

PK e përbërë: **(UID_Prof, QID)**.

### 3.7 Disponueshmeria
Oraret javore kur profesionisti pranon punë.

| Kolona | Tipi | Kufizime | Përshkrimi |
|---|---|---|---|
| DID | INT | PK | |
| UID_Prof | INT | NN, FK → Profesionisti(UID) | |
| Dita_Javes | TINYINT | NN, CHECK 1–7 | 1 = e hënë … 7 = e diel |
| Ora_Fillimit | TIME | NN | |
| Ora_Mbarimit | TIME | NN | CHECK Ora_Fillimit < Ora_Mbarimit |

### 3.8 Rezervimi
Tabela qendrore: një klient rezervon një profesionist për një kategori.

| Kolona | Tipi | Kufizime | Përshkrimi |
|---|---|---|---|
| RZID | INT | PK | |
| UID_Klienti | INT | NN, FK → Perdoruesi(UID) | Kush rezervon |
| UID_Prof | INT | NN | Pjesë e FK të përbërë (shih poshtë) |
| KID | INT | NN | Pjesë e FK të përbërë |
| QID | INT | NN, FK → Qyteti(QID) | Ku kryhet puna |
| Adresa | VARCHAR(150) | NN | |
| Data_Terminit | DATE | NN | |
| Ora | TIME | NN | |
| Pershkrimi_Problemit | TEXT | NN | |
| Statusi | ENUM | NN, `ne_pritje` / `konfirmuar` / `perfunduar` / `anuluar`, default `ne_pritje` | |
| Cmimi_Final | DECIMAL(8,2) | CHECK > 0 | NULL derisa të përfundojë puna |
| Data_Krijimit | DATETIME | NN | |

- **FK e përbërë:** (UID_Prof, KID) → Profesionisti_Kategoria(UID_Prof, KID). Kështu nuk mund të rezervosh një profesionist për kategori që nuk e ofron.
- CHECK UID_Klienti ≠ UID_Prof.
- Unik (UID_Prof, Data_Terminit, Ora): profesionisti s'ka dy rezervime në të njëjtin orar (në Fazën 2 kontrollohet me trigger, duke injoruar të anuluarat).

### 3.9 Vleresimi
Vlerësimi i klientit pas një rezervimi të përfunduar.

| Kolona | Tipi | Kufizime | Përshkrimi |
|---|---|---|---|
| VID | INT | PK | |
| RZID | INT | NN, UQ, FK → Rezervimi(RZID) | Një vlerësim për rezervim |
| Nota | TINYINT | NN, CHECK 1–5 | |
| Komenti | TEXT | | |
| Data | DATE | NN | |

Klienti dhe profesionisti nuk ruhen këtu, merren nga `Rezervimi` (pa dyfishim të të dhënave).
Vlerësimi lejohet vetëm për rezervime me `Statusi = 'perfunduar'` (trigger në Fazën 2).

### 3.10 Foto_Rezervimit
Fotot e problemit që klienti ngarkon.

| Kolona | Tipi | Kufizime | Përshkrimi |
|---|---|---|---|
| FID | INT | PK | |
| RZID | INT | NN, FK → Rezervimi(RZID) | |
| URL | VARCHAR(255) | NN, UQ | |
| Tipi | ENUM | NN, `jpg` / `png` / `webp` | |
| Madhesia | INT | NN, CHECK > 0 | Në KB |
| Data_Ngarkimit | DATETIME | NN | |

### 3.11 Historiku_Statusit
Log i çdo ndryshimi të statusit të rezervimit. Mbushet nga trigger-i.

| Kolona | Tipi | Kufizime | Përshkrimi |
|---|---|---|---|
| HID | INT | PK | |
| RZID | INT | NN, FK → Rezervimi(RZID) | |
| Statusi_Vjeter | ENUM | | NULL kur krijohet rezervimi |
| Statusi_Ri | ENUM | NN | Të njëjtat vlera si Rezervimi.Statusi |
| Koha | DATETIME | NN | |
| Ndryshuar_Nga | INT | FK → Perdoruesi(UID) | NULL nëse ndryshimi bëhet nga sistemi |

---

## 4. Lidhjet (përmbledhje)

| Lidhja | Kardinaliteti | Si realizohet |
|---|---|---|
| Qyteti – Perdoruesi | 1:N | Perdoruesi.QID |
| Perdoruesi – Profesionisti | 1:1 (ISA) | Profesionisti.UID |
| Profesionisti – Kategoria | M:N | Profesionisti_Kategoria |
| Profesionisti – Qyteti (zonat) | M:N | Zona_Sherbimit |
| Profesionisti – Disponueshmeria | 1:N | Disponueshmeria.UID_Prof |
| Perdoruesi (klient) – Rezervimi | 1:N | Rezervimi.UID_Klienti |
| Profesionisti_Kategoria – Rezervimi | 1:N | FK e përbërë (UID_Prof, KID) |
| Qyteti – Rezervimi | 1:N | Rezervimi.QID |
| Rezervimi – Vleresimi | 1:0..1 | Vleresimi.RZID UNIQUE |
| Rezervimi – Foto_Rezervimit | 1:N | Foto_Rezervimit.RZID |
| Rezervimi – Historiku_Statusit | 1:N | Historiku_Statusit.RZID |

## 5. Rregulla që nuk shprehen dot vetëm me PK/FK/CHECK

Këto i shënojmë tani dhe i implementojmë në Fazën 2 me trigger ose procedurë:

1. `Rezervimi.UID_Klienti` duhet të ketë `Roli = 'klient'`.
2. Profesionisti duhet të punojë në qytetin e rezervimit (QID ∈ Zona_Sherbimit).
3. Vlerësim vetëm për rezervim `perfunduar`.
4. Pa dy rezervime aktive të të njëjtit profesionist në të njëjtën datë dhe orë.
5. Çdo ndryshim statusi → rresht i ri te `Historiku_Statusit`.

## 6. Rendi i mbushjes së të dhënave (për CSV dhe import)

Për shkak të FK, tabelat mbushen në këtë rend:

1. Qyteti, Kategoria
2. Perdoruesi
3. Profesionisti
4. Profesionisti_Kategoria, Zona_Sherbimit, Disponueshmeria
5. Rezervimi
6. Vleresimi, Foto_Rezervimit, Historiku_Statusit