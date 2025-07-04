**Requirements** :-
        ***Hardware Requirements:-***
                **Camera:**
                        *A working camera is essential for the QR code scanner application to capture and decode QR codes. Ensure the camera is functional and provides a clear image.*
                **Processor:**
                        *A modern multi-core processor is recommended for smooth operation.*
                **Memory (RAM):**
                        *At least 4 GB of RAM is recommended. More RAM can improve performance, especially if you are running other applications simultaneously.*
                **Storage:**
                        *Ensure there is sufficient storage space for the application and its dependencies. At least 1 GB of free space is recommended.*
        ***Software Requirements:-***
                **Operating System:**
                        Windows 10 or later is recommended for compatibility with the PyInstaller-built executables.
                **Excel** :- 
                        ***Your Excel Sheet must contain one column with label "Name"***
                        ***Must contain one column with unique entries***, columns like :-*UPI ID* or *Roll No* or *Transation Id*, or columns which must not contain same values.
        
**Recomendations** :- *_You can use external camera such as web cams to make it more easy for you to scan during you event entry_*

**Additional Recommendations**
        ***Permissions:***
                *Ensure the application has the necessary permissions to access the camera and any other hardware resources.*
        ***Antivirus and Firewall:***
                *Some antivirus programs or firewall settings might block the application from accessing the camera or internet. Ensure these settings are configured to allow the application to run smoothly.*
        ***User Interface:***
                *Make sure the user interface of your applications is user-friendly and provides clear instructions for using the camera to scan QR codes.*


First you have to download both the files **"qr_code_generator.zip"** and the **"qr_code_scanner.zip"** file, then extract these files.

***Steps to use the system***
***First*** You have to run the **"qr_code_generator.exe"**.
Here are the Steps to use the qr_code_generator app :-

Step 1- *_Select Excel File_* Click the Browse button and select your ***Excel File*** 
Step 2- *_Select Column_* Here in the drop down menu select the desired column you want to encode in the QR Code.
        (This column must be the column which contains all unique values. ForEx:- Transaction Id, Roll No, etc.)
Step 3- *_Select Output Folder_* Click Browse button and Select the output folder where you want all the qr codes to be saved.
        (Recomended :- Select your desired directory and create the new folder named QR-Codes to be more understandable format)
Step 4- Now, Click the *_Generate QR Codes_* Button.

Now the qr codes are created and 2 columns are added in your Excel Sheet With the names *_Ticket Code_* and _*QR Location*_ , where Ticket_code is your Encoded Data and the QR Location is the Location of your QR Codes.

***Second*** Now run the **qr_code_scanner.exe**
Steps to use the qr_code_scanner app :-

Step 1- *_Select Excel File_* Click the Browse button and select your ***Excel File*** 
Step 2- *_Select Column_* Click the dropdown menu and select the Column named *_"Ticket Code"_*.
        (NOTE:- Be carefull while selecting the Column)
Step 3- Now Click the *_Start Scanning_* Button 
Step 4- Now Focus the qr codes on the camera and wait till the message displayes weather to give entry or not,
        _For Entry it will say :-_ *_Welcome Name of the attendie_* if entry is found,
        _For no Entry it will say :-_ *_Access Denied_*

Enjoy this system and make your work easier while ticketing 

***"HAPPY TICKETING"***#   E v e n t - T i c k e t i n g - S y s t e m  
 