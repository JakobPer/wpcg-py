import wpcg.utils.utils as utils

class AppSettingsModel:
    """
    Settings for the application, cannot be shared as they are dependant on a common location.
    """

    def __init__(self,
                 base_dir: str = "",
                 download_dir: str = "",
                 prettify_dir: str = "") -> None:

        self.base_dir = base_dir or utils.get_app_dir()
        self.download_dir = download_dir or utils.get_download_dir(self.base_dir)
        self.prettify_dir = prettify_dir or utils.get_prettified_dir(self.base_dir)

class SharedSettingsModel:
    """
    Settings that can be shared.
    """

    def __init__(self, 
                wallpaper_width=1920,
                wallpaper_height=1080,
                change_interval=3600000,
                prettification_enabled=True,
                prettification_threshold=0.1,
                repeat_background=True,
                blur_background=True,
                blur_amount=10,
                blend_edges=True,
                blend_ratio=0.02,
                predownload_count=3) -> None:

        self.wallpaper_width = wallpaper_width
        self.wallpaper_height = wallpaper_height
        self.change_interval = change_interval
        self.prettification_enabled = prettification_enabled
        self.prettification_threshold = prettification_threshold
        self.repeat_background = repeat_background
        self.blur_background = blur_background
        self.blur_amount = blur_amount
        self.blend_edges = blend_edges
        self.blend_ratio = blend_ratio
        self.predownload_count = predownload_count
