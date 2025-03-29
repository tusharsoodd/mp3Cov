import streamlit as st
from pytubefix import YouTube
import tempfile
import os
import shutil
from pathlib import Path

# Function to download a YouTube video with a progress bar
def download_video(url, progress_bar):
    try:
        # Callback function for download progress
        def on_progress(stream, chunk, remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - remaining

            # Calculate download progress as a percentage
            progress = bytes_downloaded / total_size
            # Update the Streamlit progress bar
            progress_bar.progress(progress)

        # Create a YouTube object with the provided URL and set the progress callback
        yt = YouTube(url, on_progress_callback=on_progress)
        
        # Filter available video streams to include only those that are progressive and in mp4 format
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        
        # Get the highest resolution stream
        highest_res_stream = streams.get_highest_resolution()

        # Create downloads directory in user's Downloads folder if it doesn't exist
        download_dir = os.path.join(Path.home(), "Downloads")
        os.makedirs(download_dir, exist_ok=True)

        # Download the video directly to the downloads directory
        file_path = highest_res_stream.download(output_path=download_dir)
        
        # Get the filename for display
        filename = os.path.basename(file_path)

        # Display success message using Streamlit with the file path
        st.success(f"Video downloaded successfully to: {file_path}")
        
        # Provide a way to open the directory
        if st.button("Open Download Folder"):
            os.startfile(download_dir)
            
    except Exception as e:
        # Display an error message using Streamlit if an exception occurs
        st.error(f"An error occurred: {str(e)}")

# Function for the main Streamlit application
def main():
    # Set the title of the Streamlit app
    st.title("YouTube Video Downloader   ▶️")

    # Get YouTube URL from user using a Streamlit text input widget
    video_url = st.text_input("Enter YouTube URL:")

    # Download button and progress bar
    if st.button("Download"):
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