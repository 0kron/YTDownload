from pytube import YouTube

### Globals
yt = None
streams = []
info_file = {"file_extension":"", 
            "only_audio":False, 
            "resolution":"", 
            "title":"", 
            "filesize":0, 
            "itag":""}

### File Type Selecter
def f_type(streams): 
    type_file = ""
    print("\n\tFile Type\n[1] Video \n[2] Audio")
    choose = input("> ").lower()

    if "1" in choose: 
        type_file = 'video/'

    elif "2" in choose:
        info_file["only_audio"] = True
        type_file= 'audio/'

    else: 
        f_type()

    # MP4/WEBM
    print("\n\tFile Format\n[1] MP4 \n[2] WEBM")
    choose = input("> ").lower()

    if "1" in choose: 
        info_file["file_extension"] = "mp4"
        type_file += 'mp4'

    elif "2" in choose:
        info_file["file_extension"] = "webm"
        type_file += 'webm'

    else: 
        f_type()

    return list(filter(lambda stream: type_file in stream, streams))
    
### Resolution Selecter
def res_select(streams):
    resolutions = []
    for stream in streams: 
        aux = stream
        aux = aux[aux.find('res="')+5:]
        res = aux[:aux.find('"')]
        if res not in resolutions: resolutions.append(res)
    
    i = 0
    aux = ""
    while i < len(resolutions): 
        j = 0
        while j < len(resolutions)-1:
            if int(resolutions[j][:-1]) > int(resolutions[j+1][:-1]): 
                aux = resolutions[j]
                resolutions[j] = resolutions[j+1]
                resolutions[j+1] = aux 
            j +=1
        i += 1

    def selection():
        choose =-1
        i = 0
        print("")
        while i < len(resolutions): 
            print(f"[{i+1}] {resolutions[i]}")
            i += 1
        try: 
            choose = int(input("> ")) - 1
        except: selection()
        
        if 0 <= choose <= len(resolutions)-1: return choose
        else: selection()
    
    ind_res = selection()
    info_file["resolution"] = resolutions[ind_res]
    return list(filter(lambda stream: resolutions[ind_res] in stream, streams))


def get_itag(streams):
    aux = streams[0]
    aux = aux[aux.find('itag="')+6:]
    itag = aux[:aux.find('"')]
    info_file["itag"] = itag
    return itag

### Downloader
def down(video):
    print(f"""--- INFO FILE ---
    \t{info_file["title"]}
    \t{info_file["file_extension"]}""")
    choose = input("Confirm?(y/n): ").lower()
    
    if "y" in choose: 
        try:
            video.download()
        except: 
            print("Download error.")
    else: 
        print("Operation Cancelled")

############################## Connecting to YT -- CORE ##############################
def main():
    print("YOUTUBE DOWNLOADER".center(150)+"\n")
    url = input("URL: ")

    try:
        yt = YouTube(url) 
        info_file["title"] = yt.title()
        streams = [str(stream) for stream in yt.streams.all()]

    except:
        print("Connection Error")
        return None
        

    print("Video: "+info_file["title"])
    print("\n\tDownload Type\n[1] Default \n[2] Customize \n[3] Cancel")
    choose = input("> ").lower()

    if "3" in choose:
        pass

    else:
        if "1" in choose: 
            video = yt.videos.get_highest_resolution()
            down(video)

        elif "2" in choose: 
            streams = f_type(streams)
            if not info_file["only_audio"]: 
                streams = res_select(streams)
            
            itag = get_itag(streams)

            video = yt.streams.get_by_itag(itag)
            down(video)

        else: main()

main()
