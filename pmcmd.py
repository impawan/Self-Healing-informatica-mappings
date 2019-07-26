# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 16:38:52 2019

@author: paprasad
"""

import os 
import datetime
import subprocess

os.system('mkdir test')

time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
timestamp = str(time)
'''


C:\Informatica\9.6.1\server\bin>infacmd.bat 
getSessionLog -dn "Domain_item-s65484" -un pawan -pd pawan -fm Text -lo "d:\Profiles\paprasad\INFA\Pawan\src\logs.txt" -is INT_SRVC -rs INFA_REP -ru pawan -rp pawan -fn 
 "INFA_FOLDER" -ss "s_m_CrDbStatsment" -wf "wf_m_CrDbStatsment"
'''


def cmd_execute(command):
    """
    Execute an external command and return its output as a list where 
    each list element corresponds to one STDOUT line returned by the 
    command.

    Args:
        command (list): OS command call formatted for the subprocess'
            Popen

    Returns:
        List
    """
    import subprocess  # import only on demand, as it is slow on cygwin
    command_output = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
    return str(command_output[0]).strip("b'").split('\\r\\n')

def run_win_cmd(cmd):
    result = []
    print(cmd)
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    for line in process.stdout:
        result.append(line)
    errcode = process.returncode
    for line in result:
        print(str(line))
    if errcode is not None:
        raise Exception('cmd %s failed, see above for details', cmd)


def excute_commands(cmd):
    os.system(cmd)

def fetch_log(Domain_name="Domain_item-s65484",username = "pawan",pswd = "pawan",frmt = "TEXT",location = "./Logs/", IS = "INT_SRVC",
              IR = "INFA_REP",FOLDER = "INFA_FOLDER",session = "s_m_CrDbStatsment" ,wf = "wf_m_CrDbStatsment"):
    
    
    session_file_name  = session+timestamp+'.txt'
    location = location+session_file_name
    
    command_srt = "C:\Informatica\9.6.1\server\\bin\infacmd.bat getSessionLog -dn "+Domain_name+" -un "+username+" -pd "+pswd+" -fm "+frmt+" -lo "+location+" -is "+IS+" -rs "+IR+" -ru "+username+" -rp "+pswd+" -fn "+FOLDER+" -ss "+session+" -wf "+wf
    excute_commands(command_srt)
    
    #print(command_srt)
   
   
    return location




cmds = ['C:\Informatica\9.6.1\server\\bin\pmrep','connect -r INFA_REP -d Domain_ITEM-s65484 -n pawan -x pawan','objectexport -n m_CrDbStatsment -o Mapping -f INFA_FOLDER -m -s -b -r -u d:\Profiles\paprasad\python\Self-Healing-informatica-mappings\m_CrDbStatsment_test.xml']

cmd_execute(cmds)
run_win_cmd(cmds)


os.system("C:\Informatica\9.6.1\server\\bin\pmrep;")#& connect -r INFA_REP -d Domain_ITEM-s65484 -n pawan -x pawan & C:\Informatica\9.6.1\server\\bin\pmrep objectexport -n m_CrDbStatsment -o Mapping -f INFA_FOLDER -m -s -b -r –u d:\Profiles\paprasad\python\Self-Healing-informatica-mappings\m_CrDbStatsment_test.xml")
os.system("connect -r INFA_REP -d Domain_ITEM-s65484 -n pawan -x pawan")
os.system("C:\Informatica\9.6.1\server\\bin\pmrep objectexport -n m_CrDbStatsment -o Mapping -f INFA_FOLDER -m -s -b -r –u m_CrDbStatsment_test.xml)

