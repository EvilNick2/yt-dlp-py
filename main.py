import os
import requests
from zipfile import ZipFile
import shutil
import yt_dlp
import json
import enlighten
import math

def getffmpeg():
	ffmpegDir = "backend/ffmpeg"

	if os.path.exists("backend") == False or os.path.exists("backend/ffmpeg") == False:
		os.makedirs("backend/ffmpeg")

	if os.path.isfile(f"{ffmpegDir}/ffmpeg.exe") == False:
		#Download ffmpeg
		print("Downloading ffmpeg")
		
		response = requests.get("https://api.github.com/repos/GyanD/codexffmpeg/releases/latest").json()["name"].split()[1] # Get version number
		version = f"ffmpeg-{response}-essentials_build" # Assign build name
		# open(f"{ffmpegDir}/{version}.zip", "wb").write(requests.get(f"https://www.github.com/GyanD/codexffmpeg/releases/latest/download/{version}.zip").content) # Download latest ffmpeg version
		
		url = f"https://www.github.com/GyanD/codexffmpeg/releases/latest/download/{version}.zip"
		filepath = f"{ffmpegDir}/{version}.zip"
		
		# Should be one global variable
		MANAGER = enlighten.get_manager()

		r = requests.get(url, stream = True)
		assert r.status_code == 200, r.status_code
		dlen = int(r.headers.get('Content-Length', '0')) or None

		with MANAGER.counter(color = 'green', total = dlen and math.ceil(dlen / 2 ** 20), unit = 'MiB', leave = False) as ctr, \
			open(filepath, 'wb', buffering = 2 ** 24) as f:
			for chunk in r.iter_content(chunk_size = 2 ** 20):
				f.write(chunk)
				ctr.update()
	

		print("Unzipping File")
		with ZipFile(f"{ffmpegDir}/{version}.zip", "r") as zip_ref:
			zip_ref.extractall(ffmpegDir)
		
		os.remove(f"{ffmpegDir}/{version}.zip")

		files = ["ffmpeg.exe", "ffprobe.exe"]

		for file in files:
			shutil.move(f"{ffmpegDir}/{version}/bin/{file}", ffmpegDir)
		
		shutil.rmtree(f"{ffmpegDir}/{version}", ignore_errors=True)


if __name__ == "__main__":
	getffmpeg()
	if os.path.exists("backend/urls.txt") == False:
		with open('backend.urls.txt', 'w') as file:
			file.write('# Paste your video/playlist URLs in this file, save and close')
	
	# URL = ["https://www.youtube.com/watch?v=eMFOUl_n-yQ"]

	# def format_selector(ctx):
	# 	""" Select the best video and the best audio that won't result in an mkv.
	# 	NOTE: This is just an example and does not handle all cases """

	# 	# formats are already sorted worst to best
	# 	formats = ctx.get('formats')[::-1]

	# 	# acodec='none' means there is no audio
	# 	best_video = next(f for f in formats
	# 					if f['vcodec'] != 'none' and f['acodec'] == 'none')

	# 	# find compatible audio extension
	# 	audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
	# 	# vcodec='none' means there is no video
	# 	best_audio = next(f for f in formats if (
	# 		f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

	# 	# These are the minimum required fields for a merged format
	# 	yield {
	# 		'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
	# 		'ext': best_video['ext'],
	# 		'requested_formats': [best_video, best_audio],
	# 		# Must be + separated list of protocols
	# 		'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
	# 	}


	# ydl_opts = {
	# 	'format': format_selector,
	# 	'ffmpeg_location': "backend\\ffmpeg\\ffmpeg.exe"
	# }

	# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
	# 	ydl.download(URL)


	