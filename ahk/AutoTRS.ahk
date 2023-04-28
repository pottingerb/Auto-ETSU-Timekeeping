#NoEnv
#SingleInstance Force
SendMode Input
SetWorkingDir %A_ScriptDir%
SetTitleMatchMode, 2  ; Allows for partial matching of window titles
WinActivate, ahk_exe Firefox.exe

; Define the path to the CSV file
csvFilePath := "..\input\input.csv"

; Include the JSON library
#Include lib/JSON.ahk

; Function to read the config JSON file
ReadJSONConfig(configFile)
{
    FileRead, fileContent, %configFile%
    jsonObj := JSON.Load(fileContent)

    input_box_x1 := jsonObj["input_box_x1"]
    input_box_x2 := jsonObj["input_box_x2"]
    input_box_x3 := jsonObj["input_box_x3"]
    input_box_y := jsonObj["input_box_y"]
    add_button_x := jsonObj["add_button_x"]
    add_button_y := jsonObj["add_button_y"]
    submit_ok_x := jsonObj["submit_ok_x"]
    submit_ok_y := jsonObj["submit_ok_y"]
}

; Read the config file and populate the variables
ReadJSONConfig("..\config\config.json")

; Define the X and Y coordinates for the clicks
input_box_x1:= 450
input_box_x2:= 750
input_box_x3:= 990
input_box_y := 810

add_button_x := 455
add_button_y := 895

submit_ok_x := 1120
submit_ok_y := 242

newY := 0

FileRead, csvContent, % csvFilePath
index := 0
index2 := 0

Send {PgUp 5}
Sleep, 500

MouseMove, xCoord1, yCoord1, 0
Click
Sleep, 500

Loop, Parse, csvContent, `n, `r
{
	

    ; Copy the current line to the clipboard
    clipboard := A_LoopField
    ; Wait for the clipboard to contain data
    ClipWait

    ; Check the index value and set the appropriate X, Y coordinates
    if (index == 0) {
        xCoord := input_box_x1
    } else if (index == 1) {
        xCoord := input_box_x2
    } else if (index == 2) {
        xCoord := input_box_x3
    }

    if(index2 > 2 and newY == 0) {
	 input_box_y  += 30
         add_button_y += 30
         newY = 1
    }

    ; Move the cursor to the specified X, Y coordinates
    MouseMove, xCoord, input_box_y, 0
    ; Perform a left mouse button click at the current cursor position
    Click
    ; Wait for a short period of time to ensure the click has taken effect
    Sleep, 300
    Click
    Sleep, 100
    Send ^a
    Sleep, 100
    Send {Backspace}
    Sleep, 100

    ; Paste the clipboard content using Ctrl+V
    Send, ^v
    ; Wait for a short period of time to ensure the paste operation is complete
    Sleep, 300

    if (index == 2)
    {
         MouseMove, add_button_x, add_button_y, 0 
	 Click
         Sleep, 500

	 MouseMove, submit_ok_x, submit_ok_y, 0
	 Sleep, 300
	 Click
	 Sleep, 300
	 Click
    }

    ; Increment the index and reset it to 0 if it reaches 3
    index := Mod(index + 1, 3)

    index2 += 1
}