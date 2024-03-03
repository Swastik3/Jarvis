from RealtimeSTT import AudioToTextRecorder
import os
import keyboard as kbd

if __name__ == '__main__':

    print("Initializing RealtimeSTT test...")

    full_sentences = []
    displayed_text = ""

    def clear_console():
        for i in range(len(displayed_text)):
            #write a backspace for each character in the displayed text to clear it in any place that takes keyboard input
            kbd.write("\b")

    def text_detected(text):
        global displayed_text
        new_text = " ".join(full_sentences).strip() + " " + text if len(full_sentences) > 0 else text

        if new_text != displayed_text:
            clear_console()
            displayed_text = new_text
            kbd.write(displayed_text)

    def process_text(text):
        full_sentences.append(text)
        text_detected("")

    recorder_config = {
        'spinner': False,
        'model': 'small',
        'language': 'en',
        'silero_sensitivity': 0.4,
        'webrtc_sensitivity': 2,
        'post_speech_silence_duration': 0.4,
        'min_length_of_recording': 0,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0.2,
        'realtime_model_type': 'tiny.en',
        'on_realtime_transcription_update': text_detected, 
    }

    recorder = AudioToTextRecorder(**recorder_config)

    clear_console()
    print("Say something...", end="", flush=True)

    while True:
        str = recorder.text(process_text)
        if str.lower().split()[-1] == "stop":
            break