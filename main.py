from pytube import YouTube
import cv2
import os
import time 
from imagetobrailleart import imagetobraille as itb
from playsound import playsound


def download(video, video_number, pathing):
    failed = ""
    print(f"#{video_number} [+] Downloading {video.title}")
    try:
        video_output = video.streams.get_highest_resolution()
        downloaded_file = video_output.download(pathing)
        base, ext = os.path.splitext(downloaded_file)
        new_file = base + ".mp4"
        os.rename(downloaded_file, new_file)
        return new_file
    except Exception as e:
        print(e)

def download_audio(video, video_number, pathing):
    failed = ""
    print(f"#{video_number} [+] Downloading {video.title}")
    try:
        video_output = video.streams.filter(only_audio=True).first()
        downloaded_file = video_output.download(pathing)
        new_file = "AUDIO" + ".mp3"
        os.rename(downloaded_file, new_file)
        return new_file
    except Exception as e:
        print(e)

if __name__ == "__main__":
    playmusic = input("Do you want the sound to play? (Y/n)")
    if playmusic.lower() == "y":
        playmusic = True
    else:
        playmusic = False
    choice = input("Do you want to download a vid [n] or load a previously downloaded [y]: ")
    if choice.lower() == "y":
        directory = input("directory: ")
        if directory == "":
            directory = "." 
        elif not "." in directory:
            directory = "./" + directory
        try:
            config = open(f"{directory}/video/config.txt", encoding="utf-8").read().split("|")
            music = config[1]
            all_files = os.listdir(f"{directory}/coded_frames")
            all_frames = []
            for frame in all_files:
                all_frames += [frame.split(".")[0]]
            all_frames.sort(key=int)
            print("[+] ALL DONE PRINTING ALL IN 10 SECONDS")
            time.sleep(10)
            if playmusic:
                playsound(os.path.abspath(music))
            for file in all_frames:
                with open(f"{directory}/coded_frames/{file}.txt", encoding="utf-8") as f:
                    lines = f.read()
                print("\n" * 35 + lines)
                time.sleep(1 / float(config[0]))
        except FileNotFoundError:
            pass
    else:
        link = input("Youtube Video Link: ")
        video = YouTube(link)
        directory = input("directory: ")
        if directory == "":
            directory = "." 
        elif not "." in directory:
            directory = "./" + directory
        for filename in ["video", "frames", "coded_frames", "video/audio"]:
            try:
                os.mkdir(f"{directory}/{filename}")
            except FileExistsError:
                pass
        video_name = download(video, 1, f"{directory}/video")
        music = download_audio(video, 1, f"{directory}/video/audio")
        music = os.path.abspath(music)
        print("[+] Download Done")
        frames = cv2.VideoCapture(video_name)
        fps = frames.get(cv2.CAP_PROP_FPS)
        text_file = open(f"{directory}/video/config.txt", "w", encoding="utf-8")
        text_file.write(f"{str(fps)}|{music}")
        text_file.close()
        idx = 0
        while True:
            ret, frame = frames.read()
            if ret == False:
                break
            print(f"[+] Saving frame # {idx}")
            cv2.imwrite(f"{directory}/frames/{idx}.png", frame)   
            idx += 1
        new_frames = os.listdir(f"{directory}/frames")
        all_frames = []
        for frame in new_frames:
            all_frames += [frame.split(".")[0]]
        all_frames.sort(key=int)
        for picture in all_frames:
            print(f"[+] Converting frame # {picture} into Braile")
            data = itb(f"{directory}/frames/{picture}.png", size=200, inverse=0)
            text_file = open(f"{directory}/coded_frames/{picture}.txt", "w", encoding="utf-8")
            text_file.write(data)
            text_file.close()
        boomer = os.listdir(f"{directory}/coded_frames")
        all_frames = []
        for frame in boomer:
            all_frames += [frame.split(".")[0]]
        all_frames.sort(key=int)
        print("[+] ALL DONE PRINTING ALL IN 10 SECONDS")
        time.sleep(10)
        if playmusic:
            playsound(music)
        for file in all_frames:
            with open(f"{directory}/coded_frames/{file}.txt", encoding="utf-8") as f:
                lines = f.read()
            print("\n" * 35 + lines)
            time.sleep(1 / fps)
        frames.release()
        do_remove = input("Remove used files? [y/n]: ")
        if do_remove.lower() == "y":
            for filename in ["video", "frames", "coded_frames", "video/audio"]:
                try:
                    os.remove(f"{directory}/{filename}")
                except:
                    pass
