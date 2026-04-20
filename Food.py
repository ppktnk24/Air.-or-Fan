def main():
    # สร้าง Dictionary เปล่าสำหรับเก็บรายการซื้อของ
    # โดยมี Key เป็นชื่อวัตถุดิบ และ Value เป็นจำนวน
    shopping_list = {}

    print("=== ยินดีต้อนรับสู่ระบบจัดการรายการซื้อของ ===")

    while True:
        print("\nเมนูการใช้งาน:")
        print("1. เพิ่มวัตถุดิบ / แก้ไขจำนวน")
        print("2. ดูรายการซื้อของทั้งหมด")
        print("3. ลบวัตถุดิบ")
        print("4. ออกจากโปรแกรม")
        
        choice = input("กรุณาเลือกเมนู (1-4): ")

        if choice == '1':
            item_name = input("กรุณาใส่ชื่อวัตถุดิบที่ต้องการซื้อ: ").strip()
            item_qty = input("กรุณาใส่จำนวน (เช่น 2 กิโลกรัม, 3 ขวด, 5 ชิ้น): ").strip()
            
            if item_name == "" or item_qty == "":
                print("❌ ข้อมูลไม่ครบถ้วน กรุณาลองใหม่อีกครั้ง")
            else:
                shopping_list[item_name] = item_qty
                print(f"✅ เพิ่ม '{item_name}' จำนวน '{item_qty}' ลงในตระกร้าเรียบร้อยแล้ว!")

        elif choice == '2':
            print("\n--- 🛒 รายการซื้อของของคุณ ---")
            if len(shopping_list) == 0:
                print("ยังไม่มีรายการในตระกร้า")
            else:
                for index, (item, qty) in enumerate(shopping_list.items(), start=1):
                    print(f"{index}. {item} : {qty}")
            print("------------------------------")

        elif choice == '3':
            item_name = input("กรุณาใส่ชื่อวัตถุดิบที่ต้องการลบ: ").strip()
            if item_name in shopping_list:
                del shopping_list[item_name]
                print(f"🗑️ ลบ '{item_name}' ออกจากรายการแล้ว")
            else:
                print(f"❌ ไม่พบ '{item_name}' ในรายการ")

        elif choice == '4':
            print("👋 ขอบคุณที่ใช้งาน ขอให้สนุกกับการช้อปปิ้ง!")
            break

        else:
            print("❌ ตัวเลือกไม่ถูกต้อง กรุณาเลือกตัวเลข 1-4 เท่านั้น")

if __name__ == "__main__":
    main()