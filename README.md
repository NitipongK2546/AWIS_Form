# AWIS Form v0.2.2

## Markdown Directory

1. [Guideline อธิบาย](/_documentation/GUIDELINE.md)
1. [Permission อธิบาย](/_documentation/PERMISSIONS.md)


## 0. ติดตั้ง

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
ต้องให้สิทธิการรันคำสั่งให้กับ setup.sh ก่อนด้วย เพื่อให้ Execute ได้
```bash
python3 -m venv .venv

source .venv/bin/activate
```

------------------------------------------------
## 1. ตั้งค่า

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

------------------------------------------------

## 2. รายละเอียด

- awis_custom_settings: มีไว้เผื่อไว้สำหรับการทำ Single Source of Truth... ก็แค่การ Import จากที่นี่แทน ถ้าจะแก้ก็จะได้แก้ง่าย ๆ 

- project_awis: Directory หลักของโปรเจค มีไฟล์ Settings

- admin_panel: มีไว้สำหรับให้ admin ใช้ระบบได้ง่ายและเร็วขึ้น ถ้าไม่มีก็ Implement อันใหม่เอง

- api: ไว้สำหรับให้ภายนอกเชื่อม Server ของเราได้ และให้ Javascript ของเราติดต่อกับ Server ของเรา

- dashboard: หน้าหลัก สามารถเข้าถึง ร่างคำร้อง, อนุมัติฟอร์มคำร้อง, และดูสถานะคำร้องที่ส่งแล้ว

- users: เก็บข้อมูลผู้ใช้และเรื่องสิทธิในการเข้าถึง

- warrant_form: สร้างฟอร์ม (formAwaitApproval) และสร้าง Draft (ร่างคำร้อง) ได้

------------------------------------------------

## 3. สิ่งที่ต้องพัฒนาต่อ

หากมีใครคนไหนที่ต้องพัฒนาเว็บไซต์ต่อ ก็สามารถ Clone หรือ Fork ไปได้เลย

1. เตรียมสำหรับการให้ Website ทำงานได้จริง
    - เชื่อมต่อกับฐานข้อมูลของจริงที่ไม่ใช่ Sqlite เช่น MicrosoftSQL
    
    - ใช้โปรแกรมสำหรับการ Host Server โดยเฉพาะ แทนการใช้ของ Django เอง เช่น Gunicorn
    
    - เขียน Script ตั้งค่าระบบตั้งแต่ตอนเริ่มต้นใหม่ให้เรียบร้อย
    
    - ตรวจสอบสิทธิ์และเพิ่มสิทธิ์การเข้าถึงของแต่ละสิทธิ์ให้ถูกต้องและครบถ้วนทุกระบบ