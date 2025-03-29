import pytubefix
import os
import re
from pytubefix.exceptions import RegexMatchError
from pytubefix.cli import on_progress

try:
    from moviepy.editor import AudioFileClip
    print("Successfully imported moviepy.editor")
except:
    # Try alternative import or suggest solution
    print("Try reinstalling with: pip install moviepy --upgrade")

def convert_youtube_to_mp3(url, output_path=None):
    """
    Convert a YouTube video to MP3 format
    
    Args:
        url (str): YouTube URL
        output_path (str, optional): Path to save the MP3 file. Defaults to current directory.
    
    Returns:
        str: Path to the saved MP3 file
    """
    try:
        # Create YouTube object with progress callback
        yt = pytubefix.YouTube(url, on_progress_callback=on_progress)
        
        # Get video title and sanitize it for filename
        video_title = yt.title
        video_title = re.sub(r'[^\w\-_. ]', '_', video_title)
        
        # Set output path
        if output_path is None:
            output_path = os.getcwd()
        
        # Download the audio stream
        print(f"Downloading audio from: {video_title}")
        audio_stream = yt.streams.filter(only_audio=True).first()
        temp_file = audio_stream.download(output_path=output_path, filename=f"temp_{video_title}")
        
        # Convert to MP3
        print("Converting to MP3...")
        mp3_file = os.path.join(output_path, f"{video_title}.mp3")
        video_clip = AudioFileClip(temp_file)
        video_clip.write_audiofile(mp3_file)
        video_clip.close()
        
        # Remove temporary file
        os.remove(temp_file)
        
        print(f"Successfully saved as: {mp3_file}")
        return mp3_file
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# if __name__ == "__main__":
#     # Example usage
#     youtube_url = input("Enter YouTube URL: ")
    
#     if not output_directory:
#         output_directory = None
        
#     convert_youtube_to_mp3(youtube_url, output_directory)
