
import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import uuid
import base64

# PAGE SETTINGS
st.set_page_config(
    page_title="Purple AI 2.0",
    page_icon="💜",
    layout="wide"
)

# PURPLE NEON THEME
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #090414, #160923, #0c1025);
    color: white;
}

header {
    background: transparent !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #160923, #0b0716);
    border-right: 1px solid #7134a5;
}

h1 {
    color: #d9a5ff !important;
    text-shadow: 0 0 15px #a855f7;
}

h2, h3 {
    color: #d9a5ff !important;
}

p {
    color: #e5d5f5;
}

[data-testid="stChatMessage"] {
    background: rgba(75, 35, 110, 0.25);
    border: 1px solid #7539a5;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 12px;
    animation: appear 0.4s ease-in-out;
}

@keyframes appear {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

[data-testid="stChatInput"] {
    border: 2px solid #a855f7;
    border-radius: 18px;
    background: #211332;
    box-shadow: 0 0 12px #7134a5;
}

[data-testid="stChatInput"] textarea {
    color: white !important;
}

.stButton button {
    background: linear-gradient(90deg, #7024b8, #b026d3);
    color: white;
    border: 1px solid #c084fc;
    border-radius: 12px;
    transition: 0.3s;
}

.stButton button:hover {
    box-shadow: 0 0 18px #a855f7;
    color: white;
    border-color: #e9b5ff;
}

[data-testid="stChatMessageContent"] {
    color: white;
}

hr {
    border-color: #663399;
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


# NEW CHAT FUNCTION
def new_chat():
    chat_id = str(uuid.uuid4())

    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": []
    }

    st.session_state.current_chat = chat_id


# COPY RESPONSE FUNCTION
def copy_response(content, key):

    encoded = base64.b64encode(
        content.encode("utf-8")
    ).decode("ascii")

    components.html(
        f"""
        <button id="copy_{key}"
        style="
        background:#542080;
        color:white;
        border:1px solid #c084fc;
        border-radius:8px;
        padding:7px 15px;
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

    # NEW CHAT
    if st.button("＋ New Chat", use_container_width=True):
        new_chat()
        st.rerun()

    st.markdown("### 💬 Chat History")

    # DISPLAY AND DELETE CHATS
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

            if st.button(
                "🗑️",
                key="delete_" + chat_id
            ):

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
    st.caption("Purple AI 2.0 | 2026")


# CURRENT CHAT
current_id = st.session_state.current_chat
current_chat = st.session_state.chats[current_id]
messages = current_chat["messages"]


# MAIN HEADER
st.title("💜 PURPLE AI")

st.markdown(
    "<center>✨ Your Smart AI Assistant ✨</center>",
    unsafe_allow_html=True
)

st.write("")


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


# DISPLAY CHAT HISTORY
for index, msg in enumerate(messages):

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

        if msg["role"] == "assistant":
            copy_response(
                msg["content"],
                f"{current_id.replace('-', '')}_{index}"
            )


# USER INPUT
question = st.chat_input("✨ Ask Purple AI anything...")


if question:

    # SAVE USER MESSAGE
    messages.append({
        "role": "user",
        "content": question
    })

    if current_chat["title"] == "New Chat":
        current_chat["title"] = question[:30]

    with st.chat_message("user"):
        st.markdown(question)

    # AI RESPONSE
    with st.chat_message("assistant"):

        placeholder = st.empty()
        answer = ""

        try:

            api_messages = [
                {
                    "role": "system",
                    "content": (
                        "You are Purple AI, a helpful AI assistant. "
                        "Answer questions clearly and accurately. "
                        "If the user asks in Tamil, reply in Tamil. "
                        "If the user asks in English, reply in English. "
                        "You can also understand Tanglish. "
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
<p style="color:#b78bd9;">
💜 PURPLE AI 2.0 | Built with Python, Streamlit & Ollama
</p>
</center>
""", unsafe_allow_html=True)

