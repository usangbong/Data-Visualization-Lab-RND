using UnityEngine;
using System.Runtime.InteropServices;
using System.Collections.Generic;
using System.Collections;
using System;
using System.IO;

namespace Vive.Plugin.SR
{
    public enum SceneUnderstandingObjectType
    {
        NONE,
        FLOOR,
        WALL,
        CEILING,
        CHAIR,
        TABLE,
        BED,
        MONITOR,
        WINDOW,
        FURNITURE,
        DOOR,
        PICTURE,
        PERSON,
        NumOfTypes // always the last
    };

    public class SceneUnderstandingObjects
    {
        public struct Element
        {
            public string tag;
            public int id;
            public string objfilename;
            public string cldfilename;
            public List<Vector3> position;

            public Vector3 forward;
            public Vector3 bBoxMinPoint;
            public Vector3 bBoxMaxPoint;
        }
        public SceneUnderstandingObjects(string fileDir)
        {
            if (Directory.Exists(fileDir))
            {
                DirectoryInfo dir = new DirectoryInfo(fileDir);

                FileInfo[] info_xml = dir.GetFiles("*.xml");
                elements.Clear();
                foreach (FileInfo f in info_xml)
                {
#if UNITY_EDITOR
                    bool res = ViveSR_FileTool.LoadListSerialData(ref elements, f.ToString());
                    if (res == false)
                        Debug.Log("UNITY_EDITOR_NO_FILE:" + f.ToString());
#else
                    string fullPath = dir.FullName + "/" + f;
                    bool res = ViveSR_FileTool.LoadListSerialData(ref elements, fullPath.ToString());
                    if(res==false)
                        Debug.Log("Not UNITY_EDITOR_NO_FILE : " + fullPath.ToString());
#endif

                }
            }
            else
            {
                Debug.Log(fileDir + " folder is empty");
            }
        }
        public void GetElementsBoundingBoxMeshes(int tagObj, Element tagIdElement, ref List<GameObject> boxObj)
        {
            List<int> MeshDataIndices = new List<int>();

            //top lines
            MeshDataIndices.Add(0); MeshDataIndices.Add(1);
            MeshDataIndices.Add(1); MeshDataIndices.Add(2);
            MeshDataIndices.Add(2); MeshDataIndices.Add(3);
            MeshDataIndices.Add(3); MeshDataIndices.Add(0);
            //bottom lines
            MeshDataIndices.Add(4); MeshDataIndices.Add(5);
            MeshDataIndices.Add(5); MeshDataIndices.Add(6);
            MeshDataIndices.Add(6); MeshDataIndices.Add(7);
            MeshDataIndices.Add(7); MeshDataIndices.Add(4);
            //vertical lines
            MeshDataIndices.Add(0); MeshDataIndices.Add(4);
            MeshDataIndices.Add(1); MeshDataIndices.Add(5);
            MeshDataIndices.Add(2); MeshDataIndices.Add(6);
            MeshDataIndices.Add(3); MeshDataIndices.Add(7);


            //foreach (Element each in GetElements(enums[tagObj]))
            {
                GameObject Obj = new GameObject("Box_" + tagIdElement.tag + "_" + tagIdElement.id);
                MeshFilter mf = Obj.AddComponent(typeof(MeshFilter)) as MeshFilter;
                MeshRenderer mr = Obj.AddComponent(typeof(MeshRenderer)) as MeshRenderer;
                mr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off;
                mr.material.shader = Shader.Find("UI/Default");
                mr.material.color = objetsColor[tagObj];
                mf.mesh = new Mesh();
                mf.mesh.MarkDynamic();
                List<Vector3> MeshDataVertices = new List<Vector3>();

                MeshDataVertices.Add(new Vector3(tagIdElement.bBoxMinPoint.x, tagIdElement.bBoxMinPoint.y, tagIdElement.bBoxMinPoint.z)); //0
                MeshDataVertices.Add(new Vector3(tagIdElement.bBoxMinPoint.x, tagIdElement.bBoxMinPoint.y, tagIdElement.bBoxMaxPoint.z)); //1
                MeshDataVertices.Add(new Vector3(tagIdElement.bBoxMaxPoint.x, tagIdElement.bBoxMinPoint.y, tagIdElement.bBoxMaxPoint.z)); //2
                MeshDataVertices.Add(new Vector3(tagIdElement.bBoxMaxPoint.x, tagIdElement.bBoxMinPoint.y, tagIdElement.bBoxMinPoint.z)); //3
                MeshDataVertices.Add(new Vector3(tagIdElement.bBoxMinPoint.x, tagIdElement.bBoxMaxPoint.y, tagIdElement.bBoxMinPoint.z)); //4
                MeshDataVertices.Add(new Vector3(tagIdElement.bBoxMinPoint.x, tagIdElement.bBoxMaxPoint.y, tagIdElement.bBoxMaxPoint.z)); //5
                MeshDataVertices.Add(new Vector3(tagIdElement.bBoxMaxPoint.x, tagIdElement.bBoxMaxPoint.y, tagIdElement.bBoxMaxPoint.z)); //6
                MeshDataVertices.Add(new Vector3(tagIdElement.bBoxMaxPoint.x, tagIdElement.bBoxMaxPoint.y, tagIdElement.bBoxMinPoint.z)); //7

                mf.sharedMesh.Clear();
                mf.sharedMesh.SetVertices(MeshDataVertices);
                mf.sharedMesh.SetIndices(MeshDataIndices.ToArray(), MeshTopology.Lines, 0);
                Obj.SetActive(false);
                boxObj.Add(Obj);
            }

        }

