using UnityEngine;
using System.Collections;
using System.Linq;
using System.Collections.Generic;
using System;
namespace PieChart.ViitorCloud
{
    public class PieChartMesh : MonoBehaviour
    {

        float[] mData;

        int mSlices;
        float mRotationAngle;
        float mRadius;
        Material mMaterial;

        PieChartMeshController PieContorller;

        Vector3[] mVertices, WRVertices;
        Vector3[] FinalVerticesArray;
        Vector3[] mNormals;
        Vector3 mNormal = new Vector3(0, 0, -1);
        Vector3 mWRNormal = new Vector3(1, 1, 1);
        Vector2[] mUvs;
        int[] mTriangles;

        public GameObject[] gameObjs;

        int[] subTris;
        int[] subTris3D;
        int[] subTrisLeft;
        int[] subTrisRight;
        int[] sidetrinaglesFinal;

        float delay = 0.1f;
        GameObject TempObject;

        bool partcreated;

        public PieChartMeshController.AnimationType animationType;


        public void Init(float[] data, Material mainMaterial, float speed, GameObject otherobject, PieChartMeshController.AnimationType animationType)
        {
            this.animationType = animationType;
            if (animationType == PieChartMeshController.AnimationType.UpDown || animationType == PieChartMeshController.AnimationType.UpDownAndRotation)
            {
                mData = data;
                Array.Sort(mData);
            }
            else
                mData = data;
            TempObject = otherobject;
            mSlices = 100;
            mRotationAngle = -90;
            mRadius = 100;
            delay = speed;
            mMaterial = mainMaterial;
            Init(data);
        }

        public void Init(float[] data)
        {
            PieContorller = GetComponent<PieChartMeshController>();
            mSlices = 100;
            mRotationAngle = 90f;
            mRadius = 0.3f;

            mData = data;
        }

        public void Draw(float[] data)
        {
            mData = data;
            StopAllCoroutines();
            StartCoroutine(Draw());
        }

