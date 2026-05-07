# AWIS Form v0.2.3.1-fix-01

## Markdown Directory

1. [อธิบาย Setup](/_documentation/SETUP.md)
1. [อธิบาย Forms](/_documentation/FORMS.md)
1. [อธิบาย Permission](/_documentation/PERMISSIONS.md)
1. [อธิบาย API](/_documentation/API.md)

------------------------------------------------
## 1. ตั้งค่า

สามารถอ่านได้ที่ SETUP.md ด้านบน

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

TODO: Add the TDO... I know.