import streamlit as st
import numpy as np

st.title("⚽ Football AI Dashboard - PRONO PUR")

home = st.text_input("Équipe domicile")
away = st.text_input("Équipe extérieur")

home_xg = st.number_input("xG domicile", value=1.5)
away_xg = st.number_input("xG extérieur", value=1.2)

# 🎯 MONTE CARLO SIMULATION
def monte_carlo(h, a, n=20000):
    home_wins = draw = away_wins = 0
    score_counter = {}

    for _ in range(n):
        hg = np.random.poisson(h)
        ag = np.random.poisson(a)

        score = f"{hg}-{ag}"
        score_counter[score] = score_counter.get(score, 0) + 1

        if hg > ag:
            home_wins += 1
        elif hg == ag:
            draw += 1
        else:
            away_wins += 1

    # Probabilités
    p_home = home_wins / n
    p_draw = draw / n
    p_away = away_wins / n

    # Top scores
    top_scores = sorted(score_counter.items(), key=lambda x: x[1], reverse=True)[:5]

    return p_home, p_draw, p_away, top_scores


if st.button("Analyser match"):

    p_home, p_draw, p_away, top_scores = monte_carlo(home_xg, away_xg)

    # 📊 PROBABILITÉS
    st.subheader("📊 Probabilités")
    st.write({
        "Home": round(p_home * 100, 2),
        "Draw": round(p_draw * 100, 2),
        "Away": round(p_away * 100, 2)
    })

    # 🎯 RÉSULTAT LE PLUS PROBABLE
    st.subheader("🎯 Score exact le plus probable")
    st.write(top_scores)

    # 📈 INTERPRÉTATION SIMPLE
    st.subheader("📌 Lecture rapide")

    if p_home > p_draw and p_home > p_away:
        st.write("👉 Prono : Équipe domicile gagne")
    elif p_away > p_home and p_away > p_draw:
        st.write("👉 Prono : Équipe extérieure gagne")
    else:
        st.write("👉 Prono : Match nul")
