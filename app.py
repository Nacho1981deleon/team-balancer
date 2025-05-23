import streamlit as st
import pandas as pd
from itertools import combinations

st.set_page_config(page_title="Balanceador de Equipos", layout="centered")
st.title("⚽ Armador de Equipos 7 vs 7 balanceados - Fútbol 'buena leche' de los Miercoles")

st.markdown("Subí una lista de hasta 14 jugadores con su nivel del 1 al 10 (en Excel o CSV). El sistema calculará los equipos más equilibrados posibles.")

uploaded_file = st.file_uploader("Subí tu archivo Excel o CSV", type=["xlsx", "csv"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    if "Jugador" in df.columns and "Nivel" in df.columns:
        players = list(df[["Jugador", "Nivel"]].dropna().itertuples(index=False, name=None))

        if len(players) != 14:
            st.error("Tenés que ingresar exactamente 14 jugadores.")
        else:
            min_diff = float('inf')
            best_team_a = best_team_b = None

            for team_a in combinations(players, 7):
                team_b = [p for p in players if p not in team_a]
                total_a = sum(p[1] for p in team_a)
                total_b = sum(p[1] for p in team_b)
                diff = abs(total_a - total_b)
                if diff < min_diff:
                    min_diff = diff
                    best_team_a = team_a
                    best_team_b = team_b

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Equipo Negro")
                for name, lvl in best_team_a:
                    st.write(f"{name} (Nivel {lvl})")
                st.markdown(f"**Total:** {sum(p[1] for p in best_team_a)}")

            with col2:
                st.subheader("Equipo Blanco")
                for name, lvl in best_team_b:
                    st.write(f"{name} (Nivel {lvl})")
                st.markdown(f"**Total:** {sum(p[1] for p in best_team_b)}")

            st.success(f"✅ Diferencia mínima lograda: {min_diff}")
            
            import io

            # Crear un Excel con ambos equipos
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_a = pd.DataFrame(best_team_a, columns=["Jugador", "Nivel"])
                df_b = pd.DataFrame(best_team_b, columns=["Jugador", "Nivel"])

                df_a.to_excel(writer, sheet_name="Equipo A", index=False)
                df_b.to_excel(writer, sheet_name="Equipo B", index=False)

            # Botón de descarga
            st.download_button(
                label="📥 Descargar equipos en Excel",
                data=output.getvalue(),
                file_name="equipos_balanceados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    else:
        st.error("El archivo debe tener columnas llamadas 'Jugador' y 'Nivel'.")