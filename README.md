# Flask Chat Application

### **Description**  
A real-time chat application built with Flask, SocketIO, and SQLAlchemy. This project includes user authentication, a real-time messaging system, and a simple web interface for chatting. It serves as a great starting point for developers interested in learning about Flask-based web apps and real-time communication.

---

### **Features**  
- **User Authentication:**  
  - Signup and login functionality using Flask-Login.  
  - Password management (currently plaintext; can be upgraded to hashed for security).  
- **Real-time Messaging:**  
  - Real-time chat powered by Flask-SocketIO.  
  - Broadcast messages to all connected users.  
- **Database Integration:**  
  - User information stored using SQLAlchemy with a SQLite backend.  
- **Session Management:**  
  - User sessions maintained with Flask-Login.  
  - Notifications when users join or leave the chat.  

---

### **Technologies Used**  
- **Frameworks:** Flask, Flask-SocketIO  
- **Database:** SQLAlchemy with SQLite  
- **Other Tools:** Flask-Login for session handling  

---

### **Setup Instructions**  
Follow these steps to set up and run the application on your local machine:

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/yourusername/flask-chat-app.git
   cd flask-chat-app
