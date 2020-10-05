//========= Copyright 2017, HTC Corporation. All rights reserved. ===========
using System.Collections.Generic;
using UnityEngine;

namespace Vive.Plugin.SR
{
    public class ViveSR_GameViewDebugTool : MonoBehaviour
    {
        private bool EnableDebugTool = false;
        private int ToolbarIndex = 0;
        private string[] ToolbarLabels = new string[] { "SeeThrough", "Depth", "3D", "SceneUnderstanding" };
        private const short AreaXStart = 10;
        private const short AreaYStart = 45;

        private void Update()
        {
            if (Input.GetKey(KeyCode.S) && Input.GetKeyDown(KeyCode.R)) EnableDebugTool = !EnableDebugTool;
        }

        private void OnGUI()
        {
            if (!EnableDebugTool) return;

            ToolbarIndex = GUI.Toolbar(new Rect(10, 10, 550, 30), ToolbarIndex, ToolbarLabels);
            GUILayout.Space(45);
            GUILayout.BeginArea(new Rect(AreaXStart, AreaYStart, Screen.width - AreaXStart, Screen.height - AreaYStart));
            switch (ToolbarIndex)
            {
                case 0:
                    SeeThroughGUI();
                    break;
                case 1:
                    DepthGUI();
                    break;
                case 2:
                    ReconstructionGUI();
                    break;
                case 3:
                    SceneUnderstandingGUI();
                    break;
            }
            GUILayout.EndArea();
        }
        #region SeeThroughGUI
        private void SeeThroughGUI()
        {
            ViveSR_DualCameraImageRenderer.UpdateDistortedMaterial = GUILayout.Toggle(ViveSR_DualCameraImageRenderer.UpdateDistortedMaterial, "Update Camera Material");
            ViveSR_DualCameraImageRenderer.UpdateUndistortedMaterial = GUILayout.Toggle(ViveSR_DualCameraImageRenderer.UpdateUndistortedMaterial, "Update Undistorted Material");
            ViveSR_DualCameraImageRenderer.UpdateDepthMaterial = GUILayout.Toggle(ViveSR_DualCameraImageRenderer.UpdateDepthMaterial, "Update Depth Material");
            //ViveSR_DualCameraImageRenderer.CallbackMode = GUILayout.Toggle(ViveSR_DualCameraImageRenderer.CallbackMode, "Callback Mode");
        }
        #endregion

        #region DepthGUI
        private void DepthGUI()
        {
            bool EnableDepth = GUILayout.Toggle(ViveSR_DualCameraImageCapture.DepthProcessing, "Depth Processing");
            if (ViveSR_DualCameraImageCapture.DepthProcessing != EnableDepth)
            {
                ViveSR_DualCameraImageCapture.EnableDepthProcess(EnableDepth);
            }

            if (ViveSR_DualCameraImageCapture.DepthProcessing)
            {
                ViveSR_DualCameraImageCapture.DepthRefinement = GUILayout.Toggle(ViveSR_DualCameraImageCapture.DepthRefinement, "Depth Refinement");
                ViveSR_DualCameraImageCapture.DepthEdgeEnhance = GUILayout.Toggle(ViveSR_DualCameraImageCapture.DepthEdgeEnhance, "Depth Edge Enhance");
            }

            ViveSR_DualCameraDepthCollider.UpdateDepthCollider = GUILayout.Toggle(ViveSR_DualCameraDepthCollider.UpdateDepthCollider, "Depth Mesh Collider");
            if (ViveSR_DualCameraDepthCollider.UpdateDepthCollider)
            {
                ViveSR_DualCameraDepthCollider.UpdateDepthColliderRange = GUILayout.Toggle(ViveSR_DualCameraDepthCollider.UpdateDepthColliderRange, "Depth Mesh Collider Range");
                ViveSR_DualCameraDepthCollider.ColliderMeshVisibility = GUILayout.Toggle(ViveSR_DualCameraDepthCollider.ColliderMeshVisibility, "Show Depth Mesh Collider");

                GUILayout.Label("Set Mesh Near Distance:");
                GUILayout.BeginHorizontal();
                float NearDiatanceThres = ViveSR_DualCameraDepthCollider.UpdateColliderNearDistance = GUILayout.HorizontalSlider(ViveSR_DualCameraDepthCollider.UpdateColliderNearDistance, 0.0f, 10.0f);
                GUILayout.Label("" + NearDiatanceThres.ToString("0.00"));
                GUILayout.EndHorizontal();

                GUILayout.Label("Set Mesh Far Distance:");
                GUILayout.BeginHorizontal();
                float FarDiatanceThres = ViveSR_DualCameraDepthCollider.UpdateColliderFarDistance = GUILayout.HorizontalSlider(ViveSR_DualCameraDepthCollider.UpdateColliderFarDistance, 0.0f, 10.0f);
                GUILayout.Label("" + FarDiatanceThres.ToString("0.00"));
                GUILayout.EndHorizontal();
            }
        }
        #endregion

