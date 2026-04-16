# AWIS Form v0.2.1

## Markdown Directory

1. [Guideline อธิบาย](/GUIDELINE.md)
1. [Permission อธิบาย](/PERMISSIONS.md)


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

- dashboard: หน้าหลัก ดูสถานะและอนุมัติฟอร์ม

- users: เก็บข้อมูลผู้ใช้และเรื่องสิทธิในการเข้าถึง

- warrant_form: สร้างฟอร์ม (formAwaitApproval)

------------------------------------------------

## 3. สิ่งที่ต้องพัฒนาต่อ

หากมีใครคนไหนที่ต้องพัฒนาเว็บไซต์ต่อ ก็สามารถ Clone หรือ Fork ไปได้เลย

1. ปรับแบบฟอร์ม HTML ให้ตรงกับของจริง
1. แก้ Hidden Field ที่ใส่ข้อมูลที่ผู้กรอกไม่ต้องรู้โดยอัตโนมัติ
1. เพิ่ม Feature ต่าง ๆ เพิ่ม เช่น

    - Print to PDF ได้ผ่าน Browser เลย 
    - Encrypt Data 
    - ~~Text-to-Speech...~~ 