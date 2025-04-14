import numpy as np
import pandas as pd
import scalarcore as sc  # 🔗 Scalar constants and tools


def binary_to_decimal(binary_str, bit_size):
    return int(binary_str, 2) % (2 ** bit_size)


def factorize_and_analyze(file_paths):
    results = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            raw_data = file.read()

        bitstrings = raw_data.split()  # Assuming whitespace-separated bitstrings
        analysis = []

        for bitstring in bitstrings:
            bitstring = bitstring.strip()
            if len(bitstring) < 35:
                continue  # Ignore corrupted entries

            # Primary factorization using 5-bit and 7-bit splits
            five_bit_split = [bitstring[i:i+5] for i in range(0, len(bitstring), 5)]
            seven_bit_split = [bitstring[i:i+7] for i in range(0, len(bitstring), 7)]

            # Convert to decimal values
            decimal_5bit = [binary_to_decimal(b, 5) for b in five_bit_split if len(b) == 5]
            decimal_7bit = [binary_to_decimal(b, 7) for b in seven_bit_split if len(b) == 7]

            # Multi-bit conversions
            decimal_2bit = binary_to_decimal(bitstring, 2)
            decimal_3bit = binary_to_decimal(bitstring, 3)
            decimal_4bit = binary_to_decimal(bitstring, 4)
            decimal_5bit_full = binary_to_decimal(bitstring, 5)
            decimal_7bit_full = binary_to_decimal(bitstring, 7)
            decimal_8bit = binary_to_decimal(bitstring, 8)
            decimal_11bit = binary_to_decimal(bitstring, 11)
            decimal_13bit = binary_to_decimal(bitstring, 13)

            sum_5 = sum(decimal_5bit)
            sum_7 = sum(decimal_7bit)

            # Optional: Scalar alignment check on 5-bit and 7-bit sums
            resonant_5 = sc.is_resonant_scalar(sum_5)
            resonant_7 = sc.is_resonant_scalar(sum_7)

            analysis.append([
                decimal_2bit, decimal_3bit, decimal_4bit, decimal_5bit_full,
                decimal_7bit_full, decimal_8bit, decimal_11bit, decimal_13bit,
                sum_5, sum_7, resonant_5, resonant_7
            ])

        df = pd.DataFrame(analysis, columns=[
            "2-bit", "3-bit", "4-bit", "5-bit", "7-bit", "8-bit", "11-bit", "13-bit",
            "5-bit Sum", "7-bit Sum", "Resonant_5", "Resonant_7"
        ])
        results.append(df)

    return results


# === Example Usage ===
file_paths = [
    "qjit_results_ibm_run_1.txt",
    "qjit_results_ibm_run_2.txt",
    "qjit_results_ibm_run_3.txt"
]
analysis_results = factorize_and_analyze(file_paths)

# Display results
total_results = pd.concat(analysis_results, ignore_index=True)
import ace_tools as tools
tools.display_dataframe_to_user("Quantum Data Analysis (Scalar-Tagged)", total_results)
