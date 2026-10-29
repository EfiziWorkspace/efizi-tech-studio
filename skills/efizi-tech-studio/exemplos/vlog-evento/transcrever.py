import json, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
for f in sys.argv[2:]:
    pcm = subprocess.run(["ffmpeg","-v","error","-i",f,"-map","0:a:0","-ac","1","-ar","16000","-f","s16le","-"],capture_output=True,check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    segs, info = m.transcribe(audio, language="pt", word_timestamps=True, vad_filter=False, beam_size=5)
    out = []
    for s in segs:
        out.append({"ini": round(s.start, 2), "fim": round(s.end, 2), "txt": s.text.strip(),
                    "logprob": round(s.avg_logprob, 2), "palavras": [[w.word, round(w.start, 2), round(w.end, 2)] for w in s.words]})
        print(f"[{s.start:6.2f}-{s.end:6.2f}] ({s.avg_logprob:.2f}) {s.text.strip()}", flush=True)
    name = f.rsplit("/", 1)[-1]
    json.dump(out, open(f"{sys.argv[1]}/{name}.json", "w"), ensure_ascii=False, indent=1)
    print("==== fim", name, flush=True)
