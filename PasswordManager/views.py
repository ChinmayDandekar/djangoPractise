# from djangoPractise.settings import MEDIA_ROOT
from cryptography.fernet import Fernet,InvalidToken
from django.shortcuts import render,redirect
# from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Passwords,Documents
from Crypto.Cipher import AES
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
import base64
import os
import re
import shutil
import random ,array
# a = Album.objects.get(pk = 3)
# >>> a.genre = "Pop"
# >>> a.save()

isEncrypted = None

# def downloadFile(request):
#     path = request.POST['']
#     pass

# def isLogOut(request):
#     if not request.user.is_authenticated:
#         return redirect('/')
    

def checkEncryption(request):
    global isEncrypted
    docs = Documents.objects.filter(user=str(request.user.username))
    try:
        for i in docs:
            decFile(os.path.join(f"C:\\Users\\chinm\\OneDrive\\Desktop\\Python\\django practise\\djangoPractise\\media\\uploads\\{str(request.user.username)}\\{i.filename}"))
    except InvalidToken:
        pass
    finally:
        for i in docs:
            encFile(os.path.join(f"C:\\Users\\chinm\\OneDrive\\Desktop\\Python\\django practise\\djangoPractise\\media\\uploads\\{str(request.user.username)}\\{i.filename}"))
            isEncrypted =True

        
