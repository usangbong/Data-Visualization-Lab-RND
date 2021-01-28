using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;
using System.Linq.Expressions;
using System;
using Random = UnityEngine.Random;
using UnityEngine.Events;

#if UNITY_EDITOR
using UnityEditor;
#endif
namespace PieChart.ViitorCloud
{
    [Serializable]
    public class PieChartMeshController : MonoBehaviour
    {
        PieChartMesh mPieChart;


        bool randomData;
        List<float> Data =new List<float>(); 
        //public float speedofRotation;
        float delay = 0.1f;
        public Material mainMaterial;
        int randomBuffer;

        public GameObject Meshes, testobj, parent;

        internal bool createpieOnly;
        internal List<Color> customColor =new List<Color>();


        internal List<string> dataDescription = new List<string>();

        public enum AnimationType { NoAnimation, UpDown, Rotation, UpDownAndRotation }

        private void Awake()
        {

            Meshes = Resources.Load("PiePartsObj") as GameObject;

            GameObject cam = Camera.main.gameObject;
            if (cam != null)
            {
                if (cam.GetComponent<ClickEffect>() == null)
                {
                    cam.AddComponent<ClickEffect>();
                    if (cam.GetComponent<cakeslice.OutlineEffect>() == null)
                        cam.AddComponent<cakeslice.OutlineEffect>();
                    //Color c = new Color();
                    //c.r = 0.2470588f;
                    //c.g = 

                    //cam.GetComponent<cakeslice.OutlineEffect>().lineColor0
                }
            }
        }

        /// <summary>
        /// Generate Pie Chart
        /// </summary>
        /// <param name="randomData">Bool to generate random data</param>
        /// <param name="segments">how many data (each of the parts into which pie will be divided)</param>
        /// <param name="Data">data to show on pie</param>
        /// <param name="customColorofPie">bool for true for custom colors false random colors</param>
        /// <param name="customColor">color for Pie</param>
        /// <param name="dataDescription">Description about data to represent on the pie</param>
        /// <param name="dataHeadername">Name of data to represent on the pie</param>
        public void GenerateChart(int segment, AnimationType animationType, bool createpieOnly)
        {
            if (!createpieOnly)
                Instantiate(Resources.Load("Canvas") as GameObject);

            //ClickEffect.isn.allPartsObjectAndPositionDict.Clear();
            //ClickEffect.isn.allParsObjectAndCanvasObjectDict.Clear();

            this.createpieOnly = createpieOnly;

            if (segment > 1)
            {
                if (Data.Count != segment)
                {
                    Debug.LogError("Generating Random Data.\n\nThe DataList Count != segment");
                    Data = GenerateRandomValues(segment).ToList();
                }
            }
            else
            {
                Debug.LogError("Segments can not be less than 1");
                GenerateChart(5, animationType, createpieOnly);
            }
            if (mainMaterial == null)
            {
                Debug.LogError("Setting 'StandMat' as mat.");
                mainMaterial = Resources.Load("StandMat") as Material;
            }


            if (customColor.Count != segment)
            {
                Debug.LogError("Generating Random Color. \n\n ColorList Count != segment");
                customColor = GenerateRandomColors(segment).ToList();
            }

            if (gameObject.GetComponent<PieChartMesh>() == null)
                mPieChart = gameObject.AddComponent<PieChartMesh>() as PieChartMesh;

            if (mPieChart != null)
            {
                mPieChart.Init(Data.ToArray(), mainMaterial, delay, Meshes, animationType);
                mPieChart.Draw(Data.ToArray());
            }
            else
            {
                Debug.LogError("Piechart is null", gameObject);
            }


            //Random.seed = randomBuffer;

        }


        ///// <summary>
        ///// No Random data , No Random Color , Data Decription
        ///// </summary>
        ///// <param name="segments">how many data (each of the parts into which pie will be divided)</param>
        ///// <param name="Data">data to show on pie</param>
        ///// <param name="customColor">color for Pie</param>
        ///// <param name="dataDescription">Description about data to represent on the pie</param>
        ///// <param name="dataHeadername">Name of data to represent on the pie</param>
        //public void GenerateChart(int segments, float[] Data, Color[] customColor, List<string> dataDescription, AnimationType atype
        //    , bool createpieonly)
        //{
        //    GenerateChart(segments, false, Data, false, customColor, dataDescription, atype, createpieonly);
        //}

