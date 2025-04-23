import streamlit as st
import mysql.connector

# Load database credentials from Streamlit secrets
DB_HOST = st.secrets["DB_HOST"]
DB_USER = st.secrets["DB_USER"]
DB_PASSWORD = st.secrets["DB_PASSWORD"]
DB_NAME = st.secrets["DB_NAME"]

# Function to connect to the database
def connect_db():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except mysql.connector.Error as err:
        st.error(f"❌ Error: {err}")
        return None

# Streamlit app UI
st.title("📚 Add New Book")

# Inputs for book details
title = st.text_input("Book Title")
author = st.text_input("Author")
year = st.text_input("Year Published")

if st.button("➕ Add Book"):
    if not title or not author or not year:
        st.warning("Please fill in all fields.")
    else:
        try:
            # Convert year to integer and validate
            year_int = int(year)
            
            # Connect to the database
            conn = connect_db()
            if conn is not None:
                cursor = conn.cursor()

                # SQL query to insert the book
                sql = "INSERT INTO Books (title, author, year_published) VALUES (%s, %s, %s)"
                values = (title, author, year_int)
                
                # Execute and commit
                cursor.execute(sql, values)
                conn.commit()
                
                st.success("✅ Book added successfully!")

                # Clean-up
                cursor.close()
                conn.close()

        except ValueError:
            st.error("⚠️ Year must be a valid number.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
