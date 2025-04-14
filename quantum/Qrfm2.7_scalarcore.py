# QRFM v2.7 — Convergence Metrics, Amplitudes, Phase Analysis & Ancestry Visualization Upgrade
import math
import random
from typing import List, Dict, Union
import matplotlib.pyplot as plt
import networkx as nx
from numpy import dot, array
from numpy.linalg import norm
import scalarcore as sc  # 🔗 Symbolic math and scalar resonance

class ResonanceField:
    def __init__(self, name: str, base_freq: float, harmonics: List[float] = None,
                 amplitudes: List[float] = None, phase_shift: float = 0,
                 tags: Dict[str, Union[str, bool]] = None):
        self.name = name
        self.base_freq = base_freq
        self.harmonics = harmonics if harmonics else []
        self.amplitudes = amplitudes if amplitudes else [1.0 for _ in ([1] + self.harmonics)]
        self.phase_shift = phase_shift
        self.tags = tags if tags else {}
        self.scalar_aligned = sc.is_resonant_scalar(base_freq, tol=1e-2)  # Optional tighter check

    def spectrum(self, cycles: int = 1) -> List[float]:
        return sorted(set(round(self.base_freq * h * c, 4)
                          for c in range(1, cycles + 1)
                          for h in ([1] + self.harmonics)))

    def weighted_spectrum(self) -> List[tuple]:
        return [(round(self.base_freq * h, 4), a)
                for h, a in zip(([1] + self.harmonics), self.amplitudes)]

    def interfere(self, other: 'ResonanceField', cycles: int = 10) -> Dict[str, Union[str, float, List[float]]]:
        self_spec = self.spectrum(cycles)
        other_spec = other.spectrum(cycles)
        convergence = sorted(set(self_spec).intersection(set(other_spec)))
        convergence_ratio = len(convergence) / len(set(self_spec + other_spec))
        phase_diff = abs(self.phase_shift - other.phase_shift)
        return {
            "interaction": f"{self.name} + {other.name}",
            "convergent_frequencies": convergence,
            "convergence_ratio": round(convergence_ratio, 4),
            "phase_difference": round(phase_diff, 4)
        }

    def ancestry_similarity(self, other: 'ResonanceField') -> float:
        a = array([1] + self.harmonics)
        b = array([1] + other.harmonics)
        max_len = max(len(a), len(b))
        a = array(list(a) + [0]*(max_len - len(a)))
        b = array(list(b) + [0]*(max_len - len(b)))
        return round(dot(a, b) / (norm(a) * norm(b)), 4)

    def describe(self) -> Dict[str, Union[str, float, List[float]]]:
        return {
            "field": self.name,
            "base_frequency": self.base_freq,
            "harmonics": self.harmonics,
            "amplitudes": self.amplitudes,
            "spectrum": self.spectrum(),
            "phase_shift": self.phase_shift,
            "scalar_aligned": self.scalar_aligned,
            "tags": self.tags
        }

    def plot_spectrum(self, logscale: bool = False):
        spectrum = self.weighted_spectrum()
        x = list(range(len(spectrum)))
        y = [f for f, _ in spectrum]
        amp = [a for _, a in spectrum]
        labels = ["Base"] + [f"H{i+1}" for i in range(len(spectrum) - 1)]

        plt.figure(figsize=(10, 4))
        markerline, stemlines, baseline = plt.stem(x, y, basefmt=" ", linefmt='b-', markerfmt='bo')
        plt.setp(markerline, markersize=5)

        if hasattr(stemlines, 'set_linewidths'):
            stemlines.set_linewidths([a * 2 for a in amp])

        plt.xticks(x, labels, rotation=45)
        plt.title(f"Spectrum of {self.name} (Amplitude Scaled)")
        plt.xlabel("Harmonic Mode")
        plt.ylabel("Frequency (Hz)")
        if logscale:
            plt.yscale('log')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.show()


def plot_ancestry_tree(fields: List[ResonanceField], threshold: float = 0.8):
    G = nx.Graph()
    labels = {}
    node_colors = {
        f.name: (0.2, 0.8, 0.3) if f.scalar_aligned else (random.random(), random.random(), random.random())
        for f in fields
    }

    for field in fields:
        label = field.name + ("*" if field.scalar_aligned else "")
        G.add_node(label)

    for i in range(len(fields)):
        for j in range(i + 1, len(fields)):
            score = fields[i].ancestry_similarity(fields[j])
            if score >= threshold:
                n1 = fields[i].name + ("*" if fields[i].scalar_aligned else "")
                n2 = fields[j].name + ("*" if fields[j].scalar_aligned else "")
                G.add_edge(n1, n2, weight=score)
                labels[(n1, n2)] = str(score)

    pos = nx.spring_layout(G, seed=42, k=1.75)
    plt.figure(figsize=(14, 10))
    nx.draw(G, pos, with_labels=True, node_color=[node_colors[n.replace("*","")] for n in G.nodes()],
            edge_color='gray', node_size=2500, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
    plt.title("Harmonic Ancestry Tree of Resonant Fields (Scalar-Aligned)", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# === Field Map ===
resonance_map = sorted([
    ResonanceField("Photon Field", 3e8, [1.5, 2, 4], phase_shift=0.0, tags={"massless": True, "mediator": "EM"}),
    ResonanceField("Graviton Field", 1e35, [0.25, 0.5, 1.5], phase_shift=0.05, tags={"massless": True, "mediator": "gravity", "hypothetical": True}),
    ResonanceField("Neutrino Echo Field", 5.1e12, [2, 7, 11], phase_shift=1.2, tags={"weak_interaction": True, "near_massless": True}),
    ResonanceField("Tau Field", 2.7e13, [1.1, 3.3, 5.1], phase_shift=0.7, tags={"lepton": True, "massive": True}),
    ResonanceField("Muon Field", 1.88e14, [1.2, 2.8, 3.5], phase_shift=0.6, tags={"lepton": True, "massive": True}),
    ResonanceField("Electron Field", 1.42e15, [2, 3, 5], phase_shift=0.1, tags={"charge": -1, "massive": True}),
    ResonanceField("Gluon Field", 5e17, [1, 2, 3], phase_shift=0.15, tags={"massless": True, "mediator": "strong", "color_charge": True}),
    ResonanceField("Quark Triplet Field", 8.12e20, [0.5, 2, 3.5], phase_shift=0.3, tags={"confinement": True, "color_charge": True}),
    ResonanceField("Proton Field", 2.27e23, [1.5, 2, 4], phase_shift=0.2, tags={"baryon": True, "charge": +1, "massive": True}),
    ResonanceField("Neutron Field", 2.27e23, [1.3, 2.1, 3.7], phase_shift=0.2, tags={"baryon": True, "neutral": True, "massive": True}),
], key=lambda f: f.base_freq)

# === Run ===
if __name__ == '__main__':
    print("\n=== QRFM Unified Ancestry & Spectrum System (v2.7 Scalar Aligned) ===")
    for field in resonance_map:
        print(field.describe())
        field.plot_spectrum(logscale=False)

    print("\n=== Generating Harmonic Ancestry Tree ===")
    plot_ancestry_tree(resonance_map, threshold=0.85)


