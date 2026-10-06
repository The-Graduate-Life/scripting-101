#!/usr/bin/env bash
#SBATCH --job-name=sensor_qc          # name shown in the queue
#SBATCH --output=logs/%x_%j.out       # %x = job name, %j = job ID
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=01:00:00               # wall-time limit (hh:mm:ss): the job is killed after this
#SBATCH --cpus-per-task=8             # CPU cores for this job
#SBATCH --mem=8G                      # RAM for this job
#SBATCH --partition=standard          # queue name: ask your HPC support team

# sensor_qc.sbatch — run the Lab 04 pipeline on a SLURM cluster.
# Submit with:  sbatch slurm_job.sbatch     Check with:  squeue -u $USER     Cancel: scancel JOBID
set -euo pipefail

module load miniforge 2> /dev/null || true        # many clusters provide conda via "modules"
eval "$(conda shell.bash hook)"
conda activate scripting101

echo "job $SLURM_JOB_ID on $(hostname) with $SLURM_CPUS_PER_TASK CPUs, started $(date)"

# Use exactly the CPUs the scheduler gave you, never $(nproc) on a shared node
./sensor_pipeline.sh -i "$HOME/scripting-101/datasets/sensors" \
                     -o "results/sensor_qc_$SLURM_JOB_ID" \
                     -j "$SLURM_CPUS_PER_TASK"

echo "finished $(date)"
