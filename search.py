import os
import torch
from transformers import CLIPProcessor, CLIPModel
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

try:
    while True:
        print("> ", end="")

        text = input()
        inputs = processor(text=text, return_tensors="pt", padding=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model.get_text_features(**inputs)
            text_embedding = outputs[0].squeeze().cpu().numpy()

        QUERY = """
            SELECT name, embeddings <=> %s::vector AS cosine_distance
            FROM image_embeddings
            ORDER BY cosine_distance ASC
            LIMIT 10;
        """
        cursor = db_conn.cursor()

        cursor.execute(QUERY, (text_embedding.tolist(),))
        results = cursor.fetchall()

        print("Matching images (ordered by cosine similarity):")
        for name, cosine_distance in results:
            print(f"Name: {name}, Cosine Distance: {cosine_distance}")

        cursor.close()
except KeyboardInterrupt:
    db_conn.close()
