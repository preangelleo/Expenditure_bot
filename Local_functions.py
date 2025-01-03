from Gemini_gpt import *
from pytube import YouTube
import string, glob

debug = True
WORKING_FOLDER = '/Users/lgg/Downloads/AI_Workingspace'

my_addresses = [
        '0xb411B974c0ac75C88E5039ea0bf63a84aa7B5377', 
        '0xd5Fcbf30f55Cd0EF5b44653B74d45052dC838001', 
        '0x5e278a70193F214C3536FD6f1D298a5eaeF52795', 
        '0x52A1c564d2cf654522D4A229Dd3B7FFbD7C5cd5e',
        '0xc45e28fFBaa9AFd811c37494A07c49A6D16A727D',
        '0x5E3eBE229035D8D920C73b3A98D4ee7AE8b853A4',
        '0x4F3713177e30ae06d78b670Fa49CD94a31891bb7',
        '0x4408d8991D9f4419A53487Fe2027223BA5cf2207',
        '0x7bc198266f1552223A17a6a7660f3feF9171B888',
        '0x95cb45493BcE408e05ec446c4c3D44e619FD2Eac',
        '0xB39Eda9eb34e0F348E84638095fa35640751e206',
        '0x524c1Df83B365484f5293B18269b8007e1A33deb',
        '0x4Dfb418B2dd552cA085FAc5a64b1C4508dc2877F',
        '0x7B6d13C1481a4996545FA32A1a9Dd637446B2a92',
        '0xDa763773158559b7DA4b6caef07D443B850416B7',
        '0x6aFA87a7DEee011269646131fAB580292b64eDb1',
        '0xfc7Eb8e7C2CfE420B7B1E406292Dd5ed53e9cE00',
        '0x9cdcF2cEE75E0cb075aF55b71b1D046286B689EC']

# generate_text(prompt, model_name='gemini-pro')

def remove_punctuation(working_folder = WORKING_FOLDER):
    file_list = os.listdir(working_folder)
    # Define the set of punctuation characters to remove
    punctuation_set = set(string.punctuation) - set(".") - set("_")
    # Loop through all files in the working folder and remove punctuation
    for file_name in file_list:
        # Ignore subdirectories
        if not os.path.isfile(os.path.join(working_folder, file_name)): continue
        # Split the file name into base name and extension
        file_base, file_ext = os.path.splitext(file_name)
        # Remove punctuation from the file base name
        for p in punctuation_set: file_base = file_base.replace(p, '_') if p in file_base else file_base
        file_base = file_base.replace(" ", "_")
        file_base = file_base.replace("___", "_")
        file_base = file_base.replace("__", "_")
        # Rename the file if the file base name has changed
        file_name_new = file_base + file_ext
        os.rename(os.path.join(working_folder, file_name), os.path.join(working_folder, file_name_new))
    return file_base


def get_latest_file_in_folder(folder, extension):
    # Get a list of all files with the given extension in the folder
    files = glob.glob(os.path.join(folder, f"*{extension}"))
    if not files: return False
    # Find the latest file by comparing modification times
    latest_file = max(files, key=os.path.getmtime)
    return latest_file


def download_video_with_captions(url, working_folder = WORKING_FOLDER):
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video.download(working_folder)
    print(f"Downloaded video: {video.title} to {working_folder}")


def download_youtube_video(video_url: str, working_folder = WORKING_FOLDER):
    if not video_url.startswith('https://www.youtube.com/watch?v='): video_url = f'https://www.youtube.com/watch?v={video_url}'
    print(f"DEBUG: Downloading {video_url}")
    today_video_url_file = os.path.join(working_folder, 'today_video_url.txt')
    with open(today_video_url_file, 'w') as f: f.write(video_url)
    download_video_with_captions(video_url, working_folder)
    return remove_punctuation(working_folder)


def create_video_content(working_folder: str = WORKING_FOLDER):
    while True:
        video_url = input("Please input the YouTube video url or Enter 'q' to quit or Enter 'v' to use latest downloaded video: ")
        if not video_url: continue
        if video_url == 'q': break
        if not video_url.lower() == 'v': file_base = download_youtube_video(video_url, working_folder)
        file_base = get_latest_file_in_folder(working_folder, '.mp4').split('.')[0]
        


if __name__ == '__main__':
    print(f"Local_functions is running...")
    create_video_content()