        public void GetElementsIcons(int tagObj, Element tagIdElement, ref List<GameObject> iconObj)
        {
            Texture iconTexture = (Texture)Resources.Load(GetElementName(tagObj));

            Mesh m = new Mesh();
            m.vertices = new Vector3[]
            {
                new Vector3(-0.15f,0,0),
                new Vector3(0.15f,0,0),
                new Vector3(-0.15f,0.3f,0),
                new Vector3(0.15f,0.3f,0)
            };
            m.uv = new Vector2[]
            {
                new Vector2(1,0),
                new Vector2(0,0),
                new Vector2(1,1),
                new Vector2(0,1)
            };
            m.triangles = new int[] { 0, 1, 2, 2, 1, 3 };


            //foreach (Element each in GetElements(enums[tagObj]))
            {
                GameObject Obj = new GameObject("Icon_" + tagIdElement.tag + "_" + tagIdElement.id);
                MeshFilter mf = Obj.AddComponent(typeof(MeshFilter)) as MeshFilter;
                MeshRenderer mr = Obj.AddComponent(typeof(MeshRenderer)) as MeshRenderer;
                Vector3 iconPosition;
                Vector2 compareX;
                Vector2 compareY;
                Vector2 compareZ;

                if (tagIdElement.bBoxMinPoint.x > tagIdElement.bBoxMaxPoint.x)
                {
                    compareX = new Vector2(tagIdElement.bBoxMinPoint.x, tagIdElement.bBoxMaxPoint.x);
                }
                else
                {
                    compareX = new Vector2(tagIdElement.bBoxMaxPoint.x, tagIdElement.bBoxMinPoint.x);
                }

                if (tagIdElement.bBoxMinPoint.y > tagIdElement.bBoxMaxPoint.y)
                {
                    compareY = new Vector2(tagIdElement.bBoxMinPoint.y, tagIdElement.bBoxMaxPoint.y);
                }
                else
                {
                    compareY = new Vector2(tagIdElement.bBoxMaxPoint.y, tagIdElement.bBoxMinPoint.y);
                }

                if (tagIdElement.bBoxMinPoint.z > tagIdElement.bBoxMaxPoint.z)
                {
                    compareZ = new Vector2(tagIdElement.bBoxMinPoint.z, tagIdElement.bBoxMaxPoint.z);
                }
                else
                {
                    compareZ = new Vector2(tagIdElement.bBoxMaxPoint.z, tagIdElement.bBoxMinPoint.z);
                }

                if (tagIdElement.tag == "Chair" || tagIdElement.tag == "Table" || tagIdElement.tag == "Bed" || tagIdElement.tag == "Floor")
                {
                    iconPosition = new Vector3(compareX.y + (compareX.x - compareX.y) / 2, compareY.x, compareZ.y + (compareZ.x - compareZ.y) / 2);
                }
                else if (tagIdElement.tag == "Ceiling")
                {
                    iconPosition = new Vector3(compareX.y + (compareX.x - compareX.y) / 2, compareY.y, compareZ.y + (compareZ.x - compareZ.y) / 2);
                }
                else if (tagIdElement.tag == "Wall" || tagIdElement.tag == "Window" || tagIdElement.tag == "Monitor" || tagIdElement.tag == "Door" || tagIdElement.tag == "Picture")
                {
                    iconPosition = new Vector3(compareX.y + (compareX.x - compareX.y) / 2, compareY.y + (compareY.x - compareY.y) / 2, compareZ.x);
                }
                else if (tagIdElement.tag == "Furniture" || tagIdElement.tag == "Person")
                {
                    iconPosition = new Vector3(compareX.y + (compareX.x - compareX.y) * 0.5f, compareY.y + (compareY.x - compareY.y) * 0.5f, compareZ.y + (compareZ.x - compareZ.y) * 0.5f);
                }
                else
                {
                    iconPosition = new Vector3(0, 0, 0);
                }

                Obj.transform.Translate(iconPosition);

                mf.mesh = m;
                m.RecalculateBounds();
                m.RecalculateNormals();
                mr.material.shader = Shader.Find("UI/Default");
                mr.material.mainTexture = iconTexture;
                Obj.SetActive(false);
                iconObj.Add(Obj);
            }
        }

