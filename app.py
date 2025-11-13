import streamlit as st
import requests

# --- SYSTEM PROMPTS ---
SYSTEM_MODE = {
    "narrative": "Eres EIRA, una IA optimista y viral. Convierte cualquier insight en un tuit poderoso, positivo, con hashtags y emoji. Máximo 280 caracteres.",
    "analytic": "Eres EIRA, una IA analítica y precisa. Responde con datos, lógica y claridad. Sin emociones, solo hechos."
}

# --- FUNCIÓN PARA LLAMAR A GROK ---
def call_grok(prompt, mode="analytic"):
    try:
        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {st.secrets['XAI_API_KEY']}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "grok-3",
            "messages": [
                {"role": "system", "content": SYSTEM_MODE[mode]},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1500
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# --- INTERFAZ ---
st.set_page_config(page_title="Oraclum Hub", page_icon="🔮")
st.title("Oraclum Hub")
st.subheader("EIRA — Sistema de Inteligencia Causal")

mode = st.selectbox("Modo", ["narrative", "analytic"])
prompt = st.text_input("¿Qué quieres saber?")

if st.button("Consultar a EIRA"):
    if prompt.strip():
        with st.spinner("EIRA está pensando..."):
            answer = call_grok(prompt, mode)
            st.success("**Respuesta de EIRA:**")
            st.write(answer)

            if mode == "narrative" and len(answer) <= 280:
                st.code(answer, language="text")
                st.download_button("Copiar para X", answer)
    else:
        st.warning("Escribe una pregunta.")
         
