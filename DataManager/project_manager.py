import fnmatch
import json
import os
import io
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from faster_whisper import WhisperModel
import yt_dlp as yt

class ProjectManager():
    def __init__(self, app_path: str, project_name: str):
        """Inicializes a project, loadings it's files. It's folder structure must be created first.

        Args:
            app_path (str): The app path
            project_name(str): The project name, sanitized.
        """        
        
        self.app_data = {}
        self.load_configuration(app_path)
        self.project_name = project_name
        self.project_path = os.path.join(app_path, self.project_name)
        self.models_path = os.path.join(app_path, 'models')
        self.audio_path = os.path.join(self.project_path, 'audios')
        self.text_path = os.path.join(self.project_path, 'texts')
        self.db_path = os.path.join(self.project_path, 'databases')
        self.project_settings = {}
        self.ydl_opts = {
            "format": "m4a/bestaudio/best",
            "noplaylist": True,
            "outtmpl": f"{self.audio_path}/%(title)s.%(ext)s",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
            "progress_hooks": [self.get_audio_download_status],
            }
        
        self.process_files()

    def load_configuration(self, app_path: str) -> None:
        path = os.path.join(app_path, 'app_config.json')
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
            self.app_data = json.loads(text)

    def process_files(self) -> None:
        """Process the project files. If the files haven't been processed yet(transcribed and vectorized), it does so.

        Returns:
            None
        """        
        
        text_file = os.path.join(self.project_path, 'text')
        text_file = os.path.join(self.project_path, 'text')
        text_file = os.path.join(self.project_path, 'text')

    def get_audio_download_status(self, d):
        if d['status'] == 'downloading':
            print(d['eta'])

    def get_audio_from_video(self):
        pass

    def get_audio_file(self):
        pass

    def delete_audio_text_files(self, audio_filaneme: str) -> None:
        """Deletes a corresponding audio and text file.

        Args:
            audio_filaneme (str): The filename for the audio file.
        """        

    def get_audio_online(self, url: str) -> str:
        """Extracts the audio from an online media, given the `url`."""

        try:
            yt_handler = yt.YoutubeDL(self.ydl_opts)
            info = yt_handler.extract_info(url, download=False)
            file_path = yt_handler.prepare_filename(info)
            filename_ext = os.path.basename(file_path)
            filename = os.path.splitext(filename_ext)[0]
            yt_handler.process_info(info)
            print('filename is ', filename)
            return filename
        except:
            return ''


    def process_audios(self) -> bool:
        exts = ['*.m4a', '*.mp3', '*.wav', '*.flac', '*.mp4', '*.wma', '*.aac', '*.ogg']

        print(os.listdir(self.audio_path))

        for filename in os.listdir(self.audio_path):
            if any(fnmatch.fnmatch(filename, extension) for extension in exts):
                cur_file = os.path.join(self.audio_path, filename)
                filename_extensionless = os.path.splitext(filename)[0]
                print('cur_file is: ', cur_file) 
                print('is valid: ', os.path.isfile(cur_file))

                model = WhisperModel(model_size_or_path=self.app_data['user_config']['model'],
                                     cpu_threads=self.app_data['user_config']['cpu_threads'],
                                     download_root=self.models_path)
                segments, info = model.transcribe(cur_file)
                print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

                buffer = io.StringIO()
                for segment in segments:
                    print("[%.2fm -> %.2fm] %s"% (segment.start / 60, segment.end / 60, segment.text))
                    buffer.write(segment.text)

                transcribed_text_path = os.path.join(self.text_path, f"{filename_extensionless}.txt")
                with open(transcribed_text_path, 'w', encoding='utf-8') as f:
                    f.write(buffer.getvalue())

        self.build_vector_store()
        

    def build_vector_store(self) -> bool:
        exts = ['*.txt']
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=32)

        for filename in os.listdir(self.text_path):
            if any(fnmatch.fnmatch(filename, extension) for extension in exts):
                cur_file = os.path.join(self.text_path, filename)

                with open(cur_file, 'r', encoding='utf-8') as f:
                    text = f.read()
                    splits = text_splitter.split_text(text)
            
        embeddings = OpenAIEmbeddings()
        vectordb = FAISS.from_texts(splits, embeddings)
        vectordb.save_local(self.db_path, self.project_name)

    def _load_project_file(self) -> bool:
        """Loads the project settings to self.project_settings.

        Returns:
            bool: True true if found and loaded successfully. False otherwise.
        """

        path = os.path.join(self.project_path, 'project_settings.json')
        path = os.path.join(self.project_path, 'project_settings.json')
        path = os.path.join(self.project_path, 'project_settings.json')
        if not os.path.isfile(path):
            return False
        else:
            self.project_settings = json.load(path)
            return True


from storage_manager import StorageManager
#info = StorageManager().create_project_files('testing', 'aaaaaaaaaa', 'medium')
m = ProjectManager('/Users/lmonteir/.HandySpeechBot', '/Users/lmonteir/.HandySpeechBot/projects/testing')
m.get_audio_online('https://www.youtube.com/watch?v=_5u6XokSq4M')
m.process_audios()
m.build_vector_store()