        public IEnumerator Draw()
        {
            yield return new WaitForEndOfFrame();
            //Check data validity for pie chart...
            while (mData == null)
            {
                Debug.LogError("PieChart: Data null");
                yield break;
            }
            if (gameObjs == null)
                gameObjs = new GameObject[mData.Length];

            float zscale = -17.3388f;
            for (int i = 0; i < mData.Length; i++)
            {
                if (mData[i] < 0)
                {
                    Debug.LogError("PieChart: Data < 0");
                    yield break;
                }
                gameObjs[i] = Instantiate(TempObject);
                gameObjs[i].transform.parent = PieContorller.parent.transform;
                gameObjs[i].transform.localPosition = Vector3.zero;
                if (animationType == PieChartMeshController.AnimationType.UpDown || animationType == PieChartMeshController.AnimationType.UpDownAndRotation)
                {
                    gameObjs[i].transform.localScale = new Vector3(4.878767f, 4.878767f, zscale);
                    zscale -= 3;
                }
            }

            // Calculate sum of data values
            float sumOfData = 0;
            foreach (float value in mData)
            {
                sumOfData += value;
            }
            if (sumOfData <= 0)
            {
                Debug.LogError("PieChart: Data sum <= 0");
                yield break;
            }
            // Determine how many triangles in slice
            int[] slice = new int[mData.Length];
            int numOfTris = 0;
            int numOfSlices = 0;
            int countedSlices = 0;

            // Caluclate slice size
            for (int i = 0; i < mData.Length; i++)
            {
                numOfTris = (int)((mData[i] / sumOfData) * mSlices);
                slice[numOfSlices++] = numOfTris;
                countedSlices += numOfTris;
            }
            // Check that all slices are counted.. if not -> add/sub to/from biggest slice..
            int idxOfLargestSlice = 0;
            int largestSliceCount = 0;
            for (int i = 0; i < mData.Length; i++)
            {
                if (largestSliceCount < slice[i])
                {
                    idxOfLargestSlice = i;
                    largestSliceCount = slice[i];
                }
            }

            // Check validity for pie chart
            if (countedSlices == 0)
            {
                Debug.LogError("Check data");
                yield break;
            }

            // Adjust largest dataset to get proper slice
            slice[idxOfLargestSlice] += mSlices - countedSlices;

            // Check validity for pie chart data
            if (slice[idxOfLargestSlice] <= 0)
            {
                Debug.LogError("Check data");
                yield break;
            }

            // Init vertices and triangles arrays
            mVertices = new Vector3[mSlices * 3];
            WRVertices = new Vector3[mSlices * 3];
            FinalVerticesArray = new Vector3[mSlices * 6];

            mNormals = new Vector3[mSlices * 3];

            mUvs = new Vector2[mSlices * 6];

            mTriangles = new int[mSlices * 6];
            //WRTriangles = new int[mSlices * 3];
            //FinalTriangles = new int[mSlices * 3];

            //gameObject.AddComponent("MeshFilter");
            //gameObject.AddComponent("MeshRenderer");

            //Mesh mesh = ((MeshFilter)GetComponent("MeshFilter")).mesh;
            //mesh.Clear();

            //mesh.name = "Pie Chart Mesh";

            // Roration offset (to get star point to "12 o'clock")
            float rotOffset = mRotationAngle / 360f * 2f * Mathf.PI;

            // Calc the points in circle
            float angle;
            float[] x = new float[mSlices];
            float[] y = new float[mSlices];

            for (int i = 0; i < mSlices; i++)
            {
                angle = i * 2f * Mathf.PI / mSlices;
                x[i] = (Mathf.Cos(angle + rotOffset) * mRadius);
                y[i] = (Mathf.Sin(angle + rotOffset) * mRadius);
            }
            // Generate mesh with slices (vertices and triangles)
            for (int i = 0; i < mSlices; i++)
            {
                mVertices[i * 3 + 0] = new Vector3(0f, 0f, 0f);
                mVertices[i * 3 + 1] = new Vector3(x[i], y[i], 0f);
                // This will ensure that last vertex = first vertex..
                mVertices[i * 3 + 2] = new Vector3(x[(i + 1) % mSlices], y[(i + 1) % mSlices], 0);

                WRVertices[i * 3 + 0] = new Vector3(0f, 0f, 0.033f);
                WRVertices[i * 3 + 1] = new Vector3(x[i], y[i], 0.033f);
                // This will ensure that last vertex = first vertex..
                WRVertices[i * 3 + 2] = new Vector3(x[(i + 1) % mSlices], y[(i + 1) % mSlices], 0.033f);

                mUvs[i * 3 + 0] = new Vector2(0f, 0f);
                mUvs[i * 3 + 1] = new Vector2(x[i], y[i]);
                // This will ensure that last uv = first uv..
                mUvs[i * 3 + 2] = new Vector2(x[(i + 1) % mSlices], y[(i + 1) % mSlices]);
            }

            for (int nextTris = 0; nextTris < mTriangles.Length; nextTris++)
            {
                mTriangles[nextTris] = nextTris;
            }
            for (int i = 0; i < mNormals.Length; i++)
            {
                mNormals[i] = Vector3.forward;
            }
            int k = 0, l = 0;
            for (k = 0, l = 0; k < mVertices.Length; k++)
            {
                FinalVerticesArray[l++] = mVertices[k];
            }
            for (k = 0; k < WRVertices.Length; k++)
            {
                FinalVerticesArray[l++] = WRVertices[k];
            }
            if (TempObject.name == "TestObject")
            {
                GameObject trmpParent = Instantiate(new GameObject());
                for (int i = 0; i < FinalVerticesArray.Length; i++)
                {
                    GameObject go = Instantiate(GetComponent<PieChartMeshController>().testobj, transform.TransformPoint(FinalVerticesArray[i]), Quaternion.identity);
                    go.transform.parent = trmpParent.transform;
                    go.name = i.ToString();
                }
            }

            int addingelement = 1;

            subTris = new int[mData.Length];
            subTris3D = new int[mData.Length];

            int[] sidetrinaglesB, sidetrinaglesA;
            countedSlices = 0;

            // Set sub meshes
            for (int count = 0; count < mData.Length; count++)
            {
                partcreated = false;
                // Every triangle has three veritces..
                subTris = new int[slice[count] * 3];
                subTris3D = new int[slice[count] * 3];
                subTrisLeft = new int[slice[count] * 3 + 3];
                subTrisRight = new int[slice[count] * 3 + 3];
                sidetrinaglesA = new int[slice[count] * 3];
                sidetrinaglesB = new int[slice[count] * 3];
                int sliceint = slice[count];
                for (int j = 0; j < sliceint; j++)
                {
                    subTris[j * 3 + 0] = mTriangles[countedSlices * 3 + 0];
                    subTris[j * 3 + 1] = mTriangles[countedSlices * 3 + 1];
                    subTris[j * 3 + 2] = mTriangles[countedSlices * 3 + 2];

                    subTris3D[j * 3 + 0] = mTriangles[countedSlices * 3 + 300];
                    subTris3D[j * 3 + 1] = mTriangles[countedSlices * 3 + 301];
                    subTris3D[j * 3 + 2] = mTriangles[countedSlices * 3 + 302];

                    if ((addingelement + 303) <= 600)
                    {
                        subTrisLeft[j * 3 + 0] = addingelement + 3;
                        subTrisLeft[j * 3 + 1] = addingelement;
                        subTrisLeft[j * 3 + 2] = (addingelement + 3) + 300;


                        subTrisRight[j * 3 + 0] = addingelement + 300;
                        subTrisRight[j * 3 + 1] = addingelement;
                        subTrisRight[j * 3 + 2] = (addingelement + 303);
                    }
                    else
                    {

                    }
                    sidetrinaglesA[j * 3 + 0] = subTris[j * 3 + 0];//0
                    sidetrinaglesA[j * 3 + 1] = subTris3D[j * 3 + 0];//300
                    sidetrinaglesA[j * 3 + 2] = subTris[j * 3 + 2];//2

                    sidetrinaglesB[j * 3 + 0] = subTris3D[j * 3 + 0];
                    sidetrinaglesB[j * 3 + 1] = subTris3D[j * 3 + 2];
                    sidetrinaglesB[j * 3 + 2] = subTris[j * 3 + 2];


                    addingelement += 3;
                    //if (j % 5 == 0)
                    //    yield return new WaitForSeconds(delay);
                    countedSlices++;
                    //mesh.SetTriangles(subTris[i], i);
                }

                int[] triangles = subTris;
                for (int u = 0; u < triangles.Length; u += 3)
                {
                    int temp = triangles[u + 0];
                    triangles[u + 0] = triangles[u + 1];
                    triangles[u + 1] = temp;
                }
                subTris = triangles;

                triangles = subTrisLeft;
                for (int u = 0; u < triangles.Length; u += 3)
                {
                    int temp = triangles[u + 0];
                    triangles[u + 0] = triangles[u + 1];
                    triangles[u + 1] = temp;
                }
                subTrisLeft = triangles;

                sidetrinaglesFinal = new int[12];
                try
                {
                    sidetrinaglesFinal[0] = sidetrinaglesA[2] - 1;
                    sidetrinaglesFinal[1] = sidetrinaglesA[1];
                    sidetrinaglesFinal[2] = sidetrinaglesA[0];
                    sidetrinaglesFinal[3] = sidetrinaglesB[2] - 1;
                    sidetrinaglesFinal[4] = sidetrinaglesB[1] - 1;
                    sidetrinaglesFinal[5] = sidetrinaglesB[0];


                    sidetrinaglesFinal[6] = sidetrinaglesA[sidetrinaglesA.Length - 3];
                    sidetrinaglesFinal[7] = sidetrinaglesA[sidetrinaglesA.Length - 2];
                    sidetrinaglesFinal[8] = sidetrinaglesA[sidetrinaglesA.Length - 1];
                    sidetrinaglesFinal[9] = sidetrinaglesB[sidetrinaglesA.Length - 3];
                    sidetrinaglesFinal[10] = sidetrinaglesB[sidetrinaglesA.Length - 2];
                    sidetrinaglesFinal[11] = sidetrinaglesB[sidetrinaglesA.Length - 1];

                    if (count == mData.Length - 1)
                    {
                        subTrisLeft[subTrisLeft.Length - 3] = 296;
                        subTrisLeft[subTrisLeft.Length - 2] = 1;
                        subTrisLeft[subTrisLeft.Length - 1] = 301;

                        subTrisRight[subTrisRight.Length - 3] = 301;
                        subTrisRight[subTrisRight.Length - 2] = 596;
                        subTrisRight[subTrisRight.Length - 1] = 296;
                    }

                }
                catch (System.Exception w)
                {
                    //Debug.Log(w.Message);
                    continue;
                }
                var Final = subTris.Concat(subTris3D).Concat(subTrisLeft).Concat(subTrisRight).Concat(sidetrinaglesFinal);
                CreateObjectAndSetMesh(FinalVerticesArray, Final.ToArray(), "Parts" + count, count);

                yield return new WaitUntil(() => partcreated);
            }
            if (!PieContorller.createpieOnly && CanvasDataManager.isn != null)
                CanvasDataManager.isn.PiechartCreated(sumOfData, mData, PieContorller.dataDescription.ToArray(), gameObjs);

        }
        void CreateObjectAndSetMesh(Vector3[] vertices, int[] triangles, string objectname, int index)
        {
            Vector3[] newNormals = new Vector3[vertices.Length];
            Vector2[] Uvs = new Vector2[vertices.Length];
            for (int i = 0; i < vertices.Length; i++)
            {
                newNormals[i] = Vector3.forward;
            }
            for (int i = 0; i < vertices.Length; i++)
            {
                Uvs[i] = new Vector2((vertices[i]).x, (vertices[i]).y);
            }

            GameObject gameObj = gameObjs[index];
            Mesh m = gameObj.GetComponent<MeshFilter>().mesh;
            gameObj.name = objectname;
            m.vertices = vertices;
            m.normals = newNormals;
            m.uv = Uvs;
            gameObj.transform.localPosition = Vector3.zero;
            Color color = PieContorller.customColor[index];
            color.a = 255;
            Material mainMaterial = new Material(this.mMaterial)
            {
                color = color
            };
            gameObj.GetComponent<MeshRenderer>().material = mainMaterial;

            gameObj.AddComponent<PartProperties>();

            if (animationType == PieChartMeshController.AnimationType.Rotation || animationType == PieChartMeshController.AnimationType.UpDownAndRotation)
                StartCoroutine(AnimateThePieChartRotation(gameObj, triangles.Length));
            else if (animationType == PieChartMeshController.AnimationType.NoAnimation)
            {
                m.triangles = triangles;
                m.Optimize();
                gameObj.AddComponent<MeshCollider>();
                gameObj.GetComponent<MeshCollider>().convex = true;
                gameObj.GetComponent<PartProperties>().SetInit();
                partcreated = true;
            }
            else if (animationType == PieChartMeshController.AnimationType.UpDown)
            {
                m.triangles = triangles;
                m.Optimize();
                gameObj.AddComponent<MeshCollider>();
                gameObj.GetComponent<MeshCollider>().convex = true;
                gameObj.GetComponent<PartProperties>().SetInit();
                partcreated = true;
            }

            //yield return new WaitUntil(() => partcreated);

        }

