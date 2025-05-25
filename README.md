# Professor Spark - AI Science Mentor MVP

## Project Overview

Professor Spark is an AI-powered virtual tutor designed to assist high school students, initially focusing on General Science concepts. This MVP (Minimum Viable Product) aims to provide an accessible and interactive learning experience, helping to bridge educational gaps by providing AI-driven explanations and guidance. Users can register, log in, chat with Professor Spark to understand science topics, and their chat history is saved for continuity.

This project was developed as part of a technical code challenge.

## Core Features (MVP)

- **User Registration & Login:** Secure user registration and login system using SQLite database for data persistence and password hashing for security.
- **AI-Powered Tutoring:** Integration with Google's Gemini API (specifically, `gemini-1.5-flash-latest`) to provide intelligent answers to science-related questions.
- **Interactive Chat Interface:** A user-friendly chat interface built with Streamlit.
- **Persistent Chat History:** Chat conversations are saved per user in the SQLite database, allowing users to revisit their previous discussions.
- **Professor Spark Persona:** The AI mentor has a defined persona ("Professor Spark") to make interactions more engaging, providing clear and encouraging explanations in English.

## Technology Stack

- **Backend & Frontend:** Python, Streamlit
- **AI Model:** Google Gemini API (`gemini-1.5-flash-latest`)
- **Database:** SQLite 3
- **Password Hashing:** `hashlib` (SHA256)

## High-Level Architecture

Our current architecture is designed for simplicity and rapid prototyping, running locally:

![Architecture Diagram](image_742a3a.png)
_(Pastikan Anda mengganti `image_742a3a.png` dengan nama file diagram arsitektur yang benar jika berbeda, dan unggah file gambar tersebut ke repositori GitHub Anda di folder yang sama dengan README.md agar bisa tampil)._

**Flow:**

1.  The User interacts with the application via a Web Browser.
2.  The Web Browser communicates with the Professor Spark App (built with Streamlit), which handles both UI (Frontend) and application logic (Backend) running on `localhost`.
3.  The Streamlit App interacts locally with the SQLite Database (`mentor_ai.db`) for user authentication (registration/login) and storing/retrieving chat history.
4.  For AI-powered responses, the Streamlit App sends requests (user queries + context) over the Internet to the Google Gemini API (LLM).
5.  The Google Gemini API processes the request and returns the AI-generated response to the Streamlit App.
6.  The Streamlit App displays the AI's response to the User in the chat interface.

## Estimated Monthly Operational Costs

**For the Current MVP (Running on Localhost):**

- **Streamlit Application Hosting:** $0 (runs on a local machine).
- **SQLite Database:** $0 (local file-based database).
- **Google Gemini API Usage:** $0 (assuming usage remains within the generous free tier limits provided by Google AI Studio, which is expected for development and demonstration purposes of this MVP).
- **Total Estimated Monthly Cost (Current MVP): $0**

**Potential Costs if Deployed to the Cloud (for 24/7 Accessibility & Scalability):**

- **Application Hosting (e.g., Streamlit Community Cloud, Render, Heroku):** Could start from $0 (utilizing free tiers) and potentially scale to $5-$10+/month depending on resource usage and traffic.
- **Database (if a managed cloud database is chosen, e.g., NeonDB, Supabase free tiers):** Could start from $0 for basic needs, scaling to $5-$20+/month for more robust solutions.
- **Google Gemini API:** If usage exceeds the free tier, costs would be based on token consumption. For example, the `gemini-1.5-flash` model has approximate pricing of $0.35 per 1 million input tokens and $1.05 per 1 million output tokens. Actual API costs would heavily depend on the number of active users and interaction volume.
- **Total Estimated Monthly Cost (Cloud-Deployed, Small Scale):** Could range from **$0** (fully leveraging free tiers) to **$5-$25+** depending on the chosen services and usage patterns.

## Testing Approach (Use Case Testing)

The primary goal of testing is to ensure the core functionalities of the Professor Spark MVP operate as designed, focusing on a key use case: a high school student registering, logging in, and interacting with the AI tutor to understand a science concept, with their chat history being saved and retrievable.

**Primary Test Use Case:**
A student, "Andi," wants to learn about the concept of "Photosynthesis."

**Manual Testing Steps:**

1.  **User Registration:**
    - Navigate to the application.
    - Select the "Register" option.
    - Input a unique username (e.g., "andi_science"), a password, and confirm the password.
    - Click "Register."
    - **Expected Outcome:** Successful registration, user is redirected to the login page or receives a success notification. User data (username, hashed password) is stored in the `users` table in the SQLite database.
2.  **User Login:**
    - Select the "Login" option.
    - Input the registered username ("andi_science") and the correct password.
    - Click "Login."
    - **Expected Outcome:** Successful login, user is directed to the main chat interface with Professor Spark. A personalized greeting 포함하는 "andi_science" may be displayed.
3.  **Learning Interaction (Chat Session):**
    - In the chat interface, Andi types the question: "Hello Professor, what is photosynthesis?"
    - **Expected Outcome:** Professor Spark provides a response in English that is clear, scientifically accurate (for a high school level), and easy to understand. Both Andi's question and Professor Spark's answer are displayed and stored in the chat UI.
    - Andi types a follow-up question: "What are the reactants and products needed for photosynthesis?"
    - **Expected Outcome:** Professor Spark provides a relevant and accurate answer, potentially referencing the context of the ongoing conversation about photosynthesis.
4.  **Chat History Persistence Verification:**
    - Confirm that all interactions (Andi's questions and Professor Spark's answers) are visible in the chat interface.
    - (Internal Check): Verify that corresponding entries are correctly saved in the `chat_history` table in the SQLite database, linked to Andi's `user_id`.
5.  **User Logout:**
    - Click the "Logout" button.
    - **Expected Outcome:** The user is successfully logged out and redirected to the login/initial page. The session state related to the logged-in user is cleared.
6.  **Chat History Retrieval (After Re-Login):**
    - Log in again as "andi_science."
    - **Expected Outcome:** The chat interface loads, and the entire previous conversation history about photosynthesis is successfully retrieved from the database and displayed, allowing Andi to continue where they left off.

**General Success Criteria:**

- All core functionalities (registration, login, AI chat, logout, history loading) operate without critical errors.
- AI responses from Professor Spark are relevant, scientifically sound for basic concepts, and delivered in the designated persona (friendly, English).
- User data and chat history are correctly and persistently stored in the SQLite database.
- The user interface is responsive and user-friendly.

## Future Development Ideas / Innovations

- **Multi-Subject & Multi-Persona Mentors:** Expanding to cover more subjects (Mathematics, other languages, etc.) with distinct AI personas for each.
- **Adaptive Learning Levels:** Tailoring explanations and question difficulty based on student's grade level (Elementary, Middle School, High School).
- **Interactive Quizzes & Exercises:** Incorporating simple quizzes or exercises to test understanding.
- **Teacher/Admin Dashboard:** A separate interface for teachers to potentially monitor student progress (with privacy considerations) or suggest topics.
- **Deployment to Cloud:** Hosting the application on a cloud platform (e.g., Streamlit Community Cloud, Render) for 24/7 accessibility.
- **Enhanced User Identification:** Implementing social logins (Google, Facebook) for easier onboarding.
- **Multilingual Support:** Adding support for other ASEAN languages.

---
