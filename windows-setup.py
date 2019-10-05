from shared import *

JPACKAGE_URL = "https://download.java.net/java/early_access/jpackage/1/openjdk-14-jpackage+1-49_windows-x64_bin.zip"
JDK_11_LTS = "https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.4%2B11/OpenJDK11U-jdk_x64_windows_hotspot_11.0.4_11.zip"
JFX_13 = "http://gluonhq.com/download/javafx-13-sdk-windows/"

if not os.path.isdir("windows-gen"):
    os.mkdir("windows-gen")
os.chdir("windows-gen")

download_with_progress(JPACKAGE_URL, "jpackage.zip")
unzip("jpackage.zip", "jpackage")

download_with_progress(JDK_11_LTS, "jdk.zip")
unzip("jdk.zip", "jdk")

download_with_progress(JFX_13, "javafx.zip")
unzip("javafx.zip", "javafx")

modules = [
    "jdk.unsupported",
    "jdk.httpserver",
    "javafx.base",
    "javafx.graphics",
    "javafx.controls",
    "jdk.jfr"
]

# if os.path.isdir("image"):
#     print("Removing cached image")
#     shutil.rmtree("image")

# jlink_cmd = [
#         "jdk/jdk-11.0.4+11/bin/jlink.exe",
#         "--compress=1",
#         "--no-header-files",
#         "--no-man-pages",
#         "--dedup-legal-notices=error-if-not-same-content",
#         "--strip-debug",
#         "--module-path", 
#         "javafx/javafx-sdk-13/lib/",
#         "--add-modules",
#         ",".join(modules),
#         "--output",
#         "image"
#         ]

# print("Generating Runtime")
# subprocess.run(jlink_cmd)

if os.path.isdir("app"):
    print("Removing cached app")
    shutil.rmtree("app")

jpackage_cmd = [
    "jpackage/jdk-14/bin/jpackage.exe",
    "--verbose",
    "--input",
    "inputs",
    "--output",
    "app",
    "--app-version",
    "3.0.0",
    "--name",
    "KnotBook",
    "--icon",
    "../knot.ico",
    "--runtime-image",
    "image",
    "--module",
    "kb.application/kb.application.Application"
]

# rename to bin
# remove api-ms ... .dll

print("Generating Application")
subprocess.run(jpackage_cmd)

# print("Removing extra DLL files")

# for p in os.listdir("app/KnotBook/"):
#     if p.endswith("dll") and not p.startswith("applauncher"):
#         os.remove(f"app/KnotBook/{p}")

# os.remove(f'app/KnotBook/KnotBook.ico')

print("Done")
