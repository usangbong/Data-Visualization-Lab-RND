using UnityEngine;
using System.Threading;
using System.Collections.Generic;
using System.Collections;

namespace Vive.Plugin.SR
{
    public class ViveSR_DualCameraDepthCollider : ViveSR_Module
    {

        private static bool _UpdateDepthCollider = false;
        private static bool _UpdateDepthColliderRange = true;
        private static bool _UpdateDepthColliderHoleFilling = true;
        private static bool _MeshColliderVisible = false;
        private float[] VertexData;
        private int[] CldIdxData;
        private int NumCldVertData;
        private int NumCldIdxData;

        private const int ShowGameObjCount = 20;
        private int LastDepthColliderUpdateTime = 0;

        public static GameObject ColliderObjs = null;
        private static MeshFilter ColliderMeshes = new MeshFilter();
        private static MeshCollider MeshClds = new MeshCollider();
        private static MeshRenderer ColliderMeshRenderer;
        private static int QualityScale = 8;
        private static double _ColliderNearDistance = 0.1;
        private static double _ColliderFarDistance = 10.0;

        // protect MeshDataVertices and MeshDataIndices
        private readonly object MeshLock = new object();

        public static float UpdateColliderNearDistance
        {
            get { return (float)_ColliderNearDistance; }
            set { if (value != _ColliderNearDistance) SetDepthColliderNearDistance(value); }
        }
        public static float UpdateColliderFarDistance
        {
            get { return (float)_ColliderFarDistance; }
            set { if (value != _ColliderFarDistance) SetDepthColliderFarDistance(value); }
        }

        #region Multi-Thread Get Mesh Data
        // Multi-thread Parse Raw Data to Data List for Mesh object 
        private Thread MeshDataThread = null;
        private Coroutine MeshDataCoroutine = null; // IEnumerator for main thread Mesh
        private List<Vector3> MeshDataVertices = new List<Vector3>();
        private List<int> MeshDataIndices = new List<int>();
        private bool IsMeshUpdate = false;
        private bool IsCoroutineRunning = false;
        private bool IsThreadRunning = true;
        private static int ThreadPeriod = 10;
        private int out_of_vertices_counter = 0;
        #endregion

        public static bool UpdateDepthCollider
        {
            get { return _UpdateDepthCollider; }
            set { if (value != _UpdateDepthCollider) SetColliderProcessEnable(value); }
        }

        public static bool UpdateDepthColliderHoleFilling
        {
            get { return _UpdateDepthColliderHoleFilling; }
            set { if (value != _UpdateDepthColliderHoleFilling) { SetDepthColliderHoleFillingEnable(value); } }
        }

        public static bool UpdateDepthColliderRange
        {
            get { return _UpdateDepthColliderRange; }
            set { if (value != _UpdateDepthColliderRange) SetColliderRangeEnable(value); }
        }

        public static bool ColliderMeshVisibility 
        {
            get { return _MeshColliderVisible; }
            set { if (value != _MeshColliderVisible) SetLiveMeshVisibility(value); }
        }
        public static Material ColliderDefaultMaterial
        {
            get
            {
                return new Material(Shader.Find("ViveSR/Wireframe"))
                {
                    color = new Color(0.51f, 0.94f, 1.0f)
                };
            }
        }

        public override bool Initial()
        {
            if (!ViveSR.Instance.EnableDepthModule)
            {
                return false;
            }
            if (ViveSR.FrameworkStatus == FrameworkStatus.WORKING)
            {
                ViveSR_DualCameraDepthExtra.InitialDepthCollider(ViveSR_DualCameraImageCapture.DepthImageWidth,
                                                                 ViveSR_DualCameraImageCapture.DepthImageHeight);
                if (ColliderObjs == null)
                {
                    ColliderObjs = new GameObject("Depth Collider");
                    ColliderObjs.transform.SetParent(gameObject.transform, false);

                    ColliderMeshes = ColliderObjs.AddComponent<MeshFilter>();
                    ColliderMeshes.mesh = new Mesh();
                    ColliderMeshes.mesh.MarkDynamic();

                    ChangeColliderMaterial(ColliderDefaultMaterial);

                    MeshClds = ColliderObjs.AddComponent<MeshCollider>();
                }
                ColliderObjs.SetActive(true);
                ColliderMeshVisibility = true;

                SetQualityScale(QualityScale);
                /*
                if (MeshDataThread == null)
                {
                    IsMeshUpdate = false;
                    IsCoroutineRunning = false;
                    IsThreadRunning = true;
                    MeshDataThread = new Thread(ExtractMeshDataThread) { IsBackground = true };
                    MeshDataThread.Start();
                }
                */
                IsMeshUpdate = false;
                IsCoroutineRunning = false;
                return true;
            }
            else
            {
                return false;
            }
        }

