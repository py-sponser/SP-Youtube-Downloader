from colorama import Fore, Style
from pytube import Playlist, YouTube, Stream
from shutil import get_terminal_size
from sys import stdout
from os.path import join
from os import remove


def display_progress_bar(bytes_received: int, filesize: int, ch: str = "█", scale: float = 0.55
                         ) -> None:
    """Display a simple, pretty progress bar.

    Example:
    ~~~~~~~~
    PSY - GANGNAM STYLE(강남스타일) MV.mp4
    ↳ |███████████████████████████████████████| 100.0%

    :param int bytes_received:
        The delta between the total file size (bytes) and bytes already
        written to disk.
    :param int filesize:
        File size of the media stream in bytes.
    :param str ch:
        Character to use for presenting progress segment.
    :param float scale:
        Scale multiplier to reduce progress bar size.

    """
    columns = get_terminal_size().columns
    max_width = int(columns * scale)

    filled = int(round(max_width * bytes_received / float(filesize)))
    remaining = max_width - filled
    progress_bar = ch * filled + " " * remaining
    percent = round(100.0 * bytes_received / float(filesize), 1)
    text = f"{Fore.BLUE} ↳ |{progress_bar}| {percent}%\r{Fore.RESET}"
    stdout.write(text)
    stdout.flush()


def on_progress(stream: Stream, chunk: bytes, bytes_remaining: int
                ) -> None:  # pylint: disable=W0613
    filesize = stream.filesize
    bytes_received = filesize - bytes_remaining
    display_progress_bar(bytes_received, filesize)


def check_quality(video, quality):
    """Check whether given/default quality of video exists or not"""
    try:
        quality = int(quality)
    except ValueError:
        print(f"{Fore.RED}[-] Given quality '{quality}' isn't integer.{Fore.RESET}")
        exit(0)
    handler = video.streams.get_by_resolution(f"{quality}p")
    if handler:
        print(f"{Fore.GREEN}[+] Downloading with given quality '{quality}p'.{Fore.RESET}")
        return True
    return False


def get_range(sequence):
    start, end = sequence.split("-")
    try:
        start = int(start)
        end = int(end)
    except ValueError:
        print(f"{Fore.RED}[-] Invalid range - '{start}' & '{end}' aren't integers.{Fore.RESET}")
        exit(0)
    return start, end


def get_specific_videos(specific_videos):
    videos = specific_videos.split(",")
    try:
        videos = [int(num) for num in videos]
    except ValueError:
        print(f"{Fore.RED}[-] Given video numbers aren't valid - they are not integers {videos}{Fore.RESET}")
        exit(0)
    return videos


def fix_video_title(title):
    for symbol in ["\\", "/", "|"]:
        if symbol in title:
            title = title.replace(symbol, "-")
    return title


