import subprocess
import os
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--log_path",type=str,help="which parameter set to give the model",default="./logs")

def create_slurm_scripts(script_name,parameter,log_path="./logs"
                        ,account="project_462000444"
                        ,cpus_per_task=1,time="00:05:00"
                        ,mem_per_cpu=100,partition='debug',
                        py_script='train_model.py',
                        flag='--parameter'):
    """Creates a slurm script in right string format

    Args:
        script_name (str): name for log files and slurm 
        lang (str): lang to dedup
        log_path (str): path where logs are saved.
        account (str): billing account Defaults to "project_462000444".
        cpus_per_task (int): n cpus. Defaults to 1.
        time (str): running time give in HH:MM:SS format. Defaults to "00:05:00".
        mem_per_cpu (int): mem per cpu in mb. Defaults to 100.
        partition (str): partition to run the scirpt. Defaults to 'small'.
    Returns:
    - str: the script
    """    
    
    script_content = f"""#!/bin/bash
#SBATCH --job-name={script_name}
#SBATCH --output={log_path}/{script_name}_%j.out
#SBATCH --error={log_path}/{script_name}_%j.err
#SBATCH --account={account}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={cpus_per_task}
#SBATCH --time={time}
#SBATCH --mem-per-cpu={mem_per_cpu}
#SBATCH --partition={partition}
echo "Script launched with SLURM parameters:"
echo "--job-name={script_name}"
echo "--output={log_path}/{script_name}_%j.out"
echo "--error={log_path}/{script_name}_%j.err"
echo "--account={account}"
echo "--cpus-per-task={cpus_per_task}"
echo "--time={time}"
echo "--mem-per-cpu={mem_per_cpu}"
echo "--partition={partition}"
echo "Script launched with program parameter:"
echo "parameter: {parameter}"
module purge
module load cray-python
srun \
    python {py_script} {flag} {parameter}
""" 

    return script_content


if __name__ == "__main__":
    args = parser.parse_args()
    something_failed = False
    dependencies = []
    if not os.path.exists(args.log_path):
        os.mkdir(args.log_path)
    for param in range(5):
        temp_file_name = f"{os.getcwd()}/slurm_job_param_{param}.sh"
        s = create_slurm_scripts(f"train_model_param_{param}",parameter=param,cpus_per_task=1,time='00:01:00',partition='small',log_path=args.log_path)
        with open(temp_file_name,"w") as temp_file:
            temp_file.write(s)
            # Submit the SLURM job using sbatch with the temporary file
        result = subprocess.run(["sbatch", temp_file_name], text=True,stdout=subprocess.PIPE)
        time.sleep(1)
        os.remove(temp_file_name)
        if result.returncode == 0:
            output = result.stdout
            print(output)
            job_id = output.split()[3]
            dependencies.append(job_id)
        else:
            print(f"Failed to run sbatch with param {param}, terminating the whole loop")
            something_failed=True
            break
    if not something_failed:
        temp_file_name = f"{os.getcwd()}/slurm_job_final.sh"
        s = create_slurm_scripts(f"use_best_model",parameter='',py_script='explain_best_model.py',flag='',cpus_per_task=1,time='00:01:00',partition='small',log_path=args.log_path)
        with open(temp_file_name,"w") as temp_file:
            temp_file.write(s)
            # Submit the SLURM job using sbatch with the temporary file
        result = subprocess.run(["sbatch",f"--dependency=afterok:{':'.join(dependencies)}", temp_file_name],text=True,stdout=subprocess.PIPE)
        print("Submitting a dependency job")
        print(result)
        time.sleep(1) 
        os.remove(temp_file_name)
