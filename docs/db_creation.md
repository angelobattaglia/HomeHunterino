# SQL tables
I clienti possono esplorare gli annunci relativi alle case attualmente disponibili per l’affitto e, se
interessati, prenotare una visita. Prima di poter agire da cliente, l’utente deve registrarsi e fare
login. Il login/registrazione richiede un campo univoco che sarà utilizzato per riconoscere l’utente
nel sito (per esempio, la mail)

```sql
CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER NOT NULL,
    "email" TEXT NOT NULL UNIQUE,
    "user_type" TEXT NON NULL,
    "password" TEXT NOT NULL,
    PRIMARY KEY("id")
);
```

Here's how to delete a table
```sql
DROP TABLE "users"
```

```sql
CREATE TABLE IF NOT EXISTS "adverts" (
	"id"	INTEGER NOT NULL,
	"title"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	"type"	TEXT NOT NULL,
	"rooms"	INTEGER NOT NULL,
	"description"	TEXT NOT NULL,
	"price"	INTEGER NOT NULL,
	"furnished"	TEXT NOT NULL,
	"id_landlord"	INTEGER NOT NULL,
	"publicly_available"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
```

```sql
CREATE TABLE IF NOT EXISTS "photos" (
	"id" INTEGER NOT NULL,
	"advert_id"	INTEGER NOT NULL,
	"file_name"	TEXT,
	FOREIGN KEY("advert_id") REFERENCES "annunci"("id"),
	PRIMARY KEY("id")
);
```

```sql
CREATE TABLE IF NOT EXISTS "bookings" (
    "id" INTEGER NOT NULL,
    "advert_id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    "status" TEXT NOT NULL CHECK(status IN ('request', 'accepted', 'refused')),
    "refusal_reason" TEXT,
    FOREIGN KEY("advert_id") REFERENCES "adverts"("id"),
    FOREIGN KEY("user_id") REFERENCES "users"("id"),
    PRIMARY KEY("id")
);
```

