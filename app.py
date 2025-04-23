import streamlit as st
import mysql.connector

# --- Streamlit UI ---
st.title("📚 Add New Book")

title = st.text_input("Book Title")
author = st.text_input("Author")
year = st.text_input("Year Published")

# Connect to database
def connect_db():
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"]
    )

if st.button("➕ Add Book"):
    if not title or not author or not year:
        st.warning("Please fill in all fields.")
    else:
        try:
            conn = connect_db()
            cursor = conn.cursor()

            sql = "INSERT INTO Books (title, author, year_published) VALUES (%s, %s, %s)"
            values = (title, author, int(year))
            cursor.execute(sql, values)
            conn.commit()

            st.success("✅ Book added successfully!")

            cursor.close()
            conn.close()

        except ValueError:
            st.error("⚠️ Year must be a number.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
