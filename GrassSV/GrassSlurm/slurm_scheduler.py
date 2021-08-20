#!/usr/local/bin/python

import subprocess, os
from enum import Enum, IntEnum

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
        Task_UID.RUN_ALGA       : "run_quast.out",
        Task_UID.RUN_QUAST      : "run_alga.out",
        Task_UID.RUN_QUAST_ALGA : "run_quast_alga.out"
    }

    _ERROR_FILES = {
        Task_UID.GEN_MUTATION   : "gen_mutation.err",
        Task_UID.RUN_ART        : "run_art.err",
        Task_UID.CALC_DEPTH     : "calculate_depth.err",
        Task_UID.EXTRACT_READS  : "extract_reads.err",
        Task_UID.RUN_GRASS      : "run_grasshopper.err",
        Task_UID.RUN_ALGA       : "run_quast.err",
        Task_UID.RUN_QUAST      : "run_alga.err",
        Task_UID.RUN_QUAST_ALGA : "run_quast_alga.err",
    }

    _BASH_CMDS = {
        Task_UID.GEN_MUTATION   : __file__ + "/multiple.sh ${SV_TYPE} ${MUTATION_FOLDER}/genome.fsa temp_${SV_TYPE} ${MUTATION_FOLDER}/out.bed",
        Task_UID.RUN_ART        : __file__ + "/run_art.sh ${MUTATION_FOLDER}",
        Task_UID.CALC_DEPTH     : __file__ + "/calculate_depth.sh ${MUTATION_FOLDER}",
        Task_UID.EXTRACT_READS  : __file__ + "/whole_pipeline.sh ${MUTATION_FOLDER}",
        Task_UID.RUN_GRASS      : __file__ + "/whole_pipeline2.sh ${MUTATION_FOLDER}",
        Task_UID.RUN_ALGA       : __file__ + "/whole_pipeline3.sh ${MUTATION_FOLDER}",
        Task_UID.RUN_QUAST      : __file__ + "/whole_pipeline2_alga.sh ${MUTATION_FOLDER}",
        Task_UID.RUN_QUAST_ALGA : __file__ + "/whole_pipeline3.sh ${MUTATION_FOLDER} alga contigs.fasta_contigs.fasta"
    }

    @staticmethod
    def GetTaskInfo( UID : Task_UID):
        return UID, Task_Info._JOB_NAMES[UID], Task_Info._LOG_FILES[UID], Task_Info._ERROR_FILES[UID], Task_Info._BASH_CMDS[UID] 

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
    def IsDependentOnAnything(UID : Task_UID) -> bool:
        return Dependency_Info._DEPENDENCY_UID[UID] != Task_UID.NONE

    @staticmethod
    def IsReadyForScheduling(UID : Task_UID) -> bool:
        return Dependency_Info._IS_SCHEDULED[UID]

    @staticmethod
    def GetDependencyJid(UID : Task_UID) -> int:
        return Dependency_Info._DEPENDENCY_JID[UID]

class Task:
    def __init__(self, Task_UID : Task_UID, dependency : Task_UID = Task_UID.NONE) -> None:
        self.Task_UID = Task_UID
        _, self.name, self.error_file, self.log_file, self.cmd = Task_Info.GetTaskInfo(Task_UID.GEN_MUTATION )
        Dependency_Info.SetDependencyForUID(Task_UID, dependency)

    def __iter__(self):
        return Task_Info.GetTaskInfo(self.Task_UID )

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
    def schedule_tasks(self):
        task : Task
        for task in PredefinedTasks:
            #TODO: Pick up on job failure
            self.run_task_cmd(task)
            #TODO: Use Dependency_Info.IsReadyForScheduling

        print("\nCurrent status:\n")
        print("To Be Done\n")
        #show the current status with 'sjobs'
        #os.system("sjobs")

    def run_task_cmd(self, task:Task):
        #Construct command
        Task_UID = task.Task_UID
        dependency_exists = Dependency_Info.IsDependentOnAnything(Task_UID)
        job_id = Dependency_Info.GetDependencyJid(Task_UID)
        dependency = "--dependency=afterok:{} ".format() % job_id if dependency_exists else ""
        cmd = "smart_sbatch " + dependency + "-J {} -e {} -o {} {} ".format(*task)

        #Submit command
        print("Submitting Job with command: %s" % cmd)

        status,jobnum = commands.getstatusoutput(cmd)
        if status == 0:
            print("Success submitting job")
            Dependency_Info.SetJobIdForUID(Task_UID, jobnum)
        else:
            print("Error submitting job")