import streamlit as st

# --- Sidebar dan Page Routing ---
def render_sidebar():
    st.sidebar.title("Muhammad Ilham Ikhwanul Akram")
    st.sidebar.markdown("**Tugas Skripsi: Intolerant Analysis**")
    st.sidebar.markdown("---")
    menu = st.sidebar.radio(
        "Menu", 
        options=["Analisis Data", "Intoleran Analysis", "Intolerant Level"],
        index=1  # default ke Intoleran Analysis
    )
    st.sidebar.markdown("---")
    st.sidebar.write("Dibuat menggunakan Streamlit")
    return menu


def main():
    st.set_page_config(page_title="Intolerant Analysis Dashboard", layout="wide")
    menu = render_sidebar()
    st.title("🔍 Tolerance vs Intolerance Classifier")

    if menu == "Analisis Data":
        import analisis_data as analisis_data
        analisis_data.render()

    elif menu == "Intoleran Analysis":
        import intoleran_analysis as intoleran_analysis
        intoleran_analysis.render()

    elif menu == "Intolerant Level":
        import intolerant_level as intolerant_level
        intolerant_level.render()

if __name__ == '__main__':
    main()