        public Element[] GetElements(int tag)
        {
            return GetElements(enums[tag]);
        }

        public Element[] GetElements()
        {
            return elements.ToArray();
        }

        public string GetElementName(int tag)
        {
            return enums[tag];
        }

        public int GetNElement()
        {
            return elements.Count;
        }
        //"Floor", "Wall", "Ceiling", "Chair", "Table", "Bed", "Window", "Monitor"
        private Color[] objetsColor = new[] { Color.clear, Color.yellow, Color.blue, Color.cyan, Color.green, Color.red, Color.black, Color.magenta, Color.grey, new Color(160.0f, 32.0f, 240.0f), new Color(218.0f, 112.0f, 214.0f), new Color(227.0f, 168.0f, 105.0f), new Color(107.0f, 142.0f, 35.0f) };
        private String[] enums = new[] { "None", "Floor", "Wall", "Ceiling", "Chair", "Table", "Bed", "Monitor", "Window", "Furniture", "Door", "Picture", "Person" };
        private List<Element> elements = new List<Element>();
        private Element[] GetElements(string tag)
        {
            List<Element> matchs = new List<Element>();
            foreach (Element each in elements)
            {
                if (each.tag == tag) matchs.Add(each);
            }
            return matchs.ToArray();
        }
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct SceneUnderstandingConfig
    {
        public int nFloorMaxInst;
        public int nWallMaxInst;
        public int nCeilingMaxInst;
        public int nChairMaxInst;
        public int nTableMaxInst;
        public int nBedMaxInst;
        public int nMonitorMaxInst;
        public int nWindowMaxInst;
        public int nFurnitureMaxInst;
        public int nDoorMaxInst;
        public int nPictureMaxInst;
        public int nPersonMaxInst;
    };

    public class ViveSR_SceneUnderstanding
    {
        public static bool IsEnabledSceneUnderstanding = false;
        public static bool IsEnabledSceneUnderstandingRefinement = true;
        public static bool IsEnabledSceneUnderstandingView = false;
        public static bool IsExportingSceneUnderstandingInfo = false;
        public static string SemanticObjDir = "SceneUnderstanding/";

        private delegate void ExportProgressCallback(int stage, int percentage);
        private static int ScUndProcessingStage = 0;
        private static int ScUndProcessingProgressBar = 0;

        public static void ResetParameter()
        {
            IsEnabledSceneUnderstanding = false;
            IsEnabledSceneUnderstandingRefinement = true;
            IsEnabledSceneUnderstandingView = false;
            IsExportingSceneUnderstandingInfo = false;
            ScUndProcessingProgressBar = 0;
            ScUndProcessingProgressBar = 0;
        }

        public static void EnableSceneUnderstanding(bool enable)
        {
            int result = SRWorkModule_API.SetReconstructionParameterBool((int)ReconstructionParam.SCENE_UNDERSTANDING_ENABLE, enable);

            if (result == (int)Error.WORK)
                IsEnabledSceneUnderstanding = enable;
            else
            {
                Debug.Log("[ViveSR] [Scene Understanding] Activation/Deactivation failed");
                return;
            }

            if (IsEnabledSceneUnderstanding)
            {
                //result = ViveSR_Framework.RegisterCallback(ViveSR_Framework.MODULE_ID_RIGID_RECONSTRUCTION, (int)ReconstructionCallback.SCENE_UNDERSTANDING_PROGRESS, Marshal.GetFunctionPointerForDelegate((ExportProgressCallback)UpdateSceneUnderstandingProgress));
                if (result != (int)Error.WORK)
                    Debug.Log("[ViveSR] [Scene Understanding] Progress listener failed to register");
            }
            else if (IsEnabledSceneUnderstandingView)
                EnableSceneUnderstandingView(false);
        }

