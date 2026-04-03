import socket
import json
import sys
import os
import time

HOST = '127.0.0.1'
PORT = 5050

def print_board(board):
    symbols = { "Blue": '🔵', "White": '⚪', ' ': '  ' }



    print("\n   0    1    2    3    4    5    6")
    print("+" + "----+" * 7)
    for row in board:
        display_row = [symbols[cell] for cell in row]
        print("| " + " | ".join(display_row) + " |")
        print("+" + "----+" * 7)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(json.dumps({"type": "CONNECT"}).encode('utf-8'))
    print("Waiting for an opponent...")
    
    my_role = None
    
    while True:
        data = client.recv(4096).decode('utf-8')
        if not data: break
            
        for chunk in data.strip().split('\n'):
            if not chunk: continue
            msg = json.loads(chunk)
            
            if msg["type"] == "WELCOME":
                my_role = msg["role"]
                print(f"Connected! You are Player {my_role}")
                
            elif msg["type"] == "UPDATE":
                clear_screen()

                print("\n====================================")
                print("            CONNECT FOUR")
                print("====================================\n")

                print(f"You are Player {my_role}")
                print(f"Current turn: Player {msg['turn']}\n")

                print_board(msg["board"])
                
                if msg["status"] != "ongoing":
                    print(f"GAME OVER: {msg['status']}")
                    continue
                
                if msg["turn"] == my_role:
                    while True:
                        try:
                            col = int(input("Your Turn (Column 0-6): "))
                            if col < 0 or col > 6:
                                print("[!] Out of bounds. Choose 0-6.")
                                continue
                            if msg["board"][0][col] != ' ':
                                print("[!] Column is full! Choose another.")
                                continue
                            move_msg = json.dumps({"type": "MOVE", "col": col}) + '\n'
                            client.sendall(move_msg.encode('utf-8'))
                            break
                        except ValueError:
                            print("[!] Enter a valid number.")
                else:
                    print(f"Waiting for Player {msg['turn']}...")
            
            elif msg["type"] == "ERROR":
                print(f"\n[!] SERVER ERROR: {msg['payload']}")

            elif msg["type"] == "REPLAY_REQUEST":
                answer = input("Play again? (Y/N): ").strip().upper()
                while answer not in ["Y", "N"]:
                    answer = input("Please enter Y or N: ").strip().upper()

                replay_msg = json.dumps({"type": "REPLAY", "answer": answer}) + '\n'
                client.sendall(replay_msg.encode('utf-8'))

    client.close()

if __name__ == "__main__":
    start_client()