    public override bool Release()
        {
            if (ColliderObjs!=null)
                ColliderObjs.SetActive(false);

            UpdateDepthCollider = false;
            UpdateDepthColliderRange = true;
            UpdateDepthColliderHoleFilling = true;
            ColliderMeshVisibility = false;
            IsThreadRunning = false;
            if (MeshDataThread != null)
            {
                MeshDataThread.Join();
                MeshDataThread.Abort();
                MeshDataThread = null;
            }
            if (IsCoroutineRunning == true)
            {
                StopCoroutine(MeshDataCoroutine);
                MeshDataCoroutine = null;
            }
            
            ViveSR_DualCameraDepthExtra.ReleaseDepthCollider();
            MeshDataVertices.Clear();
            MeshDataIndices.Clear();
            return true;
        }

        public static bool ChangeColliderMaterial(Material mat)
        {
            if (ColliderObjs == null) return false;
            else if (ColliderMeshRenderer == null) ColliderMeshRenderer = ColliderObjs.AddComponent<MeshRenderer>();

            ColliderMeshRenderer.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off;
            ColliderMeshRenderer.material = mat;
            return true;
        }

        private void Update()
        {
            //initisl to open depth mesh
            //ViveSR_DualCameraImageCapture.EnableDepthProcess(true);

            //SetColliderProcessEnable(Is_enable_mesh);
            if ((_UpdateDepthCollider))
            {
                if (IsMeshUpdate == true)
                    MeshDataCoroutine = StartCoroutine(RenderMeshDataIEnumerator());
            }
        }

        private static bool SetColliderProcessEnable(bool value)
        {
            Debug.Log("SetColliderProcessEnable value = " + value);
            int result = (int)Error.FAILED;

            if (value)
            {
                result = SRWorkModule_API.SetSkipVGAProcess(false);
                result = SRWorkModule_API.LinkModule((int)ModuleType.DEPTH, (int)ModuleType.DEPTHMESH);
            }
            else
                result = SRWorkModule_API.UnlinkModule((int)ModuleType.DEPTH, (int)ModuleType.DEPTHMESH);

            if (value != _UpdateDepthCollider)
            {
                if (result == (int)Error.WORK)
                    result = SRWorkModule_API.SetDepthMeshIsEnable(value);
            }
            if (result == (int)Error.WORK)
            {
                _UpdateDepthCollider = value;
            }
            if (_UpdateDepthCollider == false)
            {
                ColliderMeshes.sharedMesh.Clear();
                ColliderMeshVisibility = false;
            }
            else
            {
                ColliderMeshVisibility = true;
            }

            return true;
        }

        public static bool SetDepthColliderHoleFillingEnable(bool value)
        {
            int result = SRWorkModule_API.SetDepthMeshParameterBool((int)DepthCmd.ENABLE_DEPTH_MESH_HOLE_FILLING, value);
            if (result == (int)Error.WORK)
            {
                _UpdateDepthColliderHoleFilling = value;
                return true;
            }
            return false;
        }

        private static bool SetColliderRangeEnable(bool value)
        {
            int result = SRWorkModule_API.SetDepthMeshParameterBool((int)DepthCmd.ENABLE_SELECT_MESH_DISTANCE_RANGE, value);
            if (result == (int)Error.WORK)
            {
                _UpdateDepthColliderRange = value;
                return true;
            }
            return false;
        }

        private void ExtractCurrentColliders()
        {
            ViveSR_DualCameraDepthExtra.GetDepthColliderData(ref NumCldVertData, out VertexData, ref NumCldIdxData, out CldIdxData);
            if (NumCldVertData != 0 && NumCldIdxData != 0)
            {
                lock (MeshLock) {
                    GenerateMeshColliders();
                }
            }
        }
        private void GenerateMeshColliders()
        {
            int numVert = NumCldVertData;
            int numIdx = NumCldIdxData;

            MeshDataVertices.Clear();
            MeshDataIndices.Clear();

            for (int i = 0; i < numVert; ++i)
            {
                float x = VertexData[i * 3];
                float y = VertexData[i * 3 + 1];
                float z = VertexData[i * 3 + 2];
                MeshDataVertices.Add(new Vector3(x, y, z));
            }

            for (int i = 0; i < numIdx; ++i) {
                if (CldIdxData[i] > numVert) {
                    IsMeshUpdate = false;
                    out_of_vertices_counter++;
                    if (out_of_vertices_counter > 100)
                        Debug.Log("depth mesh index doesn't match.");
                    return;
                }
                MeshDataIndices.Add(CldIdxData[i]);
            }
            out_of_vertices_counter = 0;
            IsMeshUpdate = true;

        }

