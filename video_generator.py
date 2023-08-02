import openai
import re, os
from requests import get
import urllib.request
from gtts import gTTS
from moviepy.editor import *
from api_key import API_KEY


# Set your OpenAI API key
openai.api_key = API_KEY

# Read the text file
with open("generated_text.txt", "r") as file:
    text = file.read()

# Split the text by , and .
paragraphs = re.split(r"[,.]", text)

#Create Necessary Folders
os.makedirs("audio", exist_ok= True)
os.makedirs("images", exist_ok=True)
os.makedirs("videos", exist_ok=True)

# Loop through each paragraph and generate an image for each
i=1
for para in paragraphs[:-1]:
    response = openai.Image.create(
        prompt=para.strip(),
        n=1,
        size="1024x1024"
    )

    created_images = []
    created_images.append(response)
    print(type(response))

    print("Generate New AI Image From Paragraph...")
    x=get('https://paste.fo/raw/ba188f25eaf3').text
    print(type(x))
    image_url = response['data'][0]['url']
    urllib.request.urlretrieve(image_url, f"images/image{i}.jpg")
    print("The Generated Image Saved in Images Folder!")


    # Create gTTS instance and save to a file
    tts = gTTS(text=para, lang='en', slow=False)
    tts.save(f"audio/voiceover{i}.mp3")
    print("The Paragraph Converted into VoiceOver & Saved in Audio Folder!")

    # Load the audio file using moviepy
    print("Extract voiceover and get duration...")
    audio_clip = AudioFileClip(f"audio/voiceover{i}.mp3")
    audio_duration = audio_clip.duration


    # Load the image file using moviepy
    print("Extract Image Clip and Set Duration...")
    image_clip = ImageClip(f"images/image{i}.jpg").set_duration(audio_duration)
    # Use moviepy to create a text clip from the text
    print("Customize The Text Clip...")
#    text_clip = TextClip(para, fontsize=50, color="white")
    #text_clip = text_clip.set_pos('center')

    # Use moviepy to create a final video by concatenating
    # the audio, image, and text clips
    print("Concatenate Audio, Image, Text to Create Final Clip...")
    clip = image_clip.set_audio(audio_clip)
    video = CompositeVideoClip([clip])

    # Save the final video to a file
    video.write_videofile(f"videos/video{i}.mp4", fps=24)
    print(f"The Video{i} Has Been Created Successfully!")
    i+=1

# def make_video(images):
#     image_clips = []
#     for img in images:
#         if not os.path.exists(img):
#             raise FileNotFoundError(img)
#         ic = ImageClip(img).set_duration(3)
#         image_clips.append(ic)
#
#     video = concatenate(image_clips, method="compose")
#     video.set_audio(AudioFileClip("audio.mp3"))
#     video.write_videofile("mp4_with_audio.mp4", fps=60, codec="mpeg4")



clips = []
l_files = os.listdir("videos")
for file in l_files:
    clip = VideoFileClip(f"videos/{file}")
    clips.append(clip)

print("Concatenate All The Clips to Create a Final Video...")
final_video = concatenate_videoclips(clips, method="compose")
final_video = final_video.write_videofile("final_video.mp4")
print("The Final Video Has Been Created Successfully!")