        #region ReconstructionGUI
        //string[] displayMode = new[] { "Full Scene Point", "Field Of View", "Adaptive Mesh" };
        //string[] adaptiveLable = new[] { "64cm", "32cm", "16cm", "8cm", "4cm", "2cm" };
        List<float> adaptiveLevel = new List<float> { 64.0f, 32.0f, 16.0f, 8.0f, 4.0f, 2.0f };

        int maxSelectID, minSelectID;
        float errorThres, exportMaxSize, exportMinSize;
        private void ReconstructionGUI()
        {
            GUIStyle StyleBold = new GUIStyle { fontStyle = FontStyle.Bold };

            GUILayout.Label(new GUIContent("[Runtime Command]"), StyleBold);        // start / stop
            string btnStrEnableReconstructionProcess = ViveSR_RigidReconstruction.ReconstructionProcessing ? "Disable Reconstruction Processing" : "Enable Reconstruction Processing";
            if (GUILayout.Button(btnStrEnableReconstructionProcess, GUILayout.ExpandWidth(false)))
            {
                ViveSR_RigidReconstruction.EnableReconstructionProcess(!ViveSR_RigidReconstruction.ReconstructionProcessing);
            }
            if (ViveSR_RigidReconstruction.ReconstructionProcessing)
            {

                GUILayout.Label(new GUIContent("--Start/Stop--"), StyleBold);
                if (!ViveSR_RigidReconstruction.IsScanning && !ViveSR_RigidReconstruction.IsExportingMesh && !ViveSR_RigidReconstruction.IsDuringScannedMeshPreview)
                {
                    if (GUILayout.Button("Start Reconstruction", GUILayout.ExpandWidth(false)))
                    {
                        ViveSR_RigidReconstruction.StartScanning();
                    }
                }
                if (ViveSR_RigidReconstruction.IsScanning && !ViveSR_RigidReconstruction.IsExportingMesh && !ViveSR_RigidReconstruction.IsDuringScannedMeshPreview)
                {
                    if (GUILayout.Button("Stop Reconstruction", GUILayout.ExpandWidth(false)))
                    {
                        ViveSR_RigidReconstruction.StopScanning();
                    }

                    GUILayout.Label(new GUIContent("--Live Extraction--"), StyleBold);
                    int curMode = (int)ViveSR_RigidReconstructionRenderer.LiveMeshDisplayMode;

                    if (curMode != (int)ViveSR_RigidReconstructionRenderer.LiveMeshDisplayMode)
                    {
                        ViveSR_RigidReconstructionRenderer.LiveMeshDisplayMode = (ReconstructionDisplayMode)curMode;
                    }
                    // adaptive tunning
                    if (curMode == (int)ReconstructionDisplayMode.ADAPTIVE_MESH)
                    {
                        GUILayout.Label(new GUIContent("--Live Adaptive Mesh Tuning--"), StyleBold);
                        DrawAdaptiveParamUI(ViveSR_RigidReconstruction.LiveAdaptiveMaxGridSize, ViveSR_RigidReconstruction.LiveAdaptiveMinGridSize, ViveSR_RigidReconstruction.LiveAdaptiveErrorThres);
                        ViveSR_RigidReconstruction.LiveAdaptiveMaxGridSize = adaptiveLevel[maxSelectID];
                        ViveSR_RigidReconstruction.LiveAdaptiveMinGridSize = adaptiveLevel[minSelectID];
                        ViveSR_RigidReconstruction.LiveAdaptiveErrorThres = errorThres;
                    }
                }

                // export
                if (ViveSR_RigidReconstruction.IsScanning && !ViveSR_RigidReconstruction.IsExportingMesh && !ViveSR_RigidReconstruction.IsDuringScannedMeshPreview)
                {
                    GUILayout.Label(new GUIContent("--Export--"), StyleBold);
                    bool exportAdaptive = ViveSR_RigidReconstruction.ExportAdaptiveMesh;
                    ViveSR_RigidReconstruction.ExportAdaptiveMesh = GUILayout.Toggle(exportAdaptive, "Export Adaptive Model");

                    if (ViveSR_RigidReconstruction.ExportAdaptiveMesh)
                    {
                        // live extraction mode
                        GUILayout.Label(new GUIContent("--Export Adaptive Mesh Tuning--"), StyleBold);
                        DrawAdaptiveParamUI(ViveSR_RigidReconstruction.ExportAdaptiveMaxGridSize, ViveSR_RigidReconstruction.ExportAdaptiveMinGridSize, ViveSR_RigidReconstruction.ExportAdaptiveErrorThres);
                        ViveSR_RigidReconstruction.ExportAdaptiveMaxGridSize = adaptiveLevel[maxSelectID];
                        ViveSR_RigidReconstruction.ExportAdaptiveMinGridSize = adaptiveLevel[minSelectID];
                        ViveSR_RigidReconstruction.ExportAdaptiveErrorThres = errorThres;
                    }

                    if (GUILayout.Button("Start Export Model", GUILayout.ExpandWidth(false)))
                    {
                        ViveSR_RigidReconstruction.StopScanning();
                        ViveSR_RigidReconstruction.ExportModel("Model");
                    }
                }
            }
        }

