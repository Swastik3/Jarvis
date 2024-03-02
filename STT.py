from faster_whisper import WhisperModel
import sounddevice as sd
import soundfile as sf
import os
import time

model_size = "large-v3"

class STT():
    def __init__(self,model_size="small.en"):
        print("Loading model...")
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        print("Model loaded")
        self.audio = None

    def record_audio(self, duration=5, sample_rate=44100, save_location=os.path.join("tmp","audio.mp3")):
        
        frames = int(duration * sample_rate)
        print("Recording audio for ", duration, " seconds")
        audio = sd.rec(frames, samplerate=sample_rate, channels=1)
        sd.wait()
        sf.write(save_location, audio, sample_rate)
        print("Audio saved as: ", save_location)
    
    def transcribe(self, audio_filename = os.path.join("tmp","audio.mp3")):
        segments, info = self.model.transcribe(audio_filename, beam_size=5)
        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
        segment_list = []
        for segment in segments:
            segment_list.append(segment.text)
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        return segment_list
        

def main():
    stt = STT()
    stt.record_audio()
    time1 = time.time()
    text = stt.transcribe("tmp/audio.mp3")
    print(text)
    time2 = time.time()
    print("Time taken: ", time2-time1)

if __name__ == "__main__":
    main()
    
    def record_audio(duration=5, sample_rate=44100, save_location=os.path.join("tmp","audio.mp3")):
        frames = int(duration * 60)
        print("Recording audio for ", duration, " seconds")
        audio = sd.rec(frames, samplerate=sample_rate, channels=1)
        sd.wait()
        sf.write(save_location, audio, sample_rate)
        print("Audio saved as: ", save_location)