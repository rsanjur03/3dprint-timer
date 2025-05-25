import streamlit as st
from datetime import timedelta
import time

def parse_time(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return timedelta(hours=hours, minutes=minutes)

def format_time(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}"

def play_sound():
    sound_html = """
    <audio autoplay>
        <source src="https://www.soundjay.com/buttons/sounds/beep-07.mp3" type="audio/mpeg">
        Tu navegador no soporta audio HTML5.
    </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

def countdown_timer(color, duration, stage, total_stages):
    total_minutes = int(duration.total_seconds() // 60)
    progress_bar = st.progress(0)
    status_text = st.empty()

    while duration.total_seconds() > 0:
        remaining_minutes = int(duration.total_seconds() // 60)
        progress = (total_minutes - remaining_minutes) / total_minutes
        status_text.markdown(
            f"**Etapa {stage} de {total_stages}**  \n"
            f"Color: `{color}`  \n"
            f"Tiempo restante: `{format_time(duration)}`"
        )
        progress_bar.progress(progress)
        time.sleep(60)
        duration -= timedelta(minutes=1)

    play_sound()
    status_text.markdown(f"✅ **Cambio de color: {color} completado.**")
    progress_bar.progress(1.0)

def main():
    st.title("🎨 Temporizador de Colores para Impresión 3D")

    num_colors = st.number_input("Ingrese el número de colores que se usarán:", min_value=1, step=1)
    colors = []
    durations = []

    for i in range(num_colors):
        color = st.text_input(f"Nombre del color {i+1}:", key=f"color_{i}")
        duration_str = st.text_input(f"Tiempo de impresión para {color} (hh:mm):", key=f"dur_{i}")
        if duration_str:
            try:
                duration = parse_time(duration_str)
                colors.append(color)
                durations.append(duration)
            except:
                st.error(f"Formato inválido para el tiempo del color {color}. Usa hh:mm")

    if num_colors > 0 and len(colors) == num_colors:
        current_color_index = st.number_input(
            f"¿Por qué color vas? (1-{num_colors}):", min_value=1, max_value=num_colors, step=1
        ) - 1

        if st.button("▶️ Iniciar Temporizador"):
            for i in range(current_color_index, num_colors):
                countdown_timer(colors[i], durations[i], i + 1, num_colors)

if __name__ == "__main__":
    main()