class SPDownloader:

    # noinspection PyUnusedLocal

    @staticmethod
    def download_playlist(url, path, sequence, numbering, quality, specific_videos):
        playlist = Playlist(str(url))

        print(
            f"\n\t\t{Fore.CYAN}{Style.BRIGHT}{playlist.owner} Channel - '{playlist.title}' playlist - {playlist.length} "
            f"videos{Style.RESET_ALL}{Fore.RESET}\n")
        print(f"{Fore.BLUE}[+] Playlist download path >> {path}{Fore.RESET}")
        print("")

        videos = playlist.videos
        sample_video = videos[0].streams.get_highest_resolution()
        video_extension = sample_video.mime_type.split("/")[1]
        highest_quality = sample_video.resolution
        quality_available = bool()
        playlist_length = playlist.length

        if quality:
            quality_available = check_quality(videos[0], quality)
        else:
            print(f"{Fore.BLUE}[+] Downloading playlist videos of highest resolution. ({highest_quality}){Fore.RESET}")

        if not quality_available and quality:
            print(f"{Fore.RED}[-] '{quality}p' isn't available - proceeding to download highest resolution. "
                  f"({highest_quality}){Fore.RESET}")

        if specific_videos:
            numbers = get_specific_videos(specific_videos)
            print(f"{Fore.BLUE}[+] Downloading videos of indexes {specific_videos} from the playlist.{Fore.RESET}")
            print("")

            try:
                for num in numbers:
                    index = num-1
                    if num > playlist_length:
                        print(f"\n{Fore.RED}[-] Video #{num} is not found - playlist has no index '{num}'.{Fore.RESET}\n")
                        continue

                    videos[index].register_on_progress_callback(on_progress)

                    handler = videos[index].streams.get_highest_resolution() if not quality_available \
                        else videos[index].streams.get_by_resolution(f"{quality}p")
                    file_size = handler.filesize_mb
                    print(f"{Fore.BLUE}[+] Downloading Video #{num} --- ({videos[index].title}.{video_extension}) "
                          f"({handler.resolution}) ({file_size}MB){Fore.RESET}")

                    title = fix_video_title(videos[index].title)
                    file_name = f"{num}- {title}" if numbering else f"{title}"
                    handler.download(path, filename=f"{file_name}.{video_extension}")

                    print("")
            except KeyboardInterrupt:
                print(f"{Fore.RED}[-] Download has stopped - last downloaded video can be incomplete.{Fore.RESET}")
                exit(0)

        elif sequence:
            start, end = get_range(sequence)

            print(f"{Fore.BLUE}[+] Downloading {sequence} sequence/range from the playlist.{Fore.RESET}")
            print("")
            try:
                i = start
                for count in range(start - 1, end):
                    """Had to decrement start-1 due to playlist.videos ordering issue comparing to Youtube
                    if sequence/range is 23-41, then it'll download video 24 on youtube instead of starting with 23.
                    """
                    if count+1 > playlist_length:
                        print(f"\n{Fore.RED}[-] Video #{count+1} is not found - playlist has no index '{count+1}'.{Fore.RESET}")
                        exit(0)
                    videos[count].register_on_progress_callback(on_progress)

                    handler = videos[count].streams.get_highest_resolution() if not quality_available \
                        else videos[count].streams.get_by_resolution(f"{quality}p")
                    file_size = handler.filesize_mb
                    print(f"{Fore.BLUE}[+] Downloading Video #{i} --- ({videos[count].title}.{video_extension}) "
                          f"({handler.resolution}) ({file_size}MB){Fore.RESET}")

                    title = fix_video_title(videos[count].title)
                    file_name = f"{i}- {title}" if numbering else f"{title}"
                    handler.download(path, filename=f"{file_name}.{video_extension}")

                    print("")
                    i += 1
                print(f"\n{Fore.GREEN}[+] Download is complete.{Fore.RESET}")
            except KeyboardInterrupt:
                print(f"{Fore.RED}[-] Download has stopped - last downloaded video can be incomplete.{Fore.RESET}")
                exit(0)
        else:
            try:
                count = 1
                print("")
                for video in playlist.videos:
                    title = fix_video_title(video.title)
                    video.register_on_progress_callback(on_progress)
                    handler = video.streams.get_highest_resolution() if not quality_available \
                        else video.streams.get_by_resolution(f"{quality}p")
                    file_size = handler.filesize_mb
                    print(
                        f"{Fore.BLUE}[+] Downloading Video #{count} --- ({title}.{video_extension}) ({handler.resolution})"
                        f" ({file_size}MB){Fore.RESET}")
                    file_name = f"{count}- {title}" if numbering else f"{title}"

                    handler.download(path, filename=f"{file_name}.{video_extension}")
                    print("")
                    count += 1

                print(f"\n{Fore.GREEN}[+] Download is complete.{Fore.RESET}")
            except KeyboardInterrupt:
                print(f"{Fore.RED}[-] Download has stopped - last downloaded video can be incomplete.{Fore.RESET}")
                exit(0)

    @staticmethod
    def download_video(url, path, quality):
        video = YouTube(str(url), on_progress_callback=on_progress)
        quality_available = bool()
        yt = video.streams.get_highest_resolution()
        highest_quality = yt.resolution
        if quality:
            quality_available = check_quality(video, quality)
        else:
            print(f"{Fore.BLUE}[+] Downloading video of highest resolution. ({highest_quality}){Fore.RESET}")

        if not quality_available and quality:
            print(f"{Fore.RED}[-] '{quality}p' isn't available - proceeding to download highest resolution. "
                  f"({highest_quality}){Fore.RESET}")

        title = fix_video_title(video.title)
        full_path = join(path, f"{title}.{yt.mime_type.split('/')[1]}")
        try:
            handler = video.streams.get_highest_resolution() if not quality_available \
                else video.streams.get_by_resolution(quality)
            video_extension = handler.mime_type.split("/")[1]
            file_size = handler.filesize_mb
            print("")
            print(
                f"{Fore.BLUE}[+] Downloading ({title}.{video_extension}) - ({handler.resolution}) "
                f"({file_size}MB){Fore.RESET}")
            handler.download(path, filename=f"{title}.{video_extension}")

            print("")
            print(f"\n{Fore.GREEN}[+] Download is complete.{Fore.RESET}")

        except KeyboardInterrupt:
            print("")
            print(f"{Fore.RED}[-] Download is failed{Fore.RESET}")
            try:
                remove(full_path)
            except FileNotFoundError:
                exit(0)
            exit(0)

    @staticmethod
    def download_single_audio(url, path):
        video = YouTube(str(url), on_progress_callback=on_progress)

        title = fix_video_title(video.title)
        try:
            handler = video.streams.get_audio_only()
            file_size = handler.filesize_mb
            print(f"{Fore.BLUE}[+] Downloading ({title}.mp3) ({file_size}MB){Fore.RESET}")
            handler.download(path, filename=f"{title}.mp3")

            print("")
            print(f"\n{Fore.GREEN}[+] Download is complete.{Fore.RESET}")

        except KeyboardInterrupt:
            print("")
            print(f"{Fore.RED}[-] Download is failed{Fore.RESET}")
            try:
                file_path = join(path, f"{title}.mp3")
                remove(file_path)
            except FileNotFoundError:
                exit(0)
            exit(0)

    @staticmethod
    def download_audio_playlist(url, path, sequence, specific_videos):
        playlist = Playlist(str(url))
        playlist_length = playlist.length
        print(
            f"\t\t{Fore.CYAN}{Style.BRIGHT}{playlist.owner} Channel - '{playlist.title}' playlist - {playlist_length} "
            f"videos{Style.RESET_ALL}{Fore.RESET}\n")
        print(f"{Fore.BLUE}[+] Playlist download path >> {path}{Fore.RESET}")

        videos = playlist.videos
        if specific_videos:
            numbers = get_specific_videos(specific_videos)
            print(f"{Fore.BLUE}[+] Downloading audios of indexes {specific_videos} from the playlist.{Fore.RESET}")
            try:
                print("")
                for num in numbers:
                    index = num-1
                    if num > playlist_length:
                        print(f"\n{Fore.RED}[-] Audio #{num} is not found - playlist has no index '{num}'.{Fore.RESET}\n")
                        continue
                    videos[index].register_on_progress_callback(on_progress)

                    handler = videos[index].streams.get_audio_only()
                    file_size = handler.filesize_mb
                    print(f"{Fore.BLUE}[+] Downloading Audio #{num} --- ({videos[index].title}.mp3) ({file_size})"
                          f"{Fore.RESET}")

                    title = fix_video_title(videos[index].title)
                    handler.download(path, filename=f"{title}.mp3")

                    print("")
                print(f"\n{Fore.GREEN}[+] Download is complete.{Fore.RESET}")
            except KeyboardInterrupt:
                print(f"{Fore.RED}[-] Download has stopped - last downloaded video can be incomplete.{Fore.RESET}")
                exit(0)

        elif sequence:
            start, end = get_range(sequence)

            print(f"{Fore.BLUE}[+] Downloading audios of '{sequence}' sequence/range from the playlist.{Fore.RESET}")
            print("")
            try:
                i = start
                for count in range(start - 1, end):
                    """Had to decrement start-1 due to playlist.videos ordering issue comparing to Youtube
                    if sequence/range is 23-41, then it'll download video 24 on youtube instead of starting with 23.
                    """
                    if count+1 > playlist_length:
                        print(f"\n{Fore.RED}[-] Audio #{count+1} is not found - playlist has no index '{count+1}'.{Fore.RESET}")
                        exit(0)

                    videos[count].register_on_progress_callback(on_progress)

                    handler = videos[count].streams.get_audio_only()
                    file_size = handler.filesize_mb

                    print(f"{Fore.BLUE}[+] Downloading Audio #{i} --- ({videos[count].title}.mp3) ({file_size}MB)"
                          f"{Fore.RESET}")

                    title = fix_video_title(videos[count].title)
                    handler.download(path, filename=f"{title}.mp3")

                    print("")
                    i += 1
                print(f"\n{Fore.GREEN}[+] Download is complete.{Fore.RESET}")
            except KeyboardInterrupt:
                print(f"{Fore.RED}[-] Download has stopped - last downloaded audio can be incomplete.{Fore.RESET}")
                exit(0)
        else:
            try:
                count = 1
                print("")
                for video in playlist.videos:
                    title = fix_video_title(video.title)
                    video.register_on_progress_callback(on_progress)

                    handler = video.streams.get_audio_only()
                    file_size = handler.filesize_mb

                    print(
                        f"{Fore.BLUE}[+] Downloading Audio #{count} --- ({title}.mp3) ({file_size}MB){Fore.RESET}")

                    handler.download(path, filename=f"{title}.mp3")
                    print("")
                    count += 1

                print(f"\n{Fore.GREEN}[+] Download is complete.{Fore.RESET}")
            except KeyboardInterrupt:
                print(f"{Fore.RED}[-] Download has stopped - last downloaded audio can be incomplete.{Fore.RESET}")
                exit(0)
