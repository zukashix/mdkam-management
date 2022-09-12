# name: Ertugul Enterprises client money management program
# author: zukashix (https://github.com/zukashix)
# python version used: 3.8.10 x64 for Windows
# 3rd party pip modules: pwinput, prettytable

# import modules
try:
    import pickle
    import time
    import os
    import platform
    import traceback
    from prettytable import PrettyTable as ptab # v3.3.0
    from shutil import rmtree
except:
    print('FATAL: Importing of modules failed. Please contact the developer')
    exit(3)

# first run setup
try:
    APPDATA = '/storage/emulated/0'
    ADPATH = APPDATA + '/zukashix.mdkam_management'

    if not os.path.isdir(APPDATA + '/zukashix.mdkam_management'):
        os.mkdir(APPDATA + '/zukashix.mdkam_management')

        print('There is no user listed in the database. Please create a user!')
        newUserUSR = str(input('Enter a username for the new user: '))
        newUserPWD = str(input('Enter a password for the new user: '))

        userDataDictNew = {
            newUserUSR: newUserPWD
        }

        userClientDictNew = {newUserUSR: []}

        pickle.dump(userDataDictNew, open(f'{ADPATH}/D1', 'wb'))
        pickle.dump(userClientDictNew, open(f'{ADPATH}/D2', 'wb'))

        print('First-Time Processing Successful!! Proceed to Login...')
        time.sleep(3)
        os.system('clear')

    # load from dataz
    try:
        userDataDict = pickle.load(open(f'{ADPATH}/D1', 'rb'))
        userClientDataDict = pickle.load(open(f'{ADPATH}/D2', 'rb'))
    except:
        print('Data files are unreadable!! Performing database reset. Please rerun program...')

        try:
            print('Making an attempt to backup current data files...')

            try:
                os.mkdir(APPDATA + '/zukashix.mdkam_management.crash_backup')
            except FileExistsError:
                pass

            try:
                os.rename(f'{ADPATH}/D1', f'{APPDATA}/zukashix.mdkam_management.crash_backup/D1_CRASH_BACKUP')
                print('>>> D1 Backup Success!')
            except:
                print('>>> D1 Backup Failed...')

            try:
                os.rename(f'{ADPATH}/D2', f'{APPDATA}/zukashix.mdkam_management.crash_backup/D2_CRASH_BACKUP')
                print('>>> D2 Backup Success!')
            except:
                print('>>> D2 Backup Failed...')

            print('Backup sucessfull! Please contact developer to help with restoring backup')

        except:
            print('Backup failed. Please contact the developer. The program will reset.')

        rmtree(ADPATH)
        time.sleep(3)
        exit(4)

    # func to create new client entry
    def createNewClientEntry(usr, usrDD):
        print('Please enter the required data to create a new client entry:\n')
        tempDict = {}
        tempDict['Name'] = str(input('Please enter client name: '))
        tempDict['Work'] = str(input('Please enter work type: '))
        tempDict['Money'] = {}
        tempDict['Money']['MoneyStats'] = []
        tempDict['Money']['TotalWorkValue'] = float(input('Please enter total work value in integers: '))
        tempDict['Money']['PaidWorkValue'] = float(input('Please enter paid work value if any or enter 0 (zero): '))

        if tempDict['Money']['PaidWorkValue'] == 0:
            tempDict['Money']['RemainingWorkValue'] = tempDict['Money']['TotalWorkValue']
        else:
            tempDict['Money']['RemainingWorkValue'] = tempDict['Money']['TotalWorkValue'] - tempDict['Money']['PaidWorkValue']

        if tempDict['Money']['PaidWorkValue'] > 0:
            print('Please provide details for the amount of money that has already been paid\n')
            irange = int(input('How many statement entries do you want to create? (In Integers): '))

            for i in range(irange):
                print(f'\nEntry #{i+1}\n')

                mEntryDate = str(input('Enter date in format DD/MM/YYYY: '))
                mEntryMode = str(input('Enter mode of payment: '))
                mEntryWhere = str(input('Where was the amount paid at? (Enter N/A if not available): '))
                mEntryAmount = float(input('Enter amount recieved in integers: '))
                tempDict['Money']['MoneyStats'].append([mEntryDate, mEntryMode, mEntryWhere, mEntryAmount])

        matchMoney = 0
        try:
            for entry in tempDict['Money']['MoneyStats']:
                matchMoney = matchMoney + entry[3]
        except:
            pass

        if matchMoney != tempDict['Money']['PaidWorkValue']:
            print('Paid work value entered was not equal to the money recieved according to statement entries.\nCancelling Entry...')
            time.sleep(3)
            return

        print('Entry Processed!!')
        time.sleep(3)
        os.system('clear')

        usrDD[usr].append(tempDict)
        return usrDD 

    # Temporary data dict
    '''
    userClientDataDict = {
        'mdkamrul': [
            {
                'Name': 'ATS Village',
                'Work': 'Civil',
                'Money': {
                    'TotalWorkValue': 1500000,
                    'PaidWorkValue': 200000,
                    'RemainingWorkValue': 1300000,
                    'MoneyStats': [['30/07/2022', 'Cash', 'N/A', 50000], ['24/07/2022', 'Online', 'UPI_CentralBank', 150000]]
                }
            }
        ]
    }
    '''

    # Login System
    print('Welcome to Ertugul Enterprises Client Money Management System\n----------------------------------')

    userInputUsername = str(input('Please Enter Your Username: '))

    try:
        currentUserPassword = userDataDict[userInputUsername]
    except Exception as e:
        print('This user was not found! Quitting Program...')
        time.sleep(3)
        exit(1)

    userPassword = str(input('Please Enter Your Password: '))

    if userPassword != currentUserPassword:
        print('Incorrect Password! Quitting...')
        time.sleep(3)
        exit(2)

    os.system('clear')

    # Client Viewer
    def viewClient(curUsClid, i):
        cud = curUsClid[i]
        mud = cud['Money']
        mod = mud['MoneyStats']

        if mod == []:
            datab = 'No payment statements were found in database...'
        else:
            datab = ptab(['Date', 'Mode Of Payment', 'Where Paid', 'Amount'])
            for l in range(len(mod)):
                datab.add_row([mod[l][0], mod[l][1], mod[l][2], mod[l][3]])

        print(f'Here are the details for {cud["Name"]}:\n')
        print(f'Name: {cud["Name"]}\nWork Type: {cud["Work"]}\nTotal Work Value: {mud["TotalWorkValue"]}\nPaid Amount Total: {mud["PaidWorkValue"]}\nRemaining Amount Total: {mud["RemainingWorkValue"]}\n')

        print('Payment Statements:')

        print(datab)
        str(input('\nPress any key to go back...'))
        os.system('clear')
        return

    # Client Money Operations
    def CMoneyOP(currusr, usrDD, usr):
        print('Please provide details for the amount of money that has already been paid\n')
        irange = int(input('How many statement entries do you want to create? (In Integers): '))
        MoneyStats = []
        MoneyPlus = 0

        for i in range(irange):
            print(f'\nEntry #{i+1}\n')

            mEntryDate = str(input('Enter date in format DD/MM/YYYY: '))
            mEntryMode = str(input('Enter mode of payment: '))
            mEntryWhere = str(input('Where was the amount paid at? (Enter N/A if not available): '))
            mEntryAmount = float(input('Enter amount recieved in integers: '))
            MoneyStats.append([mEntryDate, mEntryMode, mEntryWhere, mEntryAmount])

        for data in MoneyStats:
            MoneyPlus += data[3]

        print('Please choose the client you want to add the entries to!\n')
        for i in range(len(currentUserClientDict)):
            print(f'[ {i} ] [ {currentUserClientDict[i]["Name"]} ] [ Work: {currentUserClientDict[i]["Work"]} ]')

        userViewChoice = int(input('Enter S. No. Of The Client: '))

        cud = currusr[userViewChoice]

        cud['Money']['PaidWorkValue'] += MoneyPlus

        if cud['Money']['PaidWorkValue'] > cud['Money']['TotalWorkValue']:
            print('ERROR: Paid work value is larger than total work value')
            time.sleep(3)
            return  

        cud['Money']['RemainingWorkValue'] -= cud['Money']['PaidWorkValue']

        for data in MoneyStats:
            cud['Money']['MoneyStats'].append([data[0], data[1], data[2], data[3]])

        usrDD[usr][userViewChoice] = cud

        print('Entry Processed!')
        time.sleep(3)
        return usrDD

    def clientEditSimpleData(currusr, usrDD, usr):
        print('Please choose the client you want to edit!\n')
        for i in range(len(currentUserClientDict)):
            print(f'[ {i} ] [ {currentUserClientDict[i]["Name"]} ] [ Work: {currentUserClientDict[i]["Work"]} ]')

        userViewChoice = int(input('Enter S. No. Of The Client: '))

        cud = currusr[userViewChoice]

        nameC = str(input(f'Do you want to change client name? [Current: {cud["Name"]}] [Leave blank for no change]: '))
        
        if nameC != '':
            cud["Name"] = nameC

        workC = str(input(f'Do you want to change work details? [Current: {cud["Work"]}] [Leave blank for no change]: '))

        if workC != '':
            cud["Work"] = workC

        # Process Money Edits

        moneyEditPrompt = str(input('Do you want to make changes in money related values? [yes/y//no/n]: '))

        if moneyEditPrompt.lower() == 'y' or moneyEditPrompt.lower() == 'yes':
            try:
                totalValC = float(input(f'Do you want to change total work value? [Current: {cud["Money"]["TotalWorkValue"]} [Leave blank for no change]: '))

                cud['Money']['TotalWorkValue'] = totalValC

            except ValueError:
                pass

            if len(cud['Money']['MoneyStats']) == 0:
                pass
            else:
                while True:
                    moneyEditPrompt = str(input('Do you want to make changes in payment statemets? [yes/y//no/n] [Type "b" to complete editing]: '))

                    if moneyEditPrompt.lower() == 'b':
                        break

                    if moneyEditPrompt.lower() == 'y' or moneyEditPrompt.lower() == 'yes':
                        moneyStatementData = cud['Money']['MoneyStats']

                        for i in range(len(moneyStatementData)):
                            print(f'[ {i} ] [ {moneyStatementData[i][0]} ] [ {moneyStatementData[i][1]} ] [ {moneyStatementData[i][2]} ] [ {moneyStatementData[i][3]} ] ')

                        userStatementChoice = int(input('\nEnter S. No. of the statement you want to edit: '))

                        currentStatement = moneyStatementData[userStatementChoice]

                        cDate = str(input(f'\nDo you want to change the date? [Current: {currentStatement[0]}] [Format: DD/MM/YYYY] [Leave blank for no change]: '))

                        if cDate != '':
                            cud['Money']['MoneyStats'][userStatementChoice][0] = cDate

                        cMode = str(input(f'Do you want to change the mode of payment? [Current: {currentStatement[1]}] [Leave blank for no change]: '))

                        if cMode != '':
                            cud['Money']['MoneyStats'][userStatementChoice][1] = cMode

                        cWherePaid = str(input(f'Do you want to change the "Where Paid" details? [Current: {currentStatement[2]}] [Leave blank for no change]: '))

                        if cWherePaid != '':
                            cud['Money']['MoneyStats'][userStatementChoice][2] = cWherePaid

                        # Logical Changes

                        cAmount = float(input(f'Do you want to change the amount? [Current: {currentStatement[3]}] [Leave blank for no change]: '))

                        try:
                            tempAmount = cud['Money']['MoneyStats'][userStatementChoice][3]

                            if tempAmount == cAmount:
                                print('WARNING: Current and new amounts are same. Returning...')
                                time.sleep(3)
                                return

                            cud['Money']['MoneyStats'][userStatementChoice][3] = cAmount

                            cud['Money']['PaidWorkValue'] = (cud['Money']['PaidWorkValue'] - tempAmount) + cAmount

                            if cud['Money']['PaidWorkValue'] > cud['Money']['TotalWorkValue']:
                                print('\nWARNING: Paid work value is larger than total work value.')
                                time.sleep(3)
                                return

                            cud['Money']['RemainingWorkValue'] = ((cud['Money']['RemainingWorkValue']) - tempAmount) + cAmount

                        except ValueError:
                            pass

                        print('Entries Processed!')
                        time.sleep(3)

                    else:
                        break

        else:
            pass

        usrDD[usr][userViewChoice] = cud

        print('Entry Processed!')
        time.sleep(3)
        return usrDD

    # Options / List Page
    while True:
        print('Welcome to Management!!')

        currentUserClientDict = userClientDataDict[userInputUsername]

        print('Here are your clients!\n-----------------------')

        for i in range(len(currentUserClientDict)):
            print(f'[ {i} ] [ {currentUserClientDict[i]["Name"]} ] [ Work: {currentUserClientDict[i]["Work"]} ]')

        print('\nOptions:\n[ A ] Create a new client entry\n[ B ] Add money entries to an existing client\n[ C ] Edit values for clients\n[ D ] Exit Program\n[ E ] Developer Data')

        userViewChoice = str(input('Enter S. No. Of A Client You Want To View Or Choose An Option By Alphabet: '))

        try:
            viewClient(currentUserClientDict, int(userViewChoice))

        except:
            if userViewChoice.lower() == 'a':
                userClientDataDict = createNewClientEntry(userInputUsername, userClientDataDict)
                if userClientDataDict == None:
                    pass 
                else: 
                    pickle.dump(userClientDataDict, open(f'{ADPATH}/D2', 'wb'))

            if userViewChoice.lower() == 'b':
                if len(currentUserClientDict) == 0:
                    print('WARNING: You cannot perform this action as there are no client entries! You must create a client entry first!')
                    time.sleep(3)
                    continue

                userClientDataDict = CMoneyOP(currentUserClientDict, userClientDataDict, userInputUsername)
                if userClientDataDict == None:
                    pass 
                else: 
                    pickle.dump(userClientDataDict, open(f'{ADPATH}/D2', 'wb'))

            if userViewChoice.lower() == 'c':
                if len(currentUserClientDict) == 0:
                    print('WARNING: You cannot perform this action as there are no client entries! You must create a client entry first!')
                    time.sleep(3)
                    continue

                userClientDataDict = clientEditSimpleData(currentUserClientDict, userClientDataDict, userInputUsername)
                if userClientDataDict == None:
                    pass 
                else: 
                    pickle.dump(userClientDataDict, open(f'{ADPATH}/D2', 'wb'))

            if userViewChoice.lower() == 'd':
                print('Qutting...')
                time.sleep(3)
                os.system('clear')
                exit(0)

            if userViewChoice.lower() == 'e':
                pythonV = platform.python_version()
                osV = platform.platform()
                userhost = os.getlogin() + '@' + platform.node()
                BKPATH = APPDATA + '/zukashix.mdkam_management.crash_backup'
                appV = '1.0'
                appShipping = 'Android_Termux/Pydroid/Emu_Shipping'

                print('Developer Related Data: ')
                dro = f'Python Version: {pythonV}\nOS Data: {osV}\nUser/Sys Data: {userhost}\nScript Version: {appV}\nScript Platform Target: {appShipping}\nStorage Path: {ADPATH}\nBackup Path: {BKPATH}\nDeveloper: https://github.com/zukashix'
                print(f'\n{dro}')

                dumpChoice = str(input('\nDo you want to save this data in a file? [y/yes//n/no]: '))

                if dumpChoice.lower() in ['y', 'yes']:
                    try:
                        dumpFile = open(f'{ADPATH}/sysDump.txt', 'w')
                        dumpFile.write(dro)
                        dumpFile.close()
                        print('File dumped!')
                    except:
                        print('File dump failed. Returning...')

                time.sleep(3)

except KeyboardInterrupt:
    print('WARNING: Keyboard interrupt detected. Quitting...')
    time.sleep(3)
    exit(5)

except Exception as error:
    try:
        tbc = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__)
        finaltbc = ''
        for line in tbc:
            finaltbc += line

        f = open(ADPATH + '/crashlog.txt', 'w')
        f.write(finaltbc)
        f.close()

        print(f'FATAL: An unexpected internal error has occurred.\nPlease contact the developer with the log file stored at {ADPATH}/crashlog.txt')
        time.sleep(3)

    except:
        print('FATAL: An unexpected internal error has occurred. Crash Log could not be generated. Please contact the developer')
        time.sleep(3)
        exit(2)
