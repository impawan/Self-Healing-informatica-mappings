

cd C:\Informatica\9.6.1\server\bin
echo %C%
call pmrep connect -r INFA_REP -d Domain_ITEM-s65484 -n pawan -x pawan 
call pmrep objectexport -n m_CrDbStatsment -o Mapping -f INFA_FOLDER -m -s -b -r -u d:\Profiles\paprasad\python\Self-Healing-informatica-mappings\m_CrDbStatsment_test.xml

TIMEOUT /T 10