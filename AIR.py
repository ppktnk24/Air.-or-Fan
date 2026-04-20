import cv2
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

def main():
    print("กำลังดาวน์โหลดและโหลดโมเดล AI (อาจใช้เวลาสักครู่ในการรันครั้งแรก)...")
    model_id = "openai/clip-vit-base-patch32"
    processor = CLIPProcessor.from_pretrained(model_id)
    model = CLIPModel.from_pretrained(model_id)

    # กำหนดหมวดหมู่ให้ AI ค้นหา (ใส่หมวดพื้นหลัง/คน ไว้เป็นตัวหลอกเผื่อไม่เจอทั้งพัดลมและแอร์)
    labels = ["a fan", "an air conditioner", "a generic room background or person"]

    # เปิดกล้องเว็บแคม (ตัวเลข 0 คือกล้องตัวหลักของคอมพิวเตอร์)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ข้อผิดพลาด: ไม่สามารถเชื่อมต่อกับกล้องได้")
        return

    print("เปิดกล้องสำเร็จ! ลองหันกล้องไปที่พัดลมหรือแอร์ดูครับ (กดปุ่ม 'q' บนแป้นพิมพ์เพื่อออก)")

    while True:
        # อ่านภาพจากกล้องทีละเฟรม
        ret, frame = cap.read()
        if not ret:
            break

        # OpenCV ปกติจะอ่านสีเป็น BGR แต่ AI ตัวนี้ต้องการสีแบบ RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_frame)

        # นำภาพและคำศัพท์ที่เราตั้งไว้ แปลงให้อยู่ในรูปแบบที่ AI เข้าใจ
        inputs = processor(text=labels, images=pil_img, return_tensors="pt", padding=True)
        
        # ป้อนข้อมูลเข้า AI เพื่อทำนายผล
        with torch.no_grad():
            outputs = model(**inputs)
        
        # คำนวณหาความน่าจะเป็น (เปอร์เซ็นต์ความมั่นใจ)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1).cpu().numpy()[0]
        
        # หาหมวดหมู่ที่ AI มั่นใจมากที่สุด
        max_idx = probs.argmax()
        predicted_label = labels[max_idx]
        confidence = probs[max_idx] * 100

        # กำหนดข้อความที่จะแสดงบนหน้าจอ
        if "background" in predicted_label or confidence < 55:
            display_text = "Scanning for Fan or AC..."
            box_color = (0, 0, 255) # สีแดง แปลว่ากำลังค้นหา
        else:
            # แปลงข้อความให้แสดงผลได้สวยงามขึ้น
            if predicted_label == "a fan":
                thai_label = "Fan"
            else:
                thai_label = "Air Conditioner"
                
            display_text = f"Detected: {thai_label} ({confidence:.1f}%)"
            box_color = (0, 255, 0) # สีเขียว แปลว่าตรวจพบแล้ว

        # วาดข้อความทับลงไปบนวิดีโอ (มุมซ้ายบน)
        cv2.putText(frame, display_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, box_color, 2)
        
        # แสดงหน้าต่างวิดีโอ
        cv2.imshow("Fan vs AC Detector", frame)

        # วนลูปไปเรื่อยๆ จนกว่าผู้ใช้จะกดปุ่ม 'q' เพื่อออกจากโปรแกรม
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # คืนค่าการใช้งานกล้องและปิดหน้าต่างทั้งหมด
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()