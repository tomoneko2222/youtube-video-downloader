import os
import string
import re
import colorama
from pytube import YouTube, Playlist

# coloramaの初期化
colorama.init()

# 進捗バーを表示する関数
def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining 
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_bar_length = 10  # 進捗バーの長さを設定
    filled_length = int(progress_bar_length * percentage_of_completion // 100)
    progress_bar = '█' * filled_length + '_' * (progress_bar_length - filled_length)
    print(f'\r{colorama.Fore.GREEN}進捗状況: [{progress_bar}] {percentage_of_completion:.2f}%{colorama.Style.RESET_ALL}', end='')

# ファイル名をクリーンアップする関数
def clean_filename(filename, replace=' '):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned = ''.join(c for c in filename if c in valid_chars)
    cleaned = cleaned.replace(' ', replace)
    return cleaned

# URLが有効かどうかを確認する関数
def is_valid_url(url):
    youtube_regex = r'^(https?://)?(www\.)?youtu(\.be/|be\.com/watch\?v=).*'
    return bool(re.match(youtube_regex, url))

# メディアをダウンロードする関数
def download_media():
    while True:
        url = input("YouTube video url: ")
        if is_valid_url(url):
            while True:
                media_type = input("mp3/mp4: ")
                if media_type.lower() == "mp3":
                    download_mp3(url)
                    break
                elif media_type.lower() == "mp4":
                    download_mp4(url)
                    break
                elif media_type == "":
                    print(f"{colorama.Fore.RED}mp3 or mp4{colorama.Style.RESET_ALL}")
                else:
                    print(f"{colorama.Fore.RED}mp3 or mp4{colorama.Style.RESET_ALL}")
        else:
            print("有効なYouTubeのURLを入力してください。")

# mp3 をダウンロードする関数
def download_mp3(url):
    if "playlist" in url:
        pl = Playlist(url)
        pl.register_on_progress_callback(progress_function)
        pl_name = clean_filename(pl.title)
        os.makedirs(pl_name, exist_ok=True)
        for video in pl.videos:
            audio = video.streams.filter(only_audio=True).first()
            clean_title = clean_filename(video.title)
            filename = f"{clean_title}.mp3"
            counter = 1
            while os.path.exists(os.path.join(pl_name, filename)):
                filename = f"{clean_title} ({counter}).mp3"
                counter += 1
            print(f"\nダウンロード中: {video.title}")
            audio.download(output_path=pl_name, filename=filename)
            print(f"{video.title} をダウンロードしました")
    else:
        yt = YouTube(url)
        yt.register_on_progress_callback(progress_function)
        clean_title = clean_filename(yt.title)
        filename = f"{clean_title}.mp3"
        counter = 1
        while os.path.exists(filename):
            filename = f"{clean_title} ({counter}).mp3"
            counter += 1
        print(f"\nダウンロード中: {yt.title}")
        audio = yt.streams.filter(only_audio=True).first()
        audio.download(filename=filename)
        print(f"{yt.title} をダウンロードしました")

# mp4 をダウンロードする関数
def download_mp4(url):
    if "playlist" in url:
        pl = Playlist(url)
        pl.register_on_progress_callback(progress_function)
        pl_name = clean_filename(pl.title)
        os.makedirs(pl_name, exist_ok=True)
        for video in pl.videos:
            video_stream = video.streams.filter(progressive=True).order_by('resolution').desc().first()
            clean_title = clean_filename(video.title)
            filename = f"{clean_title}.mp4"
            counter = 1
            while os.path.exists(os.path.join(pl_name, filename)):
                filename = f"{clean_title} ({counter}).mp4"
                counter += 1
            print(f"\nダウンロード中: {video.title}")
            video_stream.download(output_path=pl_name, filename=filename)
            print(f"{video.title} をダウンロードしました")
    else:
        yt = YouTube(url)
        yt.register_on_progress_callback(progress_function)
        clean_title = clean_filename(yt.title)
        filename = f"{clean_title}.mp4"
        counter = 1
        while os.path.exists(filename):
            filename = f"{clean_title} ({counter}).mp4"
            counter += 1
        print(f"\nダウンロード中: {yt.title}")
        video_stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
        video_stream.download(filename=filename)
        print(f"{yt.title} をダウンロードしました")

if __name__ == "__main__":
    while True:
        download_media()