        private static bool SetLiveMeshVisibility(bool value)
        {
            _MeshColliderVisible = value; 
            if (ColliderMeshes == null || ColliderObjs == null) return false;
            if (value == false && _UpdateDepthCollider == false) ColliderMeshes.sharedMesh.Clear();
            ColliderMeshRenderer.enabled = value;            
            return true;
        }
        public static bool SetColliderEnable(bool value)
        {
            if (value == false) {
                if (MeshClds != null) {
                    Destroy(MeshClds);
                }
                else {
                    return false;
                }
            }
            else {
                if (MeshClds != null)
                    return false;
                MeshClds = ColliderObjs.AddComponent<MeshCollider>();
                MeshClds.enabled = value;
            }
            return true;
        }


        public static bool GetQualityScale(out int value)
        {
            int result = SRWorkModule_API.GetDepthMeshParameterInt((int)DepthParam.COLLIDER_QUALITY, ref QualityScale);
            if (result == (int)Error.WORK)
            {
                value = QualityScale;
                return true;
            }
            else
            {
                value = -1;
                return false;
            }
        }
        public static bool SetQualityScale(int value)
        {
            int result = SRWorkModule_API.SetDepthMeshParameterInt((int)DepthParam.COLLIDER_QUALITY, value);
            if (result == (int)Error.WORK)
            {
                QualityScale = value;
                return true;
            }
            else
                return false;
        }

        private static bool SetDepthColliderNearDistance(double value)
        {
            value = (value > _ColliderFarDistance) ? _ColliderFarDistance : value;
            int result = SRWorkModule_API.SetDepthMeshParameterDouble((int)DepthParam.MESH_NEAR_DISTANCE, value);
            if (result == (int)Error.WORK)
            {
                _ColliderNearDistance = value;
                return true;
            }
            else
                return false;
        }

        private static bool SetDepthColliderFarDistance(double value)
        {
            value = (value < _ColliderNearDistance) ? _ColliderNearDistance : value;
            int result = SRWorkModule_API.SetDepthMeshParameterDouble((int)DepthParam.MESH_FAR_DISTANCE, value);
            if (result == (int)Error.WORK)
            {
                _ColliderFarDistance = value;
                return true;
            }
            else
                return false;
        }

        //IEnumerator//
        private IEnumerator RenderMeshDataIEnumerator()
        {
            IsCoroutineRunning = true;
            if (IsMeshUpdate == true)
            {
                // it is basically try lock, use try lock to avoid spending too much time in update()
                if (Monitor.TryEnter(MeshLock)) {
                    try {
                        ColliderMeshes.sharedMesh.Clear();
                        ColliderMeshes.sharedMesh.SetVertices(MeshDataVertices);
                        ColliderMeshes.sharedMesh.SetIndices(MeshDataIndices.ToArray(), MeshTopology.Triangles, 0);
                        MeshClds.sharedMesh = ColliderMeshes.sharedMesh;

                        IsMeshUpdate = false;
                    }
                    finally {
                        Monitor.Exit(MeshLock);
                    }
                }
            }
            IsCoroutineRunning = false;

            yield return 0;

        }

        public void ExtractMeshData()
        {
            try
            {
                if (IsMeshUpdate == false && _UpdateDepthCollider == true)
                {
                    ViveSR_DualCameraDepthExtra.GetDepthColliderFrameInfo();
                    int currentDepthColliderTimeIndex = ViveSR_DualCameraDepthExtra.DepthColliderTimeIndex;
                    if (currentDepthColliderTimeIndex != LastDepthColliderUpdateTime)
                    {
                        ExtractCurrentColliders();
                        LastDepthColliderUpdateTime = currentDepthColliderTimeIndex;
                    }
                }
            }
            catch (System.Exception e)
            {
                Debug.LogWarning(e.Message);
            }
        }

        private void ExtractMeshDataThread()
        {
            while (IsThreadRunning == true)
            {
                try
                {
                    if (IsMeshUpdate == false && _UpdateDepthCollider == true)
                    {
                        if (DepthMesh.SRWork_Depth_Mesh.UpdateData()) {
                            ViveSR_DualCameraDepthExtra.GetDepthColliderFrameInfo();
                            int currentDepthColliderTimeIndex = ViveSR_DualCameraDepthExtra.DepthColliderTimeIndex;
                            if (currentDepthColliderTimeIndex != LastDepthColliderUpdateTime)
                            {
                                ExtractCurrentColliders();
                                LastDepthColliderUpdateTime = currentDepthColliderTimeIndex;
                            }
                        }
                    }
                }
                catch (System.Exception e)
                {
                    Debug.LogWarning(e.Message);
                }

                Thread.Sleep(ThreadPeriod); //Avoid too fast get data from SR SDK DLL 
            }
        }
    }
}