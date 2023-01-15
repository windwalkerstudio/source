from tkinter import *

import os , shutil
import time
import colorsys
import requests
import matplotlib
def deleteTemp():
    folder = 'temp'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

deleteTemp()
root =Tk()
root.title('Rapid Deployer')
root.iconbitmap('icon.ico')
root.geometry('500x550')

toSetRgb = []

mainFrame = Frame(root, bg = "black")
mainFrame.pack(expand=True,side="left",fill="both")
toSetRgb.append(mainFrame)

downloadFrame = LabelFrame(mainFrame, text="Actions", bg = "black", fg = "white")
downloadFrame.pack(side="left",fill="both")
toSetRgb.append(downloadFrame)

tabsFrame = LabelFrame(mainFrame, text="Toolbar", bg = "black", fg = "white")
tabsFrame.pack(side="top",fill="x")
toSetRgb.append(tabsFrame)

def exitApp():
    exit()

exitButton = Button(tabsFrame, text="Exit" , bg="#ff0000" , fg="#000000" ,command=exitApp)
exitButton.pack(side="right")

activeTab = LabelFrame(mainFrame,text="workspace" , fg = "white", padx=5,pady=5)
activeTab.pack(expand=True,side="left",fill="both")
toSetRgb.append(activeTab)

activeTabName = "workspace"

def renameActiveTab(tabName):
    global activeTabName
    activeTabName = (tabName)
    activeTab.config(text=tabName)   

onActiveTabCloseToDelete = []

def closeActiveTab():
    global activeTabName
    for module in onActiveTabCloseToDelete:
        module.destroy() 
    activeTabName = "workspace"    
     

def downloadVersions(category):
    temp_dir = "temp/"
    category_path = os.path.join(temp_dir, category)
    os.mkdir(category_path)
    versions = requests.get('https://raw.githubusercontent.com/windwalkerstudio/rapideploy-api/main/' + category + '/versions.rpdapi')
    versionsFile = open('temp/'+ category +'/versions.rpdapi', 'w')
    versionsFile.write(versions.text)
    versionsFile.close()
    versionsFile = open('temp/'+ category +'/versions.rpdapi', 'r')
    versionsList = versionsFile.readlines()
    versionsFile.close()

    return versionsList

def downloadDownloadableFiles(category,version):
    category_dir = "temp/"+ category +"/"
    version_path = os.path.join(category_dir, version)
    os.mkdir(version_path)
    downloadables = requests.get('https://raw.githubusercontent.com/windwalkerstudio/rapideploy-api/main/' + category + '/' + version + "/toDownload.rpdapi")
    downloadablesFile = open('temp/'+ category +'/'+ version + '/toDownload.rpdapi', 'w')
    downloadablesFile.write(downloadables.text)
    downloadablesFile.close()
    downloadablesFile = open('temp/'+ category +'/'+ version + '/toDownload.rpdapi', 'r')
    downloadablesList = downloadablesFile.readlines()
    downloadablesFile.close()

    return downloadablesList


def downloadFile(category,version,downloadable):
    download_dir = "downloads/"
    download_path = os.path.join(download_dir, category + "-" + version)
    os.mkdir(download_path)
    downloadable = requests.get('https://raw.githubusercontent.com/windwalkerstudio/rapideploy-api/main/' + category + '/' + version + "/" + downloadable)
    downloadableFile = open('downloads/'+ category + "-" + version + '/' + downloadable, 'w')
    downloadableFile.write(downloadable.content)
    downloadableFile.close()


def openCategoriesTab(categoriesList):
    if (activeTabName == "Download center"):
        closeActiveTab()
        openCategoriesTab(categoriesList)
    else:
        count = 0
        renameActiveTab("Download center")
        for category in categoriesList:
            categoryFrame = LabelFrame(activeTab, text=category.strip(), bg = "black", fg = "white", padx=5,pady=5)
            categoryFrame.pack(expand=True,side="left",fill="both")
            versions = downloadVersions(category.strip())
            for version in versions:
                versionFrame = LabelFrame(categoryFrame, text=version.strip(), bg = "black", fg = "white")
                versionFrame.pack(expand=True,side="left",fill="both")
                onActiveTabCloseToDelete.append(versionFrame)
                downloadables = downloadDownloadableFiles(category.strip(), version.strip())
                for downloadable in downloadables:
                    downloadButton = Button(versionFrame, text=downloadable.strip(), bg="#ff0000" , fg="#000000" , justify="left" ,command=downloadFile(category.strip(),version.strip(),downloadable.strip()))
                    downloadButton.pack()    

            onActiveTabCloseToDelete.append(categoryFrame)
            count = count + 1

def showErrorPage(errorID):
    if(errorID == "ce"):
        renameActiveTab("connection error")
        retryButton = Button(activeTab, text="retry", bg="#ff0000" , fg="#000000" , justify="left" ,command=DownloadCategories)
        retryButton.pack()
        onActiveTabCloseToDelete.append(retryButton)

def DownloadCategories():

    closeActiveTab()

    deleteTemp()

    renameActiveTab("Downloading content. Please wait . . .") 

    categories = requests.get('https://raw.githubusercontent.com/windwalkerstudio/rapideploy-api/main/categories.rpdapi')
    categoriesFile = open('temp/categories.rpdapi', 'w')
    categoriesFile.write(categories.text)
    categoriesFile.close()
    categoriesFile = open('temp/categories.rpdapi', 'r')
    categoryList = categoriesFile.readlines()
    categoriesFile.close()
    openCategoriesTab(categoryList)

         
UpdateButton = Button(downloadFrame, text="Update categories from server" ,command=DownloadCategories)
UpdateButton.pack(side="top" , padx=5)

def setToRgb():
    hue = (round(time.time()*1000) % 10000 ) / 10000
    (h, s, v) = (hue, 0.8, 0.2)
    (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
    thecolor = matplotlib.colors.to_hex([ r, g, b ])

    for module in toSetRgb:
        module.config(bg=thecolor)
    root.after(1, lambda: setToRgb())
    
setToRgb()

root.mainloop()
