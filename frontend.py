import streamlit as st
from pytubefix import YouTube
import tempfile
import os
import shutil
from pathlib import Path
from io import BytesIO

def download_video(url, progress_bar):
    try:
        # Callback function for download progress
        def on_progress(stream, chunk, remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - remaining
            progress = bytes_downloaded / total_size
            progress_bar.progress(progress)

        yt = YouTube(url, on_progress_callback=on_progress)
        # Get the audio stream instead of video
        audio_stream = yt.streams.get_audio_only()

        # Download the audio to a BytesIO object
        audio_buffer = BytesIO()
        audio_stream.stream_to_buffer(audio_buffer)
        audio_buffer.seek(0)  # Reset buffer position for reading

        # Provide download button for MP3
        st.download_button(
            label="Download MP3",
            data=audio_buffer,
            file_name=f"{yt.title}.mp3",
            mime="audio/mp3"
        )

        st.success("Audio is ready for download!")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")



# Function for the main Streamlit application
def main():
    # Set the title of the Streamlit app
    st.title("YouTube Video Downloader   ▶️")

    # Get YouTube URL from user using a Streamlit text input widget
    video_url = st.text_input("Enter YouTube URL:")

    # Download button and progress bar
    if st.button("Convert"):
        if video_url:
            # Create a Streamlit progress bar
            progress_bar = st.progress(0)
            # Call the download_video function with the provided URL and progress bar
            download_video(video_url, progress_bar)
        else:
            # Display a warning message if URL is not provided
            st.warning("Please enter a valid YouTube URL.")

# Entry point for the Streamlit app
if __name__ == "__main__":
    # Call the main function to run the Streamlit app
    main()