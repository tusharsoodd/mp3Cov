import streamlit as st
from convertor import convert_youtube_to_mp3
import os
import tempfile
import threading
import time

def main():
    st.title("YouTube to MP3 Converter")
    
    # URL Input
    youtube_url = st.text_input("YouTube URL:")
    
    # Convert Button
    if st.button("Convert"):
        if not youtube_url:
            st.error("Please enter a YouTube URL")
        else:
            try:
                # Create temp directory for output
                temp_dir = tempfile.mkdtemp()
                
                # Show progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                status_text.text("Starting conversion...")
                
                # Initialize progress tracking
                progress_placeholder = {"value": 0}
                
                # Create a thread to update progress bar while conversion runs
                stop_thread = threading.Event()
                
                def update_progress_bar():
                    while not stop_thread.is_set():
                        # Update progress bar with current progress value
                        progress_bar.progress(progress_placeholder["value"])
                        time.sleep(0.1)
                
                # Start progress thread
                progress_thread = threading.Thread(target=update_progress_bar)
                progress_thread.start()
                
                try:
                    # Convert the video with progress tracking
                    status_text.text("Converting video to MP3...")
                    mp3_path = convert_youtube_to_mp3(youtube_url, temp_dir, progress_callback=lambda p: progress_placeholder.update({"value": p}))
                finally:
                    # Stop the progress thread
                    stop_thread.set()
                    progress_thread.join()
                
                # Ensure progress is at 100% when done
                progress_bar.progress(100)
                status_text.text("Conversion Complete!")
                
                # Create download button
                with open(mp3_path, "rb") as file:
                    btn = st.download_button(
                        label="Download MP3",
                        data=file,
                        file_name=os.path.basename(mp3_path),
                        mime="audio/mpeg"
                    )
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
