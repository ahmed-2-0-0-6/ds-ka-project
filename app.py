import streamlit as st
import mysql.connector

# --- Connect to DB using secrets from secrets.toml or Streamlit Cloud ---
def connect_db():
    return mysql.connector.connect(
        host=st.secrets["database"]["DB_HOST"],
        user=st.secrets["database"]["DB_USER"],
        password=st.secrets["database"]["DB_PASSWORD"],
        database=st.secrets["database"]["DB_NAME"]
    )

# --- Streamlit UI ---
st.title("📚 Add New Book")

title = st.text_input("Book Title")
author = st.text_input("Author")
year = st.text_input("Year Published")

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

            # Clean-up
            cursor.close()
            conn.close()

        except ValueError:
            st.error("⚠️ Year must be a number.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
