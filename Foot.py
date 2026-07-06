import streamlit as st
import numpy as np
from scipy.stats import poisson

st.title("⚽ Football AI Dashboard")

home = st.text_input("Équipe domicile")
away = st.text_input("Équipe extérieur")

home_xg = st.number_input("xG domicile", value=1.5)
away_xg = st.number_input("xG extérieur", value=1.2)

odds_home = st.number_input("Cote domicile", value=2.1)
odds_draw = st.number_input("Cote nul", value=3.2)
odds_away = st.number_input("Cote extérieur", value=3.5)

def monte_carlo(h, a, n=20000):
    home = draw = away = 0

    for _ in range(n):
        hg = np.random.poisson(h)
        ag = np.random.poisson(a)

        if hg > ag:
            home += 1
        elif hg == ag:
            draw += 1
        else:
            away += 1

    return home/n, draw/n, away/n

def ev(p, odds):
    return (p * odds) - 1

def kelly(p, odds):
    b = odds - 1
    q = 1 - p
    return max(0, min((b*p - q)/b, 0.05))

if st.button("Analyser match"):

    p_home, p_draw, p_away = monte_carlo(home_xg, away_xg)

    st.subheader("📊 Probabilités")
    st.write({"Home": p_home, "Draw": p_draw, "Away": p_away})

    st.subheader("💰 Value Bet (EV)")
    st.write({
        "Home EV": ev(p_home, odds_home),
        "Draw EV": ev(p_draw, odds_draw),
        "Away EV": ev(p_away, odds_away)
    })

    st.subheader("📉 Kelly (mise recommandée)")
    st.write({
        "Home": kelly(p_home, odds_home),
        "Draw": kelly(p_draw, odds_draw),
        "Away": kelly(p_away, odds_away)
    })
