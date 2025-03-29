import streamlit as st
from convertor import convert_youtube_to_mp3
import os
import tempfile

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
                
                # Convert the video
                status_text.text("Converting video to MP3...")
                mp3_path = convert_youtube_to_mp3(youtube_url, temp_dir)
                
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
