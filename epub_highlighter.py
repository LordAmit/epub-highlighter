'''
Oh, an attractive module description here.
'''
import os
import shutil
import zipfile
from gi.repository import Gtk
from xml.dom import minidom
from xml.etree import ElementTree as ET
import re
import distutils.archive_util

EPUB_PATH = "/home/amit/git/epub-highlighter/epub/winFriends.epub"
# print(os.path.spli(EPUB_PATH)[0] + "tmp")
# os.mkdir(os.path.spli(EPUB_PATH)[0]+"tmp")
EXTRACT_ROOT = "/home/amit/git/epub-highlighter/epub/tmp/"
MIMETYPE_OPF = 'application/oebps-package+xml'
MEDIA_TYPE = 'application/xhtml+xml'
# XML_PATH = '/home/amit/git/epub-highlighter/epub/tmp/test.epub/index_split_000.xhtml'
LIST_PATH = "/home/amit/git/epub-highlighter/list"
current_progress_in_percent = 0
counter = 0


def get_content_files(opf_path: str):
    opf_xml = minidom.parse(opf_path).documentElement
    xhtmls = []
    for element in opf_xml.getElementsByTagName('item'):
        # print(element.getAttribute("href"))
        if element.getAttribute("media-type") == MEDIA_TYPE:
            xhtmls.append(element.getAttribute("href"))
    return xhtmls
    # if element.getAttribute("media-type") is (MEDIA_TYPE):
    #     print(element.getAttribute("href"))


def read_container(extract_path: str)->str:
    container_xml = extract_path + "META-INF/container.xml"
    minidom_xml = minidom.parse(container_xml).documentElement
    opf_path = None
    for element in minidom_xml.getElementsByTagName('rootfile'):
        if element.getAttribute('media-type') == MIMETYPE_OPF:
            # Only take the first full-path available
            opf_path = element.getAttribute('full-path')
            break
    opf_path = extract_path + opf_path
    return opf_path
    # i = root.findall('./rootfile')
    # print(i[0].tag)


def bold_contents(data, to_bold):
    global counter
    # insensitive_hippo = re.compile(re.escape('hippo'), re.IGNORECASE)
    # insensitive_hippo.sub('giraffe', 'I want a hIPpo for my birthday')
    to_bold = str(to_bold).strip()
    to_bold = ' ' + to_bold + ' '
    after_bold = " <b><i>" + to_bold.upper() + "</i></b> "
    # print(to_bold, after_bold)
    insensitive_pattern = re.compile(re.escape(to_bold), re.IGNORECASE)
    changed_data = insensitive_pattern.sub(after_bold, data)
    if data != changed_data:
        counter = counter + 1
    # print(data, changed_data)
    return changed_data


def read_contents(xml_path) -> str:
    return str(open(xml_path, "r").read())


def read_list_of_words(list_path):
    return open(list_path).readlines()


def write_content(xml_path, content):
    open(xml_path, mode='w').write(content)


def do_something_with_progress(progress_in_hundred: int):
    print("Current Progress: " + str(progress_in_hundred))


def replace_xml_files(xmls_with_path, texts, progress_bar=None, status_bar=None):
    global current_progress_in_percent
    xml_file_count = len(xmls_with_path)
    files_processed = 0
    for xml in xmls_with_path:
        # content = open(xml).read()
        # print("Processing: " + xml)
        xml_file_contents = read_contents(xml)
        # print(xml_file_contents)
        for text in texts:
            # print(text)
            xml_file_contents = bold_contents(xml_file_contents, text)
            # print(xml_file_contents)
            write_content(xml, xml_file_contents)
        files_processed = files_processed + 1
        current_progress_in_percent = (files_processed / xml_file_count)
        msg = "processing " + os.path.basename(xml)
        status_bar.push(1, msg)
        progress_bar.set_fraction(current_progress_in_percent)
        while Gtk.events_pending():
            Gtk.main_iteration()
        # do_something_with_progress(current_progress_in_percent)


def create_epub(extracted_epub_path, original_epub_path):
    original_epub_basename = os.path.split(original_epub_path)[1]
    original_epub_dir = os.path.split(original_epub_path)[0]
    # print(original_epub_dir)
    # print(original_epub_basename)
    new_epub_name = os.path.splitext(original_epub_basename)[
        0] + "_highlighted.epub"
    # print(new_epub_name)
    # print(extracted_epub_path)
    new_epub_path = original_epub_dir + "/" + new_epub_name
    # print(new_epub_path)
    zip_path = distutils.archive_util.make_archive(
        new_epub_name, format='zip', root_dir=extracted_epub_path)
    shutil.move(zip_path, new_epub_path + '.zip')
    os.rename(new_epub_path + '.zip', new_epub_path.replace('zip', ''))


def remove_extracted_directory(extract_root):
    import shutil
    shutil.rmtree(extract_root)


def extract_epub_to_tmp_directory(
        epub_path) ->str:
    epub_basename = os.path.basename(EPUB_PATH)
    temp_dir = os.path.split(EPUB_PATH)[
        0] + "/tmp-" + os.path.splitext(epub_basename)[0]
    # os.mkdir(temp_dir)
    # words = ["Test"]
    epub_file = zipfile.ZipFile(epub_path, mode='r')
    # print(epub_basename)
    # extract_path: str = EXTRACT_ROOT + epub_basename + "/"
    extract_path = temp_dir + "/"
    # print(extract_path)
    epub_file.extractall(path=extract_path)
    return extract_path


def get_full_content_xmls_filepaths(extract_path):
    opf_path = read_container(extract_path)
    opf_path_base = os.path.split(opf_path)[0]

    xmls = get_content_files(opf_path)

    xmls_with_path = []
    for xml in xmls:
        xml_with_path = opf_path_base + '/' + xml
        xmls_with_path.append(xml_with_path)

    return xmls_with_path


def main(epub_path, list_path, progress_bar=None, status_bar=None):
    extract_path = extract_epub_to_tmp_directory(epub_path)
    xmls_with_path = get_full_content_xmls_filepaths(extract_path)
    texts = read_list_of_words(LIST_PATH)
    replace_xml_files(xmls_with_path, texts, progress_bar, status_bar)
    create_epub(extract_path, epub_path)
    remove_extracted_directory(extract_path)
    global counter
    success_msg = "Complete! Highlighted " + \
        str(counter) + " Words in " + str(len(xmls_with_path)) + " files"
    status_bar.push(1, success_msg)


if __name__ == '__main__':

    main(EPUB_PATH, LIST_PATH, None)
