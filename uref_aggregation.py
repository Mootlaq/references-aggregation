import argparse
import sys
import re
import glob
from mdutils.mdutils import MdUtils
from mdutils import Html

def get_pages(foldername): #Gets a list of the page titles
    pages = glob.glob("./{}/*.md".format(foldername))
    if len(pages) == 0:
        print("Error!")
        print('''- Make sure you typed the database's name correctly.
- Make sure the database folder is in the same directory as the '.py' file.''')
    sys.exit()
    pages_names = [page_name.split('/')[-1] for page_name in pages]
    pages_names = [name.split('.md')[0] for name in pages_names]
    return pages_names

def clean_text(text): # Deletes every [[page]], #page and page::
    text = re.sub(r'([\[]{2}[\w\d\s\d_\-,()\"#/@;:<>{&*}`+=~^|.!?∆]+[\]]{2})', '', text)
    text = re.sub(r'([#])([A-Za-z0-9_ء-ي\-]+)', '', text)
    text = re.sub(r'([A-Za-z0-9_ء-ي]+)([:]{2})', '', text)
    return text
    
def find_refs(args, ref):
    found_refs = []
    page_titles = get_pages(args)
    for text in page_titles:
        with open('./{}/{}.md'.format(args, text)) as f:
            note = f.read()
            note = clean_text(note)
            if ref in note:
                found_refs.append(text)            
    return found_refs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('db', type=str, help='add the name of the database folder (NOTE: the folder must be in the same directory as the prorgram file')
    args = parser.parse_args()
    page_titles = get_pages(args.db)
    #print(args.db)
    
    #print(page_titles)
    ref_texts = {}
    for ref in page_titles:
        ref_texts[ref] = find_refs(args.db, ref)
        if ref_texts[ref] == []:
            del ref_texts[ref]
    refs_page = ''
    for k,v in ref_texts.items():
        refs_page = refs_page + ''' - [[{}]] was referenced on: \n'''.format(k)
        for a in v:
            refs_page = refs_page + ''' \t - [[{}]] \n'''.format(a)

    mdFile = MdUtils(file_name='Aggregated Unlinked References')
    mdFile.write(refs_page)
    mdFile.create_md_file()

    
if __name__ == '__main__':
    main()