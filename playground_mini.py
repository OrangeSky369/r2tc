import os
import shutil

# lsd = os.listdir("temp_sessions")
# shutil.rmtree("temp_sessions\\" + lsd[0])

folders = [os.path.join("temp_sessions", folder) for folder in os.listdir("temp_sessions") if
                   os.path.isdir(os.path.join("temp_sessions", folder))]

print(folders)
print(type(folders))
print(folders[0])

shutil.rmtree(folders[0])