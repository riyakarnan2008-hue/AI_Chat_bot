
import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import uuid
import base64
from urllib.parse import quote_plus

# PAGE SETTINGS
st.set_page_config(
    page_title="Purple AI Assistant",
    page_icon="💜",
    layout="wide"
)

# PURPLE THEME - WHITE TEXT
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #090414, #160923, #0c1025);
    color: white !important;
}

.stApp p, .stApp span, .stApp li,
.stApp label, .stApp strong {
    color: white !important;
}

h1, h2, h3, h4, h5 {
    color: white !important;
    text-shadow: 0 0 10px #a855f7;
}

section[data-testid="stSidebar"] {
    background: #12091f !important;
    border-right: 1px solid #a855f7;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stChatMessage"] {
    background: #241333 !important;
    border: 1px solid #8845b5 !important;
    border-radius: 18px !important;
    padding: 15px !important;
    margin-bottom: 12px !important;
}

[data-testid="stChatMessage"] * {
    color: white !important;
}

[data-testid="stChatMessage"] pre {
    background: #10091a !important;
    border: 1px solid #8845b5 !important;
}

[data-testid="stChatMessage"] code {
    background: #3a2050 !important;
    color: white !important;
}

[data-testid="stChatInput"] {
    background: #241333 !important;
    border: 2px solid #a855f7 !important;
    border-radius: 18px !important;
}

[data-testid="stChatInput"] textarea {
    color: white !important;
    -webkit-text-fill-color: white !important;
    caret-color: white !important;
    background: #241333 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: white !important;
    -webkit-text-fill-color: white !important;
    opacity: 0.8 !important;
}

