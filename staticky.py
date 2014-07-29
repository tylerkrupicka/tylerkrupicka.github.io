import re as regex
import os
import datetime
import time
"""
pyng is a static site generator
Created by: Tyler Krupicka and James Dolan
"""

class Post:

    def __init__(self):
        #variables for each post  
        self.title = ""
        self.link = ""
        self.date = ""
        self.content = ""
        self.thumbContent = ""

class Pyng:

    def __init__(self):
        #variables
        self.config = "config.txt"
        self.dict = {}
        self.posts = []

    def main(self):
        #ask the user what task to perform until quit
        while(True):
            cmd = input("Enter Command (generate, new_post, preview, quit): ")
            if cmd == "generate":
                self.generate()
            elif cmd == "new_post":
                self.new_post()
            elif cmd == "preview":
                self.preview()
            elif cmd == "quit":
                break

    def preview(self):
        print("Previewing. Press Ctrl-C to Exit.")
        while True:
            time.sleep(2)
            self.getConfig()
            self.loadPosts()
            self.createPosts()
            self.createIndex()
            self.createAllPosts()        
    
    def generate(self):
        #generate the site by moving pages and filling in text
        self.getConfig()
        print("Loaded Configuration Variables")
        self.loadPosts()
        print("Load Post Data")
        self.createPosts()
        print("Created Post Pages")
        self.createIndex()
        print("Create Index.html")
        self.createAllPosts()
        print("Create All Posts Page")
        print("Generate Completed.")

    def getConfig(self):
        #load all the config variables in to a dictionary
        for line in open(self.config):
            pair = line.split(": ")
            for i in range(0,len(pair)):
                pair[i] = pair[i].strip()
            self.dict[pair[0]] = pair[1]

    def createIndex(self):
        il=open("layouts/index_layout.html", 'r', encoding="utf8")
        page = ''
        for a in il:
            page += a
        #replace each of the dictionary keywords
        for key in self.dict:
            page = page.replace('[[' + key + ']]',self.dict[key])

        #read thumbnail layouts
        ptl=open("layouts/post_thumb_layout.html", 'r', encoding="utf8")
        thumbLayout = ''
        for a in ptl:
            thumbLayout += a

        maxP = 5
        numP = len(self.posts)
        i=0
        thumbs = ''
        while i <= numP-1 and i < maxP:
            post = self.posts[i]
            pL = thumbLayout;
            pL = pL.replace('[[title]]',post.title)
            pL = pL.replace('[[date]]',post.date)
            pL = pL.replace('[[thumbContent]]',post.thumbContent)
            pL = pL.replace('[[link]]',post.link)
            thumbs += pL
            i += 1

        page = page.replace('[[post_thumb]]',thumbs)
            
        
        index = open("index.html",'a',encoding="utf8")
        index.seek(0)
        index.truncate()
        index.write(page)
        index.close()

    def createAllPosts(self):
        ap=open("layouts/all_thumb_layout.html", 'r', encoding="utf8")
        page = ''
        for a in ap:
            page += a
        #replace each of the dictionary keywords
        for key in self.dict:
            page = page.replace('[[' + key + ']]',self.dict[key])

        #read thumbnail layouts
        ptl=open("layouts/post_thumb_layout.html", 'r', encoding="utf8")
        thumbLayout = ''
        for a in ptl:
            thumbLayout += a

        numP = len(self.posts)
        thumbs = ''
        for post in self.posts:
            pL = thumbLayout;
            pL = pL.replace('[[title]]',post.title)
            pL = pL.replace('[[date]]',post.date)
            pL = pL.replace('[[thumbContent]]',post.thumbContent)
            pL = pL.replace('[[link]]',post.link)
            thumbs += pL

        page = page.replace('[[post_thumb]]',thumbs)
            
        
        allPosts = open("allPosts.html",'a',encoding="utf8")
        allPosts.seek(0)
        allPosts.truncate()
        allPosts.write(page)
        allPosts.close()

    def loadPosts(self):
        #make each post file a class and then store them in a list
        self.posts = []
        for filename in os.listdir("posts"):
            #dont add the git ignore
            if filename == ".gitignore":
                pass
            else:
                post = Post()
                p = ""
                for line in open("posts/" + filename):
                    p += line.strip()
                pl = p.split("---")
                head = pl[0].split("Date: ")

                #determine title and date
                post.title = head[0].replace("Title: ", '')
                post.date = head[1]
                content = pl[1].split("<!-- more -->")
                post.thumbContent = content[0]
                post.content = pl[1]
                post.link = "blog/" + filename.strip(".txt") + ".html"

                self.posts.append(post)

        #sort the list of posts by date
        self.posts.sort(key=lambda x: x.date, reverse=True)

    def createPosts(self):
        pl=open("layouts/post_layout.html", 'r', encoding="utf8")
        page = ''
        for a in pl:
            page += a
        #replace each of the dictionary keywords
        for key in self.dict:
            page = page.replace('[[' + key + ']]',self.dict[key])
        
        for post in self.posts:
            pL = page;
            pL = pL.replace('[[post_title]]',post.title)
            pL = pL.replace('[[date]]',post.date)
            pL = pL.replace('[[content]]',post.content)
            pL = pL.replace('[[link]]',post.link)
        
            postFile = open(post.link,'a',encoding="utf8")
            postFile.seek(0)
            postFile.truncate()
            postFile.write(pL)
            postFile.close()
                    
    def new_post(self):
        #create a new post file with the desired header information
        today = datetime.date.today()
        date = today.isoformat()
        title = input("Title: ")
        valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        filename = ''.join(c for c in title if c in valid_chars)
        os.chdir("posts")
        file=open(filename+".txt", "a")
        file.write("Title: " + title + "\n" + "Date: " + date + "\n---\n")
        file.close()
        os.chdir("..")
        print("Post file created. Be careful editing the post header formatting.")

if __name__ == '__main__':
    Pyng().main()