        public static void EnableSceneUnderstandingRefinement(bool enable)
        {
            int result;

            result = SRWorkModule_API.SetReconstructionParameterBool((int)ReconstructionParam.SCENE_UNDERSTANDING_REFINEMENT, enable);
            if (result == (int)Error.WORK)
            {
                IsEnabledSceneUnderstandingRefinement = enable;
                //Debug.Log("[ViveSR] [Scene Understanding] Refinement " + (enable ? "enabled" : "disabled"));
            }
            else
                Debug.Log("[ViveSR] [Scene Understanding] Setting Refinement failed");

        }

        public static void EnableSceneUnderstandingView(bool enable)
        {
            int result = 0;

            if (!ViveSR_RigidReconstruction.IsScanning) return;

            result = SRWorkModule_API.SetReconstructionParameterBool((int)ReconstructionParam.SCENE_UNDERSTANDING_MACHINE_VISION, enable);
            if (result == (int)Error.WORK)
            {
                IsEnabledSceneUnderstandingView = enable;
                Debug.Log("[ViveSR] [Scene Understanding] Preview " + (enable ? "enabled" : "disabled"));

                if (IsEnabledSceneUnderstandingView)
                {
                    ViveSR_RigidReconstructionRenderer.EnableSector = false;
                    ViveSR_RigidReconstructionRenderer.SetWireFrameOpaque = false;
                }
                else
                {
                    // ViveSR_RigidReconstructionRenderer.EnableSector = true;
                    ViveSR_RigidReconstructionRenderer.SetWireFrameOpaque = true;

                    ResetSceneUnderstandingProgress();
                }
            }
        }
        private static bool ReconstructionSectorSetting;
        public static void ExportSceneUnderstandingInfo(string filename)
        {
            ResetSceneUnderstandingProgress();
            //if ((int)Error.WORK != SRWorkModule_API.RegisterSceneUnderstandingCallback(Marshal.GetFunctionPointerForDelegate((ExportProgressCallback)UpdateSceneUnderstandingProgress)))
            //    Debug.Log("[ViveSR] [Scene Understanding] Progress listener failed to register");
            ReconstructionSectorSetting = ViveSR_RigidReconstructionRenderer.EnableSector;
            ViveSR_RigidReconstructionRenderer.EnableSector = false;
            byte[] bytearray = System.Text.Encoding.ASCII.GetBytes(filename);
            IntPtr parameter = Marshal.AllocCoTaskMem(filename.Length);
            Marshal.Copy(bytearray, 0, parameter, filename.Length);
            SRWorkModule_API.SetSceneUnderstandingOutputFileName(parameter, filename.Length);

            IsExportingSceneUnderstandingInfo = true;
        }

        private static void ResetSceneUnderstandingProgress()
        {
            ScUndProcessingProgressBar = 0;
            ScUndProcessingStage = 0;
        }

        private static void UpdateSceneUnderstandingProgress(int stage, int percentage)
        {

            if (stage == (int)ReconstructionExportStage.SCENE_UNDERSTANDING_PASS_1) ScUndProcessingStage = 0;
            else if (stage == (int)ReconstructionExportStage.SCENE_UNDERSTANDING_PASS_2) ScUndProcessingStage = 1;
            ScUndProcessingProgressBar = percentage;
            // Debug.Log("[ViveSR] [Scene Understanding] Progress : " + GetSceneUnderstandingProgress());

            if (IsExportingSceneUnderstandingInfo)
            {
                Debug.Log("[ViveSR] [Scene Understanding] Progress : " + GetSceneUnderstandingProgress());

                if (GetSceneUnderstandingProgress() == 100)
                {
                    Debug.Log("[ViveSR] [Scene Understanding] Finished");
                    //ViveSR_RigidReconstructionRenderer.EnableSector = true;
                    IsExportingSceneUnderstandingInfo = false;
                    //if ((int)Error.WORK != SRWorkModule_API.UnregisterSceneUnderstandingCallback())
                    //    Debug.Log("[ViveSR] [Scene Understanding] Progress listener failed to unregister");
                }
            }
        }