        private void DrawAdaptiveParamUI(float maxGridSize, float minGridSize, float thres)
        {
            GUILayout.Label("Adaptive Range (Max~Min):");
            GUILayout.BeginHorizontal();
            maxSelectID = adaptiveLevel.IndexOf(maxGridSize);
            minSelectID = adaptiveLevel.IndexOf(minGridSize);
            GUILayout.EndHorizontal();

            GUILayout.Label("Divide Threshold:");
            GUILayout.BeginHorizontal();
            errorThres = GUILayout.HorizontalSlider(thres, 0.0f, 1.5f);
            GUILayout.Label("" + errorThres.ToString("0.00"));
            GUILayout.EndHorizontal();
        }
        #endregion


        #region SceneUnderstandingGUI        
        bool[] SceneObjectToggle = new[] { false, false, false, false, false, false, false, false, false, false, false, false };
        string[] SceneObjectName = new[] { "Floor", "Wall", "Ceiling", "Chair", "Table", "Bed", "Monitor", "Window", "Furniture", "Door", "Picture", "Person" };
        string[] ObjectColor = new[] { "Green", "Blue", "Yellow", "Red", "Cyan", "Magenta", "Dark Red", "Dark Green", "Purple", "Pink", "Orange", "Grass Green" };

        private string ReconsSceneDir = "Recons3DAsset/";
        private string SemanticObjDir = "SemanticIndoorObj/";
        private string SemanticObjDirPath;
        private string ReconstructionResultDir = System.IO.Path.GetDirectoryName(System.Environment.GetFolderPath(System.Environment.SpecialFolder.ApplicationData)) + "\\LocalLow\\HTC Corporation\\SR_Reconstruction_Output\\";
        private void SceneUnderstandingGUI()
        {
            GUIStyle StyleBold = new GUIStyle { fontStyle = FontStyle.Bold };
            GUILayout.Label(new GUIContent("--Scene Understanding--"), StyleBold);
            if (ViveSR_RigidReconstruction.IsScanning)
            {
                bool isSemanticEnabled = GUILayout.Toggle(ViveSR_SceneUnderstanding.IsEnabledSceneUnderstanding, "Enable Scene Understanding");
                if (isSemanticEnabled != ViveSR_SceneUnderstanding.IsEnabledSceneUnderstanding)
                {
                    ViveSR_SceneUnderstanding.EnableSceneUnderstanding(isSemanticEnabled);
                }
                bool isSemanticRefinementEnabled = GUILayout.Toggle(ViveSR_SceneUnderstanding.IsEnabledSceneUnderstandingRefinement, "Enable Scene Understanding Refinement");
                if (isSemanticRefinementEnabled != ViveSR_SceneUnderstanding.IsEnabledSceneUnderstandingRefinement)
                {
                    ViveSR_SceneUnderstanding.EnableSceneUnderstandingRefinement(isSemanticRefinementEnabled);
                }
            }
            else
            {
                GUILayout.Label(new GUIContent("Please Start Reconstruction"), StyleBold);
            }
            if (ViveSR_SceneUnderstanding.IsEnabledSceneUnderstanding && ViveSR_RigidReconstruction.IsScanning)
            {
                GUILayout.Label(new GUIContent("--Scene Understanding Live Dispaly & Export--"), StyleBold);
                bool isSemanticPreviewEnabled = GUILayout.Toggle(ViveSR_SceneUnderstanding.IsEnabledSceneUnderstandingView, "Enable Preview");
                if (isSemanticPreviewEnabled != ViveSR_SceneUnderstanding.IsEnabledSceneUnderstandingView)
                {
                    ViveSR_SceneUnderstanding.EnableSceneUnderstandingView(isSemanticPreviewEnabled);
                }
                int index = 0;
                foreach (bool toggle in SceneObjectToggle)
                {
                    bool _toggle = GUILayout.Toggle(toggle, "View/Export " + SceneObjectName[index] + " (" + ObjectColor[index] + ")");
                    if (_toggle != toggle)
                    {
                        SceneObjectToggle[index] = _toggle;
                        switch (SceneObjectName[index])
                        {
                            case "Bed":
                                ViveSR_SceneUnderstanding.SetCustomSceneUnderstandingConfig(SceneUnderstandingObjectType.BED, 10, _toggle);
                                break;
                            case "Ceiling":
                                ViveSR_SceneUnderstanding.SetCustomSceneUnderstandingConfig(SceneUnderstandingObjectType.CEILING, 10, _toggle);
                                break;
                            case "Chair":
                                ViveSR_SceneUnderstanding.SetCustomSceneUnderstandingConfig(SceneUnderstandingObjectType.CHAIR, 10, _toggle);
                                break;
                            case "Floor":
                                ViveSR_SceneUnderstanding.SetCustomSceneUnderstandingConfig(SceneUnderstandingObjectType.FLOOR, 10, _toggle);
                                break;
                            case "Table":
                                ViveSR_SceneUnderstanding.SetCustomSceneUnderstandingConfig(SceneUnderstandingObjectType.TABLE, 10, _toggle);
                                break;
                            case "Wall":
                                ViveSR_SceneUnderstanding.SetCustomSceneUnderstandingConfig(SceneUnderstandingObjectType.WALL, 10, _toggle);
                                break;
                            case "Window":
                                ViveSR_SceneUnderstanding.SetCustomSceneUnderstandingConfig(SceneUnderstandingObjectType.WINDOW, 10, _toggle);
                                break;
                            case "Monitor":
                                ViveSR_SceneUnderstanding.SetCustomSceneUnderstandingConfig(SceneUnderstandingObjectType.MONITOR, 10, _toggle);
                                break;
                            case "Furniture":
                                ViveSR_SceneUnderstanding.SetCustomSceneUnderstandingConfig(SceneUnderstandingObjectType.FURNITURE, 10, _toggle);
                                break;
                            case "Door":
                                ViveSR_SceneUnderstanding.SetCustomSceneUnderstandingConfig(SceneUnderstandingObjectType.DOOR, 10, _toggle);
                                break;
                            case "Picture":
                                ViveSR_SceneUnderstanding.SetCustomSceneUnderstandingConfig(SceneUnderstandingObjectType.PICTURE, 10, _toggle);
                                break;
                            case "Person":
                                ViveSR_SceneUnderstanding.SetCustomSceneUnderstandingConfig(SceneUnderstandingObjectType.PERSON, 10, _toggle);
                                break;
                        }

                    }
                    index++;
                }
            }

            if (ViveSR_SceneUnderstanding.IsEnabledSceneUnderstanding && ViveSR_RigidReconstruction.IsScanning)
            {

                if (GUILayout.Button("Export SceneObjects (.xml)", GUILayout.ExpandWidth(false)))
                {
                    ViveSR_SceneUnderstanding.ExportSceneUnderstandingInfo(SemanticObjDir);
                }
            }
            GUILayout.Label(new GUIContent("--SceneObjects Operation--"), StyleBold);
            if (GUILayout.Button("Load & Show SceneObjects BoundingBox", GUILayout.ExpandWidth(false)))
            {
                SemanticObjDirPath = ReconstructionResultDir + ReconsSceneDir + SemanticObjDir;
                ViveSR_SceneUnderstanding.ImportSceneObjects(SemanticObjDirPath);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.CHAIR, true, true);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.CEILING, true, true);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.FLOOR, true, true);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.WALL, true, true);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.BED, true, true);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.TABLE, true, true);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.MONITOR, true, true);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.WINDOW, true, true);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.FURNITURE, true, true);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.DOOR, true, true);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.PICTURE, true, true);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.PERSON, true, true);
            }
            if (GUILayout.Button("Destroy All SceneObjects BoundingBox", GUILayout.ExpandWidth(false)))
            {
                ViveSR_SceneUnderstanding.DestroySceneObjects();
            }
        }
        #endregion
    }
}