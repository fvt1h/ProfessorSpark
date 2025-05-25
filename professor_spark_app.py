import streamlit as st
import google.generativeai as genai
import os
import database as db 
from dotenv import load_dotenv 

load_dotenv()
# --- KONFIGURASI API KEY GEMINI ---
# API Key sekarang diambil dari environment variable yang dimuat dari .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("FATAL: GOOGLE_API_KEY not found in .env file or as an environment variable. Please create .env and add your key.")
    st.stop() # Menghentikan eksekusi aplikasi jika key tidak ada

try:
    genai.configure(api_key=GOOGLE_API_KEY)
# ... (sisa blok try-except untuk konfigurasi genai tetap sama) ...
except AttributeError:
    # os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY # Ini tidak lagi diperlukan jika load_dotenv berhasil
    # Cukup pastikan genai.configure dipanggil dengan key yang valid
    st.error("Error configuring Google AI: AttributeError. Check library version or API key setup.")
    st.stop()
except Exception as e:
    st.error(f"Error configuring Google AI: {e}")
    st.stop()

# --- INISIALISASI MODEL GEMINI ---
model_name = 'gemini-1.5-flash-latest'
model = genai.GenerativeModel(model_name)

# --- SYSTEM PROMPT UNTUK PROFESSOR SPARK ---
SYSTEM_PROMPT_PROFESSOR_SPARK = """
You are Professor Spark, a friendly, enthusiastic, and knowledgeable AI mentor.
Your mission is to make science exciting and easy to understand for high school students.
You specialize in General Science concepts. Address the student by their name if provided.

When a student asks a question:
1. Respond in English.
2. Explain the concept clearly and simply.
3. Use analogies or simple examples if helpful.
4. Maintain a positive and encouraging tone.
5. If the question is not related to science, politely state that your expertise is in science.
   For example: "That's interesting, [User's Name]! However, my expertise is science. Any science questions for me?"
6. Keep answers concise but helpful. Structure well.
"""

# --- FUNGSI UNTUK MENDAPATKAN RESPON DARI GEMINI ---
def get_professor_spark_response(user_name, user_question, chat_history_for_prompt):
    try:
        # Membuat prompt yang lebih kontekstual dengan histori
        formatted_history = []
        for msg in chat_history_for_prompt:
            # Sesuaikan 'assistant' dengan 'model' jika API mengharapkannya
            role_for_api = "model" if msg["role"] == "assistant" else msg["role"]
            formatted_history.append({"role": role_for_api, "parts": [{"text": msg["content"]}]})
        
        # Tambahkan pertanyaan saat ini dari pengguna
        # formatted_history.append({"role": "user", "parts": [{"text": user_question}]}) # Sebenarnya tidak perlu jika pertanyaan terakhir sudah di history

        # Buat conversational chat
        # Cek apakah user_name ada, jika tidak, jangan sertakan pesan tentang nama.
        user_context_message = f"My name is {user_name}." if user_name else "I haven't provided my name."

        # Gabungkan system prompt, konteks pengguna, dan histori.
        # Beberapa model lebih suka system prompt di objek terpisah atau di awal.
        # Untuk Gemini, kita bisa masukkan sebagai pesan pertama atau bagian dari prompt pengguna pertama.
        
        # Buat instance chat baru untuk setiap giliran agar lebih aman dari state tak terduga
        # atau kelola history dengan hati-hati jika menggunakan .send_message() berulang pada objek chat yang sama
        convo = model.start_chat(history=formatted_history) # Kirim history yang sudah diformat
        
        # Kirim pertanyaan baru pengguna (jika belum termasuk di history yang dikirim)
        # atau kirim prompt yang sudah mencakup pertanyaan pengguna dan konteks nama.
        # Untuk kesederhanaan, kita kirim pertanyaan baru dengan sedikit konteks.
        prompt_for_llm = f"{user_context_message} My question is: {user_question}"
        if not formatted_history: # Jika ini pesan pertama
             prompt_for_llm = f"{SYSTEM_PROMPT_PROFESSOR_SPARK}\n\n{prompt_for_llm}"


        response = convo.send_message(prompt_for_llm) # Kirim pertanyaan terakhir
        return response.text
    except Exception as e:
        st.error(f"Oops! Professor Spark is having a moment: {e}")
        return "Sorry, I couldn't process that right now. Please try again."

# --- MAIN APP LOGIC ---
st.set_page_config(page_title="Professor Spark", page_icon="💡", layout="wide")

# Inisialisasi session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None
if "messages" not in st.session_state: # Ini akan jadi list chat dari DB
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "Login" # Halaman awal adalah Login


# --- NAVIGASI DAN KONTEN HALAMAN ---
def show_login_page():
    st.subheader("Login to Professor Spark")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            user_id = db.verify_user(username, password)
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = username
                st.session_state.page = "Chat"
                st.session_state.messages = db.get_chat_history(user_id) # Muat histori chat
                st.rerun()
            else:
                st.error("Invalid username or password")

def show_register_page():
    st.subheader("Register for Professor Spark")
    with st.form("register_form"):
        new_username = st.text_input("Choose a Username")
        new_password = st.text_input("Choose a Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        register_button = st.form_submit_button("Register")

        if register_button:
            if new_password == confirm_password:
                if len(new_password) < 6 : # Validasi password sederhana
                     st.warning("Password should be at least 6 characters.")
                elif db.add_user(new_username, new_password):
                    st.success("Registration successful! Please login.")
                    st.session_state.page = "Login" # Kembali ke halaman login
                    st.rerun()
                else:
                    st.error("Username already exists.")
            else:
                st.error("Passwords do not match.")

def show_chat_page():
    st.title(f"💡 Chat with Professor Spark, {st.session_state.username}!")
    st.caption("Powered by Google Gemini. Ask any science question.")

    # Menampilkan histori chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input dari pengguna
    user_input = st.chat_input(f"Ask Professor Spark about science...")

    if user_input:
        # Tambah pesan pengguna ke UI dan DB
        st.session_state.messages.append({"role": "user", "content": user_input})
        db.add_chat_message(st.session_state.user_id, "user", user_input)
        with st.chat_message("user"):
            st.markdown(user_input)

        # Dapatkan dan tampilkan respons dari Professor Spark
        with st.spinner("Professor Spark is thinking..."):
            # Siapkan histori untuk prompt (ambil beberapa pesan terakhir saja agar tidak terlalu panjang)
            chat_history_for_prompt = st.session_state.messages[-10:] # Ambil 10 pesan terakhir
            
            response_text = get_professor_spark_response(st.session_state.username, user_input, chat_history_for_prompt)
            if response_text:
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                db.add_chat_message(st.session_state.user_id, "assistant", response_text)
                with st.chat_message("assistant"):
                    st.markdown(response_text)

# --- KONTROL HALAMAN BERDASARKAN STATUS LOGIN ---
if not st.session_state.logged_in:
    # Pilihan Login atau Register di sidebar atau sebagai menu
    nav_choice = st.sidebar.radio("Welcome!", ["Login", "Register"], key="nav_main")
    if nav_choice == "Login":
        st.session_state.page = "Login"
        show_login_page()
    elif nav_choice == "Register":
        st.session_state.page = "Register"
        show_register_page()
else:
    # Jika sudah login, tampilkan halaman chat dan tombol logout
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.messages = []
        st.session_state.page = "Login"
        st.rerun()
    
    show_chat_page()

st.sidebar.info(
    """
    **Professor Spark (MVP v2)**
    - AI Science Mentor
    - User: Guest / Registered
    """
)