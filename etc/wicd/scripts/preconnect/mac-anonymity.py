#!/usr/bin/python2
import getopt, sys, os
import ConfigParser as configparser

# Fixed commit

""" MAC-Anonymity is very simple script for WICD which changes your MAC when you are connecting to selected network """

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"]) # output=
    except getopt.GetoptError, err:
        sys.exit(2)

    if len(args) != 3:
        print "Plugin accepts only three arguments from commandline (connection type, essid, bssid)"
        sys.exit(2)

    # args:
    # 0 => connection_type (wireless, ethernet)
    # 1 => essid
    # 2 => bssid

    # supports only wireless connections
    if args[0] != "wireless":
        sys.exit(2)

    fileName = "/etc/mac-anonymity.conf"
    Parser = configparser.ConfigParser()

    try:
        Parser.read(fileName)
    except ConfigParser.MissingSectionHeaderError:
        print "Error: Missing section header in "+fileName
        return


    # MAC Changer
    Items = Parser.options("change_mac")
    Interface = Parser.get("settings", "interface")
    found = False

    if Parser.get("settings", "enabled") == "False":
        print "MAC-Anonymity is currently disabled, to change it you need to edit /etc/mac-anonymity.conf"
        sys.exit(0)

    for Item in Items:
        # Will change mac if found a network
        if Item == args[1] or Item == args[2]:
            print "Network recognized: Changing MAC to "+Parser.get("change_mac", Item)+" on "+Interface+" interface"
            os.system("ifconfig wlan0 down")
            os.system("macchanger -m \""+Parser.get("change_mac", Item)+"\" "+Interface)
            os.system("ifconfig wlan0 up")

            found = True
            break

    if found == False:
        if Parser.get("settings", "default_mac_for_unknown_networks") == "random":
            print "Unknown network: Changing MAC adress to random on "+Interface+" interface"
            os.system("ifconfig wlan0 down")
            os.system("macchanger -r "+Interface)
            os.system("ifconfig wlan0 up")
        else:
            print "Unknown network: Changing MAC adress to "+Parser.get("settings", "default_mac_for_unknown_networks")+" on "+Interface+" interface"
            os.system("ifconfig wlan0 down")
            os.system("macchanger -m "+Parser.get("settings", "default_mac_for_unknown_networks")+" "+Interface)
            os.system("ifconfig wlan0 up")
    
if __name__ == "__main__":
    main()
