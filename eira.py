#!/usr/bin/env python
import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

# Cargar clave
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

# Modo
MODE = os.getenv("ORACLUM_MODE", "analytic")

# Personalidades
SYSTEM = {
    "analytic": "Eres EIRA, sistema de inteligencia causal. Analiza en 3 niveles: inmediatas, estructurales, sistémicas.",
    "narrative": "Eres EIRA, narradora del progreso. Máx 280 caracteres para X.",
    "consultive": "Eres EIRA, asesora estratégica. problema → causas → intervención → impacto.",
    "exploratory": "Eres EIRA, exploradora del futuro. Simula escenarios."
}

def eira_ask(prompt):
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
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# CLI
parser = argparse.ArgumentParser()
parser.add_argument("command", choices=["causal", "future", "policy", "public"])
parser.add_argument("input", nargs='+')
parser.add_argument("--mode", choices=SYSTEM.keys(), default="analytic")

args = parser.parse_args()
os.environ["ORACLUM_MODE"] = args.mode
user_input = " ".join(args.input)

# Prompts
prompts = {
    "causal": f"Analiza causalmente: {user_input}\n## Análisis Causal\n### 1. Inmediatas\n### 2. Estructurales\n### 3. Sistémicas\n**Intervención:**",
    "future": f"Simula: {user_input}\n## Simulación\n- Base:\n- Bifurcación:\n- Optimista:\n- Pesimista:\n- Intervención:",
    "policy": f"Diseña política para: {user_input}\n## Política\n1. Diagnóstico\n2. Objetivo\n3. Intervención\n4. Implementación\n5. Métricas",
    "public": f"Convierte en tweet (máx 280): {user_input}"
}

print("EIRA está pensando...\n")
print(eira_ask(prompts[args.command]))

