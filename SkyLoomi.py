from pygame import mixer
from App import SkyLoomi
import App
# set up audio
mixer.init()
# gui creation
mainWindow = App.get_root()
mainWindow.iconbitmap('icon.ico')
mainWindow.title("SkyLoomi")
mainWindow.geometry("800x275")
# throw in class to complete gui
app = SkyLoomi()
# print nodes for testing
for node in app.song_linked_list:
    print(node.data)
# set resizable to false
mainWindow.resizable(False, False)
# set main loop
mainWindow.mainloop()