        public static void UpdateSceneUnderstandingProgress()
        {
            SRWorkModule_API.GetSceneUnderstandingProgress(ref ScUndProcessingProgressBar);
            if (ScUndProcessingProgressBar == 100)
            {
                IsExportingSceneUnderstandingInfo = false;
                ViveSR_RigidReconstructionRenderer.EnableSector = ReconstructionSectorSetting;
            }
        }

        public static void GetSceneUnderstandingProgress(ref int stage, ref int percentage)
        {
            stage = ScUndProcessingStage;
            percentage = ScUndProcessingProgressBar;
        }

        public static int GetSceneUnderstandingProgress()
        {
            /*
            const float ProportionStage1 = 0.6f;
            const float ProportionStage2 = 0.4f;
            int percentage = 0;
            if (ScUndProcessingStage == 0) percentage = (int)(ProportionStage1 * ScUndProcessingProgressBar);
            if (ScUndProcessingStage == 1) percentage = (int)(ProportionStage1 * 100 + ProportionStage2 * ScUndProcessingProgressBar);
            return percentage;
            */

            return ScUndProcessingProgressBar;
        }

        public static void GetSceneUnderstandingConfig(ref SceneUnderstandingConfig config)
        {
            SRWorkModule_API.GetSceneUnderstandingConfig(ref config);
        }

        public static void SetSceneUnderstandingConfig(SceneUnderstandingConfig config)
        {
            SRWorkModule_API.SetSceneUnderstandingConfig(config);
        }

        public static void SetCustomSceneUnderstandingConfig(SceneUnderstandingObjectType objectType, int objectMaxNum, bool isOn)
        {
            SceneUnderstandingConfig config = new SceneUnderstandingConfig();

            GetSceneUnderstandingConfig(ref config);

            switch (objectType)
            {
                case SceneUnderstandingObjectType.BED:
                    if (isOn) config.nBedMaxInst = objectMaxNum;
                    else config.nBedMaxInst = 0;
                    break;
                case SceneUnderstandingObjectType.CEILING:
                    if (isOn) config.nCeilingMaxInst = objectMaxNum;
                    else config.nCeilingMaxInst = 0;
                    break;
                case SceneUnderstandingObjectType.CHAIR:
                    if (isOn) config.nChairMaxInst = objectMaxNum;
                    else config.nChairMaxInst = 0;
                    break;
                case SceneUnderstandingObjectType.FLOOR:
                    if (isOn) config.nFloorMaxInst = objectMaxNum;
                    else config.nFloorMaxInst = 0;
                    break;
                case SceneUnderstandingObjectType.TABLE:
                    if (isOn) config.nTableMaxInst = objectMaxNum;
                    else config.nTableMaxInst = 0;
                    break;
                case SceneUnderstandingObjectType.WALL:
                    if (isOn) config.nWallMaxInst = objectMaxNum;
                    else config.nWallMaxInst = 0;
                    break;
                case SceneUnderstandingObjectType.WINDOW:
                    if (isOn) config.nWindowMaxInst = objectMaxNum;
                    else config.nWindowMaxInst = 0;
                    break;
                case SceneUnderstandingObjectType.MONITOR:
                    if (isOn) config.nMonitorMaxInst = objectMaxNum;
                    else config.nMonitorMaxInst = 0;
                    break;
                case SceneUnderstandingObjectType.FURNITURE:
                    if (isOn) config.nFurnitureMaxInst = objectMaxNum;
                    else config.nFurnitureMaxInst = 0;
                    break;
                case SceneUnderstandingObjectType.DOOR:
                    if (isOn) config.nDoorMaxInst = objectMaxNum;
                    else config.nDoorMaxInst = 0;
                    break;
                case SceneUnderstandingObjectType.PICTURE:
                    if (isOn) config.nPictureMaxInst = objectMaxNum;
                    else config.nPictureMaxInst = 0;
                    break;
                case SceneUnderstandingObjectType.PERSON:
                    if (isOn) config.nPersonMaxInst = objectMaxNum;
                    else config.nPersonMaxInst = 0;
                    break;
            }
            SetSceneUnderstandingConfig(config);
        }

