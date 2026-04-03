import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 5050
ROWS = 6
COLS = 7

matchmaking_queue = []

def check_winner(board):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] != ' ':
                return board[r][c]
    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] != ' ':
                return board[r][c]
    # Check diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] != ' ':
                return board[r][c]
    # Check diagonal (up-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] != ' ':
                return board[r][c]
    
    if all(cell != ' ' for row in board for cell in row): return 'Draw'
    return None

def game_session(conn_r, conn_y):
    # Assign Roles (B = Blue, W = White)
    conn_r.sendall((json.dumps({"type": "WELCOME", "role": "Blue"}) + '\n').encode('utf-8'))
    conn_y.sendall((json.dumps({"type": "WELCOME", "role": "White"}) + '\n').encode('utf-8'))
    
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    turn = "Blue"
    sockets = {"Blue": conn_r, "White": conn_y}
    
    while True:
        # Broadcast state
        update_msg = json.dumps({"type": "UPDATE", "board": board, "turn": turn, "status": "ongoing"}) + '\n'
        for s in sockets.values():
            s.sendall(update_msg.encode('utf-8'))

        active_socket = sockets[turn]
        try:
            data = active_socket.recv(1024).decode('utf-8')
            if not data: break
            
            msg = json.loads(data.strip().split('\n')[0])
            if msg["type"] == "MOVE":
                col = msg["col"]
                
                # Connect 4 Gravity: find the lowest empty row
                success = False
                for r in range(ROWS-1, -1, -1):
                    if board[r][col] == ' ':
                        board[r][col] = turn
                        success = True
                        break
                
                if not success:
                    continue 

                winner = check_winner(board)
                if winner:
                    status = "Draw!" if winner == 'Draw' else f"Player {winner} wins!"
                    final_msg = json.dumps({"type": "UPDATE", "board": board, "turn": turn, "status": status}) + '\n'
                    for s in sockets.values(): s.sendall(final_msg.encode('utf-8'))
                    break
                
                turn = "White" if turn == "Blue" else "Blue"
        except:
            break

    conn_r.close()
    conn_y.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    server.settimeout(1)
    print(f"[SERVER] Listening on {HOST}:{PORT}")
    
    try:
        while True:
            try:
                conn, addr = server.accept()
            except socket.timeout:
                continue
            data = conn.recv(1024).decode('utf-8')
            if "CONNECT" in data:
                matchmaking_queue.append(conn)
                print(f"[QUEUE] Players: {len(matchmaking_queue)}")
                
                if len(matchmaking_queue) >= 2:
                    p1, p2 = matchmaking_queue.pop(0), matchmaking_queue.pop(0)
                    threading.Thread(target=game_session, args=(p1, p2)).start()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
        server.close()

if __name__ == "__main__":
    start_server()