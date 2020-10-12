using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.Events;

namespace Vive.Plugin.SR
{
    public class ViveSR : MonoBehaviour
    {
        public class FrameworkInitialError {
            public int ErrorCode = (int)Error.WORK;
            public ModuleType FailedModule = 0;
        }
        /// <summary>
        /// Status of SRanipal context and engines.
        /// </summary>
        public static FrameworkStatus FrameworkStatus { get; protected set; }
        public static FrameworkInitialError InitialError = new FrameworkInitialError();
        /// <summary>
        /// Enable the seethrough engine or not.
        /// </summary>
        [Header("[ViveSR Framework Pre-Setting]")]
        public bool EnableSeeThroughModule;
        public bool EnableDepthModule;
        public bool EnableDepthMeshModule;
        public bool EnableRigidReconstructionModule;

        [Header("[ViveSR Framework SeeThrough Data Setting]")]
        public bool EnableSeeThroughNon4KDistortDataUse;

        public static bool EnableUnitySeeThrough = false;
        public static bool EnableUnitySeeThroughNon4KDistortData = false;
        public static bool EnableUnityDepthMesh = false;
        public static bool EnableUnityReconstruction = false;
        public static bool EnableUnityAI = false;

        [Header("[ViveSR Modules Unity Registration]")]
        public ViveSR_Module[] Modules = new ViveSR_Module[3];

        private List<ModuleType> moduleTypes = new List<ModuleType>();

        private static ViveSR Mgr = null;

        private bool refinement_setting = false;

        public static ViveSR Instance
        {
            get
            {
                if (Mgr == null)
                {
                    Mgr = FindObjectOfType<ViveSR>();
                }
                if (Mgr == null)
                {
                    Debug.LogError("SRWork_Module_Framework does not be attached on GameObject");
                }
                return Mgr;
            }
        }

        // Use this for initialization
        void Start()
        {
            StartFramework();
        }

        void Update()
        {
            UpdateWhileWorking();

            if (EnableUnitySeeThrough)
                SeeThrough.SRWork_SeeThrough.UpdateData();

            // UpdateData will be called in ExtractMeshDataThread
            // Also we don't need to get depth data
            if (ViveSR_DualCameraImageRenderer.UpdateDepthMaterial)
            {
                Depth.SRWork_Depth.UpdateData();
            }
            if (EnableUnityDepthMesh)
            {
                if (DepthMesh.SRWork_Depth_Mesh.UpdateData()) {
                    ((ViveSR_DualCameraDepthCollider)Modules[1]).ExtractMeshData();
                }
            }
            if (EnableUnityReconstruction
                && !ViveSR_SceneUnderstanding.IsExportingSceneUnderstandingInfo
                && !ViveSR_RigidReconstruction.IsExportingMesh)
            {
                if (RigidReconstruction.SRWork_Rigid_Reconstruciton.UpdateData()) {
                    ((ViveSR_RigidReconstructionRenderer)Modules[2]).ExtractMeshData();
                }
            }
            if (ViveSR_RigidReconstruction.IsExportingMesh) {
                ViveSR_RigidReconstruction.UpdateExportProgress();
            }
            if (ViveSR_SceneUnderstanding.IsExportingSceneUnderstandingInfo) {
                ViveSR_SceneUnderstanding.UpdateSceneUnderstandingProgress();
            }
        }
        void Release()
        {
            if (EnableUnitySeeThrough == true)
                Modules[0].Release();
            if (EnableUnityDepthMesh == true)
                Modules[1].Release();
            if (EnableUnityReconstruction == true)
                Modules[2].Release();
            ViveSR_DualCameraDepthCollider.UpdateDepthCollider = false;
        }
        void OnDestroy()
        {
            Release();
            StopFramework();
            SRWorkModule_API.StopViveSR();
        }

