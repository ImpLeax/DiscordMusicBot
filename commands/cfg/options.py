ffmpeg_standart = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -re -thread_queue_size 2048 -threads 2",
    "options": "-vn -ar 48000 -ac 2 -f s16le  -c:a pcm_s16le"
}

ffmpeg_looped = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -re -stream_loop -1 -thread_queue_size 2048 -threads 2",
    "options": "-vn -ar 48000 -ac 2 -f s16le -c:a pcm_s16le"
}

ydl_opts = {
        'format': 'webm[abr>0]/bestaudio/best',  
        'quiet': True,              
        'noplaylist': True,         
        'skip_download': True,
        'extract_flat': True,
        'no_warnings': True,   
        'username': None,       
        'password': None,   
    }
