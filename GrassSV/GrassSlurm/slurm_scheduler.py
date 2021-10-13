#!/usr/local/bin/python

import shlex
from subprocess import Popen, PIPE
import os, shutil
from enum import Enum, IntEnum

class GenMutEnums(Enum):
    NONE = 0
    DUP = 1
    DEL = 2
    TRA = 3
    INS = 4
    INV = 5
    ALL = 6

class Task_UID(IntEnum):
    GEN_MUTATION = 0
    RUN_ART = 1
    CALC_DEPTH = 2
    EXTRACT_READS = 3
    RUN_GRASS = 4
    RUN_QUAST = 5
    RUN_ALGA = 6
    RUN_QUAST_ALGA = 7
    NONE = 8

    @staticmethod
    def GetSize() -> int:
        return Task_UID.NONE

class Task_Info:
    _JOB_NAMES = {
        Task_UID.GEN_MUTATION   : "gen_mutation",
        Task_UID.RUN_ART        : "run_art",
        Task_UID.CALC_DEPTH     : "calculate_depth",
        Task_UID.EXTRACT_READS  : "extract_reads",
        Task_UID.RUN_GRASS      : "run_grasshopper",
        Task_UID.RUN_ALGA       : "run_alga",
        Task_UID.RUN_QUAST      : "run_quast",
        Task_UID.RUN_QUAST_ALGA : "run_quast_alga"
    }

    _LOG_FILES = {
        Task_UID.GEN_MUTATION   : "gen_mutation.out",
        Task_UID.RUN_ART        : "run_art.out",
        Task_UID.CALC_DEPTH     : "calculate_depth.out",
        Task_UID.EXTRACT_READS  : "extract_reads.out",
        Task_UID.RUN_GRASS      : "run_grasshopper.out",
        Task_UID.RUN_ALGA       : "run_alga.out",
        Task_UID.RUN_QUAST      : "run_quast.out",
        Task_UID.RUN_QUAST_ALGA : "run_quast_alga.out"
    }

    _ERROR_FILES = {
        Task_UID.GEN_MUTATION   : "gen_mutation.err",
        Task_UID.RUN_ART        : "run_art.err",
        Task_UID.CALC_DEPTH     : "calculate_depth.err",
        Task_UID.EXTRACT_READS  : "extract_reads.err",
        Task_UID.RUN_GRASS      : "run_grasshopper.err",
        Task_UID.RUN_ALGA       : "run_alga.err",
        Task_UID.RUN_QUAST      : "run_quast.err",
        Task_UID.RUN_QUAST_ALGA : "run_quast_alga.err",
    }

    _BASH_CMDS = { # 0 SV_TYPE # 1 MUTATION_FOLDER
        Task_UID.GEN_MUTATION   : os.path.dirname(__file__) + "/Bash/multiple.sh {0} {1}/genome.fsa temp_{0} {1}/out.bed",
        Task_UID.RUN_ART        : os.path.dirname(__file__) + "/Bash/run_art.sh {1}",
        Task_UID.CALC_DEPTH     : os.path.dirname(__file__) + "/Bash/calculate_depth.sh {1}",
        Task_UID.EXTRACT_READS  : os.path.dirname(__file__) + "/Bash/whole_pipeline.sh {1}",
        Task_UID.RUN_GRASS      : os.path.dirname(__file__) + "/Bash/whole_pipeline2.sh {1}",
        Task_UID.RUN_ALGA       : os.path.dirname(__file__) + "/Bash/whole_pipeline2_alga.sh {1}",
        Task_UID.RUN_QUAST      : os.path.dirname(__file__) + "/Bash/whole_pipeline3.sh {1} grasshopper contigs.fasta",
        Task_UID.RUN_QUAST_ALGA : os.path.dirname(__file__) + "/Bash/whole_pipeline3.sh {1} alga contigs.fasta_contigs.fasta"
    }

    @staticmethod
    def GetTaskInfo( UID : Task_UID):
        return Task_Info._JOB_NAMES[UID], Task_Info._ERROR_FILES[UID], Task_Info._LOG_FILES[UID], Task_Info._BASH_CMDS[UID] 

