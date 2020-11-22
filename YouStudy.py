import re
from datetime import timedelta
from googleapiclient.discovery import build

api_key = 'AIzaSyA9GoHCZoFefD0U0xxvgTYTE6-fLr4s3yU'
youtube = build('youtube', 'v3', developerKey=api_key)

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')
print("Welcome to YouStudy - A study platform from YouTube")

class YouStudy:
		
	def video_playlist_id(self):
		
		vid_src = input("Enter the skill you wish to learn from youtube:")
		print("Searching the best video for you to learn ..........................")
		print("")

		vid_search = youtube.search().list(
				q = vid_src,
				part='snippet,id',
				type = 'video,playlist',
				maxResults = 5
			)
		response = vid_search.execute()
		#print(response)
		self.vid_id = []
		self.pl_id = []
		for item in response['items']:
			if item['id']['kind'] == 'youtube#video':
				self.vid_id.append(item['id']['videoId'])
			else:	
				self.pl_id.append(item['id']['playlistId'])
				
		#print(vid_id)
		#print(pl_id)

	def vid_info(self):

		vid_request = youtube.videos().list(
				part='snippet,contentDetails',
				id = ','.join(self.vid_id)
			)

		vid_response = vid_request.execute()
		for item in vid_response['items']:
			duration = item['contentDetails']['duration']
			#print(duration)

			hours = hours_pattern.search(duration)
			minutes = minutes_pattern.search(duration)
			seconds = seconds_pattern.search(duration)

			hours = int(hours.group(1)) if hours else 0
			minutes = int(minutes.group(1)) if minutes else 0
			seconds = int(seconds.group(1)) if seconds else 0
			
			vid_id = item['id']
			yt_link = f'https://youtu.be/{vid_id}'	

			print("The title for the video is:",item['snippet']['title'])
			print("To watch above video the duration is: " + "{0} hours:{1} minutes:{2} seconds".format(hours, minutes, seconds))
			print("The video url is ",yt_link)
			print("")

	def playlist_info(self):
		total_seconds = 0
		for pl_item in self.pl_id: 
			pl_request = youtube.playlistItems().list(
					part='snippet,contentDetails',
					playlistId = pl_item,
					maxResults = 50
				)

			pl_response = pl_request.execute()
			pl_vid_ids = []
			for item in pl_response['items']:
				pl_vid_ids.append(item['contentDetails']['videoId'])

				pl_vid_request = youtube.videos().list(
					part='contentDetails',
					id = ','.join(pl_vid_ids)
				)
				pl_title = item['snippet']['title']

				pl_vid_response = pl_vid_request.execute()
				for item in pl_vid_response['items']:
					pl_duration = item['contentDetails']['duration']
					#print(pl_duration)

					hours = hours_pattern.search(pl_duration)
					minutes = minutes_pattern.search(pl_duration)
					seconds = seconds_pattern.search(pl_duration)

					hours = int(hours.group(1)) if hours else 0
					minutes = int(minutes.group(1)) if minutes else 0
					seconds = int(seconds.group(1)) if seconds else 0

					video_seconds = timedelta(
						hours = hours,
						minutes = minutes,
						seconds = seconds
						).total_seconds()
					
					
					total_seconds += video_seconds

					pl_id = pl_item
					pl_yt_link = f'https://youtu.be/playlist?list={pl_id}'	
			
						
			total_seconds = int(total_seconds)

			minutes, seconds = divmod(total_seconds, 60)
			hours, minutes = divmod(minutes, 60)

			print("The title for the playlist is:",pl_title)
			print("To watch above playlist the duration is:" + "{0} hours:{1} minutes:{2} seconds".format(hours, minutes, seconds))
			print("The playlist url is ",pl_yt_link)
			print("")


while True:

	run = YouStudy()
	run.video_playlist_id()
	run.vid_info()
	run.playlist_info()
	print("Do you wish to watch another video(yes/no):")
	i = input()
	print("")
	if i == "yes":
		continue
	else:
		print("Thank you for using YouStudy!")
		break

