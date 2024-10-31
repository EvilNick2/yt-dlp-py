import yt_dlp
import subprocess

def videoDownload():
	def format_selector(ctx):
		# formats are already sorted worst to best
		formats = ctx.get('formats')[::-1]

		# acodec='none' means there is no audio
		best_video = next(f for f in formats
						if f['vcodec'] != 'none' and f['acodec'] == 'none')

		# find compatible audio extension
		audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
		# vcodec='none' means there is no video
		best_audio = next(f for f in formats if (
			f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

		# These are the minimum required fields for a merged format
		yield {
			'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
			'ext': best_video['ext'],
			'requested_formats': [best_video, best_audio],
			# Must be + separated list of protocols
			'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
		}


	ydl_opts = {
		'format': format_selector,
		'ffmpeg_location': 'backend\\ffmpeg\\ffmpeg.exe',
		'outtmpl': {'default': 'downloads/Videos/%(uploader)s/%(title)s.%(ext)s',
					'pl_thumbnail': ''},
		'postprocessors': [{'format': 'jpg',
												'key': 'FFmpegThumbnailsConvertor',
												'when': 'before_dl'},
												{'already_have_subtitle': False,
												'key': 'FFmpegEmbedSubtitle'},
												{'add_chapters': True,
												'add_infojson': 'if_exists',
												'add_metadata': True,
												'key': 'FFmpegMetadata'},
												{'already_have_thumbnail': False, 'key': 'EmbedThumbnail'}],
		'subtitleslangs': ['en.*'],
		'writesubtitles': True,
		'writethumbnail': True,
		'ratelimit': None
	}

	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		ydl.download(URLS)

def musicDownload():
    def format_selector(ctx):
        # formats are already sorted worst to best
        formats = ctx.get('formats')[::-1]

        # acodec='none' means there is no audio
        best_video = next(f for f in formats if f['vcodec'] != 'none' and f['acodec'] == 'none')

        # find compatible audio extension
        audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
        # vcodec='none' means there is no video
        best_audio = next(f for f in formats if f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext)

        # These are the minimum required fields for a merged format
        return [{
            'format_id': f'{best_audio["format_id"]}',
            'ext': best_audio['ext'],
            'requested_formats': [best_audio],
            # Must be + separated list of protocols
            'protocol': f'{best_audio["protocol"]}'
        }]

    ydl_opts_playlist = {
        'format': format_selector,
        'ffmpeg_location': 'backend\\ffmpeg\\ffmpeg.exe',
        'outtmpl': 'downloads/Music/%(uploader)s/%(playlist_index)s - %(title)s.%(ext)s',
        'merge_output_format': 'm4a',  # Specify the desired output format
        'postprocessors': [
            {'key': 'FFmpegMetadata'},
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegEmbedSubtitle'}
        ],
        'ratelimit': None
    }

    ydl_opts = {
        'format': format_selector,
        'ffmpeg_location': 'backend\\ffmpeg\\ffmpeg.exe',
        'outtmpl': 'downloads/Music/%(uploader)s/%(title)s.%(ext)s',
        'merge_output_format': 'm4a',  # Specify the desired output format
        'postprocessors': [
            {'key': 'FFmpegMetadata'},
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegEmbedSubtitle'}
        ],
        'ratelimit': None
    }


    musicOrdered = input("Make video playlist ordered? (Y/N) ")
    while True:
        if musicOrdered.lower() == "y" or musicOrdered == '':
            with yt_dlp.YoutubeDL(ydl_opts_playlist) as ydl:
                ydl.download(URLS)
                break
        elif musicOrdered.lower() == "n":
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(URLS)
                break
        else:
            print("You did not enter a correct option.")
            musicOrdered = input("Make video playlist ordered? (Y/N) ")

if __name__ == "__main__":
    URLS = []

    while True:
        url = input("Please enter a YouTube URL, or press enter to continue: ")
        if url == '':
            break
        with open('backend/urls.txt', 'a') as file:
            file.write(url + '\n')

    # Read URLs from the file, ignoring the first line
    with open('backend/urls.txt', 'r') as file:
        next(file)  # Skip the first line
        for line in file:
            url = line.strip()
            if url:
                URLS.append(url)
        
    musicDownload()