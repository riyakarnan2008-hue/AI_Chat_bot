
import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import uuid
import base64

# PAGE SETTINGS
st.set_page_config(
    page_title="Purple AI",
    page_icon="💜",
    layout="wide"
)

# PURPLE THEME
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #090414, #160923, #0c1025);
    color: #ffffff;
}

/* HEADER */
h1 {
    color: #e5b8ff !important;
    text-shadow: 0 0 15px #a855f7;
}

h2, h3 {
    color: #d9a5ff !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #12091f;
    border-right: 1px solid #8b45bd;
}

/* CHAT MESSAGES */
[data-testid="stChatMessage"] {
    background: rgba(90, 40, 130, 0.30);
    border: 1px solid #8845b5;
    border-radius: 18px;
    padding: 15px;
    margin-bottom: 12px;
}

[data-testid="stChatMessage"] p {
    color: #ffffff !important;
}

/* CHAT INPUT BACKGROUND */
[data-testid="stChatInput"] {
    background: #f3e8ff !important;
    border: 2px solid #b45cff !important;
    border-radius: 18px !important;
    box-shadow: 0 0 15px #7134a5;
}

/* TYPING TEXT - IMPORTANT FIX */
[data-testid="stChatInput"] textarea {
    color: #241033 !important;
    -webkit-text-fill-color: #241033 !important;
    caret-color: #7024b8 !important;
    background: #f3e8ff !important;
    font-size: 16px !important;
}

/* PLACEHOLDER */
[data-testid="stChatInput"] textarea::placeholder {
    color: #75528d !important;
    -webkit-text-fill-color: #75528d !important;
    opacity: 1 !important;
}

/* INPUT FOCUS */
[data-testid="stChatInput"]:focus-within {
    border: 2px solid #d9a5ff !important;
    box-shadow: 0 0 20px #a855f7;
}

