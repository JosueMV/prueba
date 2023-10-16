import subprocess
import os
import pandas as pd

nombre_repo = "Laboratorio2_2Sem23/laboratorio-2-grupo8"
ruta_gem5 = "/home/arqui/lab2/gem5"

values_to_check = [
    # Miss rate for overall accesses (Ratio)
    'system.cpu.icache.overallMissRate::cpu.inst',
    'system.cpu.dcache.overallMissRate::cpu.data',
    'system.l2cache.overallMissRate::total',

    # Number of overall hits (Count)
    'system.cpu.dcache.overallHits::cpu.data',
    'system.cpu.icache.overallHits::cpu.inst',
    'system.l2cache.overallHits::total',

    # Number of instructions simulated (Count)
    'simInsts',

    # Number of ops (including micro ops) simulated (Count)
    'simOps',

    # CPI: cycles per instruction (core level) ((Cycle/Count)
    'system.cpu.cpi',

    # IPC: instructions per cycle (core level) ((Count/Cycle))
    'system.cpu.ipc',

    # Number of cpu cycles simulated (Cycle)
    'system.cpu.numCycles',

    # Number of overall misses (Count)
    'system.cpu.icache.overallMisses::cpu.inst',
    'system.l2cache.overallMisses::cpu.inst',
    'system.l2cache.overallMisses::cpu.data',
    'system.l2cache.overallMisses::total',
    'system.cpu.dcache.overallMisses::cpu.data',
]

def run_simulation(binary, l1i_size, l1i_assoc, l1d_size, l1d_assoc, l2_size, l2_assoc, cache_line_size, l1i_rp, l1d_rp, l2_rp):
    # Print the configuration being used
    print(f"Running simulation with configuration: binary={binary}, l1i_size={l1i_size}, l1i_assoc={l1i_assoc}, l1d_size={l1d_size}, l1d_assoc={l1d_assoc}, l2_size={l2_size}, l2_assoc={l2_assoc}, cache_line_size={cache_line_size}, l1i_rp={l1i_rp}, l1d_rp={l1d_rp}, l2_rp={l2_rp}")

    # Define the command as a list of strings
    cmd = [
        f"{ruta_gem5}/build/X86/gem5.opt",
        f"{ruta_gem5}/configs/learning_gem5/part1/two_level.py",
        f"--binary={binary}",
        f"--l1i_size={l1i_size}",
        f"--l1i_assoc={l1i_assoc}",
        f"--l1d_size={l1d_size}",
        f"--l1d_assoc={l1d_assoc}",
        f"--l2_size={l2_size}",
        f"--l2_assoc={l2_assoc}",
        f"--cache_line_size={cache_line_size}",
        f"--l1i_rp={l1i_rp}",
        f"--l1d_rp={l1d_rp}",
        f"--l2_rp={l2_rp}"
    ]

    # Run the command
    subprocess.run(cmd)

    # Parse the stats.txt file and store results in a dictionary
    results = {"binary": binary, "l1i_size": l1i_size, "l1i_assoc": l1i_assoc, "l1d_size": l1d_size, "l1d_assoc": l1d_assoc, "l2_size": l2_size, "l2_assoc": l2_assoc, "cache_line_size": cache_line_size, "l1i_rp": l1i_rp, "l1d_rp": l1d_rp, "l2_rp": l2_rp}
    with open('m5out/stats.txt', 'r') as f:
        lines = f.readlines()
        for line in lines[1:-2]:
            name, value, *_ = line.split()
            if name in values_to_check:
                results[name] = value
                print(f'{name} has value {value}')  # Print the resulting value

    return results

# List of configurations
cache_configs = [
  
    
    {
        "binary": f"/home/arqui/lab2/Laboratorio2_2Sem23/laboratorio-2-grupo8/gem5/Part1_optimizations/Tiling_OP-O0",
        "l1i_size": '16kB',
        "l1i_assoc": 2,
        "l1d_size": '64kB',
        "l1d_assoc": 2,
        "l2_size": '256kB',
        "l2_assoc": 8,
        "cache_line_size": '64',
        "l1i_rp": 'FIFO',
        "l1d_rp": 'FIFO',
        "l2_rp": 'FIFO'
    },
    
    {
        "binary": f"/home/arqui/lab2/Laboratorio2_2Sem23/laboratorio-2-grupo8/gem5/Part1_optimizations/Tiling_OP-O1",
        "l1i_size": '16kB',
        "l1i_assoc": 2,
        "l1d_size": '64kB',
        "l1d_assoc": 2,
        "l2_size": '256kB',
        "l2_assoc": 8,
        "cache_line_size": '64',
        "l1i_rp": 'FIFO',
        "l1d_rp": 'FIFO',
        "l2_rp": 'FIFO'
    },
    
    {
        "binary": f"/home/arqui/lab2/Laboratorio2_2Sem23/laboratorio-2-grupo8/gem5/Part1_optimizations/Tiling_OP-O2",
        "l1i_size": '16kB',
        "l1i_assoc": 2,
        "l1d_size": '64kB',
        "l1d_assoc": 2,
        "l2_size": '256kB',
        "l2_assoc": 8,
        "cache_line_size": '64',
        "l1i_rp": 'FIFO',
        "l1d_rp": 'FIFO',
        "l2_rp": 'FIFO'
    },
    
    {
        "binary": f"/home/arqui/lab2/Laboratorio2_2Sem23/laboratorio-2-grupo8/gem5/Part1_optimizations/Tiling_OP-O3",
        "l1i_size": '16kB',
        "l1i_assoc": 2,
        "l1d_size": '64kB',
        "l1d_assoc": 2,
        "l2_size": '256kB',
        "l2_assoc": 8,
        "cache_line_size": '64',
        "l1i_rp": 'FIFO',
        "l1d_rp": 'FIFO',
        "l2_rp": 'FIFO'
    },
]

# Initialize an empty DataFrame to store all results
df = pd.DataFrame()

# Run simulations for each binary and each cache configuration
for i, config in enumerate(cache_configs):
    result = run_simulation(**config)
    result['experiment'] = i + 1  # Add an experiment identifier
    df = pd.concat([df, pd.DataFrame([result])], ignore_index=True)

# Save the DataFrame to a CSV file
df.to_csv(f'/home/arqui/lab2/{nombre_repo}/gem5/Part1_optimizations/Sim_Res_Opt.csv', index=False)

