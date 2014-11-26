import re as regex
import os
import datetime
import time
"""
Staticky is a static site generator
Created by: Tyler Krupicka with help from James Dolan
"""

class Post:

    def __init__(self):
        #variables for each post  
        self.title = ""
        self.link = ""
        self.date = ""
        self.content = ""
        self.thumbnail = ""
        self.thumbContent = ""

class Staticky:

    def __init__(self):
        #variables
        self.config = "config.txt"
        self.dict = {}
        self.elements = {}
        self.posts = []
        self.thumbs = []
        self.valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.previewing = False

    def main(self):
        self.setup()
        #ask the user what task to perform until quit
        while(True):
            cmd = input("Enter Command (generate, new_post, new_page, preview, quit): ")
            if cmd == "generate":
                self.generate()
            elif cmd == "new_post":
                self.new_post()
            elif cmd == "preview":
                self.preview()
            elif cmd == "new_page":
                self.new_page()
            elif cmd == "quit":
                break

    def preview(self):
        print("Previewing. Press Ctrl-C to Exit.")
        self.previewing = True
        while True:
            time.sleep(2)
            self.getConfig()
            self.loadElements()
            self.loadPosts()
            self.createPosts()
            self.createPages()        
    
    def generate(self):
        #generate the site by moving pages and filling in text
        self.getConfig()
        print("Loaded Configuration Variables")
        self.loadElements()
        print("Elements Loaded")
        self.loadPosts()
        print("Loaded Post Data")
        print("Creating Post Files")
        self.createPosts()
        print("Creating Pages")
        self.createPages()
        print("Generate Completed.")

    def getConfig(self):
        #load all the config variables in to a dictionary
        for line in open(self.config):
            pair = line.split(": ")
            for i in range(0,len(pair)):
                pair[i] = pair[i].strip()
            self.dict[pair[0]] = pair[1]

    def loadElements(self):
        for filename in os.listdir("layouts/elements"):
            name = filename.replace(".html","")
            element = ""
            for line in open("layouts/elements/" + filename):
                element += line
            self.elements[name] = element

    def createThumbs(self):
        self.thumbs = []
        #read thumbnail layouts
        ptl=open("layouts/elements/post_thumb.html", 'r', encoding="utf8")
        thumbLayout = ''
        for a in ptl:
            thumbLayout += a
        thumbs = ''
        for post in self.posts:
            pL = thumbLayout;
            pL = pL.replace('[[post.title]]',post.title)
            pL = pL.replace('[[post.date]]',post.date)
            pL = pL.replace('[[post.thumbContent]]',post.thumbContent)
            pL = pL.replace('[[post.link]]',post.link)
            pL = pL.replace('[[post.thumbnail]]',post.thumbnail)
            self.thumbs.append(pL)
    
    def createPages(self):
        for filename in os.listdir("layouts/"):
            if filename == "elements":
                pass
            else:
                file = open("layouts/" + filename, 'r', encoding="utf8")
                page = ''
                #propigate page
                for a in file:
                    page += a
                #thumbs
                self.createThumbs()
                #limit page length
                limitThumbs = ""
                for i in range(int(self.dict["num_thumb"])):
                    if len(self.thumbs) >= i-1 and len(self.thumbs) != 0:
                        limitThumbs += self.thumbs[i]
                #all thumbs
                allThumbs = ""
                for thumb in self.thumbs:
                    allThumbs += thumb
                self.elements["post_thumb_all"] = allThumbs
                self.elements["post_thumb"] = limitThumbs

                #replace elements
                for element in self.elements:
                    page = page.replace('[[' + element + ']]',self.elements[element])

                #replace config keywords
                for key in self.dict:
                    page = page.replace('[[' + key + ']]',self.dict[key])
                
                #create file
                f = open(filename,'a',encoding="utf8")
                f.seek(0)
                f.truncate()
                f.write(page)
                f.close()
                if self.previewing == False:
                    print("     Created " + filename)

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
                t = pl[0].split("Date: ")
                t2 = t[1].split("Thumbnail:")

                #determine title and date
                post.title = t[0].replace("Title: ", '')
                post.date = t2[0].replace("Date: ", '')
                post.thumbnail = t2[1]
                post.thumbnail = post.thumbnail.strip()
                content = pl[1].split("<!-- more -->")
                post.thumbContent = content[0]
                post.content = pl[1]
                link = ''.join(c for c in post.title if c in self.valid_chars)
                link = link.replace(" ","-")
                post.link = "blog/" + link + ".html"

                self.posts.append(post)

        #sort the list of posts by date
        self.posts.sort(key=lambda x: x.date, reverse=True)

    def createPosts(self):
        pl=open("layouts/elements/post.html", 'r', encoding="utf8")
        page = ''
        for a in pl:
            page += a
        #replace each of the dictionary keywords
        for key in self.dict:
            page = page.replace('[[' + key + ']]',self.dict[key])
        
        for post in self.posts:
            pL = page;
            pL = pL.replace('[[post.title]]',post.title)
            pL = pL.replace('[[post.date]]',post.date)
            pL = pL.replace('[[post.content]]',post.content)
            pL = pL.replace('[[post.link]]',post.link)
            pL = pL.replace('[[post.thumbnail]]',post.thumbnail)
        
            postFile = open(post.link,'a',encoding="utf8")
            postFile.seek(0)
            postFile.truncate()
            postFile.write(pL)
            postFile.close()

            if self.previewing == False:
                    print("     Created " + post.title)
            
    def new_post(self):
        #create a new post file with the desired header information
        today = datetime.date.today()
        date = today.isoformat()
        title = input("Title: ")
        thumbnail = input("Thumbnail (hit enter for none): ")
        filename = ''.join(c for c in title if c in self.valid_chars)
        os.chdir("posts")
        file=open(filename+".txt", "a")
        file.write("Title: " + title + "\n" + "Date: " + date + "\n" + "Thumbnail: " + thumbnail + "\n---\n\n<!-- more -->\n")
        file.close()
        os.chdir("..")
        print("Post file created. Be careful editing the post header formatting.")

    def new_page(self):
        title = input("Page filename (no extension): ")
        filename = ''.join(c for c in title if c in self.valid_chars)
        #create page
        file = open("layouts/" + filename + ".html",'a',encoding="utf8")
        file.write(" ")
        file.close()
        print("Page created in the layouts folder.")
        
    def setup(self):
        if len(os.listdir(".")) <= 3:
            choice = input("Setup Directory? (y/n): ")
            if choice == "y":
                os.mkdir("blog")
                os.mkdir("images")
                os.mkdir("assets")
                os.mkdir("layouts")
                os.mkdir("layouts/elements")
                os.mkdir("posts")
                os.mkdir("css")

                #make files
                #create config
                file = open("config.txt",'a',encoding="utf8")
                pL =("url: https://github.com/tylerkrupicka/staticky\n" +
                    "year: 2014\n" +
                    "title: Staticky\n" +
                    "subtitle: Python static site builder\n" +
                    "author: Tyler Krupicka\n" +
                    "num_thumb: 5\n" +
                    "about: Staticky is a simple static site builder that uses a set of layouts and configuration variables to quickly populate page layouts with content.\n" +
                    "email: none\n" +
                    "github: none\n" +
                    "twitter: none\n" +
                    "google+: none\n" +
                    "google_analytics_id: none\n")
                file.write(pL)
                file.close()
                #create index
                file = open("layouts/index.html",'a',encoding="utf8")
                file.write(" ")
                file.close()
                #create post thumb
                file = open("layouts/elements/post_thumb.html",'a',encoding="utf8")
                file.write(" ")
                file.close()
                #create post
                file = open("layouts/elements/post.html",'a',encoding="utf8")
                file.write(" ")
                file.close()
                
                print("Setup Complete.")

if __name__ == '__main__':
    Staticky().main()
