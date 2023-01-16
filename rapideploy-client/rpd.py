import sys
import requests

argsList = sys.argv
import os , shutil

def createRepoMap():
    repomap_dir = "./"
    repomap_path = os.path.join(repomap_dir, "repomap")
    if(os.path.exists(repomap_path)):
        print("Note: consider running ( python3 rpd.py update ) before deploying anything")
    else:
        os.mkdir(repomap_path)


createRepoMap()

def deleteRepoMap():
    folder = 'repomap'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def deletePrevDownload(path_to_folder):
    folder = path_to_folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))    

if(argsList.__len__() < 2):
    print("looks like you are lost.")
    print("use ( python3 rpd.py help ) for help")
    exit()


def UpdateRepoMap():
    deleteRepoMap()
    try:

        categoriesRaw = requests.get('https://raw.githubusercontent.com/windwalkerstudio/rapideploy-api/main/category.rpdapi')
        categoriesFile = open('repomap/categories.rpdapi', 'w')
        categoriesFile.write(categoriesRaw.text)
        categoriesFile.close()

        print("GET: categories")

        categoriesFile = open('repomap/categories.rpdapi', 'r')
        categoriesList = categoriesFile.readlines()
        categoriesFile.close()

        for category in categoriesList:

            categoryName = category.strip()

            category_dir = "repomap/"
            category_path = os.path.join(category_dir, categoryName)
            os.mkdir(category_path)

            versionsRaw = requests.get('https://raw.githubusercontent.com/windwalkerstudio/rapideploy-api/main/' + categoryName + "/versions.rpdapi")
            versionsFile = open('repomap/'+categoryName+"/versions.rpdapi", 'w')
            versionsFile.write(versionsRaw.text)
            versionsFile.close()

            print("GET: " + categoryName)

            versionsFile = open('repomap/'+categoryName+"/versions.rpdapi", 'r')
            versionsList = versionsFile.readlines()
            versionsFile.close()

            for version in versionsList:

                versionName = version.strip()

                version_dir = "repomap/" + categoryName + "/"
                version_path = os.path.join(version_dir, versionName)
                os.mkdir(version_path)
                
                packageRaw = requests.get('https://raw.githubusercontent.com/windwalkerstudio/rapideploy-api/main/' + categoryName + "/" + versionName +"/package.rpdapi") 
                packageFile = open('repomap/'+categoryName+"/"+versionName+"/package.rpdapi", 'w')
                packageFile.write(packageRaw.text)
                packageFile.close()

                print("GET: " + categoryName + " - " + versionName)
    except:
        deleteRepoMap()
        print("Please check your network connection and try again.")    


def deployPackage(category, version):

    category_dir = "repomap/"
    category_path = os.path.join(category_dir, category)

    if(os.path.exists(category_path)):

        version_dir = "repomap/" + category + "/"
        version_path = os.path.join(version_dir, version)

        if(os.path.exists(version_path)):

            packageFile = open('repomap/'+ category +"/"+version+"/package.rpdapi", 'r')
            packageFileLineList = packageFile.readlines()
            packageFile.close()

            if(packageFileLineList[0].strip() == "all"):

                deploy_dir = "./"
                deploy_path = os.path.join(deploy_dir, category + "-" + version)

                if(os.path.exists(deploy_path)):
                    deletePrevDownload(category + "-" + version)
                else:
                    os.mkdir(deploy_path)
                
                downloadFileName = packageFileLineList[1].strip()

                downloadRaw = requests.get('https://raw.githubusercontent.com/windwalkerstudio/rapideploy-api/main/' + category + "/" + version +"/" + downloadFileName) 
                downloadFile = open(category + "-" + version + "/" + downloadFileName , 'w')
                downloadFile.write(downloadRaw.text)
                downloadFile.close()

                print("You have successfully deployed: " + category + " - " + version)

            else:
                print("you cannot install that package")    


        else:
            print("Error: " + category + " does not have version: " + version)    

    else:
        print("Error: No category named: " + category)


if ( argsList[1] == "update"):
    UpdateRepoMap()
elif ( argsList[1] == "deploy"):

        category = argsList[2]
        version = argsList[3]
        deployPackage(category, version)
   
