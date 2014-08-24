import os
import pickle


def ensure_accessible_cache_dir(cache_dir_path):
    if not os.path.exists(cache_dir_path):
        os.mkdir(cache_dir_path)


def store_in_cache(file_path, content):
    file_handle = open(file_path, 'w')
    pickle.dump(content, file_handle)
    file_handle.close()


def get_from_cache(path):
    if not os.path.exists(path):
        return
    file_handle = open(path)
    content = pickle.load(file_handle)
    file_handle.close()
    return content