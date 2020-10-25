from tkinter import *
from tkinter.filedialog import askopenfilename
import pygame as pyg
from pygame import mixer
import Algorithms
import Database

# database
connection = Database.connect()
Database.create_table(connection)
# create root
mainWindow = Tk()


# return root
def get_root():
    return mainWindow


# create class
class SkyLoomi:
    # add frames
    addSongFrame = Frame(mainWindow)
    listBoxFrame = Frame(mainWindow)
    # add widgets that need to be created independently
    song_list = Listbox(listBoxFrame, width=100)
    volume = Scale(listBoxFrame, from_=10, to=0)
    # create strings
    path = StringVar()
    song = StringVar()
    current_song = ""
    # linked list for songs
    song_linked_list = Algorithms.LinkedList()

    def __init__(self):
        # initialize
        self.path_field = None
        self.song_field = None
        self.pack_frames()
        self.create_buttons()
        self.path.set('')
        self.make_list_box()
        self.volume.set(5)
        self.set_volume()
        self.make_linked_list()

    # pack frames
    def pack_frames(self):
        self.addSongFrame.pack()
        self.listBoxFrame.pack()

    # create all the widgets and organize them
    def create_buttons(self):
        song_title = Label(self.addSongFrame, text="Song Name:")
        song_location = Label(self.addSongFrame, text="Song Location:")
        path_field = Entry(self.addSongFrame, textvariable=self.path, width=60)
        song_field = Entry(self.addSongFrame, width=15)
        browse_button = Button(self.addSongFrame, text="Browse", command=lambda: self.enter_path(), width=5)
        add_button = Button(self.addSongFrame, text="Add", command=lambda: self.add_song(), width=5)
        delete_button = Button(self.listBoxFrame, text="Delete", command=lambda: self.delete_song())
        play_button = Button(mainWindow, text="Play", command=lambda: self.play_song())
        stop_button = Button(mainWindow, text="Stop", command=lambda: self.stop_song())
        next_button = Button(mainWindow, text="Next", command=lambda: self.next_song())
        song_title.grid(row=1, column=0)
        song_location.grid(row=1, column=2)
        path_field.grid(row=1, column=3)
        song_field.grid(row=1, column=1)
        browse_button.grid(row=1, column=4)
        add_button.grid(row=1, column=5)
        self.volume.pack(side=LEFT)
        self.song_list.pack(side=LEFT)
        delete_button.pack()
        play_button.pack()
        stop_button.pack()
        next_button.pack()

    # function to grab path for file name
    def enter_path(self):
        path_to_file = askopenfilename()
        self.path.set(path_to_file)

    # function create listbox on app startup
    def make_list_box(self):
        songs = Database.get_all_songs(connection)
        for song in songs:
            self.song_list.insert(song[0], f"{song[1]}")

    # creates the linked list
    def make_linked_list(self):
        songs = Database.get_all_songs(connection)
        for song in songs:
            self.song_linked_list.at_end(f"{song[1]}")

    # deletes song from database and listbox
    def delete_song(self):
        songs = Database.get_all_songs(connection)
        try:
            name = self.song_list.get(self.song_list.curselection())
            for song in songs:
                if song[1] == name:
                    self.song_list.delete(self.song_list.curselection())
                    Database.delete_song(connection, name)
        except TclError:
            print("No song selected")

    # add song to database and listbox
    def add_song(self):
        name = self.song_field.get()
        path = self.path_field.get()
        Database.add_song(connection, name,
                          path)
        self.song_linked_list.at_end(name)
        songs = Database.get_all_songs(connection)
        for song in songs:
            self.song_list.delete(0)
        self.make_list_box()

    # grab current song
    def get_current_song(self):
        return self.current_song

    # set current song
    def set_current_song(self, song):
        self.current_song = song

    # play song, grabs either selected listbox entry or first entry
    def play_song(self):
        try:
            name = self.song_list.get(self.song_list.curselection())
        except TclError:
            name = self.song_list.get(0)
        self.set_current_song(name)
        song = Database.get_songs_by_name(connection, name)
        try:
            mixer.music.load(song[0])
            mixer.music.play()
        except pyg.error:
            print("Not a sound file")
        self.update_song()

    # plays next song from currently selected song
    def next_song(self):
        name = self.get_current_song()
        try:
            for node in self.song_linked_list:
                if name == node.data:
                    name = node.next
            if name is not None:
                name = name.data
                self.set_current_song(name)
            else:
                name = self.song_linked_list.head
                name = name.data
                self.set_current_song(name)
            song = Database.get_songs_by_name(connection, name)
            mixer.music.load(song[0])
            mixer.music.play()
        except AttributeError:
            print("no song playing")

    # function to update current song, not currently used
    def update_current(self):
        name = self.get_current_song()
        for node in self.song_linked_list:
            if name == node.data:
                name = node.next
        if name is not None:
            name = name.data
            self.set_current_song(name)
        else:
            name = self.song_linked_list.head
            name = name.data
            self.set_current_song(name)

    # function to update song to next after song ends, not fully working with next button
    def update_song(self):
        name = self.get_current_song()
        for node in self.song_linked_list:
            if name == node.data:
                name = node.next
        if name is not None:
            name = name.data
        else:
            name = self.song_linked_list.head
            name = name.data
        song = Database.get_songs_by_name(connection, name)
        if name is not None:
            mixer.music.queue(song[0])
            # self.set_current_song(name)
        mainWindow.after(1000, self.update_song)

    # set volume function
    def set_volume(self):
        value = self.volume.get() / 10
        mixer.music.set_volume(value)
        mainWindow.after(500, self.set_volume)

    # stops song from playing.
    @staticmethod
    def stop_song():
        mixer.music.stop()
