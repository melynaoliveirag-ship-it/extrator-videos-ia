import streamlit as st
import cv2
import tempfile
import whisper

st.title("Extrator de Vídeos IA")

video = st.file_uploader(
    "Envie um vídeo",
    type=["mp4", "mov", "avi"]
)

if video:

    st.success("Vídeo enviado com sucesso!")

    temp_video = tempfile.NamedTemporaryFile(delete=False)
    temp_video.write(video.read())

    cap = cv2.VideoCapture(temp_video.name)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    st.write("Frames encontrados:", total_frames)

    # BOTÃO TRANSCRIÇÃO
    if st.button("Transcrever Vídeo"):

        st.info("Transcrevendo vídeo...")

        modelo = whisper.load_model("base")

        resultado = modelo.transcribe(
            temp_video.name,
            language="pt"
        )

        st.subheader("Transcrição")

        st.text_area(
            "Texto do vídeo",
            resultado["text"],
            height=300
        )

    # BOTÃO IMAGENS
    if st.button("Extrair 5 Melhores Imagens"):

        posicoes = [
            0,
            int(total_frames * 0.25),
            int(total_frames * 0.50),
            int(total_frames * 0.75),
            total_frames - 1
        ]

        for i, posicao in enumerate(posicoes):

            cap.set(cv2.CAP_PROP_POS_FRAMES, posicao)

            sucesso, frame = cap.read()

            if sucesso:

                frame = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )

                st.image(
                    frame,
                    caption=f"Imagem {i+1}"
                )

    cap.release()