        public void StartFramework()
        {
            if (FrameworkStatus == FrameworkStatus.WORKING) return;
            FrameworkStatus = FrameworkStatus.START;

            moduleTypes.Clear();
            if (EnableSeeThroughModule)
            {
                moduleTypes.Add(ModuleType.SEETHROUGH);
                moduleTypes.Add(ModuleType.SEETHROUGH4K);
                moduleTypes.Add(ModuleType.CONTROLLER_POSE);
            }
            if (EnableDepthModule) moduleTypes.Add(ModuleType.DEPTH);
            if (EnableDepthMeshModule) moduleTypes.Add(ModuleType.DEPTHMESH);
            if (EnableRigidReconstructionModule) moduleTypes.Add(ModuleType.RIGIDRECONSTRUCTION);

            InitialModule();
        }
        public void StopFramework()
        {
            if (FrameworkStatus != FrameworkStatus.STOP)
            {
                foreach (var type in moduleTypes)
                {
                    int result = SRWorkModule_API.Release(type);
                    if (result == (int)Error.WORK) Debug.Log("[SRWorkModule] Release " + type + " : " + result);
                    else Debug.LogWarning("[SRWorkModule] Release " + type + " : " + result);
                }
            }
            else
            {
                Debug.Log("[SRWorkModule] Stop Framework : not open");
            }
            FrameworkStatus = FrameworkStatus.STOP;
        }
        private void InitialModule()
        {
            foreach (var type in moduleTypes)
            {
                InitialError.ErrorCode = SRWorkModule_API.Initial(type, IntPtr.Zero);
                if (InitialError.ErrorCode != (int)Error.WORK) {
                    InitialError.FailedModule = type;
                    Debug.LogWarning("[SRWorkModule] Initial " + type + " : " + InitialError.ErrorCode);
                    FrameworkStatus = FrameworkStatus.ERROR;
                    return;
                }
                Debug.Log("[SRWorkModule] Initial " + type + " : " + InitialError.ErrorCode);
            }
            FrameworkStatus = FrameworkStatus.WORKING;
        }
        private void UpdateWhileWorking()
        {
            if (FrameworkStatus != FrameworkStatus.WORKING)
                return;

            if (EnableSeeThroughModule == true && EnableUnitySeeThrough == false)
            {
                Modules[0].Initial();
                SRWorkModule_API.TurnOffUndistortDataToDepth();
                SRWorkModule_API.UnlinkModule((int)ModuleType.SEETHROUGH, (int)ModuleType.DEPTH);
                if (SeeThrough.SRWork_SeeThrough.b4KImageReady)
                {
                    SeeThrough.SRWork_SeeThrough.SkipVGASeeThrough(true);
                }
                EnableUnitySeeThrough = true;
            }

            if (EnableSeeThroughNon4KDistortDataUse == true && EnableUnitySeeThroughNon4KDistortData == false)
            {
                bool result = SeeThrough.SRWork_SeeThrough.TurnOnSeeThroughDistortData();
                if (result) EnableUnitySeeThroughNon4KDistortData = true;
            }
            else if (EnableSeeThroughNon4KDistortDataUse == false && EnableUnitySeeThroughNon4KDistortData == true)
            {
                bool result = SeeThrough.SRWork_SeeThrough.TurnOffSeeThroughDistortData();
                if (result) EnableUnitySeeThroughNon4KDistortData = false;
            }

            if (EnableDepthMeshModule == true && EnableUnityDepthMesh == false)
            {
                Modules[1].Initial();
                //Get refinement setting of engine.
                int result = SRWorkModule_API.GetDepthParameterBool((int)DepthCmd.ENABLE_REFINEMENT, ref refinement_setting);
                if (result == (int)SR.Error.WORK)
                    ViveSR_DualCameraImageCapture.DepthRefinement = refinement_setting;
                SRWorkModule_API.UnlinkModule((int)ModuleType.DEPTH, (int)ModuleType.DEPTHMESH);
                EnableUnityDepthMesh = true;
            }

            if (EnableRigidReconstructionModule == true && EnableUnityReconstruction == false)
            {
                Modules[2].Initial();
                SRWorkModule_API.UnlinkModule((int)ModuleType.DEPTH, (int)ModuleType.RIGIDRECONSTRUCTION);
                EnableUnityReconstruction = true;
            }
        }
    }
}
