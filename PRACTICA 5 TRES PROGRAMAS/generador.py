import pandas as pd

# Cargar el archivo Excel
def load_excel(file_path):
    return pd.read_excel(file_path)

# Generar el código LaTeX con soporte para símbolos Unicode
def generate_latex_code(data):
    latex_code = data.to_latex(index=False, escape=False)
    # Reemplazar caracteres Unicode por sus equivalentes en LaTeX
    unicode_map = {
        'α': r'\alpha', 'β': r'\beta', 'γ': r'\gamma', 'ε': r'\varepsilon', 
        'ζ': r'\zeta', 'η': r'\eta', 'θ': r'\theta', 'ι': r'\iota', 
        'κ': r'\kappa', 'λ': r'\lambda', 'μ': r'\mu', 'ν': r'\nu', 
        '∅': r'\emptyset'
    }
    for unicode_char, latex_char in unicode_map.items():
        latex_code = latex_code.replace(unicode_char, latex_char)
    return latex_code

# Guardar el código LaTeX en un archivo con codificación utf-8
def save_latex_file(latex_code, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex_code)

# Ruta del archivo de entrada
input_file = 'TablaAutomata.xlsx'
output_file = 'tabla_latex_con_simbolos.tex'

# Ejecutar el proceso
if __name__ == "__main__":
    # Cargar datos
    data = load_excel(input_file)
    
    # Generar código LaTeX
    latex_code = generate_latex_code(data)
    
    # Guardar en archivo
    save_latex_file(latex_code, output_file)
    print(f"Archivo LaTeX generado y guardado en: {output_file}")