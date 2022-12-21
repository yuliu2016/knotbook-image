from urllib.request import urlopen, urlretrieve
from traceback import print_exc
import sys
import platform
import tarfile
import zipfile
import os
import shutil
import ntpath
import subprocess
import stat

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def download_file(url, target, block_size=2 ** 19):
    if os.path.exists(target):
        print(f"File {target} already exists. Skipping download.")
        return
    print(f"Downloading {url} into {target}")
    try:
        u = urlopen(url)
        with open(target, 'wb') as f:
            file_size_downloaded = 0
            while True:
                buffer = u.read(block_size)
                if not buffer:
                    break
                file_size_downloaded += len(buffer)
                f.write(buffer)

                mb = file_size_downloaded / 1000000
                print(f"Downloaded {mb:.2f}MB")
        print("Done downloading.")
    except Exception:
        print_exc()
        print("Failed to download files")
        input()
        sys.exit(1)

def unzip(path: str, name: str):
    # assume file format here
    if os.path.exists(name):
        print(f"Folder {name} Already Exists. Skipping unzip.")
        return
    print(f"Unzipping {path}")
    with zipfile.ZipFile(path, "r") as zf:
        zf.extractall(name)
    print("Done unzipping.")

def extract_tar(path: str, name: str):
    if os.path.exists(name):
        print(f"Folder {name} Already Exists. Skipping extract tar.")
        return
    print(f"Extracting {path}")
    with tarfile.open(path, "r:gz") as tf:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tf, name)
    print("Done extracting tar.")

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:xz") as tar:
        tar.add(source_dir)

# https://stackoverflow.com/questions/1889597/deleting-directory-in-python
def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

p = platform.system()
is_windows = p == "Windows"
is_mac = p == "Darwin"
is_linux = p == "Linux"

if is_windows:
    if not os.path.isdir("windows-gen"):
        os.mkdir("windows-gen")
    os.chdir("windows-gen")
    JPACKAGE_URL = "https://download.java.net/java/early_access/jpackage/1/openjdk-14-jpackage+1-70_windows-x64_bin.zip"
    JDK_URL = "https://download.java.net/java/GA/jdk13.0.1/cec27d702aa74d5a8630c65ae61e4305/9/GPL/openjdk-13.0.1_windows-x64_bin.zip"
    JFX_URL = "https://gluonhq.com/download/javafx-13-jmods-windows/"
    JLINK_EXEC = "jdk/jdk-13.0.1/bin/jlink.exe"
    JPACKAGE_EXEC = "jpackage/jdk-14/bin/jpackage.exe"
    ICON_PATH = "knot.ico"
    download_file(JPACKAGE_URL, "jpackage.zip")
    unzip("jpackage.zip", "jpackage")

    download_file(JDK_URL, "jdk.zip")
    unzip("jdk.zip", "jdk")

    download_file(JFX_URL, "javafx.zip")
    unzip("javafx.zip", "javafx")
elif is_mac:
    if not os.path.isdir("mac-gen"):
        os.mkdir("mac-gen")
    os.chdir("mac-gen")
    JPACKAGE_URL = "https://download.java.net/java/early_access/jpackage/1/openjdk-14-jpackage+1-70_osx-x64_bin.tar.gz"
    JDK_URL = "https://download.java.net/java/GA/jdk13.0.1/cec27d702aa74d5a8630c65ae61e4305/9/GPL/openjdk-13.0.1_osx-x64_bin.tar.gz"
    JFX_URL = "https://gluonhq.com/download/javafx-13-jmods-mac/"
    JLINK_EXEC = "jdk/jdk-13.0.1.jdk/Contents/Home/bin/jlink"
    JPACKAGE_EXEC = "jpackage/jdk-14,jdk/Contents/Home/bin/jpackage"
    ICON_PATH = "knot.png"
    download_file(JPACKAGE_URL, "jpackage.tar.gz")
    extract_tar("jpackage.tar.gz", "jpackage")

    download_file(JDK_URL, "jdk.tar.gz")
    extract_tar("jdk.tar.gz", "jdk")

    download_file(JFX_URL, "javafx.zip")
    unzip("javafx.zip", "javafx")
