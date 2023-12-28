# SP Youtube-Downloader Console App

[+] USAGE Examples:<br />
`> pip install -r requirements.txt`<br />
`> python sp_downloader.py -h`<br />
`> python sp_downloader.py video -h`<br />
`> python sp_downloader.py -u '<url>' -p '<path>' video --quality 720`<br />
`> python sp_downloader.py -u '<url>' -p '<path>' playlist -n`<br />
`> python sp_downloader.py -u '<url>' audio --playlist -V 1,5,6`<br />


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