.stButton button {
    background: linear-gradient(90deg, #7024b8, #b026d3) !important;
    color: white !important;
    border: 1px solid #c084fc !important;
    border-radius: 12px !important;
}

.stButton button * {
    color: white !important;
}

[data-testid="stAlert"] * {
    color: white !important;
}

a {
    color: #e5b8ff !important;
}

hr {
    border-color: #7134a5 !important;
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


# WIKIMEDIA IMAGE SEARCH
def get_related_images(query):

    try:
        url = "https://commons.wikimedia.org/w/api.php"

        params = {
            "action": "query",
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": 6,
            "gsrlimit": 4,
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": 500,
            "format": "json"
        }

        headers = {
            "User-Agent": "PurpleAIChatbot/1.0"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()
        pages = data.get("query", {}).get("pages", {})

        images = []

        for page in pages.values():
            info = page.get("imageinfo", [])

            if info:
                image_url = info[0].get("thumburl") or info[0].get("url")

                if image_url:
                    images.append({
                        "title": page.get("title", "Image"),
                        "url": image_url,
                        "page": info[0].get("descriptionurl", "")
                    })

        return images

    except Exception:
        return []


# DISPLAY PICTURES, VIDEOS AND LINKS
def show_resources(message):

    images = message.get("images", [])
    video_url = message.get("video_url", "")
    web_url = message.get("web_url", "")

    if images:
        st.markdown("### 🖼️ Related Pictures")

        cols = st.columns(2)

        for i, item in enumerate(images):
            with cols[i % 2]:
                st.image(
                    item["url"],
                    caption=item["title"],
                    use_container_width=True
                )

                if item.get("page"):
                    st.markdown(
                        f"[View image source]({item['page']})"
                    )
    else:
        st.caption("No related pictures were found.")

    st.markdown("### 🎬 Related Videos")

    if video_url:
        st.markdown(
            f"[▶️ Watch related YouTube videos]({video_url})"
        )

    st.markdown("### 🔗 Useful Links")

    if web_url:
        st.markdown(
            f"[🌐 Search more information]({web_url})"
        )


# AI VOICE
def speak_answer(content, key):

    encoded = base64.b64encode(
        content.encode("utf-8")
    ).decode("ascii")

    components.html(
        f"""
        <div style="display:flex; gap:10px;">
            <button id="play_{key}"
            style="
                background:#7024b8;
                color:white;
                padding:9px 16px;
                border:1px solid #c084fc;
                border-radius:10px;
                cursor:pointer;
            ">🔊 Play Voice</button>

            <button id="stop_{key}"
            style="
                background:#3a2050;
                color:white;
                padding:9px 16px;
                border:1px solid #c084fc;
                border-radius:10px;
                cursor:pointer;
            ">⏹ Stop</button>
        </div>

        <script>
        const play = document.getElementById("play_{key}");
        const stop = document.getElementById("stop_{key}");

        const bytes = Uint8Array.from(
            atob("{encoded}"),
            c => c.charCodeAt(0)
        );

        const answer = new TextDecoder().decode(bytes);

        play.addEventListener("click", function() {{
            window.speechSynthesis.cancel();

            const speech = new SpeechSynthesisUtterance(answer);
            speech.rate = 1;
            speech.pitch = 1;

            window.speechSynthesis.speak(speech);
        }});

        stop.addEventListener("click", function() {{
            window.speechSynthesis.cancel();
        }});
        </script>
        """,
        height=60
    )


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
                button.innerText = "Copy unavailable";
            }}
        }});
        </script>
        """,
        height=45
    )


# SIDEBAR
with st.sidebar:

    st.markdown("# 💜 PURPLE AI")
    st.caption("Your Visual AI Assistant")

    st.markdown("---")

    if st.button("＋ New Chat", use_container_width=True):
        new_chat()
        st.rerun()

    st.markdown("### 💬 Chat History")

    for chat_id in reversed(list(st.session_state.chats.keys())):

        title = st.session_state.chats[chat_id]["title"]

        if len(title) > 20:
            title = title[:20] + "..."

        col1, col2 = st.columns([4, 1])

        with col1:
            if st.button(
                "💬 " + title,
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


# MAIN HEADER
st.title("💜 PURPLE AI")
st.markdown(
    "<center>✨ Chat • Pictures • Videos • Voice ✨</center>",
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
        padding:30px;
        box-shadow:0 0 20px #411568;
    ">
        <h2>Welcome to Purple AI 💜</h2>
        <p>Your smart visual and voice assistant.</p>
        <p>Ask questions in English or Tamil!</p>
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
        st.info("Tell me about space")
        st.info("தமிழில் இயற்கையைப் பற்றி சொல்லு")


# DISPLAY PREVIOUS MESSAGES
for index, msg in enumerate(messages):

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

        if msg["role"] == "assistant":

            key = f"{current_id.replace('-', '')}_{index}"

            speak_answer(msg["content"], "voice_" + key)
            copy_response(msg["content"], "copy_" + key)

            show_resources(msg)


# USER INPUT
question = st.chat_input("💜 Ask Purple AI anything...")


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
                        "You are Purple AI, a helpful assistant. "
                        "Answer clearly and accurately. "
                        "Use headings and examples when useful. "
                        "Reply in Tamil if the user asks in Tamil. "
                        "Reply in English if the user asks in English. "
                        "Understand Tanglish. "
                        "Keep answers simple and friendly."
                    )
                }
            ] + [
                {"role": m["role"], "content": m["content"]}
                for m in messages
            ]

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

            # GET RELATED IMAGES
            with st.spinner("🖼️ Finding related pictures..."):
                images = get_related_images(question)

            # VIDEO AND WEBSITE LINKS
            video_url = (
                "https://www.youtube.com/results?search_query="
                + quote_plus(question)
            )

            web_url = (
                "https://www.google.com/search?q="
                + quote_plus(question)
            )

            # SAVE ASSISTANT RESPONSE
            assistant_message = {
                "role": "assistant",
                "content": answer,
                "images": images,
                "video_url": video_url,
                "web_url": web_url
            }

            messages.append(assistant_message)

            # DISPLAY VOICE AND COPY
            unique_key = uuid.uuid4().hex

            speak_answer(answer, "voice_" + unique_key)
            copy_response(answer, "copy_" + unique_key)

            # DISPLAY PICTURES AND LINKS
            show_resources(assistant_message)

        except requests.exceptions.ConnectionError:

            placeholder.error(
                "Ollama is not running. Start Ollama and try again."
            )

        except requests.exceptions.RequestException as e:

            placeholder.error(f"Connection Error: {e}")

        except Exception as e:

            placeholder.error(f"Error: {e}")


# FOOTER
st.markdown("---")

st.markdown("""
<center>
<p style="color:white;">
💜 PURPLE AI | Python • Streamlit • Gemma • Ollama
</p>
</center>
""", unsafe_allow_html=True)