elif is_linux:
    if not os.path.isdir("linux-gen"):
        os.mkdir("linux-gen")
    os.chdir("linux-gen")
    JPACKAGE_URL = "https://download.java.net/java/early_access/jpackage/1/openjdk-14-jpackage+1-70_linux-x64_bin.tar.gz"
    JDK_URL = "https://download.java.net/java/GA/jdk13.0.1/cec27d702aa74d5a8630c65ae61e4305/9/GPL/openjdk-13.0.1_linux-x64_bin.tar.gz"
    JFX_URL = "https://gluonhq.com/download/javafx-13-jmods-linux/"
    JLINK_EXEC = "jdk/jdk-13.0.1/bin/jlink"
    JPACKAGE_EXEC = "jpackage/jdk-14/bin/jpackage"
    ICON_PATH = "knot.png"
    download_file(JPACKAGE_URL, "jpackage.tar.gz")
    extract_tar("jpackage.tar.gz", "jpackage")

    download_file(JDK_URL, "jdk.tar.gz")
    extract_tar("jdk.tar.gz", "jdk")

    download_file(JFX_URL, "javafx.zip")
    unzip("javafx.zip", "javafx")
else:
    print("Unspported Platform")
    sys.exit(1)

if not os.path.isdir("kotlin"):
    os.mkdir("kotlin")

KT = "1.3.60"

KT_STDLIB = f"http://repo1.maven.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/{KT}/kotlin-stdlib-{KT}-modular.jar"
KT_REFLECT = f"http://repo1.maven.org/maven2/org/jetbrains/kotlin/kotlin-reflect/{KT}/kotlin-reflect-{KT}-modular.jar"

download_file(KT_STDLIB, f"kotlin/kotlin-stdlib-{KT}-modular.jar")
download_file(KT_REFLECT, f"kotlin/kotlin-reflect-{KT}-modular.jar")

modules = [
    "java.logging",
    "java.desktop",
    "jdk.unsupported",
    "jdk.httpserver",
    "jdk.jfr",
    "jdk.crypto.cryptoki",
    "jdk.crypto.ec",
    "jdk.crypto.mscapi",
    "javafx.base",
    "javafx.graphics",
    "javafx.controls",
    "javafx.fxml",
    "javafx.swing",
    "kotlin.stdlib",
    "kotlin.reflect",
    "org.controlsfx.controls",
    "rsyntaxtextarea"
]

if os.path.isdir("image"):
    print("Removing cached image")
    shutil.rmtree("image")

jlink_cmd = [
        JLINK_EXEC,
        "--compress=1",
        "--no-header-files",
        "--no-man-pages",
        "--strip-debug",
        "--strip-native-commands",
        "--module-path", 
        "javafx/javafx-jmods-13/;kotlin/;../lib/",
        "--add-modules",
        ",".join(modules),
        "--output",
        "image"
        ]

print("Generating Runtime")
ret = subprocess.run(jlink_cmd).returncode
if ret != 0:
    sys.exit(ret)

if os.path.isdir("KnotBook"):
    print("Removing cached app")
    shutil.rmtree("KnotBook", onerror=remove_readonly)

jpackage_cmd = [
    JPACKAGE_EXEC,
    "--verbose",
    "--type",
    "app-image",
    "--app-version",
    "3.0.0",
    "--name",
    "KnotBook",
    "--icon",
    f"../{ICON_PATH}",
    "--runtime-image",
    "image",
    "--java-options",
    " ".join([
        "--module-path app/libs/",
        # Enable SpreadsheetView
        "--add-exports=javafx.controls/com.sun.javafx.scene.control.behavior=org.controlsfx.controls",
        "--add-exports=javafx.base/com.sun.javafx.event=org.controlsfx.controls",
        # For accessing VirtualFlow field from the base class in GridViewSkin
        "--add-opens=javafx.controls/javafx.scene.control.skin=org.controlsfx.controls",
        # For accessing getChildren in ImplUtils
        "--add-opens=javafx.graphics/javafx.scene=org.controlsfx.controls",
        "-Xms32m",
        "-Xmx256m"
    ]),
    "--module",
    "kb.abc/kb.abc.Main"
]

print("Generating Application")
ret = subprocess.run(jpackage_cmd).returncode
if ret != 0:
    sys.exit(ret)

if is_windows:
    print("Removing extra files")

    for p in os.listdir("KnotBook/"):
        if p.endswith("dll") and not p.startswith("applauncher"):
            os.remove(f"KnotBook/{p}")

    os.remove("KnotBook/KnotBook.ico")
    os.remove("KnotBook/.jpackage.xml")

print("Done")