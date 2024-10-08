from flask import Flask, request, jsonify, session, redirect, url_for
from flask_session import Session
import psycopg2
from flask_cors import CORS 

app = Flask(__name__)
CORS(app) 

# Oturum için gizli anahtar ayarlayın
app.config['SECRET_KEY'] = 'GSAJK5673554b5s#wadd1.VDKK5'

# Oturum verilerini saklamak için Flask-Session'ı yapılandırın
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def is_json_empty(json_data):
    return len(json_data) == 0

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Authentication
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": False, "message": "Username and password are required"}), 400

    try:
        conn = psycopg2.connect("postgresql://postgres:479528@localhost/havelsan_suit")
        cur = conn.cursor()

        # Parametreli sorgu kullanarak SQL enjeksiyonunu önleme
        sql = "SELECT * FROM users WHERE username=%s AND password=%s"
        cur.execute(sql, (username, password))
        record = cur.fetchone()

        if record is not None:
            session['user_id'] = record[0]
            session['user_name'] = record[1]
            session['sys_role'] = record[3]
            
            return jsonify({"status": True, "sys_role": session['sys_role'], "session": session['user_id'], "session_username": session['user_name']})
        else:
            return jsonify({"status": False, "message": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"logout": True,})

@app.route("/api/getSuperOperatorUserData", methods=["POST"])
def get_superOperatorData():
    data = request.json
    username = data.get('username')
    try:
        conn = psycopg2.connect("postgresql://postgres:479528@localhost/havelsan_suit")
        cur = conn.cursor()
        sql = "SELECT * FROM users WHERE username = %s"
        cur.execute(sql, (username,))
        operators = cur.fetchall()
        conn.commit()
        return jsonify(operators)
    except (psycopg2.Error, Exception) as error:
        # Hata oluştuğunda uygun bir yanıt döndürün
        return jsonify({'error': str(error)})
    finally:
        # Bağlantıyı ve imleci kapat
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route("/api/updateSuperOperatorUserData", methods=["POST"])
def superOperator_update_profile():
    data = request.json
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    username = data.get('username')
    real_username = data.get("real_username")
    email = data.get('email')
    address = data.get("address")
    phone=data.get("phone")

    if not all([firstName, lastName, username, real_username, email, address]):
        return jsonify({"status": False, "message": "All fields are required"}), 400

    try:
        conn = psycopg2.connect("postgresql://postgres:479528@localhost/havelsan_suit")
        cur = conn.cursor()

        # Mevcut kullanıcı adını ve e-postayı kontrol et
        sql = "SELECT username, email FROM users WHERE username = %s"
        cur.execute(sql, (real_username,))
        existing_user = cur.fetchone()

        if not existing_user:
            return jsonify({"status": False, "message": "No user found with the given username"}), 404

        existing_username, existing_email = existing_user

        # Yeni kullanıcı adı veya e-posta mevcut mu kontrol et
        if username != existing_username:
            sql = "SELECT 1 FROM users WHERE username = %s"
            cur.execute(sql, (username,))
            if cur.fetchone():
                return jsonify({"status": False, "message": "Username already exists"}), 409

        if email != existing_email:
            sql = "SELECT 1 FROM users WHERE email = %s"
            cur.execute(sql, (email,))
            if cur.fetchone():
                return jsonify({"status": False, "message": "Email already exists"}), 409

        # Kullanıcı bilgilerini güncelle
        sql = """
        UPDATE users SET firstname = %s, lastname = %s, username = %s, email = %s, address = %s, phone=%s
        WHERE username = %s
        """
        cur.execute(sql, (firstName, lastName, username, email, address,phone, real_username))
        conn.commit()

        response = {"status": True, "message": "User data updated successfully", "logout":False}

        # Kullanıcı adı veya e-posta değişmişse oturumu sonlandır ve özel bir durum döndür
        if username != existing_username or email != existing_email:
            session.clear()
            return jsonify({"logout":True})  

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.route("/api/operators'", methods=['POST'])
def get_operators():
    conn = psycopg2.connect("postgresql://postgres:479528@localhost/havelsan_suit")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    operators = cur.fetchall()
    conn.close()
    return jsonify(operators)