        public static void SetAllCustomSceneUnderstandingConfig(int objectMaxNum, bool isOn)
        {
            for (int i = 0; i < (int)SceneUnderstandingObjectType.NumOfTypes; i++)
            {
                SetCustomSceneUnderstandingConfig((SceneUnderstandingObjectType)i, objectMaxNum, isOn);
            }
        }

        public static SceneUnderstandingObjectType GetSemanticTypeFromObjName(string str)
        {
            if (str.Contains("Floor")) return SceneUnderstandingObjectType.FLOOR;
            else if (str.Contains("Wall")) return SceneUnderstandingObjectType.WALL;
            else if (str.Contains("Ceiling")) return SceneUnderstandingObjectType.CEILING;
            else if (str.Contains("Chair")) return SceneUnderstandingObjectType.CHAIR;
            else if (str.Contains("Table")) return SceneUnderstandingObjectType.TABLE;
            else if (str.Contains("Bed")) return SceneUnderstandingObjectType.BED;
            else if (str.Contains("Monitor")) return SceneUnderstandingObjectType.MONITOR;
            else if (str.Contains("Window")) return SceneUnderstandingObjectType.WINDOW;
            else if (str.Contains("Furniture")) return SceneUnderstandingObjectType.FURNITURE;
            else if (str.Contains("Door")) return SceneUnderstandingObjectType.DOOR;
            else if (str.Contains("Picture")) return SceneUnderstandingObjectType.PICTURE;
            else if (str.Contains("Person")) return SceneUnderstandingObjectType.PERSON;
            else return SceneUnderstandingObjectType.NONE;
        }

        public static string SemanticTypeToString(SceneUnderstandingObjectType type)
        {
            if (type == SceneUnderstandingObjectType.FLOOR) return "Floor";
            else if (type == SceneUnderstandingObjectType.WALL) return "Wall";
            else if (type == SceneUnderstandingObjectType.CEILING) return "Ceiling";
            else if (type == SceneUnderstandingObjectType.CHAIR) return "Chair";
            else if (type == SceneUnderstandingObjectType.TABLE) return "Table";
            else if (type == SceneUnderstandingObjectType.BED) return "Bed";
            else if (type == SceneUnderstandingObjectType.MONITOR) return "Monitor";
            else if (type == SceneUnderstandingObjectType.WINDOW) return "Window";
            else if (type == SceneUnderstandingObjectType.FURNITURE) return "Furniture";
            else if (type == SceneUnderstandingObjectType.DOOR) return "Door";
            else if (type == SceneUnderstandingObjectType.PICTURE) return "Picture";
            else if (type == SceneUnderstandingObjectType.PERSON) return "Person";
            else return "NONE";
        }

        public struct SceneObject
        {
            public string name;
            public SceneUnderstandingObjectType objTypeID;
            public int objID;
            public string objFileName;
            public string cldFileName;
            public Vector3 forward;
            public List<Vector3> positions;
            public List<GameObject> BoundingBoxGameObj;
            public List<GameObject> IconGameObj;

            public SceneObject Clone()
            {
                SceneObject output = new SceneObject();
                output = this;
                return output;
            }

            public void SetName(string name)
            {
                this.name = name;
            }

            public void Clear()
            {
                objTypeID = SceneUnderstandingObjectType.NONE;
                objID = -1;
                objFileName = "";
                cldFileName = "";
                forward = new Vector3();

                if (positions == null) positions = new List<Vector3>();
                else positions.Clear();

                if (BoundingBoxGameObj == null) BoundingBoxGameObj = new List<GameObject>();
                else
                {
                    foreach (GameObject obj in BoundingBoxGameObj)
                    {
                        if (obj != null)
                            GameObject.Destroy(obj);
                    }
                    BoundingBoxGameObj.Clear();
                }

                if (IconGameObj == null) IconGameObj = new List<GameObject>();
                else
                {
                    foreach (GameObject obj in IconGameObj)
                    {
                        if (obj != null)
                            GameObject.Destroy(obj);
                    }
                    IconGameObj.Clear();
                }
            }
        }

        public static List<SceneObject> ShowSceneObjects = new List<SceneObject>();


        public static void DestroySceneObjects()
        {
            foreach (SceneObject obj in ShowSceneObjects) obj.Clear();
            ShowSceneObjects.Clear();
        }

        public static void SetIconLookAtPlayer(Transform player)
        {
            foreach (SceneObject obj in ShowSceneObjects)
            {
                foreach (GameObject icon in obj.IconGameObj)
                {
                    icon.transform.LookAt(player);
                }
            }
        }

