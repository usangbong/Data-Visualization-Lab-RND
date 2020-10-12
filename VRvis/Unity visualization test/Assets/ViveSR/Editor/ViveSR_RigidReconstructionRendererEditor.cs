using UnityEditor;
using UnityEngine;
using Vive.Plugin.SR;
using System.Collections.Generic;

[CustomEditor(typeof(ViveSR_RigidReconstructionRenderer))]
[CanEditMultipleObjects]
public class ViveSR_RigidReconstructionRendererEditor : Editor
{
    string[] displayMode = new[] { "Full Scene Point", "Field Of View", "Adaptive Mesh" };
    string[] adaptiveLable = new[] { "64cm", "32cm", "16cm", "8cm", "4cm", "2cm" };
    List<float> adaptiveLevel = new List<float> { 64.0f, 32.0f, 16.0f, 8.0f, 4.0f, 2.0f };
    int maxSelectID, minSelectID;
    float errorThres, exportMaxSize, exportMinSize;

    bool[] SceneObjectToggle = new[] { false, false, false, false, false, false, false, false, false, false, false, false };
    string[] SceneObjectName = new[] { "Floor", "Wall", "Ceiling", "Chair", "Table", "Bed", "Monitor", "Window", "Furniture", "Door", "Picture", "Person" };
    string[] ObjectColor = new[] { "Green", "Blue", "Yellow", "Red", "Cyan", "Magenta", "Dark Red", "Dark Green", "Purple", "Pink", "Orange", "Grass Green" };

    public string ReconsSceneDir = "Recons3DAsset/";
    public string SemanticObjDir = "SemanticIndoorObj/";
    private string ReconstructionResultDir = System.IO.Path.GetDirectoryName(System.Environment.GetFolderPath(System.Environment.SpecialFolder.ApplicationData)) + "\\LocalLow\\HTC Corporation\\SR_Reconstruction_Output\\";

    bool SetReconstructionFPS = false;
    float ReconstructionFPS = 10.0f;

