import gi
gi.require_version('Gtk', '3.0')
import epub_highlighter
import util
from gi.repository import Gtk


class InfoHolder:
    def __init__(self):
        self.epub_file_address = "None"
        self.epub_word_list_address = "None"

    def __str__(self):
        return "epub_file: {} epub_word: {} ".format(self.epub_file_address, self.epub_word_list_address)


class Handler:
    def __init__(self, info_holder: InfoHolder, builder):
        self.info_holder = info_holder

    def on_delete_window(self, *args):
        Gtk.main_quit(*args)

    def epub_file_chosen(self, *args):
        self.info_holder.epub_file_address = args[0].get_filename()

    def list_file_chosen(self, *args):
        self.info_holder.epub_word_list_address = args[0].get_filename()

    def button_convert(self, *args):
        check_meaning = builder.get_object("check_with_meaning")
        status_bar = builder.get_object("status_bar")
        if util.check_if_path_exists(self.info_holder.epub_file_address) and util.check_if_path_exists(self.info_holder.epub_word_list_address) and util.check_if_epub(self.info_holder.epub_file_address):
            progress_bar = builder.get_object("epub_progress")
            # print("got epub_progress")
            epub_highlighter.main(
                self.info_holder.epub_file_address, self.info_holder.epub_word_list_address, progress_bar, status_bar, check_meaning.get_active())
        else:
            status_bar.push(1, "Error: Please check files.")


builder = Gtk.Builder()
builder.add_from_file("second.glade")

window = builder.get_object("epub_window")
info_holder = InfoHolder()

builder.connect_signals(Handler(info_holder, builder))
window.show_all()

Gtk.main()
