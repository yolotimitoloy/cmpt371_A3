# **CMPT 371 A3 `Connect Four`**

**Course:** CMPT 371 \- Data Communications & Networking  
**Instructor:** Mirza Zaeem Baig  
**Semester:** Spring 2026  
<span style="color: purple;">***RUBRIC NOTE: As per submission guidelines, only one group member will submit the link to this repository on Canvas.***

## **Group Members**

| Name | Student ID | Email |
| :---- | :---- | :---- |
| Nok Tim Yeung | 301649679 | nty1@sfu.ca |
| Daniil Bugakov | 301540700 | dba73@sfu.ca |

## **1\. Project Overview & Description**

This project is a multiplayer Connect Four game built using Python's TCP sockets. Two clients to connect to a central server, which matches them into a game session, and allows them to play against each other in real-time through the terminal.

The server is authoritative, meaning it:

* Maintains the board state
* Validates all moves 
* Determines win/draw conditions

The clients:

* Render the board in the terminal
* Send play inputs to the server

## **2\. Features**

* Two player gameplay over TCP
* Terminal based UI
* Turn based system with input validation
* Win and draw detection
* Replay system (both players must agree to a rematch to restart)
* Multi-game support using threading

## **2\. System Limitations & Edge Cases**

As required by the project specifications, we have identified and handled (or defined) the following limitations and potential issues within our application scope:

* **Concurrency (Threading):** 
  * <span style="color: green;">*Solution:*</span> Each pair of players runs in its own game session thread. Allows multiple games to run at the same time.
  * <span style="color: red;">*Limitation:*</span> Threading is limited by system resources. A scalable system would use asynchronous I/O.
* **TCP Stream Buffering:** 
  * <span style="color: green;">*Solution:*</span> TCP is a continuous byte stream, meaning multiple JSON messages can merge. Appending a newline \n to each JSON message and splitting the buffer on receive.  
* **Input Validation & Security:** 
  * <span style="color: red;">*Limitation:*</span> Clients validates user input (0-6 range, integer). Server assumes correctly formatted messages. However, a modified client could send invalid data.

## **3\. Video Demo**

<span style="color: purple;">***RUBRIC NOTE: Include a clickable link.***</span>  
Our 2-minute long video demonstration covering connection establishment, data exchange, real-time gameplay, and process termination can be viewed below:  
[**▶️ Watch Project Demo on YouTube**](https://youtu.be/z3_nOhoy3gM)

## **4\. Prerequisites (Fresh Environment)**

To run this project, you need:

* **Python 3.10** or higher.  
* No external pip installations are required (uses standard socket, threading, json, sys libraries).  
* (Optional) VS Code or Terminal.

<span style="color: purple;">***RUBRIC NOTE: No external libraries are required.***</span>

## **4\. Step-by-Step Run Guide**

<span style="color: purple;">***RUBRIC NOTE: The grader must be able to copy-paste these commands.***</span>


### **Step 1: Start the Server**

Open your terminal and navigate to the project folder. The server binds to 127.0.0.1 on port 5050\.  
```bash
python server.py  
# Console output: "[STARTING] Server is listening on 127.0.0.1:5050"
```

### **Step 2: Connect Player 1 (Blue)**

Open a **new** terminal window (keep the server running). Run the client script to start the first client.  
```bash
python client.py  
# Console output: "Connected. Waiting for opponent..."
```

### **Step 3: Connect Player 2 (White)**

Open a **third** terminal window. Run the client script again to start the second client.  
```bash
python client.py  
```

### **Step 4: Gameplay**

1. **Player Blue** will be prompted: Enter col (e.g., '1') and press Enter.  
2. The server updates the board on both screens.  
3. **Player White** takes their turn.  
4. After the match ends, both players are prompted:
```bash
  # Console output: Play again? (Y/N)
```
   * If both players choose Y - a new game starts
5. The connection naturally terminates when one of the players declines a rematch offer.

## **5\. Technical Protocol (JSON over TCP)**

All communication uses JSON messages over TCP:

* **Message Format:** `{"type": <string>, "payload": <data>}`  
* **Handshake:** \* Client: `{"type": "CONNECT"}`  
  * Server: `{"type": "WELCOME", "role": "Blue"}`  
* **Gameplay Phase:**  
  * Client: `{"type": "MOVE", "col": 1}`  
  * Server: `{"type": "UPDATE", "board": [...], "turn": "Blue", "status": "ongoing"}`

## **6\. Academic Integrity & References**

<span style="color: purple;">***RUBRIC NOTE: List all references used and help you got. Below is an example.***</span>

* **Code Origin:**  
  * The project was developed by adapting the provided sample repository.
  * The sample repository informed the initial client-server structure, socket setup, matchmaking flow, and basic game-session logic.
  * Our group then modified and extended the code, including replay support, terminal UI improvements, Blue/White player presentation and shutdown handling.
* **GenAI Usage:**  
  * ChatGPT was used to assist in debugging, UI improvements.  
* **References:**  
  * [Python Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)  
  * [Real Python: Intro to Python Threading](https://realpython.com/intro-to-python-threading/)
  * [Sample Repository] (provided for assignment reference)(https://github.com/mariam-bebawy/CMPT371_A3_Socket_Programming) 