        ///// <summary>
        ///// Random data , No Random Color , Data Decription
        ///// </summary>
        ///// <param name="segments">how many data (each of the parts into which pie will be divided)</param>
        ///// <param name="customColor">color for Pie</param>
        ///// <param name="dataDescription">Description about data to represent on the pie</param>
        ///// <param name="dataHeadername">Name of data to represent on the pie</param>
        //public void GenerateChart(int segments, Color[] customColor, List<string> dataDescription, AnimationType atype, bool createpieonly)
        //{
        //    GenerateChart(segments, true, GenerateRandomValues(segments), false, customColor, dataDescription, atype, createpieonly);
        //}

        ///// <summary>
        ///// No Random data , Random Color , Data Decription
        ///// </summary>
        ///// <param name="segments">how many data (each of the parts into which pie will be divided)</param>
        ///// <param name="Data">data to show on pie</param>
        ///// <param name="dataDescription">Description about data to represent on the pie</param>
        ///// <param name="dataHeadername">Name of data to represent on the pie</param>
        //public void GenerateChart(int segments, float[] Data, List<string> dataDescription, AnimationType atype, bool createpieonly)
        //{
        //    GenerateChart(segments, false, Data, true, GenerateRandomColors(segments), dataDescription, atype, createpieonly);
        //}
        ///// <summary>
        ///// Random data , Random Color , Data Decription
        ///// </summary>
        ///// <param name="segments">how many data (each of the parts into which pie will be divided)</param>
        ///// <param name="dataDescription">Description about data to represent on the pie</param>
        ///// <param name="dataHeadername">Name of data to represent on the pie</param>
        //public void GenerateChart(int segments, List<string> dataDescription, AnimationType atype, bool createpieonly)
        //{
        //    GenerateChart(segments, true, GenerateRandomValues(segments), true, GenerateRandomColors(segments), dataDescription, atype, createpieonly);
        //}

        ///// <summary>
        ///// Random data , Random Color , no Data Decription
        ///// </summary>
        ///// <param name="segments">how many data (each of the parts into which pie will be divided)</param>
        //public void GenerateChart(int segments, AnimationType atype, bool createpieonly)
        //{
        //    GenerateChart(segments, true, GenerateRandomValues(segments), true, GenerateRandomColors(segments), dataDescription, atype, createpieonly);
        //}

        /// <summary>
        /// Set the Matrial Of Pie
        /// Note : call this before generating pie chart
        /// </summary>
        /// <param name="mat"></param>
        public void SetMatrialOfPie(Material mat)
        {
            mainMaterial = mat;
        }
        /// <summary>
        /// Set the color of the pie
        /// </summary>
        /// <param name="color">Color of the pie</param>
        public void SetColor(Color[] color)
        {
            customColor = color.ToList();
        }
        /// <summary>
        /// Data of the pie
        /// </summary>
        /// <param name="data"></param>
        public void SetData(float[] data)
        {
            this.Data = data.ToList();
        }
        /// <summary>
        /// Description of the pie
        /// </summary>
        /// <param name="data"></param>
        public void SetDescription(string[] data)
        {
            this.dataDescription = data.ToList();
        }



        float[] GenerateRandomValues(int length)
        {
            float[] targets = new float[length];
            for (int i = 0; i < length; i++)
            {
                targets[i] = Random.Range(1f, 100f);
            }
            return targets;
        }

        Color[] GenerateRandomColors(int length)
        {
            Color[] targets = new Color[length];
            for (int i = 0; i < length; i++)
            {
                Color c = new Color32((byte)Random.Range(0, 256), (byte)Random.Range(0, 256), (byte)Random.Range(0, 256), (byte)255);
                targets[i] = c;
            }
            return targets;
        }
    }
}