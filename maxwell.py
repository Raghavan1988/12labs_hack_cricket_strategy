api_key_val = "tlk_054T7PB14TAHJ82EPATGJ08NGYWW"
from twelvelabs import TwelveLabs

client = TwelveLabs(api_key=api_key_val)

video_ids = ["66370d91d1cd5a287c957d14", "66370d91d1cd5a287c957d15", "66370d95d1cd5a287c957d16","663715d0d1cd5a287c957d17"]

summary = ""

for id in video_ids:
    print(id)
    res = client.generate.text(video_id= id,prompt=" Listen to the commentary. Generate a ball by ball commentary of how Maxwell played. For  every ball, generate a description of the shot that Maxwell played. if Maxwell got out, explain how he got out?")
    summary += res.data
    print(res.data)
    print(len(summary))

with open("maxwell_innings_video_analysis.txt", "w") as w:
    w.write(summary)