        IEnumerator AnimateThePieChartRotation(GameObject obj, int tris)
        {
            List<int> triangles = new List<int>();
            Mesh mesh = obj.GetComponent<MeshFilter>().sharedMesh;
            bool issubtrisDone, isleftrightDone;

            //triangles.AddRange(sidetrinaglesFinal.TakeFirst(6));
            for (int i = 0; i < 6; i++)
            {
                triangles.Add(sidetrinaglesFinal[i]);
            }
            for (int i = 0; i < tris; i++)
            {
                if (i + 2 < subTris.Length)
                {
                    triangles.Add(subTris[i]);
                    triangles.Add(subTris[i + 1]);
                    triangles.Add(subTris[i + 2]);

                    triangles.Add(subTris3D[i]);
                    triangles.Add(subTris3D[i + 1]);
                    triangles.Add(subTris3D[i + 2]);
                    issubtrisDone = false;
                }
                else
                    issubtrisDone = true;

                if (i + 2 < subTrisLeft.Length)
                {
                    triangles.Add(subTrisLeft[i]);
                    triangles.Add(subTrisLeft[i + 1]);
                    triangles.Add(subTrisLeft[i + 2]);

                    triangles.Add(subTrisRight[i]);
                    triangles.Add(subTrisRight[i + 1]);
                    triangles.Add(subTrisRight[i + 2]);
                    isleftrightDone = false;
                }
                else
                    isleftrightDone = true;

                if (isleftrightDone && issubtrisDone)
                {
                    for (int ji = 6; ji < 12; ji++)
                    {
                        triangles.Add(sidetrinaglesFinal[ji]);
                    }
                    mesh.SetTriangles(triangles.ToArray(), 0);
                    break;
                }
                mesh.SetTriangles(triangles.ToArray(), 0);
                yield return new WaitForEndOfFrame();
            }
            mesh.Optimize();
            partcreated = true;
            obj.AddComponent<MeshCollider>();
            obj.GetComponent<MeshCollider>().convex = true;

            obj.GetComponent<PartProperties>().SetInit();



        }
        public float[] Data { get { return mData; } set { mData = value; } }

        public int Slices { get { return mSlices; } set { mSlices = value; } }

        public float RotationAngle { get { return mRotationAngle; } set { mRotationAngle = value; } }

        public float Radius { get { return mRadius; } set { mRadius = value; } }

    }
    public static class MiscExtensions
    {
        // Ex: collection.TakeLast(5);
        public static IEnumerable<T> TakeLast<T>(this IEnumerable<T> source, int N)
        {
            return source.Skip(Math.Max(0, source.Count() - N));
        }
        public static IEnumerable<T> TakeFirst<T>(this IEnumerable<T> source, int N)
        {
            return source.Skip(Math.Max(source.Count() - N, source.Count()));
        }
    }
}