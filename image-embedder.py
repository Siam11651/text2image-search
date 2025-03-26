import os
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

MODEL = "openai/clip-vit-base-patch32"
processor = CLIPProcessor.from_pretrained(MODEL)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CLIPModel.from_pretrained(MODEL).to(device)
DIRECTORY = "images"

for index, file in enumerate(os.listdir(DIRECTORY)):
    image = Image.open(os.path.join(DIRECTORY, file))
    width, height = image.size
    resize_factor = 256 / max(width, height)
    image = image.resize((int(round(width * resize_factor)), int(round(height * resize_factor))))
    inputs = processor(images=image, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.get_image_features(**inputs)
        image_embedding = outputs[0].squeeze().cpu().numpy()

    try:
        cursor = db_conn.cursor()

        cursor.execute(
            "INSERT INTO image_embeddings (name, embeddings) VALUES (%s, %s::vector)", 
            (file, image_embedding.tolist())
        )
        db_conn.commit()
        print(f"{index + 1} images complete")
    except Exception as e:
        db_conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        cursor.close()

db_conn.close()