/* BUTTONS */
.stButton button {
    background: linear-gradient(90deg, #7024b8, #b026d3);
    color: white !important;
    border: 1px solid #c084fc;
    border-radius: 12px;
}

.stButton button:hover {
    box-shadow: 0 0 15px #a855f7;
    border-color: #ffffff;
}

/* OTHER INPUTS */
.stTextInput input,
.stTextArea textarea {
    background: #f3e8ff !important;
    color: #241033 !important;
    -webkit-text-fill-color: #241033 !important;
}

/* FOOTER */
hr {
    border-color: #7134a5;
}

</style>
""", unsafe_allow_html=True)


# SESSION STATE
if "chats" not in st.session_state:

    first_id = str(uuid.uuid4())

    st.session_state.chats = {
        first_id: {
            "title": "New Chat",
            "messages": []
        }
    }

    st.session_state.current_chat = first_id


# NEW CHAT
def new_chat():

    chat_id = str(uuid.uuid4())

    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": []
    }

    st.session_state.current_chat = chat_id


# COPY RESPONSE
def copy_response(content, key):

    encoded = base64.b64encode(
        content.encode("utf-8")
    ).decode("ascii")

    components.html(
        f"""
        <button id="copy_{key}"
        style="
        background:#7024b8;
        color:white;
        border:1px solid #c084fc;
        border-radius:8px;
        padding:8px 15px;
        cursor:pointer;
        ">
        📋 Copy Response
        </button>

        <script>
        const button = document.getElementById("copy_{key}");

        button.addEventListener("click", async function() {{

            const bytes = Uint8Array.from(
                atob("{encoded}"),
                c => c.charCodeAt(0)
            );

            const text = new TextDecoder().decode(bytes);

            try {{
                await navigator.clipboard.writeText(text);
                button.innerText = "✓ Copied!";
            }} catch (error) {{
                const area = document.createElement("textarea");
                area.value = text;
                document.body.appendChild(area);
                area.select();
                document.execCommand("copy");
                area.remove();
                button.innerText = "✓ Copied!";
            }}
        }});
        </script>
        """,
        height=45
    )


# SIDEBAR
with st.sidebar:

    st.markdown("# 💜 PURPLE AI")
    st.caption("Your Intelligent AI Assistant")

    st.markdown("---")

    if st.button("＋ New Chat", use_container_width=True):

        new_chat()
        st.rerun()

    st.markdown("### 💬 Chat History")

    for chat_id in reversed(list(st.session_state.chats.keys())):

        chat_title = st.session_state.chats[chat_id]["title"]

        if len(chat_title) > 20:
            chat_title = chat_title[:20] + "..."

        col1, col2 = st.columns([4, 1])

        with col1:

            if st.button(
                "💬 " + chat_title,
                key="chat_" + chat_id,
                use_container_width=True
            ):

                st.session_state.current_chat = chat_id
                st.rerun()

        with col2:

            if st.button("🗑️", key="delete_" + chat_id):

                del st.session_state.chats[chat_id]

                if not st.session_state.chats:
                    new_chat()

                elif st.session_state.current_chat == chat_id:

                    st.session_state.current_chat = next(
                        reversed(st.session_state.chats)
                    )

                st.rerun()

    st.markdown("---")

    st.markdown("### ⚙️ Model Information")
    st.success("Gemma 3:1B")
    st.caption("Powered by Ollama")

    st.markdown("---")
    st.caption("Purple AI | 2026")


# CURRENT CHAT
current_id = st.session_state.current_chat
current_chat = st.session_state.chats[current_id]
messages = current_chat["messages"]


# MAIN TITLE
st.title("💜 PURPLE AI")

st.markdown(
    "<center>✨ Your Smart AI Assistant ✨</center>",
    unsafe_allow_html=True
)


# WELCOME SCREEN
if not messages:

    st.markdown("""
    <div style="
    text-align:center;
    background:rgba(112,36,184,0.15);
    border:1px solid #9b4dca;
    border-radius:20px;
    padding:35px;
    box-shadow:0 0 20px #411568;
    ">

    <h2>Welcome to Purple AI 💜</h2>
    <p>Ask anything. Learn anything.</p>
    <p>உங்களுக்கு தேவையான கேள்விகளை கேளுங்கள்!</p>
    <h3>How can I help you today?</h3>

    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown("### ✨ Try asking")

    col1, col2 = st.columns(2)

    with col1:
        st.info("What is Artificial Intelligence?")
        st.info("Explain Python programming")

    with col2:
        st.info("தமிழில் Python என்றால் என்ன?")
        st.info("Explain DBMS in simple words")


# DISPLAY OLD MESSAGES
for index, msg in enumerate(messages):

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

        if msg["role"] == "assistant":

            copy_response(
                msg["content"],
                f"{current_id.replace('-', '')}_{index}"
            )


# CHAT INPUT
question = st.chat_input("✨ Ask Purple AI anything...")


if question:

    messages.append({
        "role": "user",
        "content": question
    })

    if current_chat["title"] == "New Chat":
        current_chat["title"] = question[:30]

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        placeholder = st.empty()
        answer = ""

        try:

            api_messages = [
                {
                    "role": "system",
                    "content": (
                        "You are Purple AI, a helpful AI assistant. "
                        "Answer clearly and accurately. "
                        "If the user asks in Tamil, reply in Tamil. "
                        "If the user asks in English, reply in English. "
                        "Understand Tanglish too. "
                        "Keep answers simple and friendly."
                    )
                }
            ] + messages

            with st.spinner("💜 Purple AI is thinking..."):

                response = requests.post(
                    "http://localhost:11434/api/chat",
                    json={
                        "model": "gemma3:1b",
                        "messages": api_messages,
                        "stream": True
                    },
                    stream=True,
                    timeout=(10, 300)
                )

                response.raise_for_status()

                for line in response.iter_lines():

                    if line:

                        data = json.loads(line)

                        chunk = data.get(
                            "message", {}
                        ).get("content", "")

                        answer += chunk

                        placeholder.markdown(answer + "▌")

            placeholder.markdown(answer)

            messages.append({
                "role": "assistant",
                "content": answer
            })

            copy_response(
                answer,
                f"new_{uuid.uuid4().hex}"
            )

        except requests.exceptions.ConnectionError:

            placeholder.error(
                "Ollama is not running. Please start Ollama."
            )

        except requests.exceptions.RequestException as e:

            placeholder.error(f"Connection Error: {e}")

        except Exception as e:

            placeholder.error(f"Error: {e}")


# FOOTER
st.markdown("---")

st.markdown("""
<center>
<p style="color:#d9a5ff;">
💜 PURPLE AI | Built with Python, Streamlit & Ollama
</p>
</center>
""", unsafe_allow_html=True)
