from shared import *

JPACKAGE_URL = "https://download.java.net/java/early_access/jpackage/1/openjdk-14-jpackage+1-49_windows-x64_bin.zip"
JDK_11_LTS = "https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.4%2B11/OpenJDK11U-jdk_x64_windows_hotspot_11.0.4_11.zip"
JFX_13 = "https://gluonhq.com/download/javafx-13-jmods-windows/"
KT_STDLIB = "http://repo1.maven.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/1.3.50/kotlin-stdlib-1.3.50-modular.jar"
KT_REFLECT = "http://repo1.maven.org/maven2/org/jetbrains/kotlin/kotlin-reflect/1.3.50/kotlin-reflect-1.3.50-modular.jar"

if not os.path.isdir("windows-gen"):
    os.mkdir("windows-gen")
os.chdir("windows-gen")

download_with_progress(JPACKAGE_URL, "jpackage.zip")
unzip("jpackage.zip", "jpackage")

download_with_progress(JDK_11_LTS, "jdk.zip")
unzip("jdk.zip", "jdk")

download_with_progress(JFX_13, "javafx.zip")
unzip("javafx.zip", "javafx")

if not os.path.isdir("kotlin"):
    os.mkdir("kotlin")

download_with_progress(KT_STDLIB, "kotlin/kotlin-stdlib-1.3.50-modular.jar")
download_with_progress(KT_REFLECT, "kotlin/kotlin-reflect-1.3.50-modular.jar")

modules = [
    "java.logging",
    "java.desktop",
    "jdk.unsupported",
    "jdk.httpserver",
    "jdk.jfr",
    "javafx.base",
    "javafx.graphics",
    "javafx.controls",
    "javafx.fxml",
    "javafx.swing",
    "kotlin.stdlib",
    "kotlin.reflect",
]

if os.path.isdir("image"):
    print("Removing cached image")
    shutil.rmtree("image")

jlink_cmd = [
        "jdk/jdk-11.0.4+11/bin/jlink.exe",
        "--compress=1",
        "--no-header-files",
        "--no-man-pages",
        "--strip-debug",
        "--module-path", 
        "javafx/javafx-jmods-13/;kotlin/",
        "--add-modules",
        ",".join(modules),
        "--output",
        "image"
        ]

print("Generating Runtime")
subprocess.run(jlink_cmd)

if os.path.isdir("KnotBook"):
    print("Removing cached app")
    shutil.rmtree("KnotBook", onerror=remove_readonly)

jpackage_cmd = [
    "jpackage/jdk-14/bin/jpackage.exe",
    "--verbose",
    "--package-type",
    "app-image",
    "--app-version",
    "3.0.0",
    "--name",
    "KnotBook",
    "--icon",
    "../knot.ico",
    "--runtime-image",
    "image",
    "--java-options",
    " ".join([
        "--module-path app",
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

# rename to bin
# remove api-ms ... .dll

print("Generating Application")
subprocess.run(jpackage_cmd)

# print("Removing extra files")

for p in os.listdir("KnotBook/"):
    if p.endswith("dll") and not p.startswith("applauncher"):
        os.remove(f"KnotBook/{p}")

os.remove("KnotBook/KnotBook.ico")
os.remove("KnotBook/.jpackage.xml")

print("Done")