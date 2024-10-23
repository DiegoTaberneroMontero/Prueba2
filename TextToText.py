import torch
from transformers import pipeline
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('archivo', type=str, help='Tu archivo')
args = parser.parse_args()
archivo = args.archivo
#python .\TextToText.py entrada.txt
#python .\TextToText.py .\web/Hack4Edu/file/entrada.txt
with open(archivo, 'r') as a:
    message = a.read()

#message = (
#            "Lately, I feel completely exhausted, both physically and emotionally. The job that used to excite me now feels like an insurmountable burden. Every morning, I struggle to get out of bed and face another day of endless tasks. I find it hard to concentrate and often make mistakes that I would never have made before. This fatigue has turned into a constant feeling of overwhelm, and weekends are no longer enough to recover. Additionally, I have lost interest in activities I once enjoyed and find it difficult to disconnect from work responsibilities, even when I’m at home. I feel like I’m losing control of my life and don’t know how to manage this constant stress."
#            "Últimamente, me siento completamente agotado, tanto física como emocionalmente. El trabajo que solía entusiasmarme ahora se siente como una carga insuperable. Cada mañana, lucho por levantarme de la cama y enfrentar otro día de tareas interminables. Me cuesta concentrarme y a menudo cometo errores que nunca habría cometido antes. Este cansancio se ha convertido en una sensación constante de agobio, y los fines de semana ya no son suficientes para recuperarme. Además, he perdido interés en actividades que antes disfrutaba y me resulta difícil desconectarme de las responsabilidades laborales, incluso cuando estoy en casa. Siento que estoy perdiendo el control de mi vida y no sé cómo manejar este estrés constante."
#            )


rol = (
    #"You are a professional psychologist who has the text of one of your clients and needs to summarize the client’s psychological problems in such a way that you can detect what illness they have and provide a summary of the reasoning you used to arrive at that conclusion."
    "Eres un psicólogo profesional que tiene el texto de uno de tus clientes y necesitas resumir los problemas psicológicos del cliente de tal manera que puedas detectar qué enfermedad tienen y proporcionar un resumen del razonamiento que utilizaste para llegar a esa conclusión."
    )

model_id = "meta-llama/Llama-3.2-3B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
messages = [
    {"role": "system", "content": rol},
    {"role": "user", "content": message},
]

outputs = pipe(
    messages,
    max_new_tokens=1024,
)

output_content = outputs[0]["generated_text"][-1]
cont = 0
rst = ""
for clave in output_content:
    if cont == 1:
        prueba = output_content[clave]
        rst = prueba
    cont += 1

#print(rst)

temp = "resultado_"+archivo
with open(f'D:/Clases/InteligenciaArtificial/Practicas/Prueba2/web/Hack4Edu/files/Clinica_A/Lunes/Resultados_Maria.txt', 'w') as f:
    f.write("Entrada Cliente:\n")
    f.write(message + "\n\n")
    f.write("Resultado Analisis:\n")
    f.write(rst)
