import ffmpeg
import datetime

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def fetch_gdrive():
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    gdrive = GoogleDrive(gauth)
    return gdrive


def save_to_gdrive(file_name, mimetype, gdrive_folder_id):
    gdrive = fetch_gdrive()

    targetFile = gdrive.CreateFile({
        "title": file_name,
        "mimetype": mimetype["mimetype"],
        "parents": [{
            "kind": "drive#fileLink",
            "id": gdrive_folder_id
        }]
    })
    file_name_with_parents = f"output/{file_name}"
    targetFile.SetContentFile(file_name_with_parents)
    targetFile.Upload()


def get_today_string(date_format):
    today = datetime.datetime.now()
    today_string = today.strftime(date_format)
    return today_string


def fetch_audio_file(archive_path, file_name, time):
    file_name_with_parents = f"output/{file_name}"
    stream = ffmpeg.input(archive_path)
    stream = ffmpeg.output(stream, file_name_with_parents,
                           format='mp3', ss=0, t=time)
    ffmpeg.run(stream)


def main():
    DATE_FORMAT = "%Y%m%d%H%M"
    ARCHIVE_PATH = "https://nhkradioakr2-i.akamaihd.net/hls/live/511929/1-r2/1-r2-01.m3u8"  # 第2放送
    AUDIO_TIME = 30
    PROGRAM_NAME = "録音テスト"
    MIMETYPE_TO_OUTPUT = {"mimetype": "audio/mpeg", "extension": "mp3"}
    GDRIVE_FOLDER_ID = "18xRd_70O53dt2FYO24LUahgVkcW62dCA"
    today_string = get_today_string(DATE_FORMAT)
    file_name_to_output = f"{today_string}_{PROGRAM_NAME}.{MIMETYPE_TO_OUTPUT['extension']}"

    fetch_audio_file(ARCHIVE_PATH, file_name_to_output, AUDIO_TIME)

    save_to_gdrive(file_name_to_output, MIMETYPE_TO_OUTPUT, GDRIVE_FOLDER_ID)


if __name__ == '__main__':
    main()
