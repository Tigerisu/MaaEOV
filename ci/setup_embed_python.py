import os
import sys
import platform
import zipfile
import tarfile
import urllib.request
import urllib.error
from pathlib import Path
import shutil

PYTHON_VERSION = "3.12.10"
DEST_DIR = os.path.join("install", "python")

def download_file(url, dest):
    print(f"Downloading {url} to {dest}...")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        with urllib.request.urlopen(url) as response, open(dest, "wb") as out_file:
            shutil.copyfileobj(response, out_file)
        print(f"Saved to {dest}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason} (URL: {url})")
        raise
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason} (URL: {url})")
        raise
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise

# def extract_archive(archive_path, dest):
#     print(f"Extracting {archive_path} to {dest} ...")
#     if archive_path.suffix == ".zip":
#         with zipfile.ZipFile(archive_path, "r") as zf:
#             zf.extractall(dest)
#     elif archive_path.suffixes[-2:] == [".tar", ".xz"]:
#         with tarfile.open(archive_path, "r:xz") as tf:
#             tf.extractall(dest)
#     else:
#         raise ValueError("Unsupported archive format.")
#     print("Extraction done.")

# def setup_embed_python():
#     system = platform.system().lower()
#     arch = platform.machine().lower()

#     print(f"Setting up Python {PYTHON_VERSION} for {system} ({arch})")

#     if DEST_DIR.exists():
#         print(f"Removing old Python installation at {DEST_DIR}")
#         shutil.rmtree(DEST_DIR)
#     DEST_DIR.mkdir(parents=True, exist_ok=True)

#     archive_file = Path("python-embed.tar.xz")

#     if system == "windows":
#         url = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/python-{PYTHON_VERSION}-embed-amd64.zip"
#         archive_file = Path("python-embed.zip")
#     elif system == "darwin":
#         url = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/python-{PYTHON_VERSION}-macos11.pkg"
#         # macOS doesn't have an embedded version; we can fall back to venv.
#         print("No embedded Python for macOS — creating venv instead.")
#         os.system(f"python3 -m venv {DEST_DIR}")
#         return
#     else:  # Linux
#         url = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/Python-{PYTHON_VERSION}.tar.xz"

#     download_file(url, archive_file)
#     extract_archive(archive_file, DEST_DIR)
#     archive_file.unlink(missing_ok=True)

#     print(f"Embedded Python {PYTHON_VERSION} setup complete at {DEST_DIR}")

# if __name__ == "__main__":
#     setup_embed_python()