@app.route("/api/operatorList", methods=["POST"])
def get_users():
    try:
        conn = psycopg2.connect("postgresql://postgres:479528@localhost/havelsan_suit")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE sys_role=0")
        users = cur.fetchall()
        result = []
        for user in users:
            user_dict = {
                "id": user[0],
                "firstname": user[6],
                "lastname": user[7],
                "username": user[1],
                "email": user[4],
                "address": user[5],
                "phone": user[8]
            }
            result.append(user_dict)
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

def add_operator_to_database(user_id, username, firstName, lastName, email, password, address, phone):
    try:
        conn = psycopg2.connect("postgresql://postgres:479528@localhost/havelsan_suit")
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
        if cur.fetchone():
            return False, "User already exists"

        cur.execute("INSERT INTO users (id,username, firstname, lastname, email, address,sys_role,password,phone) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s)", 
                    (user_id, username, firstName, lastName, email, address, 0, password, phone))
        conn.commit()

        return True, "User added successfully"
    except Exception as e:
        return False, str(e)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route("/api/addOperator", methods=["POST"])
def add_operator():
    data = request.json
    user_id = data.get('id')
    username = data.get("username")
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    password = data.get("password")
    address = data.get('address')
    phone = data.get("phone")

    if not all([user_id, email, username]):
        return jsonify({"status": False, "message": "All fields are required"}), 400

    success, message = add_operator_to_database(user_id, username, firstName, lastName, email, password, address, phone)

    if success:
        return jsonify({"status": True, "message": message}), 200
    else:
        return jsonify({"status": False, "message": message}), 409 if message == "User already exists" else 500

def delete_operator_from_database(user_id):
    try:
        conn = psycopg2.connect("postgresql://postgres:479528@localhost/havelsan_suit")
        cur = conn.cursor()
        
        # Kullanıcıyı silme sorgusu
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        
        if cur.rowcount == 0:
            return False, "User not found"
        
        return True, "User deleted successfully"
    except Exception as e:
        return False, str(e)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route("/api/deleteOperator", methods=["POST"])
def delete_operator():
    data = request.json
    user_id = data.get('id')

    if not user_id:
        return jsonify({"status": False, "message": "User ID is required"}), 400

    success, message = delete_operator_from_database(user_id)

    if success:
        return jsonify({"status": True, "message": message}), 200
    else:
        return jsonify({"status": False, "message": message}), 404 if message == "User not found" else 500

@app.route("/api/verifyPassword", methods=["POST"])
def verify_password():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": False, "message": "Username and password are required"}), 400

    try:
        conn = psycopg2.connect("postgresql://postgres:479528@localhost/havelsan_suit")
        cur = conn.cursor()

        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        cur.execute(sql, (username, password))
        user = cur.fetchone()

        if user:
            return jsonify({"status": True, "message": "Password verified"}), 200
        else:
            return jsonify({"status": False, "message": "Invalid password"}), 401

    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route("/api/changePassword", methods=["POST"])
def change_password():
    data = request.json
    username = data.get('username')
    new_password = data.get('new_password')

    if not username or not new_password:
        return jsonify({"status": False, "message": "Username and new password are required"}), 400

    try:
        conn = psycopg2.connect("postgresql://postgres:479528@localhost/havelsan_suit")
        cur = conn.cursor()

        sql = "UPDATE users SET password = %s WHERE username = %s"
        cur.execute(sql, (new_password, username))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"status": False, "message": "User not found"}), 404

        return jsonify({"status": True, "message": "Password updated successfully"}), 200

    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    app.run(debug=True)

        
