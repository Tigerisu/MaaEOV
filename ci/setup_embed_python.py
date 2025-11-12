import os
import sys
import platform
import zipfile
import tarfile
import urllib.request
import urllib.error
from pathlib import Path
import shutil
import subprocess

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

def get_python_exe_path(base_dir, system):
    """Get the path of existing python.exe or None if not found."""
    if system == "windows":
        return os.path.join(base_dir, "python.exe")
    elif system == "darwin":
        python3_path = os.path.join(base_dir, "bin", "pyhton3")
        python_path = os.path.join(base_dir, "bin", "python")
        for path in (python3_path, python_path):
            if os.path.exists(path):
                return path
    return None

def ensure_pip(python_exe_path, python_dir):
    if not python_exe_path or not os.path.exists(python_exe_path):
        print("Python installation missing.")
        return False
    
    # Check if pip already exists
    try:
        subprocess.run(
            [python_exe_path, "-m", "pip", "--version"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
        print("Existing pip installation found.")
        return True
    except subprocess.CalledProcessError:
        print("Pip not found, installing...")
    except FileNotFoundError:
        print("Python executable not found.")
        return False
    
    # Install pip using get-pip.py
    get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
    get_pip_path = os.path.join(python_dir, "get-pip.py")

    print(f"Downloading get-pip.py from {get_pip_url}")
    try:
        download_file(get_pip_url, get_pip_path)
    except Exception as e:
        print(f"Download get-pip.py failed: {e}")
        return False
    
    print("Running get-pip.py.")
    try:
        subprocess.run([python_exe_path, get_pip_path], check=True)
        print("Pip installation succeeded.")
        return True
    except (subprocess.CalledProcessError, OSError) as e:
        print(f"Pip installation failed: {e}")
        return False
    finally:
        if os.path.exists(get_pip_path):
            os.remove(get_pip_path)

def extract_archive(archive_path, dest):
    archive_path = Path(archive_path)
    print(f"Extracting {archive_path} to {dest} ...")
    if archive_path.suffix == ".zip":
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(dest)
        print("Extraction done.")
    elif ".tar" in archive_path.suffixes[-2:]:
        try:
            with tarfile.open(archive_path, "r:*") as tf:
                tf.extractall(path=dest)
            print("Extraction done")
        except tarfile.ReadError as e:
            print(f"Tarfile ReadError: {e}")
            raise
        except Exception as e:
            print(f"Unexpected Error: {e}")
            raise
    else:
        raise ValueError("Unsupported archive format.")

def main():
    system = platform.system().lower()
    arch = platform.machine().lower()
    print(f"Setting up python {PYTHON_VERSION} for {system} ({arch})")

    # Check for existing python installation
    python_exe_path = get_python_exe_path(DEST_DIR, system)
    if python_exe_path and os.path.exists(python_exe_path):
        print(f"Existing python installation found at {python_exe_path}.")
        if ensure_pip(python_exe_path, DEST_DIR):
            print("Pip already installed.")
        else:
            print("Pip installation failed.")
        return
    
    # Check for destination directory
    if os.path.exists(DEST_DIR):
        print(f"{DEST_DIR} exists, attempt to reinstall.")
        try:
            shutil.rmtree(DEST_DIR)
        except OSError as e:
            print(f"Failed to clean {DEST_DIR}: {e}\nPlease retry after removing it.")
            return
        
    # Create destination directory
    os.makedirs(DEST_DIR, exist_ok=True)

    python_exe_path = None

    if system == "windows":
        # install python for windows
        processor_id = os.environ.get("PROCESSOR_IDENTIFIER", "")

        if "ARMv8" in processor_id or "ARM64" in processor_id:
            arch = "arm64"

        arch_map = {
            "amd64": "amd64",
            "x86_64": "amd64",
            "arm64": "arm64",
            "aarch64": "arm64",
        }
        arch_suffix = arch_map.get(arch, arch)
        
        if arch_suffix not in ["amd64", "arm64"]:
            print(f"Error: {arch_suffix} is supported.")
            return
        
        print(f"Downloading python for {system} ({arch})")
        download_url = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/python-{PYTHON_VERSION}-embed-{arch_suffix}.zip"
        zip_path = os.path.join(DEST_DIR, f"python-{PYTHON_VERSION}-embed-{arch_suffix}.zip")

        try:
            download_file(download_url, zip_path)
            extract_archive(zip_path, DEST_DIR)
        except Exception as e:
            print(f"Failed to download or extract python: {e}")
            return
        finally:
            if os.path.exists(zip_path):
                os.remove(zip_path)

        # Modify ._pth
        pth_path = os.path.join(DEST_DIR, f"python{PYTHON_VERSION.replace(".", "")[:3]}._pth")
        if not os.path.exists(pth_path):
            found_pth_files = [
                f for f in os.listdir(DEST_DIR) if f.startswith("python") and f.endswith("._pth")
                ]
            if found_pth_files:
                pth_path = os.path.join(DEST_DIR, found_pth_files[0])
            else:
                print(f"Error: {os.path.join(DEST_DIR, "*._pth")} not found.")
                return
            
        print(f"Modify ._pth file: {pth_path}")
        try:
            with open(pth_path, "r") as f:
                content = f.read()
            new_lines = [
                "import site",
                ".",
                "Lib",
                "Lib\\site-packages",
                "DLLs"
            ]
            for line in new_lines:
                if line not in content.splitlines():
                    content += f"\n{line}"
            with open(pth_path, "w") as f:
                f.write(content)
            print(f"{pth_path} modified.")
        except Exception as e:
            print(f"Failed to modify {pth_path}: {e}")
            return

        python_exe_path = get_python_exe_path(DEST_DIR, system)

    # final check
    if not python_exe_path or not os.path.exists(python_exe_path):
        print("Error: Python executable not found after installation.")
        return
    # install pip
    if ensure_pip(python_exe_path, DEST_DIR):
        print("Python and pip installation succeeded.")
    else:
        print("Pip installation failed.")

if __name__ == "__main__":
    main()
