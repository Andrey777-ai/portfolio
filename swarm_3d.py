import os
import re
import random
import numpy as np
import plotly.graph_objects as go

def build_3d_swarm():
    search_dir = os.path.expanduser("~/Рабочий стол/extracted_code")
    
    # Гибкие маркеры "ДНК"
    dna_patterns = [
        r"PHI\s*=\s*1\.618", r"phi\s*=\s*1\.618",
        r"LAMBDA0", r"lambda0", r"lambda\s*=\s*0\.552",
        r"Абсолют", r"абсолют", r"Фрактал", r"фрактал",
        r"Z\s*=\s*.*sqrt", r"Z\s*=\s*.*j",
        r"0\.5527", r"γ\s*=\s*7", r"gamma\s*=\s*7"
    ]

    print("🔍 Сканирую базу знаний...")
    sessions = []
    if os.path.exists(search_dir):
        for folder in os.listdir(search_dir):
            if os.path.isdir(os.path.join(search_dir, folder)):
                sessions.append(folder)

    # Берем до 80 сессий для красоты
    random.shuffle(sessions)
    sessions = sessions[:80] 

    nodes_x, nodes_y, nodes_z = [], [], []
    node_colors, node_texts, node_sizes = [], [], []

    print(f"🧬 Анализирую {len(sessions)} узлов...")

    for session in sessions:
        folder_path = os.path.join(search_dir, session)
        has_dna = False
        
        for file in os.listdir(folder_path):
            if file.endswith(('.py', '.txt', '.md')):
                try:
                    with open(os.path.join(folder_path, file), 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if any(re.search(pattern, content, re.IGNORECASE) for pattern in dna_patterns):
                            has_dna = True
                            break
                except:
                    pass
        
        # Генерируем случайные 3D-координаты (в форме сферы/облака)
        nodes_x.append(random.uniform(-10, 10))
        nodes_y.append(random.uniform(-10, 10))
        nodes_z.append(random.uniform(-10, 10))
        
        node_colors.append('#ff0055' if has_dna else '#58a6ff')
        node_sizes.append(12 if has_dna else 6)
        node_texts.append(session)

    # --- СОЗДАЕМ СВЯЗИ (ЛИНИИ) ---
    edge_x, edge_y, edge_z = [], [], []
    for i in range(len(nodes_x)):
        # Связываем каждый узел с 3 случайными соседями
        for _ in range(3):
            j = random.randint(0, len(nodes_x) - 1)
            if i != j:
                edge_x.extend([nodes_x[i], nodes_x[j], None])
                edge_y.extend([nodes_y[i], nodes_y[j], None])
                edge_z.extend([nodes_z[i], nodes_z[j], None])

    # --- ОТРИСОВКА PLOTLY ---
    fig = go.Figure()

    # Добавляем линии связей
    fig.add_trace(go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='#30363d', width=1),
        hoverinfo='none'
    ))

    # Добавляем сами узлы (точки)
    fig.add_trace(go.Scatter3d(
        x=nodes_x, y=nodes_y, z=nodes_z,
        mode='markers',
        marker=dict(
            size=node_sizes,
            color=node_colors,
            opacity=0.9,
            line=dict(color='white', width=1)
        ),
        text=node_texts, # При наведении мыши будет видно название сессии
        hoverinfo='text'
    ))

    # Настраиваем 3D-сцену
    fig.update_layout(
        title="3D Фрактальный Рой Z-Network (Анализ ДНК)",
        title_font=dict(size=20, color='white'),
        paper_bgcolor='#0d1117',
        scene=dict(
            xaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
            zaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
            bgcolor='#0d1117'
        ),
        showlegend=False,
        margin=dict(l=0, r=0, b=0, t=50)
    )

    # Сохраняем в HTML
    output_file = os.path.expanduser("~/Z-Network/swarm_3d.html")
    fig.write_html(output_file)
    print(f"💾 3D-граф сохранен в файл: {output_file}")
    print("👉 Открой этот файл в Firefox, чтобы покрутить граф!")

if __name__ == "__main__":
    build_3d_swarm()
