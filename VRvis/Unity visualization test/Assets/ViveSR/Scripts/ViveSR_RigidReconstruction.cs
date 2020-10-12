using UnityEngine;
using System.Runtime.InteropServices;
using System;
using Vive.Plugin.SR.RigidReconstruction;

namespace Vive.Plugin.SR
{
    //Comment in ViveSR
    //public static class ViveSR_RigidReconstructionConfig
    //{
    //    public static ReconstructionDataSource ReconstructionDataSource = ReconstructionDataSource.DATASET;
    //    public static uint NumDatasetFrame = 0;
    //    public static string DatasetPath = "";
    //    public static ReconstructionQuality Quality = ReconstructionQuality.MID;
    //    public static bool ExportCollider = false;
    //}
    public class ViveSR_RigidReconstruction
    {
        public static string ReconsMeshLayerName = "Default";

        [Obsolete("use ViveSR_Framework.CallbackBasic instead.")]
        public delegate void Callback(int numFrame, IntPtr poseMtx, IntPtr vertData, int numVert, int vertStide, IntPtr idxData, int numIdx);
        public delegate void ExportProgressCallback(int stage, int percentage);

        //private static DataInfo[] DataInfoPointCloud = null;
        private static bool InitialPointCloudPtrSize = false;

        private static int[] RawPointCloudFrameIndex = new int[1];
        private static int[] RawPointCloudVerticeNum = new int[1];
        private static int[] RawPointCloudIndicesNum = new int[1];
        private static int[] RawPointCloudBytePerVetex = new int[1];
        private static int[] RawPointCloudSectorNum = new int[1];
        private static int[] RawModelChunkNum = new int[1];
        private static int[] RawModelChunkIdx = new int[1];

        private static float[] OutVertex;
        private static int[] OutIndex;
        private static float[] TrackedPose;
        private static int ExportStage;
        private static int ExportPercentage;
        private static int ExportError;
        private static int ScannedMeshPreview;
        private static int FrameSeq { get { return RawPointCloudFrameIndex[0]; } }
        private static int VertNum { get { return RawPointCloudVerticeNum[0]; } }
        private static int IdxNum { get { return RawPointCloudIndicesNum[0]; } }
        private static int VertStrideInByte { get { return RawPointCloudBytePerVetex[0]; } }
        private static int SectorNum { get { return RawPointCloudSectorNum[0]; } }
        private static int[] SectorIDList;
        private static int[] SectorVertNum;
        private static int[] SectorMeshIdNum;
        private static int ModelChunkNum { get { return RawModelChunkNum[0]; } }
        private static int ModelChunkIdx { get { return RawModelChunkIdx[0]; } }
        private static bool UsingCallback = false;

        public static bool ExportAdaptiveMesh { get; set; }
        public static float ExportAdaptiveMaxGridSize { get; set; }
        public static float ExportAdaptiveMinGridSize { get; set; }
        public static float ExportAdaptiveErrorThres { get; set; }
        public static float LiveAdaptiveMaxGridSize { get; set; }
        public static float LiveAdaptiveMinGridSize { get; set; }
        public static float LiveAdaptiveErrorThres { get; set; }
        public static bool IsScanning { get; private set; }
        public static bool IsExportingMesh { get; private set; }
        public static bool IsDuringScannedMeshPreview { get; private set; }
        public static bool IsScannedMeshPreviewCompleted { get; private set; }
        public static bool ReconstructionProcessing { get; private set; }

        public static int EnableReconstructionProcess(bool active)
        {
            int result = (int)Error.FAILED;
            if (active)
            {
                result = StartReconstructionModule();
                if (result == (int)Error.WORK) ReconstructionProcessing = true;
                else ReconstructionProcessing = false;
            }
            else
            {
                result = StopReconstructionModule();
                ReconstructionProcessing = false;
            }
            return result;
        }


        public static int StartReconstructionModule() {
            SRWorkModule_API.SetSkipVGAProcess(false);
            return SRWorkModule_API.LinkModule((int)ModuleType.DEPTH,(int)ModuleType.RIGIDRECONSTRUCTION);
        }

