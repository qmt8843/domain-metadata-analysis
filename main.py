from googlesearch import search
from time import sleep
import urllib.request
import os
import shutil

###Ask for/import domain###
def get_domains():
    domain_list = []
    get_domain_bool = True
    while get_domain_bool:
        domain = input("Type a domain you would like to search for indexed files: ")
        if domain != "" or " " in domain: #Check for blank domain or spaces
            while True:
                confirm = input(f"You gave the domain [{domain}], is this correct? (y/n) ")
                if confirm.upper()=="Y":
                    domain_list.append(domain)
                    add_more = input(f"\nYou are now searching the following domains: {domain_list}\nDo you want to add another? (y/n) ")
                    if add_more.upper()=="Y":
                        print("\n")
                        break
                    elif add_more.upper()=="N":
                        get_domain_bool = False
                        break
                    else:
                        add_more = input(f"You are now searching the following domains: {domain_list}\nDo you want to add another? (y/n) ")
                    break
                elif confirm.upper()=="N":
                    print("\n")
                    break
                else:
                    confirm = input(f"You gave the domain {domain}, is this correct? (y/n) ")
        else:
            print("You cannot enter a blank domain or a domain that contains spaces!\n")
    del get_domain_bool
    return domain_list

###Search indexers for URLs associated with that domain###
def get_urls(domain_list):
    print(f"Searching {domain_list} on indexers for files")
    total_finds = {}

    # Google
    google_filetypes = ["pdf", "ps", "csv", "epub", "kml", "kmz", "gpx", "hwp", "html", "htm", "xls", "xlsx", 
                    "ppt", "pptx", "doc", "docx", "odp", "ods", "odt", "rtf", "svg", "tex", "txt", "text", 
                    "bas", "c", "cc", "cpp", "cxx", "h", "hpp", "cs", "java", "pl", "py", "wml", "wap", 
                    "xml", "bmp", "gif", "jpeg", "jpg", "png", "webp", "avif", "3gp", "3g2", "asf", "avi",
                    "divx", "m2v", "m3u", "m3u8", "m4v", "mkv", "mov", "mp4", "mpeg", "ogv", "qvt", "ram",
                    "rm", "vob", "webm", "wmv", "xap", "php"]
    google_finds = {}
    for domain in domain_list:
        google_finds[domain]={}
        for filetype in google_filetypes:
            sleep(30)
            google_finds[domain][filetype]=[]
            query = f"site:{domain} filetype:{filetype}"
            print(f"Searching {filetype}")
            for j in search(query, tld="co.in", pause=50):
                google_finds[domain][filetype].append(j)
                #print(f"GOOGLE  {filetype.upper()}  {j}")
    total_finds["GOOGLE"] = google_finds
    
    return total_finds

###Download files found at URLs###
# Tag format: [indexer]-[filetype]-[url]-[filename]
def download_urls(finds, include_sorted=False):
    #If include_sorted is true, it will create a file directory called sorted_downloads which will
    #sort the images by their indexer, domain and filetype
    if not os.path.exists("raw-downloads"):
        os.makedirs("raw-downloads")
    if not os.path.exists("sorted-downloads") and include_sorted:
        os.makedirs("sorted-downloads")
    for indexer in finds.keys():
        if not os.path.exists(f"sorted-downloads/{indexer}") and include_sorted:
            os.makedirs(f"sorted-downloads/{indexer}")
        for domain in finds[indexer].keys():
            if not os.path.exists(f"sorted-downloads/{indexer}/{domain}") and include_sorted:
                os.makedirs(f"sorted-downloads/{indexer}/{domain}")
            for filetype in finds[indexer][domain].keys():
                if not os.path.exists(f"sorted-downloads/{indexer}/{domain}/{filetype}") and include_sorted:
                    os.makedirs(f"sorted-downloads/{indexer}/{domain}/{filetype}")
                for url in finds[indexer][domain][filetype]:
                    file_path = f'raw-downloads/{indexer}-{filetype.upper()}-{domain}-{url.split("/")[-1]}'
                    urllib.request.urlretrieve(url, file_path)
                    if include_sorted:
                        print("COPIED")
                        shutil.copy(file_path, f'sorted-downloads/{indexer}/{domain}/{filetype}/{indexer}-{filetype.upper()}-{domain}-{url.split("/")[-1]}')

###Based on file type, search for metadata###
# html searches for comments

###Analyize data###
# What does this entail??

if __name__ == "__main__":
    domain_list = get_domains()
    with open("domain_list.txt", "w") as  file:
        file.write(str(domain_list))
    finds = get_urls(domain_list)
    with open("finds.txt", "w") as  file:
        file.write(str(finds))
    #finds = {"GOOGLE":{"natgeofe.com":{"jpg":["https://i.natgeofe.com/k/62e8fe64-df59-47ef-b03d-0588f4ca292b/CHICK_CHINSTRAP_PENGUIN-PROFILES_KIDS_0123.jpg"]}}}
    download_urls(finds, True)