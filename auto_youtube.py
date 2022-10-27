import pytube
import os
from lazyload import FileLoader
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter, WebVTTFormatter


class AutoYoutube:
    can_traslate: bool = True

    def download_node(self, file_name: str):
        f: list = FileLoader(file_name).data
        self._download_node(f["items"], f["name"])

    def _download_node(self, node_items, path: str = None):
        for item in node_items:
            mkd_folder: str = item["name"]
            if path is not None:
                mkd_folder = os.path.join(path, mkd_folder)
            print("Carpeta {}".format(mkd_folder))
            try:
                os.makedirs(mkd_folder)
            except Exception:
                pass
            if "items" in item:
                self._download_node(item["items"], mkd_folder)
            elif "videos" in item:
                # Descargar en carpeta creada
                for v in item["videos"]:
                    url_video: str = v
                    if url_video is not None and len(url_video) > 0:
                        self.download_youtube(mkd_folder, url_video)

    def on_progress(self, a, b, c):
        print("Descargando... {} {}".format(a, c))

    def download_youtube(self, path: str, url: str):
        ext = "mp4"
        yt = pytube.YouTube(url, self.on_progress)
        if not os.path.exists(os.path.join(path, "{}.{}".format(yt.title, ext))):
            print(
                "Descargando {} duracción {} seg. {}".format(
                    yt.title, yt.length, "yt.description"
                )
            )
            try:
                yt.streams.filter(progressive=True, file_extension=ext).order_by(
                    "resolution"
                ).desc().first().download(path)
            except Exception as e:
                print("ERROR => {}".format(e))
        else:
            print("Ya existe {}.{}".format(yt.title, ext))
        # Tomar el id de la url del video y descargar
        video_id = url.replace("https://youtu.be/", "")
        if self.can_traslate:
            self.download_translate(video_id, path, yt.title)

    def download_translate(self, video_id, path, file_name: str):
        type: str = "en"
        try:
            file_names = [
                os.path.join(path, file_name + "_" + type + ".srt"),
                os.path.join(path, file_name + "_" + type + ".json"),
            ]
            if len([x for x in file_names if os.path.exists(x)]) == len(file_names):
                return False
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id
            )  # , languages=['es'])
            formatter = JSONFormatter()
            formater_web = WebVTTFormatter()
            web_formated = formater_web.format_transcript(transcript)
            json_formatted = formatter.format_transcript(transcript)
            data_to_files = [web_formated, json_formatted]

            # Now we can write it out to a file.
            for x in range(0, len(file_names) - 1):
                file_name = file_names[x]
                data = data_to_files[x]
                with open(file_name, "w", encoding="utf-8") as m_file:
                    m_file.write(data)
                    m_file.close()
                    print("Descargado traduccion {}".format(file_name))
        except Exception as e:
            print("ERROR download_translate => {}".format(e))


if __name__ == "__main__":
    m_cls = AutoYoutube()
    # m_cls.download_node("courses.yaml")
    m_cls.can_traslate = False
    m_cls.download_node("courses.yaml")
