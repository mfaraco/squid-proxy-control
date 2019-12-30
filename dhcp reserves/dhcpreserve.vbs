Set objExcel = CreateObject("Excel.Application")
Set objWorkbook = objExcel.Workbooks.Open("z:\scripts\network\dhcpreserves.xls")
Set objStdIn = WScript.StdIn
server = objExcel.Cells(1,2).Value 
scope  = objExcel.Cells(2,2).Value 
WScript.echo "En que linea comienzan los datos?"
intRow = objStdIn.ReadLine()
Set objShell = CreateObject("Wscript.Shell")
Do Until objExcel.Cells(intRow,2).Value = ""
	WScript.Echo "*** Procesando Linea: " & intRow
	IP  = objExcel.Cells(intRow,1).Value
	MAC = objExcel.Cells(intRow,2).Value
	WScript.Echo "IP: " & IP & " MAC " & MAC
	scriptstr1 = "netsh dhcp server " & Server & " scope " & scope & " add reservedip " & IP & " " & MAC
	'WScript.Echo scriptstr1
	intRunError = objShell.Run(scriptstr1, 2, True)
	'WScript.Echo "-----------------------Reserva Creada"
	WScript.Echo "================================================================================"
	intRow = intRow + 1
Loop
objExcel.Quit