        public static int StopReconstructionModule()
        {
            return SRWorkModule_API.UnlinkModule((int)ModuleType.DEPTH, (int)ModuleType.RIGIDRECONSTRUCTION);
        }

        public static bool InitRigidReconstructionParamFromFile(string configFile)
        {
            //return ViveSR_Framework.SetParameterString(ViveSR_Framework.MODULE_ID_RIGID_RECONSTRUCTION, (int)ReconstructionParam.CONFIG_FILEPATH, configFile) == (int)Error.WORK;
            return false;
        }

        //Comment in ViveSR
        //public static void InitRigidReconstructionParam()
        //{
        //    this function is not called in current version, keep this API on, we can allow user to adjust some default setting
        //    ViveSR_Framework.SetParameterInt(ViveSR_Framework.MODULE_ID_RIGID_RECONSTRUCTION, (int)ReconstructionParam.CONFIG_DATA_SOURCE, (int)ViveSR_RigidReconstructionConfig.ReconstructionDataSource);
        //    ViveSR_Framework.SetParameterInt(ViveSR_Framework.MODULE_ID_RIGID_RECONSTRUCTION, (int)ReconstructionParam.CONFIG_DATASET_FRAME_NUM, (int)ViveSR_RigidReconstructionConfig.NumDatasetFrame);
        //    ViveSR_Framework.SetParameterString(ViveSR_Framework.MODULE_ID_RIGID_RECONSTRUCTION, (int)ReconstructionParam.CONFIG_DATASET_PATH, ViveSR_RigidReconstructionConfig.DatasetPath);
        //    ViveSR_Framework.SetParameterBool(ViveSR_Framework.MODULE_ID_RIGID_RECONSTRUCTION, (int)ReconstructionParam.CONFIG_EXPORT_COLLIDER, ViveSR_RigidReconstructionConfig.ExportCollider);
        //    ViveSR_Framework.SetParameterBool(ViveSR_Framework.MODULE_ID_RIGID_RECONSTRUCTION, (int)ReconstructionParam.CONFIG_EXPORT_TEXTURE, true);
        //    ViveSR_Framework.SetParameterInt(ViveSR_Framework.MODULE_ID_RIGID_RECONSTRUCTION, (int)ReconstructionParam.CONFIG_QUALITY, (int)ViveSR_RigidReconstructionConfig.Quality);
        //}

        public static int GetRigidReconstructionIntParameter(int type)
        {
            int ret = -1;

            if (SRWorkModule_API.GetReconstructionParameterInt(type, ref ret) != (int)Error.WORK)
                Debug.Log("[ViveSR] [RigidReconstruction] GetRigidReconstructionIntParameter Failed");

            return ret;
        }

        public static void AllocOutputDataMemory()
        {
            InitialPointCloudPtrSize = false;
            OutVertex = new float[8 * 2500000];
            OutIndex = new int[2500000];
            TrackedPose = new float[16];
            //ExternalPose = new float[16];
            SectorIDList = new int[1000000];
            SectorVertNum = new int[1000000];
            SectorMeshIdNum = new int[1000000];

            Debug.Log("[ViveSR] [RigidReconstruction] AllocOutputMemory Done");

            ExportAdaptiveMesh = true;
            LiveAdaptiveMaxGridSize = ExportAdaptiveMaxGridSize = 64;
            LiveAdaptiveMinGridSize = ExportAdaptiveMinGridSize = 4;
            LiveAdaptiveErrorThres  = ExportAdaptiveErrorThres = 0.4f;            
        }

        public static void ReleaseAllocOutputDataMemory()
        {
            OutVertex = null;
            OutIndex = null;
            TrackedPose = null;
            SectorIDList = null;
            SectorVertNum = null;
            SectorMeshIdNum = null;
        }

        public static bool GetRigidReconstructionFrame(ref int frame)
        {
            if (!UsingCallback)
            {
                RawPointCloudFrameIndex[0] = SRWork_Rigid_Reconstruciton.rigid_reconstruction_data_.frame_seq;
            }
            frame = RawPointCloudFrameIndex[0];
            return true;
        }

