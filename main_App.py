import threading
from tkinter import filedialog as fd
import customtkinter
from CTkMessagebox import CTkMessagebox
import requests
import spacy
from bs4 import BeautifulSoup


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Anapec auto script")
        self.geometry(f"{700}x{600}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1,3,4,5),weight=0)
        self.grid_rowconfigure(2, weight=1)

        #title
        self.Title = customtkinter.CTkFrame(self, corner_radius=0)
        self.Title.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.Title.grid_columnconfigure(0, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.Title, text="ANAPEC automation", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(10,10),sticky="ew")

        #user
        self.b1 = customtkinter.CTkFrame(self, corner_radius=0, height=50)
        self.b1.grid(row=1, column=0, columnspan=1, sticky="nsew")
        self.entry = customtkinter.CTkEntry(self, placeholder_text="USER")
        self.entry.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(10, 10),sticky="nsew")

        #password
        self.b2 = customtkinter.CTkFrame(self, corner_radius=0, height=50)
        self.b2.grid(row=1, column=1, columnspan=1, sticky="nsew")
        self.entry2 = customtkinter.CTkEntry(self, placeholder_text="PASSWORD", show="*")
        self.entry2.grid(row=1, column=1, columnspan=1, padx=(20, 20), pady=(10, 10),sticky="nsew")

        #motivation
        self.txtt = customtkinter.CTkFrame(self, corner_radius=0)
        self.txtt.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=2, column=0, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        #updates
        self.txt2 = customtkinter.CTkFrame(self, corner_radius=0, height=50)
        self.txt2.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.txt2.grid_columnconfigure(0, weight=1)
        self.logo_labels = customtkinter.CTkLabel(self.txt2, text="Waiting start...",font=(None,18))
        self.logo_labels.grid(row=3, column=0, columnspan=2, pady=(0, 10),sticky="ew")


        #data
        self.b3 = customtkinter.CTkFrame(self, corner_radius=0, height=60)
        self.b3.grid(row=4, column=0, columnspan=1, sticky="nsew")
        self.sidebar_button_1 = customtkinter.CTkButton(self, text="Last post", command=self.select_file_data)
        self.sidebar_button_1.grid(row=4, column=0, columnspan=1, padx=(20, 20), pady=(10, 10),sticky="nsew")

        #keywords
        self.b4 = customtkinter.CTkFrame(self, corner_radius=0, height=60)
        self.b4.grid(row=4, column=1, columnspan=1, sticky="nsew")
        self.sidebar_button_2 = customtkinter.CTkButton(self, text="Keywords", command=self.select_file_keywords)
        self.sidebar_button_2.grid(row=4, column=1, columnspan=1, padx=(20, 20), pady=(10, 10),sticky="nsew")

        #start
        self.strt = customtkinter.CTkFrame(self, corner_radius=0, height=70)
        self.strt.grid(row=5, column=0, columnspan=2, sticky="nsew")
        self.strt_button = customtkinter.CTkButton(self, text="Start", command=self.START, fg_color="blue")
        self.strt_button.grid(row=5, column=0, columnspan=2, padx=(10, 10), pady=(10, 10),sticky="nsew" )
        
    def select_file_data(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
            )
        if filename.split("/")[-1] == "data.txt":
            self.sidebar_button_1.configure(text=f"Last data: {filename.split("/")[-1]}",fg_color="green")
            self.datafile = filename
        else:
            self.sidebar_button_1.configure(text=f"Last data: {filename.split("/")[-1]}",fg_color="red")



    def select_file_keywords(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes
            )
        if filename.split("/")[-1] == "keywords.txt":
            self.sidebar_button_2.configure(text=f"Keywords: {filename.split("/")[-1]}",fg_color="green")
            self.keywordfile = filename
        else:
            self.sidebar_button_2.configure(text=f"Keywords: {filename.split("/")[-1]}",fg_color="red")

    info = {
        "link": [],
        "title": []
        }
    datafile = ""
    keywordfile = ""
    
    def disable(self):
        self.sidebar_button_1.configure(state="disabled")
        self.sidebar_button_2.configure(state="disabled")
        self.entry.configure(state="disabled")
        self.entry2.configure(state="disabled")
        self.textbox.configure(state="disabled")
        self.strt_button.configure(state="disabled",text="Working",fg_color="Red")

    def enable(self):
        self.sidebar_button_1.configure(state="normal")
        self.sidebar_button_2.configure(state="normal")
        self.entry.configure(state="normal")
        self.entry2.configure(state="normal")
        self.textbox.configure(state="normal")
        self.strt_button.configure(state="normal",text="Start",fg_color="blue")
        self.logo_labels.configure(text="Waiting start...")

    def mainThread(self):
  
        session0 = requests.Session()
        if self.getData(session0,self.datafile) != False:
            session,useridd = self.login('http://www.anapec.org/sigec-app-rv/fr/chercheurs/login',self.entry.get(),self.entry2.get())
            validOffers = self.getMatch(self.info["title"],self.keywordfile)
            
            if session != None:
                self.apply(session,self.entry.get(),self.textbox.get("1.0", customtkinter.END).strip(),validOffers,useridd)
        self.enable()
        self.stop.set()


    def alert(self,message):
        CTkMessagebox(title="Error", message=message, icon="cancel")

    def START(self):
        if self.datafile.split("/")[-1] == "data.txt" and self.keywordfile.split("/")[-1] == "keywords.txt" and self.entry.get() != '' and self.entry2.get() != '':
            
            self.disable()
            self.stop = threading.Event()
            threading.Thread(target=self.mainThread).start()
            
        elif self.datafile.split("/")[-1] != "data.txt" or self.keywordfile.split("/")[-1] != "keywords.txt":
           self.alert("add required files")
        
        elif self.entry.get() == '' or self.entry2.get() == '':
            self.alert("Fill user information")

        

    def login(self,login_url,username,password):
    
        payload = {
        '_method': 'POST',
        'rdio': 'candidat',
        'data[cherch_empl][identifiant]': username,
        'data[cherch_empl][mot_pass]': password
        }

        with requests.Session() as session:
            login_response = session.post(login_url, data=payload)
            response = session.get('http://www.anapec.org/sigec-app-rv/fr/chercheurs/index')
            soup = BeautifulSoup(response.text, 'html.parser')
            div = soup.find('div', id="div_actualisezcv")
            if div != None:
                userID = (div.find('a').get('href').split('/')[-1])
                return session,userID
            else:
                return None, None
    
    def getData(self,session,filename="data.txt"):

        page = 1
        exito = False

        with open(filename) as f2:
            date = f2.readline().strip()
            f2.close()

        while True:
            self.logo_labels.configure(text=f"getting page {page}")
            try:
                response = session.get(f"http://www.anapec.org/sigec-app-rv/chercheurs/resultat_recherche/page:{page}/tout:all/language:fr",timeout=15)
            except requests.exceptions.ReadTimeout:
                self.alert("Server down")
                self.stop.set()
                self.enable()
                return False
            soup = BeautifulSoup(response.text, 'html.parser')
            data = soup.find('table', id='myTable')
            t = data.find('tbody').find_all('tr')

            for x in t:
                data =x.find_all('td')
                if data[1].text.encode('iso-8859-1').decode('utf-8')[-6:] == date:
                    if len(self.info['link']) != 0:
                        self.logo_labels.configure(text=f"Done scrapping we got {len(self.info['link'])} offres")
                    exito = True
                    break
                postid = data[1].text.encode('iso-8859-1').decode('utf-8')
                self.info['link'].append(postid[-6:])
                self.info['title'].append(data[3].text.encode('iso-8859-1').decode('utf-8'))
            
            if exito == True:
                if len(self.info['link']) != 0:
                    with open(filename,'r+') as f:
                        f.seek(0)
                        f.write(self.info["link"][0])
                        f.close()
                    return True
                else:
                    self.logo_labels.configure(text="no new offres, program terminated")
                    self.enable()
                    return False
            page += 1

    def getMatch(self,links, keywords):
        valid = []

        with open(keywords,encoding='utf-8') as f:
            lines = f.readline()
            list = lines.split(",")
            f.close()

        self.logo_labels.configure(text="Checking offers")

        for word in range(len(links)):
            nlp = spacy.load("fr_core_news_sm")#spaCy French model 
            doc = nlp(links[word].lower()) # Process the input links using spaCy

            for keyword in list: # Check if any field keywords are present in the processed links
                if keyword in [token.text.lower() for token in doc]:
                    valid.append(word)
                    self.logo_labels.configure(text=f"{self.info['title'][word]} MATCH!")

        self.logo_labels.configure(text=f"we got {len(valid)} matches")
        return valid

    def apply(self,requests,user,motivation,offerids,userid):
        for offerid in offerids:
            url = "http://www.anapec.org/sigec-app-rv/fr/chercheurs/postulation"

            data = {
                '_method': 'POST',
                'offre_id': self.info["link"][offerid],
                'cin': user,
                'chercheur_id': userid,
                'actionname': 'postule',
                'show': '0',
                'qualifs': 'on',
                'commentaire': motivation
            }
            
            response = requests.post(url, data=data)

            if response.status_code == 200:
                self.logo_labels.configure(text='Submitted successfully')
            else:
                self.logo_labels.configure(text='Failed to submit')
        self.enable()
        self.stop.set()

    

if __name__ == "__main__":
    app = App()
    app.mainloop()