        public static bool ShowSemanticBoundingBoxAndIconWithType(SceneUnderstandingObjectType objType, bool boxIsVisible, bool iconIsVisible)
        {
            bool found = false;
            foreach (SceneObject ssobj in ShowSceneObjects)
            {
                if (ssobj.objTypeID == objType)
                {
                    found = true;
                    foreach (GameObject obj in ssobj.BoundingBoxGameObj) { if (obj != null) { obj.SetActive(boxIsVisible); } }
                    foreach (GameObject obj in ssobj.IconGameObj) { if (obj != null) { obj.SetActive(iconIsVisible); } }
                }
            }
            return found;
        }

        public static void SetAllSemanticBoundingBoxAndIconVisible(bool boxIsVisible, bool iconIsVisible)
        {
            foreach (SceneObject ssobj in ShowSceneObjects)
            {
                foreach (GameObject obj in ssobj.BoundingBoxGameObj) { if (obj != null) { obj.SetActive(boxIsVisible); } }
                foreach (GameObject obj in ssobj.IconGameObj) { if (obj != null) { obj.SetActive(iconIsVisible); } }
            }
        }

        public static void ShowAllSemanticBoundingBoxAndIcon()
        {
            SetAllSemanticBoundingBoxAndIconVisible(true, true);
        }

        public static void HideAllSemanticBoundingBoxAndIcon()
        {
            SetAllSemanticBoundingBoxAndIconVisible(false, false);
        }

        public static void ShowSemanticBoundingBoxAndIconWithId(SceneUnderstandingObjectType objType, int objId, bool IsShowingBox, bool IsShowingIcon)
        {
            foreach (SceneObject ssobj in ShowSceneObjects)
            {
                if (ssobj.objTypeID == objType && ssobj.objID == objId)
                {
                    foreach (GameObject obj in ssobj.BoundingBoxGameObj)
                    {
                        if (obj != null)
                            obj.SetActive(IsShowingBox);
                    }

                    foreach (GameObject obj in ssobj.IconGameObj)
                    {
                        if (obj != null)
                            obj.SetActive(IsShowingIcon);
                    }
                }
            }
        }

        public static void ImportSceneObjectsByType(string dirPath, SceneUnderstandingObjectType objType)
        {
            SceneUnderstandingObjects SceneObj = new SceneUnderstandingObjects(dirPath);

            foreach (SceneObject ssobj in ShowSceneObjects)
            {
                if (ssobj.objTypeID == objType)
                {
                    foreach (GameObject obj in ssobj.BoundingBoxGameObj)
                    {
                        if (obj != null)
                            GameObject.Destroy(obj);
                    }
                }
            }
            if (SceneObj.GetNElement() < 1)
            {
                Debug.Log("Scene semantic [" + SceneObj.GetElementName((int)objType) + "] data is empty");
                return;
            }
            //Comment in ViveSR
            //else
            //{
            //    foreach (SceneUnderstandingObjects.Element each in SceneObj.GetElements(objType))
            //    {
            //        Debug.Log("id[" + each.id + "] tag[" + each.tag + "]");

            //        Debug.Log("objfilename = " + each.objfilename);
            //        Debug.Log("cldfilename = " + each.cldfilename);
            //        Debug.Log("pos num = " + each.position.Count);
            //        foreach (var pos in each.position)
            //        {
            //            Debug.Log("pos idx = " + each.position.IndexOf(pos));
            //            Debug.Log("pos.x = " + pos.x);
            //            Debug.Log("pos.y = " + pos.y);
            //            Debug.Log("pos.z = " + pos.z);
            //        }
            //        //Debug.Log("forward = " + each.forward);
            //        Debug.Log("bBoxMinPoint = " + each.bBoxMinPoint);
            //        Debug.Log("bBoxMaxPoint = " + each.bBoxMaxPoint);
            //    }
            //}

            #region Get Object Bounding Box
            foreach (SceneUnderstandingObjects.Element element in SceneObj.GetElements((int)objType))
            {
                SceneObject scene_obj = new SceneObject();
                scene_obj.BoundingBoxGameObj = new List<GameObject>();
                scene_obj.IconGameObj = new List<GameObject>();
                scene_obj.objTypeID = (SceneUnderstandingObjectType)objType;
                scene_obj.objID = element.id;
                scene_obj.objFileName = element.objfilename;
                scene_obj.cldFileName = element.cldfilename;
                scene_obj.forward = element.forward;
                scene_obj.positions = element.position;
                SceneObj.GetElementsBoundingBoxMeshes((int)objType, element, ref scene_obj.BoundingBoxGameObj);
                SceneObj.GetElementsIcons((int)objType, element, ref scene_obj.IconGameObj);
                ShowSceneObjects.Add(scene_obj);
            }
            #endregion
        }