        // live data
        public static bool GetRigidReconstructionData(ref int frame, 
                                                      out float[] pose, 
                                                      ref int verticesNum, 
                                                      out float[] verticesBuff, 
                                                      ref int vertStrideInFloat, 
                                                      out int[] sectorIDList, 
                                                      ref int sectorNum, 
                                                      out int[] sectorVertNum, 
                                                      out int[] sectorMeshIdNum,
                                                      ref int indicesNum, 
                                                      out int[] indicesBuff)
        {
            if (!UsingCallback)
            {
                int result = (int)Error.WORK;
                if (!InitialPointCloudPtrSize)
                {
                    InitialPointCloudPtrSize = (result == (int)Error.WORK);
                }
                if (result == (int)Error.WORK)
                {
                    ParseReconstructionPtrData();
                }
            }
             
            bool isUpdated = (verticesNum != VertNum);

            verticesNum = VertNum;
            indicesNum = IdxNum;
            frame = FrameSeq;
            vertStrideInFloat = VertStrideInByte / 4;
            verticesBuff = OutVertex;
            indicesBuff = OutIndex;
            pose = TrackedPose;
            sectorIDList = SectorIDList;
            sectorNum = SectorNum;
            sectorVertNum = SectorVertNum;
            sectorMeshIdNum = SectorMeshIdNum;
            return isUpdated;
        }

        // get model data chunk by chunk
        public static bool GetScannedModelPreviewData(ref int modelChunkNum,
                                                                ref int modelChunkIdx,
                                                                ref int modelVertNum,
                                                                out float[] modelVertices,
                                                                ref int modelIdxNum,
                                                                out int[] modelIndices)
        {
            if (!UsingCallback)
            {
                ParseReconstructionPtrData();
            }

            bool isUpdated = (ModelChunkNum > 0 && modelChunkIdx != ModelChunkIdx);

            modelChunkNum = ModelChunkNum;
            modelChunkIdx = ModelChunkIdx;
            modelVertNum = VertNum;
            modelVertices = OutVertex;
            modelIdxNum = IdxNum;
            modelIndices = OutIndex;

            return isUpdated;
        }

        public static int RegisterReconstructionCallback()
        {
            return 1;
        }

        public static int UnregisterReconstructionCallback()
        {
            return 1;
        }

        private static void ReconstructionDataCallback(int key)
        {
        }

        private static void ParseReconstructionPtrData()
        {
            RawPointCloudFrameIndex[0] = SRWork_Rigid_Reconstruciton.rigid_reconstruction_data_.frame_seq;
            Marshal.Copy(SRWork_Rigid_Reconstruciton.rigid_reconstruction_data_.posemtx44, TrackedPose, 0, TrackedPose.Length);
            RawPointCloudVerticeNum[0] = SRWork_Rigid_Reconstruciton.rigid_reconstruction_data_.num_vertices;
            RawPointCloudBytePerVetex[0] = SRWork_Rigid_Reconstruciton.rigid_reconstruction_data_.bytepervert;
            Marshal.Copy(SRWork_Rigid_Reconstruciton.rigid_reconstruction_data_.vertices, OutVertex, 0, (VertNum * VertStrideInByte / sizeof(float)));
            RawPointCloudIndicesNum[0] = SRWork_Rigid_Reconstruciton.rigid_reconstruction_data_.num_indices;
            Marshal.Copy(SRWork_Rigid_Reconstruciton.rigid_reconstruction_data_.indices, OutIndex, 0, IdxNum /**sizeof(int)*/);
            RawPointCloudSectorNum[0] = SRWork_Rigid_Reconstruciton.rigid_reconstruction_data_.sector_num;
            Marshal.Copy(SRWork_Rigid_Reconstruciton.rigid_reconstruction_data_.sector_id_list, SectorIDList, 0, SectorNum);
            Marshal.Copy(SRWork_Rigid_Reconstruciton.rigid_reconstruction_data_.sector_vert_num, SectorVertNum, 0, SectorNum);
            Marshal.Copy(SRWork_Rigid_Reconstruciton.rigid_reconstruction_data_.sector_idx_num, SectorMeshIdNum, 0, SectorNum);
            RawModelChunkNum[0] = SRWork_Rigid_Reconstruciton.rigid_reconstruction_data_.model_chunk_num;
            RawModelChunkIdx[0] = SRWork_Rigid_Reconstruciton.rigid_reconstruction_data_.model_chunk_idx;
        }

