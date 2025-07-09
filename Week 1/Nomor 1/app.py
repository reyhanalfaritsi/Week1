from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

def generate_password(length=6):
    """
    Fungsi untuk menghasilkan password acak dengan panjang tertentu
    """
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@app.route('/api/generate-password', methods=['POST'])
def generate_password_endpoint():
    """
    Endpoint untuk menerima NIK dan Role, kemudian menghasilkan password 6 karakter
    """
    try:
        # Mendapatkan data dari request JSON
        data = request.get_json()
        
        # Validasi apakah request berisi JSON
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request harus berupa JSON',
                'data': None
            }), 400
        
        nik = data.get('nik')
        role = data.get('role')
        
        # Validasi input
        if not nik or not role:
            return jsonify({
                'success': False,
                'message': 'NIK dan Role harus diisi',
                'data': None
            }), 400
        
        # Validasi NIK (harus berupa string/number dengan panjang 16 digit)
        nik_str = str(nik)
        if len(nik_str) != 16 or not nik_str.isdigit():
            return jsonify({
                'success': False,
                'message': 'NIK harus terdiri dari 16 digit angka',
                'data': None
            }), 400
        
        # Validasi Role (contoh role yang diizinkan)
        allowed_roles = ['admin', 'user', 'manager', 'staff']
        if role.lower() not in allowed_roles:
            return jsonify({
                'success': False,
                'message': f'Role tidak valid. Role yang diizinkan: {", ".join(allowed_roles)}',
                'data': None
            }), 400
        
        # Generate password 6 karakter
        generated_password = generate_password(6)
        
        # Response sukses dengan password
        response_data = {
            'success': True,
            'message': 'Password berhasil dibuat',
            'data': {
                'nik': nik_str,
                'role': role,
                'password': generated_password,
            }
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Terjadi kesalahan pada server',
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)