    public override void OnInspectorGUI()
    {
        DrawDefaultInspector();

        if (!Application.isPlaying) return;

        EditorGUILayout.Separator();
        EditorGUILayout.Separator();
        GUIStyle style = new GUIStyle();
        style.fontStyle = FontStyle.Bold;
        GUILayout.Label(new GUIContent("[Runtime Command]"), style);
        EditorGUILayout.Separator();

        string btnStrEnableReconstructionProcess = ViveSR_RigidReconstruction.ReconstructionProcessing ? "Disable Reconstruction Processing" : "Enable Reconstruction Processing";
        if (GUILayout.Button(btnStrEnableReconstructionProcess))
        {
            ViveSR_RigidReconstruction.EnableReconstructionProcess(!ViveSR_RigidReconstruction.ReconstructionProcessing);
        }

        if (ViveSR_RigidReconstruction.ReconstructionProcessing)
        {
            GUILayout.Label(new GUIContent("[FPS Setting]"), style);
            SetReconstructionFPS = GUILayout.Toggle(SetReconstructionFPS, "Set reconstruction FPS");
            if (SetReconstructionFPS)
            {
                GUILayout.Box("Value: " + (int)Mathf.Round(ReconstructionFPS));
                float NewReconstructionFPS = GUILayout.HorizontalSlider(ReconstructionFPS, 1.0f, 60.0f);
                if (NewReconstructionFPS != ReconstructionFPS)
                {
                    SRWorkModule_API.SetReconstructionMaxFps((int)Mathf.Round(NewReconstructionFPS));
                    ReconstructionFPS = NewReconstructionFPS;
                }
            }
            // start / stop
            GUILayout.Label(new GUIContent("--Start/Stop--"), style);
            if (!ViveSR_RigidReconstruction.IsScanning && !ViveSR_RigidReconstruction.IsExportingMesh && !ViveSR_RigidReconstruction.IsDuringScannedMeshPreview || ViveSR_RigidReconstruction.IsScannedMeshPreviewCompleted)
            {
                if (GUILayout.Button("Start Reconstruction"))
                {
                    ViveSR_RigidReconstruction.StartScanning();
                }
            }

            if (ViveSR_RigidReconstruction.IsScanning && !ViveSR_RigidReconstruction.IsExportingMesh && !ViveSR_RigidReconstruction.IsDuringScannedMeshPreview)
            {
                if (GUILayout.Button("Stop Reconstruction"))
                {
                    ViveSR_RigidReconstruction.StopScanning();
                }

                // live extraction mode
                EditorGUILayout.Separator();
                GUILayout.Label(new GUIContent("--Live Extraction--"), style);
                int curMode = (int)ViveSR_RigidReconstructionRenderer.LiveMeshDisplayMode;
                GUILayout.BeginHorizontal();
                GUILayout.Label("Display Mode:");
                curMode = EditorGUILayout.Popup(curMode, displayMode);
                GUILayout.EndHorizontal();

                bool enableSector = GUILayout.Toggle(ViveSR_RigidReconstructionRenderer.EnableSector, "Enable Sectioned Mesh");
                if (enableSector != ViveSR_RigidReconstructionRenderer.EnableSector) ViveSR_RigidReconstructionRenderer.EnableSector = enableSector;

                int sectorGroupNum = EditorGUILayout.IntSlider("Sectioned Mesh Limit", ViveSR_RigidReconstructionRenderer.MaxActiveGO, 50, 500);
                if (sectorGroupNum != ViveSR_RigidReconstructionRenderer.MaxActiveGO) ViveSR_RigidReconstructionRenderer.MaxActiveGO = sectorGroupNum;

                if (curMode != (int)ViveSR_RigidReconstructionRenderer.LiveMeshDisplayMode)
                {
                    ViveSR_RigidReconstructionRenderer.LiveMeshDisplayMode = (ReconstructionDisplayMode)curMode;
                }
                // adaptive tunning
                if (curMode == (int)ReconstructionDisplayMode.ADAPTIVE_MESH)
                {
                    EditorGUILayout.Separator();
                    GUILayout.Label(new GUIContent("--Live Adaptive Mesh Tuning--"), style);
                    DrawAdaptiveParamUI(ViveSR_RigidReconstruction.LiveAdaptiveMaxGridSize, ViveSR_RigidReconstruction.LiveAdaptiveMinGridSize, ViveSR_RigidReconstruction.LiveAdaptiveErrorThres);
                    ViveSR_RigidReconstruction.LiveAdaptiveMaxGridSize = adaptiveLevel[maxSelectID];
                    ViveSR_RigidReconstruction.LiveAdaptiveMinGridSize = adaptiveLevel[minSelectID];
                    ViveSR_RigidReconstruction.LiveAdaptiveErrorThres = errorThres;
                }
            }

            // export
            EditorGUILayout.Separator();
            if (ViveSR_RigidReconstruction.IsScanning && !ViveSR_RigidReconstruction.IsExportingMesh && !ViveSR_RigidReconstruction.IsDuringScannedMeshPreview)
            {
                GUILayout.Label(new GUIContent("--Export--"), style);
                bool exportAdaptive = ViveSR_RigidReconstruction.ExportAdaptiveMesh;
                ViveSR_RigidReconstruction.ExportAdaptiveMesh = GUILayout.Toggle(exportAdaptive, "Export Adaptive Model");

                if (ViveSR_RigidReconstruction.ExportAdaptiveMesh)
                {
                    // live extraction mode
                    EditorGUILayout.Separator();
                    GUILayout.Label(new GUIContent("--Export Adaptive Mesh Tuning--"), style);
                    DrawAdaptiveParamUI(ViveSR_RigidReconstruction.ExportAdaptiveMaxGridSize, ViveSR_RigidReconstruction.ExportAdaptiveMinGridSize, ViveSR_RigidReconstruction.ExportAdaptiveErrorThres);
                    ViveSR_RigidReconstruction.ExportAdaptiveMaxGridSize = adaptiveLevel[maxSelectID];
                    ViveSR_RigidReconstruction.ExportAdaptiveMinGridSize = adaptiveLevel[minSelectID];
                    ViveSR_RigidReconstruction.ExportAdaptiveErrorThres = errorThres;
                }

                // only support adaptive mesh now
                if (GUILayout.Button("Preview Scanned Model"))
                {
                    ViveSR_RigidReconstruction.ExtractModelPreviewData();
                }

            }
            if (!ViveSR_RigidReconstruction.IsExportingMesh && !ViveSR_RigidReconstruction.IsDuringScannedMeshPreview && (ViveSR_RigidReconstruction.IsScanning != ViveSR_RigidReconstruction.IsScannedMeshPreviewCompleted))
            {
                if (GUILayout.Button("Start Export Model"))
                {
                    ViveSR_RigidReconstruction.StopScanning();
                    ViveSR_RigidReconstruction.ExportModel("Model");
                }
            }

            // Scene Understanding 
            // output surrounding objects of interest and their attributes 
            #region Scene Understanding
            EditorGUILayout.Separator();

            GUILayout.Label(new GUIContent("--Scene Understanding--"), style);
            if (ViveSR_RigidReconstruction.IsScanning)
            {
                bool isSemanticEnabled = GUILayout.Toggle(ViveSR_SceneUnderstanding.IsEnabledSceneUnderstanding, "Enable Scene Understanding");
                if (isSemanticEnabled != ViveSR_SceneUnderstanding.IsEnabledSceneUnderstanding)
                {
                    ViveSR_SceneUnderstanding.EnableSceneUnderstanding(isSemanticEnabled);
                }
            }
            if (ViveSR_SceneUnderstanding.IsEnabledSceneUnderstanding && ViveSR_RigidReconstruction.IsScanning)
            {
                bool isSemanticRefinementEnabled = GUILayout.Toggle(ViveSR_SceneUnderstanding.IsEnabledSceneUnderstandingRefinement, "Enable Scene Understanding Refinement");
                if (isSemanticRefinementEnabled != ViveSR_SceneUnderstanding.IsEnabledSceneUnderstandingRefinement)
                {
                    ViveSR_SceneUnderstanding.EnableSceneUnderstandingRefinement(isSemanticRefinementEnabled);
                }
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

                if (GUILayout.Button("Export SceneObjects (.xml)"))
                {
                    ViveSR_SceneUnderstanding.ExportSceneUnderstandingInfo(SemanticObjDir);
                }
            }
            if (GUILayout.Button("Load & Show SceneObjects BoundingBox"))
            {
                ViveSR_SceneUnderstanding.ImportSceneObjects(ReconstructionResultDir + ReconsSceneDir + SemanticObjDir);

                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.CHAIR, true, false);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.CEILING, true, false);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.FLOOR, true, false);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.WALL, true, false);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.BED, true, false);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.TABLE, true, false);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.MONITOR, true, false);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.WINDOW, true, false);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.FURNITURE, true, false);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.DOOR, true, false);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.PICTURE, true, false);
                ViveSR_SceneUnderstanding.ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType.PERSON, true, false);
            }

            if (GUILayout.Button("Destroy All SceneObjects BoundingBox"))
            {
                ViveSR_SceneUnderstanding.DestroySceneObjects();
            }
        }
        #endregion
    }

    private void DrawAdaptiveParamUI(float maxGridSize, float minGridSize, float thres)
    {
        GUILayout.Label("Adaptive Range (Max~Min):");
        GUILayout.BeginHorizontal();
        maxSelectID = adaptiveLevel.IndexOf(maxGridSize);
        minSelectID = adaptiveLevel.IndexOf(minGridSize);
        maxSelectID = EditorGUILayout.Popup(maxSelectID, adaptiveLable);
        minSelectID = EditorGUILayout.Popup(minSelectID, adaptiveLable);
        GUILayout.EndHorizontal();

        GUILayout.Label("Divide Threshold:");
        GUILayout.BeginHorizontal();
        errorThres = GUILayout.HorizontalSlider(thres, 0.0f, 1.5f);
        GUILayout.Label("" + errorThres.ToString("0.00"));
        GUILayout.EndHorizontal();
    }
}
