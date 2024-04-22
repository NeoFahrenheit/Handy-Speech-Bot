# https://www.youtube.com/watch?v=I8UvQKvOSSw

import os
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from faster_whisper import WhisperModel
import yt_dlp as yt
import io

class DataManager:
    '''Class responsible for loading and storing the documents.'''

    def __init__(self, url: str):
        self.save_dir = 'app/vault/'
        self.ydl_opts = {
            "format": "m4a/bestaudio/best",
            "noplaylist": True,
            "outtmpl": "%(title)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                }
            ],
        }

        self.refresh_docs(url)

    def refresh_docs(self, url: str) -> None:
        '''Refresh the audio files and Documents with new data, given the `urls`.'''

        yt_handler = yt.YoutubeDL(self.ydl_opts)
        info = yt_handler.extract_info(url)
        audio_file_name = info['title'] + '.' + info['ext']
        print(f'audoooo: {audio_file_name}')

        model_size = "small.en"
        model = WhisperModel(model_size, device="cpu", cpu_threads=10, compute_type="int8")
        segments, info = model.transcribe(audio_file_name)
        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

        buffer = io.StringIO()
        for segment in segments:
            print("[%.2fm -> %.2fm] %s" % (segment.start / 60, segment.end / 60, segment.text))
            buffer.write(segment.text)

        self.text = buffer.getvalue()
        self._build_vector_store()
        os.remove(audio_file_name)

    def _build_vector_store(self) -> None:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=32)
        splits = text_splitter.split_text(self.text)
        embeddings = OpenAIEmbeddings()
        vectordb = FAISS.from_texts(splits, embeddings)
        vectordb.save_local(self.save_dir)