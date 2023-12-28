# SP Youtube-Downloader Console App

[+] USAGE Examples:<br />
- Install required python packages (Built-in packages should be already exist)
`> pip install -r requirements.txt`<br />
- Download single video of '720p' quality<br />
`> python sp_downloader.py video -h`<br />
`> python sp_downloader.py -u '<video_url>' video --q 720`<br />

- Download 5-20 range of videos within playlist of quality '720p' and add numbering prefixes to filenames.
`> python sp_downloader.py playlist -h`<br />
`> python sp_downloader.py -u '<playlist_url>' playlist -n -q 720 --range 5-20`<br />


[+] Python packages:
- argparse
- pytube
- shutil
- os
- sys

[+] Download Youtube single video:
- With specific quality - DEFAULT is highest quality.

[+] Download Youtube video playlist:
- With specific quality - DEFAULT is highest quality.
- Download specific sequence/range from playlist by their indexes shown on browser.
- Download specific videos you choose by their indexes from playlist shown on browser.
- Download full playlist.
- Ability to add numbering prefixes to playlists.

[+] Download single audio from Youtube video.

[+] Download Youtube playlist as audios (MP3) (extracting audios from playlist videos):
- Download specific sequence/range from playlist by indexes shown on browser.
- Download specific audios of videos from playlist by their indexes shown on browser.
- Download full playlist as audios.

[+] Packaging:<br />
`> cd SP-Youtube-Downloader`<br />
`> pip install -r requirements.txt`<br />
`> pyinstaller sp_downloader.py --onefile`<br />
