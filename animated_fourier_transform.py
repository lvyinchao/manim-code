# -*- coding: utf-8 -*-
"""
Animated Fourier Transform Visualization
This script creates an animation showing how the Fourier transform works by visualizing
the decomposition of a signal into its frequency components.
"""

from manim import *
import numpy as np

class AnimatedFourierTransform(Scene):
    def construct(self):
        # Set default font
        Text.set_default(font="SimSun")
        
        # Title
        title = Text("傅里叶变换动态演示").scale(0.8)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)
        
        # Create time domain axes
        time_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            axis_config={"include_tip": True},
            x_length=6,
            y_length=4
        )
        time_axes.to_edge(LEFT, buff=1)
        time_axes.shift(DOWN * 0.5)
        
        time_label = Text("时域", font="SimSun").scale(0.5)
        time_label.next_to(time_axes, UP, buff=0.2)
        
        # Create frequency domain axes
        freq_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            axis_config={"include_tip": True},
            x_length=6,
            y_length=4
        )
        freq_axes.to_edge(RIGHT, buff=1)
        freq_axes.shift(DOWN * 0.5)
        
        freq_label = Text("频域", font="SimSun").scale(0.5)
        freq_label.next_to(freq_axes, UP, buff=0.2)
        
        # Show axes
        self.play(
            Create(time_axes),
            Create(freq_axes),
            Write(time_label),
            Write(freq_label)
        )
        self.wait(1)
        
        # Define a composite signal: sum of sine waves
        def composite_signal(t):
            # A combination of sine waves with different frequencies and amplitudes
            return (
                0.5 * np.sin(1 * t) +  # Fundamental frequency
                0.3 * np.sin(3 * t) +  # 3rd harmonic
                0.2 * np.sin(5 * t)    # 5th harmonic
            )
        
        # Plot the time domain signal
        time_graph = time_axes.plot(
            composite_signal,
            color=BLUE,
            x_range=[-3, 3, 0.01]
        )
        
        time_graph_label = Text("复合信号", font="SimSun", color=BLUE).scale(0.5)
        time_graph_label.next_to(time_graph, UP, buff=0.1)
        
        self.play(
            Create(time_graph),
            Write(time_graph_label)
        )
        self.wait(1)
        
        # Show how Fourier transform works by displaying individual components
        components_title = Text("傅里叶分解", font="SimSun").scale(0.6)
        components_title.to_corner(UL, buff=1)
        self.play(Write(components_title))
        
        # Individual components
        frequencies = [1, 3, 5]
        amplitudes = [0.5, 0.3, 0.2]
        colors = [RED, GREEN, YELLOW]
        
        # Show each component separately
        component_formulas = VGroup()
        for i, (freq, amp, color) in enumerate(zip(frequencies, amplitudes, colors)):
            formula = MathTex(
                f"f_{i+1}(t) = {amp}\\sin({freq}t)",
                color=color
            ).scale(0.6)
            component_formulas.add(formula)
        
        component_formulas.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        component_formulas.to_corner(UL, buff=1.5)
        component_formulas.shift(RIGHT * 1.5)
        
        # Animate each component
        component_graphs = []
        for i, (freq, amp, color) in enumerate(zip(frequencies, amplitudes, colors)):
            # Show formula
            self.play(Write(component_formulas[i]))
            
            # Plot component
            component_func = lambda t, amp=amp, freq=freq: amp * np.sin(freq * t)
            component_graph = time_axes.plot(
                component_func,
                color=color,
                x_range=[-3, 3, 0.01]
            )
            component_graphs.append(component_graph)
            
            self.play(Create(component_graph))
            self.wait(0.5)
        
        # Show reconstruction
        reconstruction_text = Text("信号重建", font="SimSun", color=ORANGE).scale(0.6)
        reconstruction_text.next_to(component_formulas, DOWN, buff=0.5)
        self.play(Write(reconstruction_text))
        
        # Show the sum
        sum_formula = MathTex(
            "f(t) = \\sum_{n=1,3,5} a_n \\sin(n t)",
            color=ORANGE
        ).scale(0.6)
        sum_formula.next_to(reconstruction_text, DOWN, buff=0.2)
        self.play(Write(sum_formula))
        self.wait(2)
        
        # Move to frequency domain visualization
        freq_domain_title = Text("频域表示", font="SimSun").scale(0.6)
        freq_domain_title.to_corner(UR, buff=1)
        self.play(Write(freq_domain_title))
        
        # Create frequency domain representation (spectrum)
        def frequency_spectrum(f):
            # Simple representation of frequency spectrum
            if f in frequencies:
                idx = frequencies.index(f)
                return amplitudes[idx]
            return 0
        
        # Draw spectrum as sticks
        spectrum_bars = VGroup()
        for freq, amp in zip(frequencies, amplitudes):
            bar = freq_axes.get_vertical_line(
                freq_axes.c2p(freq, amp),
                line_config={"color": BLUE}
            )
            spectrum_bars.add(bar)
            
            # Negative frequencies
            neg_bar = freq_axes.get_vertical_line(
                freq_axes.c2p(-freq, amp),
                line_config={"color": BLUE}
            )
            spectrum_bars.add(neg_bar)
        
        # Zero frequency component
        dc_component = DashedLine(
            freq_axes.c2p(0, 0),
            freq_axes.c2p(0, 0),
            color=GRAY
        )
        spectrum_bars.add(dc_component)
        
        self.play(Create(spectrum_bars))
        self.wait(2)
        
        # Show frequency points
        freq_points = VGroup()
        for freq, amp in zip(frequencies, amplitudes):
            # Positive frequencies
            pos_dot = Dot(freq_axes.c2p(freq, amp), color=YELLOW)
            freq_points.add(pos_dot)
            
            # Negative frequencies
            neg_dot = Dot(freq_axes.c2p(-freq, amp), color=YELLOW)
            freq_points.add(neg_dot)
        
        self.play(Create(freq_points))
        self.wait(1)
        
        # Label frequencies
        freq_labels = VGroup()
        for freq in frequencies:
            pos_label = MathTex(f"{freq}", color=YELLOW).scale(0.5)
            pos_label.next_to(freq_axes.c2p(freq, 0), DOWN, buff=0.1)
            freq_labels.add(pos_label)
            
            neg_label = MathTex(f"{-freq}", color=YELLOW).scale(0.5)
            neg_label.next_to(freq_axes.c2p(-freq, 0), DOWN, buff=0.1)
            freq_labels.add(neg_label)
        
        self.play(Write(freq_labels))
        self.wait(2)
        
        # Final explanation
        explanation = Text(
            "傅里叶变换将时域信号转换为频域表示，显示信号的频率成分",
            font="SimSun"
        ).scale(0.5)
        explanation.to_edge(DOWN, buff=0.5)
        self.play(Write(explanation))
        self.wait(3)

