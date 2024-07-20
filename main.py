from moviepy.editor import VideoFileClip, concatenate_videoclips
from pydub import AudioSegment, silence
import os
import ffmpeg

def detect_codecs(input_video_path):
    probe = ffmpeg.probe(input_video_path)
    video_codec = None
    audio_codec = None
    for stream in probe['streams']:
        if stream['codec_type'] == 'video':
            video_codec = stream['codec_name']
        elif stream['codec_type'] == 'audio':
            audio_codec = stream['codec_name']
    return video_codec, audio_codec

def remove_silence_from_video(input_video_path, output_video_path, silence_threshold=-50.0, chunk_size=5):
    # Detect codecs
    video_codec, audio_codec = detect_codecs(input_video_path)

    # Load video clip
    video = VideoFileClip(input_video_path)
    
    # Extract audio
    audio = video.audio
    audio.write_audiofile("temp_audio.wav")

    # Load audio with pydub
    audio_segment = AudioSegment.from_file("temp_audio.wav", format="wav")

    # Detect non-silent chunks
    non_silent_chunks = silence.detect_nonsilent(audio_segment, min_silence_len=chunk_size, silence_thresh=silence_threshold)

    # Convert non-silent chunks from ms to seconds
    non_silent_chunks = [(start / 1000, end / 1000) for start, end in non_silent_chunks]

    # Create video clips for non-silent chunks
    video_clips = [video.subclip(start, end) for start, end in non_silent_chunks]

    # Concatenate non-silent video clips
    final_clip = concatenate_videoclips(video_clips)

    # Write the result to a file
    final_clip.write_videofile(output_video_path, codec=video_codec, audio_codec=audio_codec)

    # Cleanup temporary audio file
    os.remove("temp_audio.wav")

# Usage
input_video_path = "video.mp4"
output_video_path = "output_video.mp4"
remove_silence_from_video(input_video_path, output_video_path)
