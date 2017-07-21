'''
bla bla bla
'''
import os
import zipfile
from xml.dom import minidom
from xml.etree import ElementTree as ET
import re
import distutils.archive_util

epub_path = "/home/amit/git/epub-highlighter/epub/test.epub"
extract_root = "/home/amit/git/epub-highlighter/epub/tmp/"
MIMETYPE_OPF = 'application/oebps-package+xml'
MEDIA_TYPE = 'application/xhtml+xml'
# XML_PATH = '/home/amit/git/epub-highlighter/epub/tmp/test.epub/index_split_000.xhtml'
LIST_PATH = "/home/amit/git/epub-highlighter/list"


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
    after_bold = "<b>" + to_bold + "</b>"
    insensitive_data = re.compile(re.escape(to_bold), re.IGNORECASE)
    return insensitive_data.sub(after_bold, data)


def read_contents(xml_path) -> str:
    return str(open(xml_path, "r").read())


def read_list_of_words(list_path):
    return open(list_path).readlines()


def write_content(xml_path, content):
    open(xml_path, mode='w').write(content)


def replace_xml_files(xmls_with_path, texts):
    for xml in xmls_with_path:
        content = open(xml).read()
        xml_file_contents = read_contents(xml)
        # print(xml_file_contents)

        for text in texts:
            xml_file_contents = bold_contents(xml_file_contents, text)
            write_content(xml, xml_file_contents)


def create_epub(extracted_epub_path, original_epub_name):
    new_epub_name = os.path.splitext(original_epub_name)[0] + "_edited.epub"
    print(new_epub_name)
    print(extracted_epub_path)
    new_epub_path = extract_root + new_epub_name

    distutils.archive_util.make_zipfile(
        new_epub_path, extracted_epub_path)
    os.rename(new_epub_path + '.zip', new_epub_path.replace('zip', ''))


def remove_extracted_directory(extract_root):
    import shutil
    shutil.rmtree(extract_root)


def main():

    # words = ["Test"]
    epub_file = zipfile.ZipFile(epub_path, mode='r')
    epub_basename: str = os.path.basename(epub_path)
    print(epub_basename)
    extract_path: str = extract_root + epub_basename + "/"
    # print(extract_path)
    epub_file.extractall(path=extract_path)
    opf_path = read_container(extract_path)
    opf_path_base = os.path.split(opf_path)[0]

    xmls = get_content_files(opf_path)

    xmls_with_path = []
    for xml in xmls:
        xml_with_path = opf_path_base + '/' + xml
        xmls_with_path.append(xml_with_path)

    # content = open(XML_PATH).read()
    # xml_file_contents = read_contents(XML_PATH)
    # # print(xml_file_contents)
    texts = read_list_of_words(LIST_PATH)
    # for text in texts:
    #     xml_file_contents = bold_contents(xml_file_contents, text)
    # # print(xml_file_contents)
    # write_content(XML_PATH, xml_file_contents)
    replace_xml_files(xmls_with_path, texts)
    create_epub(extract_root + epub_basename, epub_basename)
    remove_extracted_directory(extract_root)


if __name__ == '__main__':
    main()