        public static void ExportModel(string filename)
        {
            ExportStage = 0;
            ExportPercentage = 0;
            ExportError = (int)Error.WORK;
            IsExportingMesh = true;
            IsScannedMeshPreviewCompleted = false;

            SRWorkModule_API.SetReconstructionParameterBool((int)ReconstructionParam.EXPORT_ADAPTIVE_MODEL, ExportAdaptiveMesh);
            if (ExportAdaptiveMesh)
            {
                SRWorkModule_API.SetReconstructionParameterFloat((int)ReconstructionParam.ADAPTIVE_MAX_GRID, ExportAdaptiveMaxGridSize * 0.01f);   // cm to m
                SRWorkModule_API.SetReconstructionParameterFloat((int)ReconstructionParam.ADAPTIVE_MIN_GRID, ExportAdaptiveMinGridSize * 0.01f);
                SRWorkModule_API.SetReconstructionParameterFloat((int)ReconstructionParam.ADAPTIVE_ERROR_THRES, ExportAdaptiveErrorThres);
            }

            //if ((int)Error.WORK != SRWorkModule_API.RegisterReconstructionCallback(Marshal.GetFunctionPointerForDelegate((ExportProgressCallback)UpdateExportProgress)))
            //    Debug.Log("[ViveSR] [ExportModel] Progress listener failed to register");
            //ViveSR_Framework.RegisterCallback(ViveSR_Framework.MODULE_ID_RIGID_RECONSTRUCTION, (int)ReconstructionCallback.EXPORT_PROGRESS, Marshal.GetFunctionPointerForDelegate((ExportProgressCallback)UpdateExportProgress));

            byte[] bytearray = System.Text.Encoding.ASCII.GetBytes(filename);
            IntPtr parameter = Marshal.AllocCoTaskMem(filename.Length);
            Marshal.Copy(bytearray, 0, parameter, filename.Length);

            SRWorkModule_API.SetReconstructionOutputFileName(parameter, filename.Length);
        }

        /*
        private static void UpdateExportProgress(int stage, int percentage)
        {
            // Fixed: The export stage should be saving mesh model first then extracting collider;
            if      (stage == (int)ReconstructionExportStage.STAGE_EXTRACTING_MODEL)    ExportStage = 0;
            else if (stage == (int)ReconstructionExportStage.STAGE_COMPACTING_TEXTURE)  ExportStage = 1;
            else if (stage == (int)ReconstructionExportStage.STAGE_SAVING_MODEL_FILE)   ExportStage = 2;
            else if (stage == (int)ReconstructionExportStage.STAGE_EXTRACTING_COLLIDER) ExportStage = 3;
            ExportPercentage = percentage;

            if (stage == (int)ReconstructionExportStage.STAGE_EXTRACTING_MODEL)
                Debug.Log("Extracting Model: " + percentage + "%");
            else if (stage == (int)ReconstructionExportStage.STAGE_COMPACTING_TEXTURE)
                Debug.Log("Compacting Textures: " + percentage + "%");
            else if (stage == (int)ReconstructionExportStage.STAGE_EXTRACTING_COLLIDER)
                Debug.Log("Extracting Collider: " + percentage + "%");
            else if (stage == (int)ReconstructionExportStage.STAGE_SAVING_MODEL_FILE)
                Debug.Log("Saving Model: " + percentage + "%");

            if (ExportStage == 3 && ExportPercentage == 100)
            {
                IsExportingMesh = false;
                Debug.Log("[ViveSR] [RigidReconstruction] Finish Exporting");
                //if ((int)Error.WORK != SRWorkModule_API.UnregisterReconstructionCallback())
                //    Debug.Log("[ViveSR] [ExportModel] Progress listener failed to unregister");
            }
        }
        */

