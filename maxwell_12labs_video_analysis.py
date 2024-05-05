api_key_val = "TWELVE LABS KEY"
from twelvelabs import TwelveLabs

client = TwelveLabs(api_key=api_key_val)

video_ids = [] ## list of video ids

summary = ""

for id in video_ids:
    print(id)
    res = client.generate.text(video_id= id,prompt=" Listen to the commentary. Generate a ball by ball commentary of how Maxwell played. For  every ball, generate a description of the shot that Maxwell played. if Maxwell got out, explain how he got out?")
    summary += res.data
    print(len(summary))

with open("maxwell_innings_video_analysis_concat.txt", "w") as w:
    w.write(summary)