using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace PieChart.ViitorCloud
{
    public class PieChart : MonoBehaviour
    {
        [Tooltip("Object of PieChartMeshController")]
        public PieChartMeshController pieChartMeshController;

        [Tooltip("Each of the parts into which the will be divided")]
        public int segments;

        [Tooltip("The data for the pie\n" +
                 "The size of this list must exact the value of Segment.")]
        public float[] Data;

        [Tooltip("Main Material that the mesh of the pie will use to rander")]
        public Material mainMaterial;

        [Tooltip("The colors that will be applied on the pie\n" +
                 "The size of this list must exact the value of Segment.")]
        public Color[] customColors;

        [SerializeField]
        [Tooltip("Pie chart with not information and title")]
        public bool justCreateThePie;

        [Tooltip("The list of description of the pie.")]
        public List<string> dataDescription = new List<string>();

        [Tooltip("Type of animation which will the pie have.")]
        public PieChartMeshController.AnimationType animationType;

        [Tooltip("Assign the parent Object where the Pie will generate")]
        public Transform parentTransform;

        void Start()
        {
            if (pieChartMeshController == null)
                pieChartMeshController = gameObject.AddComponent<PieChartMeshController>();
            pieChartMeshController.parent = parentTransform.gameObject;

            //pieChartMeshController.onPointerEnter.AddListener(onPointerClick);

            if (pieChartMeshController == null)
            {
                Debug.LogError("Drag The PieChartMeshController to Scene as PieChartMeshController is null.");
                return;
            }
            if (mainMaterial != null)
                pieChartMeshController.SetMatrialOfPie(mainMaterial);

            pieChartMeshController.SetData(Data);
            pieChartMeshController.SetColor(customColors);
            pieChartMeshController.SetDescription(dataDescription.ToArray());
            pieChartMeshController.GenerateChart(segments ,animationType, justCreateThePie);

        }

        [ContextMenu("Take SS")]
        void TakeSS()
        {
            ScreenCapture.CaptureScreenshot($"{Application.productName} {GetTimeString()}.png");

            string GetTimeString()
            {
                return System.DateTime.Now.ToString("yyyy-MM-dd-HH-mm-ss");
            }
        }



        public void ReverseAnimation(Animation anim, string AnimationName)
        {
            anim[AnimationName].speed = -1;
            anim[AnimationName].time = anim[AnimationName].length;
            anim.CrossFade(AnimationName);
        }
        public void ForwardAnimation(Animation anim, string AnimationName)
        {
            anim[AnimationName].speed = 1;
            anim[AnimationName].time = 0;
            anim.CrossFade(AnimationName);
        }
    }
}