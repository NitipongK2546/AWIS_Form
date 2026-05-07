# Users v0.2.3.1-fix-01

## 1. ระบบ Users คร่าว ๆ

1. User Access List: คือตารางเก็บ

2. UserDataModel: คือตารางเก็บข้อมูลของผู้ใช้ที่ถูกเพิ่มเข้า Access List **โดยเป็นบัญชีและช่องทางหลักสำหรับการใช้กับระบบของ Django ระบบหลายอย่างใช้ข้อมูลจาก UserDataModel**

สิทธิ์ทั้งหมดของ Users ถูกกำหนดไว้ใน /awis_custom_settings/default_perms.py และได้ถูกตั้งค่าไว้โดยการรัน setup.sh

หากต้องการเพิ่ม สามารถเข้าไปแก้ไขได้ แต่ต้องมีการ migrate ใหม่

TODO: เขียน Script ลบ / เพิ่ม Permission ได้
