# Hashed Storage


## This is python daemon, which work with FastApi and with it you able to load, delete, download, archieve your files.

For starting, you should have installed python, I show example for Linux.

`cd && git clone https://github.com/Act0r1/hashed_storage`

`cd hashed_storage && pip3 install req.txt`

`uvicorn main:app --reload`

And after this you can open page in your browser. For now, I don't have frontend for working, so best way it use docs, for that
just open 127.0.0.1/docs in your browser.

You'll see this:
![image](https://user-images.githubusercontent.com/59477383/211532106-83309eed-763b-4a80-be8c-624e667dfc7f.png)


After that, you should signup, after that authorize. And that's it, now you can upload and delete files. For upload file, just open, click button "Try it
out" and select your files. 
 
### IMPORTANT: don't load same files two times, I'm not processing this error right now!
