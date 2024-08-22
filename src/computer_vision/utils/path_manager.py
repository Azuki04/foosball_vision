import os


def get_base_image_path(state='raw'):
    return os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', state, 'images')


def get_image(filename: str, state: str = 'raw'):
    return os.path.join(get_base_image_path(state), filename)


def get_base_video_path(state='raw'):
    return os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', state, 'input_videos')


def get_video(filename: str, state: str = 'raw'):
    return os.path.join(get_base_video_path(state), filename)
