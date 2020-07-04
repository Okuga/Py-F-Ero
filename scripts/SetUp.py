import cx_Freeze

IMAGES_EXTENSION = ".png"
PLAYERS_OPTIONS = 4
PLAYER_FRAMES = 8

executables = [cx_Freeze.Executable("PyFEro.py")]

players_imgs = []
for i in range(0, PLAYERS_OPTIONS):
    for j in range(0, PLAYER_FRAMES):
        img_path = "../art/player_" + str(i) + "_" + str(j) + IMAGES_EXTENSION
        players_imgs.append(img_path)

cx_Freeze.setup(
    name = "PyFEero.py",
    options = {"build_exe": {"packages": ["pygame"],
    "include_files": players_imgs}},
    executables = executables
)