import matplotlib.pyplot as plt

plt.rcParams["mathtext.fontset"] = "cm"

def render_equation(latex_str, filename, fontsize=26, color="#166534", figsize=(6, 1.0)):
    fig = plt.figure(figsize=figsize, dpi=300)
    fig.patch.set_alpha(0.0)
    ax = fig.add_subplot(111)
    ax.patch.set_alpha(0.0)
    ax.axis("off")
    ax.text(0.5, 0.5, f"${latex_str}$", fontsize=fontsize, ha="center", va="center", color=color)
    plt.savefig(filename, bbox_inches="tight", transparent=True, pad_inches=0.04)
    plt.close(fig)
    print(f"Created: {filename}")

if __name__ == "__main__":
    render_equation(r"T_p = T_f + H \cdot \max(0,\, r)", "E:/Client/Transformer_CBM/PPT/equation_projection.png", fontsize=28, color="#166534", figsize=(6, 1.0))
    render_equation(r"r = \frac{\sum_{i=1}^N (t_i - \bar{t})(T_{f,i} - \bar{T}_f)}{\sum_{i=1}^N (t_i - \bar{t})^2}", "E:/Client/Transformer_CBM/PPT/equation_ols.png", fontsize=24, color="#111827", figsize=(6, 1.2))
