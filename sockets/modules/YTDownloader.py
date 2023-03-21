import yt_dlp
import os
class YoutubeScrapper:
    
    def __init__(self, playlists, path):
        
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': path + '%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        self.playlists = playlists
        self.path = path
    
    def clear_directory(self):
        for root, dirs, files in os.walk(self.path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.path)
    
    def download(self, should_download = True):
        valid_files = []
        if not should_download:
            return
        if os.path.exists(self.path):
            self.clear_directory()
        os.mkdir(self.path)
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                result = ydl.extract_info(self.playlists[0], download=True)
            return result
        except: 
            print("Could not download")           
        return valid_files