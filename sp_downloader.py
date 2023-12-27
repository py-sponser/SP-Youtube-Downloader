from argparse import ArgumentParser
from sys import argv
from sp_downloader_class import SPDownloader


# download specific videos from playlist by number


def get_args():
    parser = ArgumentParser("SP Youtube Downloader")
    parser.add_argument("-u", "--url", required=True, help="YouTube 'VIDEO/PLAYLIST' URL - "
                                                           "URL of a video must be given between quotations.")
    parser.add_argument("-p", "--path", default=".", help="PATH to save on disk - CWD is default.")

    subparsers = parser.add_subparsers()

    video_subparser = subparsers.add_parser("video", help="Download type is video.")
    video_subparser.add_argument("-q", "--quality", help="Video quality/resolution (EX. 720 480 360 144)"
                                                               "- DEFAULT is highest resolution.")

    playlist_subparser = subparsers.add_parser("playlist", help="Download type is playlist.")
    playlist_subparser.add_argument("-r", "--range", help="Download specific sequence/range of videos within playlist. "
                                                          "EX. 5-20 of 40 playlist length.")
    playlist_subparser.add_argument("-n", "--number-files", action="store_true",
                                    help="Add numbering to downloaded videos of "
                                         "playlist or not?")
    playlist_subparser.add_argument("-q", "--quality",
                                    help="Specify only one quality/resolution. EX. 720 480 360 144 "
                                         "- DEFAULT is highest resolution.")
    playlist_subparser.add_argument("-V", "--specific-videos", help="Download specific videos from playlist - "
                                                                    "EX. -l 1,6,24")

    audio_subparser = subparsers.add_parser("audio", help="Download type is audio.")
    audio_subparser.add_argument("--playlist", action="store_true", help="Download playlist as MP3 files.")
    audio_subparser.add_argument("-V", "--specific-videos", help="Download specific MP3 instances from playlist - "
                                                                 "EX. -l 1,6,24")
    audio_subparser.add_argument("-r", "--range", help="Download specific sequence/range of audios of playlist videos. "
                                                       "EX. 5-20 of 40 playlist length.")

    arguments = parser.parse_args()
    return arguments, parser.print_help


args, print_help = get_args()
args.url = str(args.url)

handler = SPDownloader()

if "video" in argv:
    handler.download_video(url=args.url, path=args.path, quality=args.quality)
elif "playlist" in argv:
    handler.download_playlist(url=args.url, path=args.path, sequence=args.range, numbering=args.number_files,
                              quality=args.quality, specific_videos=args.specific_videos)
elif "audio" in argv:
    if not args.playlist:
        handler.download_single_audio(url=args.url, path=args.path)
    else:
        handler.download_audio_playlist(url=args.url, path=args.path, sequence=args.range,
                                        specific_videos=args.specific_videos)
else:
    print_help()
