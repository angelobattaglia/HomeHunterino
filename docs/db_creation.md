# SQL tables
I clienti possono esplorare gli annunci relativi alle case attualmente disponibili per l’affitto e, se
interessati, prenotare una visita. Prima di poter agire da cliente, l’utente deve registrarsi e fare
login. Il login/registrazione richiede un campo univoco che sarà utilizzato per riconoscere l’utente
nel sito (per esempio, la mail)

```sql
CREATE TABLE "users" (
    "id" INTEGER NOT NULL,
    "nickname" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    PRIMARY KEY("id")
)
```

Here's how to delete a table
```sql
DROP TABLE "users"
```