def encFile(filepath):
    fernet = Fernet(b'm-RfRzx3i-0qMm1EzuNOoh10U7RXpun5VdXTIng8LP8=')
    with open(filepath, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(filepath, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    # print(encrypted)


def decFile(filepath):
    fernet = Fernet(b'm-RfRzx3i-0qMm1EzuNOoh10U7RXpun5VdXTIng8LP8=')
    with open(filepath, 'rb') as file:
        encrypted = file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(filepath, 'wb') as dec_file:
        dec_file.write(decrypted)
    # print(decrypted)

def encryptit(plainText):
    bytecode = plainText.rjust(32).encode()
    secret_key = '123'.rjust(16).encode()
    cipher = AES.new(secret_key, AES.MODE_ECB)
    encryptedText = base64.b64encode(cipher.encrypt(bytecode)).decode()
    return encryptedText

def decryptit(encryptedText):
    secret_key = '123'.rjust(16).encode()
    cipher = AES.new(secret_key, AES.MODE_ECB)
    plainText = cipher.decrypt(base64.b64decode(encryptedText)).decode()
    return plainText

def checkEmail(email):
    
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    return re.search(regex, email)
     

# def checkUrl(url):
#     regex = "((http|https)://)(www.)?" + "[a-zA-Z0-9@:%.\+~#?&//=]{2,256}\.[a-z]" + "{2,6}\b([-a-zA-Z0-9@:%.\+~#?&//=]*)"
#     return re.search(regex,url)


def isNull(n):
    if n == '':
        return True
    else:
        return False



def index(request):
    global isEncrypted
    checkEncryption(request)
    # try:
    # docs = Documents.objects.filter(user = str(request.user.username))
    # if not isEncrypted:
    #     for i in docs:
    #         encFile(os.path.join("C:\\Users\\chinm\\OneDrive\\Desktop\\Python\\django practise\\djangoPractise\\media\\uploads\\",i.filename))
            
    # finally:
    #     isEncrypted = True      
    print('index',isEncrypted)
    return render(request, 'index.html' )

def viewallsites(request):
    if not request.user.is_authenticated:
        messages.info(request,'You need to Log In first!!!')
        return redirect('accounts/login')
    global isEncrypted
    # if request.method=='POST':
    #     ppath = request.FILES['Path']
    #     print(ppath)
    #     # downloadFile(path)
    checkEncryption(request)

    # pas = Passwords.objects.all()
    passs = Passwords.objects.filter(user = str(request.user.username))
    docs = Documents.objects.filter(user = str(request.user.username))

    # if len(passs) == 0:
    #     messages.info(request, 'You dont have any Passwords saved currently!!')
    
    # if len(docs) == 0:
    #     messages.info(request, 'You dont have any Docuements saved currently!!')


    print('vault',isEncrypted)
    if isEncrypted == True :
        for i in docs:
            # print(i.filename)
            path = os.path.join(f"C:\\Users\\chinm\\OneDrive\\Desktop\\Python\\django practise\\djangoPractise\\media\\uploads\\{str(request.user.username)}\\{i.filename}")
            # print(path)
            decFile(path)
        isEncrypted = False 
    # print('vault',isEncrypted)

    for i in passs:
        i.password = decryptit(i.password)
    # passs.append(siteurl)

    print(passs)
    return render(request, 'viewallsites.html' ,{'passs' : passs,'docs':docs})



def addDocument(request):

    # isLogOut(request)
    if not request.user.is_authenticated:
        messages.info(request,'You need to Log In first!!!')
        return redirect('accounts/login')

    global isEncrypted
    checkEncryption(request)
    if request.method == 'GET':
        return render(request, 'addDocument.html')
    
    if  len(request.FILES) == 0:
        messages.info(request,'No file Selected')
        return render(request,'addDocument.html')
    
    userpath = fr"C:\Users\chinm\OneDrive\Desktop\Python\django practise\djangoPractise\media\uploads\{str(request.user.username)}"

    if not os.path.exists(userpath):
        os.makedirs(userpath)

    

    doc = request.FILES['document']
    # doc = request.FILES
    # # print(doc)
    # file = request.POST['document']
    
    if Documents.objects.filter(file = f"uploads\{str(request.user.username)}\{doc.name}").exists():
        messages.info(request,'The given document already exists.')
        return render(request, 'addDocument.html')

    document = Documents.objects.create(
        user = str(request.user.username),
        filename = doc.name,
        file = doc,  
    )
    document.save()

    ogpath = fr'C:\Users\chinm\OneDrive\Desktop\Python\django practise\djangoPractise\media\uploads\{doc.name}'
    movpath = fr'C:\Users\chinm\OneDrive\Desktop\Python\django practise\djangoPractise\media\uploads\{str(request.user.username)}\{doc.name}'
    shutil.move(ogpath,movpath)

    d = Documents.objects.filter(user = str(request.user.username)).get(filename = doc.name )
    print('helo')
    print(d.file)
    d.file =fr"uploads\{str(request.user.username)}\{doc.name}"
    d.save()


    # fs = FileSystemStorage(location= os.path.join(MEDIA_ROOT,'/uploads'))
    # filename = fs.save(doc.name, doc)
    messages.info(request,'Document Stored')
    # docs = Documents.objects.all()
    # for docu in docs:
    #     if docu.name == doc.name:
    #         path = docu.file.path()
            
    # else:
        # print('File not found')

    path = os.path.join(f"C:\\Users\\chinm\\OneDrive\\Desktop\\Python\\django practise\\djangoPractise\\media\\uploads\\{str(request.user.username)}\\{doc.name}")
    print(path)
    encFile(path)
    isEncrypted = True
  
    return render( request, 'addDocument.html')

def deleteDoc(request):
    docname=request.GET.get('doc_name')
    print(docname)
    d = Documents.objects.filter(user = str(request.user.username)).get(filename = docname )
    filepath = d.file.url
    os.remove(fr"C:\Users\chinm\OneDrive\Desktop\Python\django practise\djangoPractise{filepath}")
    print(filepath)
    d.delete()
    return redirect('viewallsites')

def deletePass(request):
    siteName = request.GET.get('siteName')
    password = request.GET.get('sitePassword')
    password = encryptit(password)
 
    p = Passwords.objects.filter(site_name = siteName , password = password)
    p.delete()
    return redirect('viewallsites')

    

    
        

def addsite(request):
    if not request.user.is_authenticated:
        messages.info(request,'You need to Log In first!!!')
        return redirect('accounts/login')
    global isEncrypted
    checkEncryption(request)
    if request.method == 'POST':
        site_name = request.POST['site-name']
        site_url = request.POST['site-url']
        username = request.POST['username']
        password = request.POST['password']

        

        if  'https://' in site_url:
            site_url = site_url[8:]
        elif 'http://' in site_url:
            site_url = site_url[7:]       
    
        password = encryptit(password)
        
        # print(request.user.username)
        if isNull(site_name) or isNull(site_url) or isNull(username) or isNull(password):
            messages.info(request, 'No information should be empty')
            return redirect('addsite')

        # if not checkUrl(site_url):
        #     messages.info(request, 'Please enter correct url!!')
        #     return redirect('addsite')


        if username.isnumeric():
            phoneNo = username
            username = '-'
            email = '-'
        elif checkEmail(username):
            email = username
            phoneNo = '-'
            username = '-'
        else:
            phoneNo = '-'
            email = '-'

        password = Passwords.objects.create(
        
        user = str(request.user.username),username=username, password=password, email=email, site_name=site_name, site_url=site_url , phoneNo = phoneNo)
        password.save()
        messages.info(request,'Password Stored')
        return redirect('addsite')

    

    else:
        

       return render(request, 'add_site.html')

def GenPass(request):
    if not request.user.is_authenticated:
        messages.info(request,'You need to Log In first!!!')
        return redirect('accounts/login')
    global isEncrypted
    checkEncryption(request)

    if request.method == 'GET':
        return render(request,'GenPass.html' ,{'max':15,'sample':'mpEjFdnhTQQfdut'})

    

    MAX_LEN = 15
    # if request.POST['range-text']:
    #     MAX_LEN = int(request.POST['range-text'])
    # else:
    MAX_LEN = int(request.POST['slider'])
        
    print(MAX_LEN)

    # onPressUpper = request.POST['UpperCase']
    # onPressLower = request.POST['LowerCase']
    # onPressSymbols = request.POST['Symbols']
    # onPressDigits = request.POST['Digits']

    onPressUpper = request.POST.get('UpperCase', '') == 'on'
    print(onPressUpper)
    onPressLower = request.POST.get('LowerCase', '') == 'on'
    print(onPressLower)

    onPressSymbols = request.POST.get('Symbols', '') == 'on'
    print(onPressSymbols)

    onPressDigits = request.POST.get('Digits', '') == 'on'
    print(onPressDigits)

    # # if request.POST['UpperCase']:
    #     onPressUpper = request.POST['UpperCase']
    # # else:
    #     onPressUpper = 'False'
    # print(onPressUpper)
    
    # if request.POST['LowerCase']:
    #     onPressLower = request.POST['LowerCase']
    # else:
    #     onPressLower = 'False'
    # print(onPressLower)

    # if request.POST['Symbols']:
    #     onPressSymbols = request.POST['Symbols']
    # else:
    #     onPressSymbols = 'False'
    # print(onPressSymbols)

    # if request.POST['Digits']:
    #     onPressDigits = request.POST['Digits']
    # else:
    #     onPressDigits = 'False'
    # print(onPressDigits)

    

    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']
    
    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']
    
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '/', '|', '~', '>',
            '*', '<']
    
    COMBINED_LIST = []
    temp_pass =""
    optChoosen =0

    if onPressUpper:
        COMBINED_LIST += UPCASE_CHARACTERS
        temp_pass += random.choice(UPCASE_CHARACTERS)
        optChoosen+=1
    if onPressLower:
        COMBINED_LIST += LOCASE_CHARACTERS
        temp_pass += random.choice(LOCASE_CHARACTERS)
        optChoosen+=1

    if onPressSymbols:
        COMBINED_LIST += SYMBOLS
        temp_pass += random.choice(SYMBOLS)
        optChoosen+=1


    if onPressDigits:
        COMBINED_LIST += DIGITS
        temp_pass += random.choice(DIGITS)      
        optChoosen+=1

    if(optChoosen ==0):
        messages.info(request, "Atleast one option should be selected")
        return redirect('GenPass')
    
    
    print(optChoosen)
    for x in range(MAX_LEN-optChoosen):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)  
        
    
    temp_pass_list = array.array('u', temp_pass)
    random.shuffle(temp_pass_list)
    

    password = ""
    for x in temp_pass_list:
            password = password + x
            

    print(password)
    val = MAX_LEN

    return render(request, 'GenPass.html' ,{'pass':password,'upper':onPressUpper,'lower':onPressLower,'sym':onPressSymbols,'digit':onPressDigits, 'max':val,'sample':''})