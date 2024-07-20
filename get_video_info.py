import subprocess
import json

def get_all_video_info(video_file):
    # Command to run ffprobe and get the output in JSON format
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_format',
        '-show_streams',
        '-print_format', 'json',
        video_file
    ]

    # Run the command and capture the output
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Parse the JSON output
    video_info = json.loads(result.stdout)
    
    return video_info

# Example usage
video_file = 'video.mp4'
video_info = get_all_video_info(video_file)

# Print the metadata in a readable format
print(json.dumps(video_info, indent=4))
