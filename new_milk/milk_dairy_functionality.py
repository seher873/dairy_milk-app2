import sqlite3
import pandas as pd
from dataclasses import dataclass
from fpdf import FPDF

# --------------------------- DATABASE SETUP --------------------------- #
class MilkDatabase:
    def __init__(self, db_name="milk_data.db"):
        try:
            self.conn = sqlite3.connect(db_name, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.create_table()
        except sqlite3.Error as e:
            raise Exception(f"Database error: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

    def create_table(self):
        try:
            self.cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT,
                    date_start TEXT,
                    date_end TEXT,
                    morning_mound REAL,
                    morning_sair INTEGER,
                    morning_rate REAL,
                    evening_mound REAL,
                    evening_sair INTEGER,
                    evening_rate REAL,
                    rent REAL,
                    commission REAL,
                    bandi REAL,
                    paid_amount REAL
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error creating table: {e}")

    def insert_entry(self, entry):
        try:
            self.cursor.execute(''' 
                INSERT INTO entries (
                    customer_name, date_start, date_end,
                    morning_mound, morning_sair, morning_rate,
                    evening_mound, evening_sair, evening_rate,
                    rent, commission, bandi, paid_amount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                entry.customer_name, entry.date_start, entry.date_end,
                entry.morning_mound, entry.morning_sair, entry.morning_rate,
                entry.evening_mound, entry.evening_sair, entry.evening_rate,
                entry.rent, entry.commission, entry.bandi, entry.paid_amount))
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error inserting entry: {e}")

    def fetch_all(self):
        try:
            self.cursor.execute("SELECT * FROM entries")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Error fetching data: {e}")

    def get_monthly_report(self, month):
        try:
            self.cursor.execute("SELECT * FROM entries WHERE strftime('%Y-%m', date_start) = ?", (month,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Error fetching monthly report: {e}")

    def get_daily_report(self, date):
        try:
            self.cursor.execute("SELECT * FROM entries WHERE date_start = ?", (date,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Error fetching daily report: {e}")

# --------------------------- DATA STRUCTURE --------------------------- #
@dataclass
class MilkEntry:
    customer_name: str
    date_start: str
    date_end: str
    morning_mound: float
    morning_sair: int
    morning_rate: float
    evening_mound: float
    evening_sair: int
    evening_rate: float
    rent: float
    commission: float
    bandi: float
    paid_amount: float

# --------------------------- PDF GENERATION --------------------------- #
def generate_pdf(df):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Adding table headers
        for col in df.columns:
            pdf.cell(40, 10, col, border=1)
        pdf.ln()

        # Adding table rows
        for i, row in df.iterrows():
            for val in row:
                pdf.cell(40, 10, str(val), border=1)
            pdf.ln()

        # Return the generated PDF as a byte stream
        return pdf.output(dest="S").encode("latin1")
    except Exception as e:
        raise Exception(f"Error generating PDF: {e}")
