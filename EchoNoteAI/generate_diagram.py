import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_design_diagram():
    fig, ax = plt.subplots(figsize=(10, 14))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')

    # Define steps
    steps = [
        {"text": "🚀 START\nLaunch EchoNote AI", "pos": (5, 13), "color": "#E3F2FD"},
        {"text": "🔴 USER ACTION\nClick 'Start Listening'", "pos": (5, 11.5), "color": "#FFF3E0"},
        {"text": "🎤 ENGINE: processor.listen()\nCaptures Audio Segments", "pos": (5, 10), "color": "#F1F8E9"},
        {"text": "☁️ GOOGLE STT\nAudio -> Raw Text", "pos": (5, 8.5), "color": "#F3E5F5"},
        {"text": "⏹️ USER ACTION\nClick 'Stop Listening'", "pos": (5, 7), "color": "#FFEBEE"},
        {"text": "🧠 AI BRAIN: Gemini 1.5\nSummarize & Format", "pos": (5, 5.5), "color": "#E0F2F1"},
        {"text": "💾 OUTPUT\nSave .md Note", "pos": (5, 4), "color": "#FFFDE7"},
        {"text": "📄 UI DISPLAY\nUpdate History Sidebar", "pos": (5, 2.5), "color": "#F5F5F5"}
    ]

    # Draw Boxes and Arrows
    for i, step in enumerate(steps):
        # Draw Box
        box = patches.FancyBboxPatch(
            (step["pos"][0]-2, step["pos"][1]-0.5), 4, 1,
            boxstyle="round,pad=0.2", linewidth=2, edgecolor="#333333", facecolor=step["color"]
        )
        ax.add_patch(box)
        
        # Add Text
        ax.text(step["pos"][0], step["pos"][1], step["text"], 
                ha='center', va='center', fontweight='bold', fontsize=11, wrap=True)

        # Draw Arrow to next step
        if i < len(steps) - 1:
            ax.annotate('', xy=(step["pos"][0], steps[i+1]["pos"][1]+0.7), 
                        xytext=(step["pos"][0], step["pos"][1]-0.7),
                        arrowprops=dict(arrowstyle='->', lw=2, color='#333333'))

    # Draw Loop Arrow for Listening
    loop_arrow = patches.ConnectionPatch(
        xyA=(7.2, 8.5), xyB=(7.2, 10), 
        coordsA="data", coordsB="data",
        arrowstyle="-|>", connectionstyle="arc3,rad=-0.8", 
        lw=2, color="#2e7bcf"
    )
    ax.add_patch(loop_arrow)
    ax.text(8.8, 9.25, "LOOP: Keep\nListening", fontsize=9, color="#2e7bcf", fontweight='bold')

    plt.title("EchoNote AI: System Design Flow", fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('EchoNoteAI_DesignFlow.png', dpi=300, bbox_inches='tight')
    print("EchoNoteAI_DesignFlow.png has been created successfully!")

if __name__ == "__main__":
    create_design_diagram()
