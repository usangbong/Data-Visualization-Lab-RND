using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MaterialManager : MonoBehaviour
{
    public Material black, blue, brown, gray, green, pupple, red, red_heart;
    public Material ring, skyblue, white, yellow, out90, ar_Back;
    public Material beige, orange, deepOrange;

    public GameObject Background, rings, downs;
    public GameObject LampManager;

    public List<Material> matList = new List<Material>();
    bool startColor;

    void Start()
    {
        //17 Material
        matList.Add(black);
        matList.Add(blue);
        matList.Add(brown);
        matList.Add(gray);
        matList.Add(green);
        matList.Add(pupple);
        matList.Add(red);
        matList.Add(red_heart);
        matList.Add(ring);
        matList.Add(skyblue);
        matList.Add(white);
        matList.Add(yellow);
        matList.Add(out90);
        matList.Add(ar_Back);
        matList.Add(beige);
        matList.Add(orange);
        matList.Add(deepOrange);

        Invoke("Starts", 2.0f);
        startColor = false;
    }

    private void Update()
    {
        if(startColor)
        {
            for (int i=0;i<Background.transform.childCount;i++)
            {
                Background.transform.GetChild(i).GetComponent<MeshRenderer>().material.color -= new Color(0, 0, 0, 0.002f);
            }

            if(Background.transform.GetChild(0).GetComponent<MeshRenderer>().material.color.a <= 0.5f)
            {
                startColor = false;
                rings.SetActive(true);
                Background.SetActive(false);
                downs.SetActive(true);
                LampManager.SetActive(true);
            }
        }
    }

    void Starts()
    {
        startColor = true;
    }
}
