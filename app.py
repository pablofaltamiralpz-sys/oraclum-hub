import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import os

# Cargar clave
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

st.set_page_config(page_title="Oraclum Hub", page_icon="Crystal Ball")
st.title("Oraclum Hub")
st.caption("EIRA — Sistema de Inteligencia Causal")

# Modos
MODE = st.selectbox("Modo de EIRA", ["narrative", "analytic", "consultive", "exploratory"])

# Personalidades
SYSTEM = {
    "analytic": "Eres EIRA, sistema de inteligencia causal. Analiza en 3 niveles: inmediatas, estructurales, sistémicas.",
    "narrative": "Eres EIRA, narradora del progreso. Máx 280 caracteres para X.",
    "consultive": "Eres EIRA, asesora estratégica. problema → causas → intervención → impacto.",
    "exploratory": "Eres EIRA, exploradora del futuro. Simula escenarios."
}

prompt = st.text_area("¿Qué quieres saber?", height=100)

if st.button("Consultar a EIRA"):
    if prompt:
        with st.spinner("EIRA está pensando..."):
            try:
                response = client.chat.completions.create(
                    model="grok-3",
                    messages=[
                        {"role": "system", "content": SYSTEM[MODE]},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                answer = response.choices[0].message.content
                st.success("**Respuesta de EIRA:**")
                st.write(answer)
                
                if MODE == "narrative" and len(answer) <= 280:
                    st.code(answer, language="text")
                    st.download_button("Copiar para X", answer)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Escribe una pregunta.")