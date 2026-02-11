import psycopg

psycopg.connect(
    "postgresql://finance:finance@localhost:5432/finance_db",
    connect_timeout=5,
)
print("CONNECTED")
