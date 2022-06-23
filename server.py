# Import required modules
import socket
import threading
import secrets
import el_gamal

HOST = '127.0.0.1'
PORT = 1234 # to 65535
LISTENER_LIMIT = 5
active_clients = [] # danh sách tất cả các client đang kết nối

# Function to listen for upcoming messages from a client
def listen_for_messages(client, username,key,elgamapublickey):
#thực hiện việc nhận tin nhắn từ client . lạp cho đến khi nhận đuọc và sử dụng "utf-8" để giải mã tín hiệu
    while 1:

        message = client.recv(2048).decode('utf-8')
        #print("RECV : ",message)    # in ra thông tin nhận được bao gồm cả khóa kết nối của client
        #nếu tin nhắn không rỗng thi thực hiện gửi lại cho tất cả các client đang hoạt dộng trong hàm send_messages_to_all   | nếu không thì sẽ báo tin nhắn trống
        if message != '':
            ####### send
            final_msg = username + '~' + message + '~' + key + "~"+elgamapublickey+"~"
            send_messages_to_all(final_msg)

# Function to send message to a single client
def send_message_to_client(client, message):
    #thực hiện gửi thông tin sang cho client với khóa kết nối và các kck,kbm
    client.sendall(message.encode()) 
    print("SEND : ", message.encode() )

# Function to send any new message to all the clients that
# are currently connected to this server
    #####here
def send_messages_to_all(message):
    # dùng vòng lặp để duyệt hết các user đang hoạt động trong active_clients   và thực hiện gửi tin nhắn đến từng client
    for user in active_clients:
        # Start the security phase using message then pass the message to client
        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client,key):
    #key sử dung để làm khóa cho việc bắt tay 3 bước cho giao thưcs TCP
    # Server sẽ lắng nghe tín hiệu từ từng user và liên hệ lại
    # Contain the username
    while 1:

        username = client.recv(2048).decode('utf-8')
        print("RECV : ",username)
        # nếu có user đang hoạt động thì thêm user vào cuối danh sách active_clients
        if username != '':
            active_clients.append((username, client,key)) #Thực hiện việc thêm vào cuối danh sách
            # generate session key sử dụng khóa này để thực hiện kết nối dánh riêng cho từng client
            key = secrets.token_hex(8).upper() #thực hiện tạo khóa sử dụng mã hóa bảo mật chuỗi dạng thập lục phân và chuyển về dạng chữ in hoa

            string_ints = [str(x) for x in ElgamalKey] # chuyển chuõi x duyệt trong danh sách các key elgamal  vào trong danh sách String_ints
            elgamalpublickey = ",".join(string_ints) # thêm dấu  "," vào trong danh sáchh
            print("elgamal public key",elgamalpublickey)
#######send
            prompt_message = "SERVER~" + f"{username} added to the chat~" + key +"~" + elgamalpublickey +"~"
            send_messages_to_all(prompt_message)  # thông báp thông tin user đã joim  vàp server với thông tin các khóa công khai, khóa riêng và khóa phiên của clients
            # thông báo khóa phiên đã được tạo ra thành công
            print("Sessison key successfully generated for " + f"{username } ==>",key)

            break
        else:
            print("Client username is empty")
    #thực hiện mở cỏng listen_for_messade và định dạng chuỗi như args.
    threading.Thread(target=listen_for_messages, args=(client, username, key,elgamalpublickey )).start()


# Main function
def main():
    global ElgamalKey  # tạo biến toàn cục và lấy thông tin vè khóa công khai được tạo
    ElgamalKey = el_gamal.generate_public_key()
    # tạo socket sử dụng ipv4 (AF_INET và giao thức truyền tin TCP(SOCK_STREAM)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # tạo ngoại lệ để bắt lỗi
    try:
        server.bind((HOST, PORT)) # thực hiện đăng kí tên miền và cổng
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")
    
    
    # Set server limit
    server.listen(LISTENER_LIMIT)  # thực hiện số lần lắng nghe tối đa

    # thực hiện chấp nhận kết nôis cho các client với
    while 1:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        key = ""
        threading.Thread(target=client_handler, args=(client,key, )).start()  # sử dung luồng thục hiện việ bắt tay 3 bước với client và sử dụng khóa phiên để kết nối


if __name__ == '__main__':
    main()