# Animated visualization of Fourier series approximation
class FourierSeriesAnimation(Scene):
    def construct(self):
        # Set default font
        Text.set_default(font="SimSun")
        
        # Title
        title = Text("傅里叶级数动态逼近").scale(0.8)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(1)
        
        # Create axes
        axes = Axes(
            x_range=[-2*PI, 2*PI, PI/2],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"include_tip": True},
            x_length=10,
            y_length=6
        )
        
        # Add axis labels
        x_label = Text("x").scale(0.6)
        y_label = Text("y").scale(0.6)
        x_label.next_to(axes.x_axis, RIGHT)
        y_label.next_to(axes.y_axis, UP)
        
        axes_group = VGroup(axes, x_label, y_label)
        self.play(Create(axes_group))
        
        # Define square wave function
        def square_wave(x):
            return np.where((x % (2*PI)) < PI, 1, -1)
        
        # Plot original square wave
        original = axes.plot(
            square_wave,
            color=BLUE,
            x_range=[-2*PI, 2*PI, 0.01]
        )
        original_label = Text("方波", font="SimSun", color=BLUE).scale(0.5)
        original_label.next_to(axes.c2p(PI/2, 1), UP, buff=0.2)
        
        self.play(
            Create(original),
            Write(original_label)
        )
        self.wait(1)
        
        # Function to compute Fourier series approximation
        def fourier_approx(x, n_terms):
            result = 0
            for n in range(1, n_terms*2, 2):  # Only odd terms
                result += (4 / (n * PI)) * np.sin(n * x)
            return result
        
        # Animate the approximation with increasing terms
        colors = [RED, GREEN, YELLOW, PURPLE, ORANGE, MAROON]
        prev_approx = None
        
        for i, n_terms in enumerate([1, 2, 3, 5, 10, 20]):
            approx = axes.plot(
                lambda x: fourier_approx(x, n_terms),
                color=colors[i],
                x_range=[-2*PI, 2*PI, 0.01]
            )
            
            approx_label = MathTex(f"n={n_terms*2-1}", color=colors[i]).scale(0.5)
            approx_label.next_to(axes.c2p(PI, fourier_approx(PI, n_terms)), UP, buff=0.2)
            
            if prev_approx is None:
                self.play(
                    Create(approx),
                    Write(approx_label)
                )
            else:
                self.play(
                    ReplacementTransform(prev_approx, approx),
                    ReplacementTransform(prev_label, approx_label)
                )
            
            prev_approx = approx
            prev_label = approx_label
            self.wait(1)
        
        # Final explanation
        explanation = Text(
            "随着项数增加，傅里叶级数逼近原方波函数",
            font="SimSun"
        ).scale(0.6)
        explanation.to_edge(DOWN, buff=0.5)
        
        self.play(Write(explanation))
        self.wait(3)

def main():
    # Render the Fourier transform animation
    scene1 = AnimatedFourierTransform()
    scene1.render()
    
    # Render the Fourier series animation
    scene2 = FourierSeriesAnimation()
    scene2.render()

if __name__ == "__main__":
    main()