        public static void ImportSceneObjects(string dirPath)
        {
            // clear
            foreach (SceneObject obj in ShowSceneObjects) obj.Clear();

            ShowSceneObjects.Clear();

            SceneUnderstandingObjects SceneObj = new SceneUnderstandingObjects(dirPath);
            if (SceneObj.GetNElement() < 1)
            {
                Debug.Log("Scene object data in " + dirPath + " is empty.");
                return;
            }

            #region Set scene object data
            for (int objType = 0; objType < (int)SceneUnderstandingObjectType.NumOfTypes; objType++)
            {
                foreach (SceneUnderstandingObjects.Element element in SceneObj.GetElements(objType))
                {
                    SceneObject scene_obj = new SceneObject();
                    scene_obj.BoundingBoxGameObj = new List<GameObject>();
                    scene_obj.IconGameObj = new List<GameObject>();
                    scene_obj.objTypeID = (SceneUnderstandingObjectType)objType;
                    scene_obj.objID = element.id;
                    scene_obj.objFileName = element.objfilename;
                    scene_obj.cldFileName = element.cldfilename;
                    scene_obj.forward = element.forward;
                    scene_obj.positions = element.position;
                    SceneObj.GetElementsBoundingBoxMeshes(objType, element, ref scene_obj.BoundingBoxGameObj);
                    SceneObj.GetElementsIcons(objType, element, ref scene_obj.IconGameObj);
                    ShowSceneObjects.Add(scene_obj);
                }
            }
            #endregion
        }

        public static void SetGameObjectByFileName(string fileName, string goName)
        {
            for (int i = 0; i < ShowSceneObjects.Count; i++)
                //foreach (SceneObject obj in ShowSceneObjects)
                if (ShowSceneObjects[i].cldFileName == fileName || ShowSceneObjects[i].objFileName == fileName)
                {
                    SceneObject obj = ShowSceneObjects[i].Clone();
                    obj.name = goName;
                    ShowSceneObjects[i] = obj;
                }
            //        ShowSceneObjects[i].SetName(goName);
        }

        public static SceneObject GetCorrespondingSceneObject(string goName)
        {
            foreach (SceneObject obj in ShowSceneObjects)
            {
                if (obj.name == goName)
                    return obj.Clone();
            }

            SceneObject emptyObj = new SceneObject();
            emptyObj.Clear();
            return emptyObj;
        }

        public static string[] GetColliderFileNames()
        {
            List<string> nameList = new List<string>();
            foreach (SceneObject obj in ShowSceneObjects) nameList.Add(obj.cldFileName);
            return nameList.ToArray();
        }

        public static string[] GetColliderFileNamesByType(SceneUnderstandingObjectType objType)
        {
            List<string> nameList = new List<string>();
            foreach (SceneObject obj in ShowSceneObjects)
                if (objType == obj.objTypeID)
                    nameList.Add(obj.cldFileName);

            return nameList.ToArray();
        }

        public static List<Vector3> GetPlacedPositionsByID(SceneUnderstandingObjectType objType, int objId)
        {
            List<Vector3> positions = new List<Vector3>();
            foreach (SceneObject obj in ShowSceneObjects)
            {
                if (obj.objTypeID == objType && obj.objID == objId)
                    positions.AddRange(obj.positions);
            }
            return positions;
        }

        public static List<Vector3> GetPlacedPositionsByType(SceneUnderstandingObjectType objType)
        {
            List<Vector3> positions = new List<Vector3>();
            foreach (SceneObject obj in ShowSceneObjects)
            {
                if (obj.objTypeID == objType)
                    positions.AddRange(obj.positions);
            }
            return positions;
        }

        public static List<Vector3> GetAllPlacedPositions()
        {
            List<Vector3> positions = new List<Vector3>();
            foreach (SceneObject obj in ShowSceneObjects)
            {
                positions.AddRange(obj.positions);
            }
            return positions;
        }
    };

}
