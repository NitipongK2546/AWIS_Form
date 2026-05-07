# Setup v0.2.3.1-fix-01

## เริ่มต้น

รันคำสั่งใน Terminal: 

```bash
git clone https://github.com/NitipongK2546/AWIS_Form awis_form

cd awis_form
```

### Windows
```bash
python -m venv .venv

source .venv/Scripts/activate
```

### Linux
```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 1) Docker

สามารถเริ่มจาก 0 ได้ผ่านคำสั่ง

ต้องให้สิทธิการรันคำสั่งให้กับ full_setup_docker.s้h ก่อนด้วย เพื่อให้ Execute ได้
```bash
./full_setup_docker.sh
```

โดยข้างในคือ

```bash
docker compose up -d --build

# รอจนกว่า Database จะเริ่มทำงานเต็มตัว 
# แล้วจึงจะไปขั้นต่อไป
# echo "Database Server is up" สามารถเปลี่ยนเป็นคำสั่งก็ได้
./_scripts/wait-for-it.sh localhost:3306 -- echo "Database Server is up."

# รัน setup.sh ใน Container ที่มี Server อยู่
docker exec awis_server ./setup.sh
```

สามารถเข้าถึง Server ได้ผ่าน localhost โดยตรง โดยไม่ต้องใส่เลข PORT

## 2) Local

รันคำสั่งใน Bash: 

### Windows
```bash
./setup.sh
```

### Linux
ต้องให้สิทธิการรันคำสั่งให้กับ setup.sh ก่อนด้วย เพื่อให้ Execute ได้
```bash
chmod +x setup.sh

./setup.sh
```

Script ควรตั้งค่าพื้นฐานให้สำเร็จแล้ว


สามารถสั่งให้ทำงานได้โดย

```bash
python manage.py runserver 127.0.0.1:8002
```

---

ไม่ว่าจะ Step ไหนก็ตาม

เมื่อรันคำสั่งตามด้านบน สิ่งที่จะเกิดขึ้นคือ

1. Database ถูก Migrate
1. Superuser ถูกสร้างขึ้น
1. Court User ถูกสร้างขึ้น
1. Group ถูกสร้างขึ้น
1. มีการสร้าง และ Assign Permission ให้อัตโนมัติ
1. Server เปิดให้เข้าถึงได้

---

## Finalize

ตั้งค่าไฟล์ .env ให้ครบตามที่ต้องการ

เปลี่ยน Field ใน /project_awis/settings.py
```python
# จาก

ENABLE_API = False
DEBUG = True

# ให้เป็น

ENABLE_API = True
DEBUG = False
```