class Dependency_Info():
    _IS_SCHEDULED = [False] * Task_UID.GetSize()
    _DEPENDENCY_UID = [Task_UID.NONE] * Task_UID.GetSize()
    _DEPENDENCY_JID = [0] * Task_UID.GetSize()

    @staticmethod
    def SetDependencyForUID(UID : Task_UID, DEPENDENCY_UID : int) -> None:
        Dependency_Info._DEPENDENCY_UID[UID] = DEPENDENCY_UID

    @staticmethod
    def SetJobIdForUID(UID : Task_UID, jid : int) -> None:
        Dependency_Info._IS_SCHEDULED[UID] = True
        Dependency_Info._DEPENDENCY_JID[UID] = jid

    @staticmethod
    def IsDependentOnAnything(UID : Task_UID) -> bool: #A 0 value in _DEPENDENCY_JID overwrites the dependency to Task_UID.NONE
        return Dependency_Info._DEPENDENCY_UID[UID] != Task_UID.NONE and Dependency_Info._DEPENDENCY_JID[UID] != 0

    @staticmethod
    def IsReadyForScheduling(UID : Task_UID) -> bool:
        return Dependency_Info._IS_SCHEDULED[UID]

    @staticmethod
    def GetDependencyJid(UID : Task_UID) -> int:
        DEP_UID = Dependency_Info._DEPENDENCY_UID[UID]
        if DEP_UID == Task_UID.NONE:
            return 0
        else:
            return Dependency_Info._DEPENDENCY_JID[DEP_UID]

class Task:
    def __init__(self, Task_UID : Task_UID, dependency : Task_UID = Task_UID.NONE) -> None:
        self.Task_UID = Task_UID
        Dependency_Info.SetDependencyForUID(Task_UID, dependency)

    def __iter__(self):
        return iter(Task_Info.GetTaskInfo(self.Task_UID) )

class PredefinedTasks(Enum):
    GEN_MUTATION    = Task( Task_UID.GEN_MUTATION   , Task_UID.NONE)
    RUN_ART         = Task( Task_UID.RUN_ART        , Task_UID.GEN_MUTATION)
    CALC_DEPTH      = Task( Task_UID.CALC_DEPTH     , Task_UID.RUN_ART)
    EXTRACT_READS   = Task( Task_UID.EXTRACT_READS  , Task_UID.CALC_DEPTH)
    RUN_GRASS       = Task( Task_UID.RUN_GRASS      , Task_UID.EXTRACT_READS)
    RUN_ALGA        = Task( Task_UID.RUN_ALGA       , Task_UID.EXTRACT_READS)
    RUN_QUAST       = Task( Task_UID.RUN_QUAST      , Task_UID.RUN_GRASS)
    RUN_QUAST_ALGA  = Task( Task_UID.RUN_QUAST_ALGA , Task_UID.RUN_ALGA)

class Scheduler:
    @staticmethod
    def schedule_tasks(output : str, genome : str, genMut : GenMutEnums):
        os.makedirs(output, mode = 0o774, exist_ok=True)
        os.makedirs(output+"/log", mode = 0o774, exist_ok=True)
        shutil.copyfile(genome, output+"/genome.fsa")

        for task in PredefinedTasks:
            if( not((task == PredefinedTasks.GEN_MUTATION or task == PredefinedTasks.RUN_ART) and genMut == GenMutEnums.NONE) ):
                Scheduler.run_task_cmd(task.value, output, genMut.value)
            #TODO: Pick up on job failure

        print("\nCurrent status:\n")
        print("To Be Done\n")
        #show the current status with 'sjobs'
        #os.system("sjobs")

    @staticmethod
    def run_task_cmd(task:Task, output : str, genmut : int):
        #Construct command
        Task_UID = task.Task_UID
        dependency_exists = Dependency_Info.IsDependentOnAnything(Task_UID)
        job_id = Dependency_Info.GetDependencyJid(Task_UID)
        dependency = ("--dependency=afterok:{} ".format(job_id)) if dependency_exists else ""


        output_dir = "{}/".format(output) if output else ""
        job, err, log, bash = task
        cmd = "smart_sbatch " + dependency + "-J {} -e {}log/{} -o {}log/{} {}".format(job, output_dir, err, output_dir, log, bash.format(genmut, output))

        #Submit command
        print("Submitting Job with command: %s" % cmd)

        args = shlex.split(cmd)
        print(args)
        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        exitcode = proc.returncode
        if exitcode == 0:
            print("Success submitting job, job id: {}".format(int(out)))
            Dependency_Info.SetJobIdForUID(Task_UID, int(out))
        else:
            print("Error submitting job, exitcode: {} error: {}".format(exitcode, err))
