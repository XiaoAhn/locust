import pdfplumber
import re

def clean_page(file_path, pg_num):
    with pdfplumber.open(file_path) as pdf:
        page = pdf.pages[pg_num]
    left, right = get_left_side(page), get_right_side(page)
    #right = get_right_side(page)
    for side in [left, right]:
        side = single_word(side)
        side = two_word(side)
        side = many_countries(side)
    return (left, right)


def get_left_side(page):
    x0 = 0
    x1 = page.width // 2
    bottom = page.height - 80
    top = 0

    rv = page.crop((x0, top, x1, bottom))
    rv = rv.extract_text()
    return rv

def get_right_side(page):
    x0 = page.width // 2
    x1 = page.width
    bottom = page.height - 80
    top = 0


    rv = page.crop((x0, top, x1, bottom))
    rv = rv.extract_text()
    return rv
    #return page.crop((x0, top, x1, bottom)).extract_text()

def single_word(text):
    print("text is: ", text)
    return re.sub(r'(\n[A-Z]) *\n([A-Z]+)', r'\1\2', text)

def two_word(text):
    line_list = text.split('\n')
    for i, line in enumerate(line_list):
        country = []
        to_replace = []
        if re.match(r'[A-Z]  [A-Z]', line):
            first_line = line
            first_line_list = line.split("  ")
            #print(first_line)
            next_line = line_list[i + 1]
            next_line_list = next_line.split(" ")
            #print(next_line)
            for n in range(len(first_line_list)):
                country.append(first_line_list[n] + next_line_list[n])
            #print(country)
            country = " ".join(country)
            to_replace.append(first_line)
            to_replace.append(next_line)
            to_replace = "\n".join(to_replace)
            text = text.replace(first_line+'\n'+next_line, country)
    return text

def many_countries(text):
    line_list = text.split('\n')
    to_replace = []
    for i, line in enumerate(line_list):
        to_replace = []
        rv = ""
        if re.match(r'[A-Z] ( [A-Z])?,', line):
            #print(line)
            #first_line = line
            to_replace.append(line)
            #print("to_replace", to_replace)
            first_line_list = re.split(" ", line)
            #first_line_list = [sub.replace('', '') for sub in first_line_list]
            #first_line_list = line.split("  ")
            #print(first_line_list)
            next_line = line_list[i + 1]
            to_replace.append(next_line)
            #print(next_line)
            next_line_list = next_line.split(" ")
            #print(next_line_list)
            suffix_cnt = 0
            for i, char in enumerate(first_line_list):
                #print("char is: ", char)
                if re.search(r'[A-Z]', char):
                    rv += char + next_line_list[suffix_cnt]
                    suffix_cnt += 1
                #elif not char and not first_line_list[i - 1]: # not repeated empty string
                elif not char: # not repeated empty string
                    #if first_line_list[i - 1]:
                    if not rv.endswith(" "):
                        rv += " "
                        #print("empty space not repeated")
                    else:
                        rv += char + next_line_list[suffix_cnt]
                        suffix_cnt += 1
                        #print(" repeated empty space")
                else:
                    rv += char
                #print(rv)    
        to_replace = '\n'.join(to_replace)
        if to_replace and rv:
            print("to_replace", to_replace)
            print(rv)
        cleaned_text = text.replace(to_replace, rv)
        # replace the text
    return cleaned_text