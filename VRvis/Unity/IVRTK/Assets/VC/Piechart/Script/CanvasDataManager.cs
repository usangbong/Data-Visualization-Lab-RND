using UnityEngine;
using UnityEngine.UI;
namespace PieChart.ViitorCloud
{
    public class CanvasDataManager : MonoBehaviour
    {
        public static CanvasDataManager isn { set; get; }
        GameObject cavasObjectInfoImage;

        Transform infoImageParent;
        GameObject[] gps = new GameObject[10];
        // Start is called before the first frame update
        void Awake()
        {
            isn = this;
            this.infoImageParent = transform.Find("Color Panel Left");
            cavasObjectInfoImage = Resources.Load("WhiteBG") as GameObject;

            Transform infoImageParent;
            for (int i = 0; i < 10; i++)
            {
                infoImageParent = this.infoImageParent;
                gps[i] = Instantiate(cavasObjectInfoImage, infoImageParent);
                gps[i].SetActive(false);

            }
        }
        public void PiechartCreated(float sumofdata, float[] data, string[] dataDescription, GameObject[] pieObjects)
        {
            for (int i = 0; i < pieObjects.Length; i++)
            {
                gps[i].transform.GetComponent<Image>().color = pieObjects[i].GetComponent<MeshRenderer>().material.color;
                gps[i].transform.Find("PercentageText").GetComponent<Text>().text = (Mathf.RoundToInt((data[i] * 100) / sumofdata)).ToString() + "%";
                //if (dataHeadername.Length > 0)
                //    gps[i].transform.Find("HeadingText").GetComponent<Text>().text = dataHeadername[i];
                if (dataDescription.Length > 0)
                    gps[i].transform.Find("InstrucationText").GetComponent<Text>().text = dataDescription[i];
                gps[i].name = pieObjects[i].name;
                gps[i].SetActive(true);

                try
                {
                    pieObjects[i].GetComponent<PartProperties>().MyDetailObject = gps[i];
                }
                catch (System.Exception) {
                    Debug.Log("123");
                }
            }
        }
    }
}