        public static void UpdateExportProgress()
        {
            ExportError = SRWorkModule_API.GetExportMeshProgress(ref ExportPercentage);
            if (ExportError != (int)Error.WORK || ExportPercentage == 100)
                IsExportingMesh = false;
        }

        public static void ExtractModelPreviewData()
        {
            ExportStage = 0;
            ScannedMeshPreview = 0;
            IsDuringScannedMeshPreview = true;

            SRWorkModule_API.SetReconstructionParameterBool((int)ReconstructionParam.EXPORT_ADAPTIVE_MODEL, ExportAdaptiveMesh);
            if (ExportAdaptiveMesh)
            {
                SRWorkModule_API.SetReconstructionParameterFloat((int)ReconstructionParam.ADAPTIVE_MAX_GRID, ExportAdaptiveMaxGridSize * 0.01f);   // cm to m
                SRWorkModule_API.SetReconstructionParameterFloat((int)ReconstructionParam.ADAPTIVE_MIN_GRID, ExportAdaptiveMinGridSize * 0.01f);
                SRWorkModule_API.SetReconstructionParameterFloat((int)ReconstructionParam.ADAPTIVE_ERROR_THRES, ExportAdaptiveErrorThres);
            }
            SRWorkModule_API.SetReconstructionParameterBool((int)(ReconstructionCmd.MODEL_PREVIEW_START_FOR_UNITY), true);
        }

        //Current runtime doesn't have callback.
        private static void UpdateModelPreviewProgress(int stage, int percentage)
        {
            if (stage == (int)ReconstructionExportStage.STAGE_EXTRACTING_MODEL) ExportStage = 0;
            else if (stage == (int)ReconstructionExportStage.STAGE_COMPACTING_TEXTURE) ExportStage = 1;
            else if (stage == (int)ReconstructionExportStage.STAGE_SAVING_MODEL_FILE) ExportStage = 2;
            else if (stage == (int)ReconstructionExportStage.STAGE_EXTRACTING_COLLIDER) ExportStage = 3;
            ScannedMeshPreview = percentage;

            if (ExportStage == 0 && ScannedMeshPreview == 100)
            {
                StopScanning();
                CompleteModelPreview();
                Debug.Log("[ViveSR] [RigidReconstruction] Complete Scanned Model Preview");
            }
        }

        /*
        public static void GetExportProgress(ref int stage, ref int percentage)
        {
            stage = ExportStage;
            percentage = ExportPercentage;
        }
        */

        public static int GetExportProgress(ref int percentage)
        {
            //percentage = ExportStage * 25 + (int)(ExportPercentage * 0.25f);
            percentage = ExportPercentage;
            return ExportError;
        }

        public static void EnableLiveMeshExtraction(bool enable)
        {
            SRWorkModule_API.SetReconstructionParameterBool((int)(ReconstructionCmd.EXTRACT_POINT_CLOUD), enable);
        }

        public static void SetLiveMeshExtractionMode(ReconstructionLiveMeshExtractMode mode)
        {
            SRWorkModule_API.SetReconstructionParameterInt((int)(ReconstructionCmd.EXTRACT_VERTEX_NORMAL), (int)mode);
        }

        public static void StartScanning()
        {
            ViveSR_RigidReconstruction.EnableReconstructionProcess(true);
            if (ReconstructionProcessing)
            {
                SRWorkModule_API.SetReconstructionParameterBool((int)(ReconstructionCmd.START), true);
                IsScanning = true;
                IsScannedMeshPreviewCompleted = false;
                Debug.Log("start");
            }
        }

        public static void StopScanning()
        {
            if (ReconstructionProcessing)
            {
                IsScanning = false;
                SRWorkModule_API.SetReconstructionParameterBool((int)(ReconstructionCmd.STOP), true);
                Debug.Log("stop");
            }
            ViveSR_RigidReconstruction.EnableReconstructionProcess(false);

        }

        public static void CompleteModelPreview()
        {
            IsScannedMeshPreviewCompleted = true;
            IsDuringScannedMeshPreview = false;
        }

        public static int ResetReconstructionModule()
        {
            return SRWorkModule_API.ResetReconstructionModule();
        }
    }

}
