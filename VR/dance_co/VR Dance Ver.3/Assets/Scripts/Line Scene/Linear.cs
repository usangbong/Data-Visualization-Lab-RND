using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Linear : MonoBehaviour
{
    public GameObject shortLinear, longLinear;
    public GameObject arrows;

    public Material red, yellow, green, black, blue, brown, orange, pupple, beige, white, gray;

    public int matNum;
    public bool MakeArrowFinish, arrowColor, ArrowMake, arrowMove, arrowDown;
    bool arrowFunc, iTweenFunc, arrowRotFinish, arrowUp;
    bool iTweenFunc2, arrowMove2;

    int colorFinNum;

    public GameObject shortLinear2;

    CircleMove circleMove;
    Vector3 scale;

    List<Material> materialList = new List<Material>();

    IEnumerator colorCor1, colorCor2, colorCor3;
    
    void Start()
    {
        matNum = colorFinNum = 0;
        circleMove = GameObject.Find("WaveManager").GetComponent<CircleMove>();
        MakeArrowFinish = arrowColor = arrowFunc = ArrowMake = false;
        iTweenFunc = arrowMove = arrowRotFinish = false;
        iTweenFunc2 = arrowUp = arrowDown = arrowMove2 = false;
        shortLinear2 = Instantiate(shortLinear);
        shortLinear2.transform.SetParent(arrows.transform);
        shortLinear2.SetActive(false);

        scale = new Vector3(0, 0, 0.01f);

        shortLinear2.transform.position = shortLinear.transform.position;

        materialList.Add(red);
        materialList.Add(yellow);
        materialList.Add(green);
        materialList.Add(black);
        materialList.Add(blue);
        materialList.Add(brown);
        materialList.Add(orange);
        materialList.Add(pupple);
        materialList.Add(beige);
        materialList.Add(white);
        materialList.Add(gray);
    }

    void Update()
    {
        if (circleMove.animFinish && !MakeArrowFinish && ArrowMake)
        {
            Invoke("MakeArrowFin", 2.5f);
            shortLinear2.SetActive(true);
            longLinear.transform.position = Vector3.MoveTowards(longLinear.transform.position,
                new Vector3(0.05f, 1.216f, 1.136f), 1.0f * Time.deltaTime);
            shortLinear.transform.position = Vector3.MoveTowards(shortLinear.transform.position,
                new Vector3(0.576f, 1.374f, 1.136f), 1.0f * Time.deltaTime);
            shortLinear2.transform.position = Vector3.MoveTowards(shortLinear2.transform.position,
                new Vector3(0.576f, 1, 1.136f), 1.0f * Time.deltaTime);

            shortLinear.transform.rotation = Quaternion.Slerp(shortLinear.transform.rotation,
                Quaternion.Euler(-45f, -90f, 0), 3.0f * Time.deltaTime);
            shortLinear2.transform.rotation = Quaternion.Slerp(shortLinear2.transform.rotation,
                Quaternion.Euler(45f, -90f, 0), 3.0f * Time.deltaTime);

            if (longLinear.transform.localScale.z > 0.4f)
            {
                longLinear.transform.localScale -= scale;
            }

            else
            {
                longLinear.transform.localScale = new Vector3(0.05f, 0.05f, 0.4f);
            }

            if (shortLinear.transform.localScale.z > 0.3f)
            {
                shortLinear.transform.localScale -= scale;
            }

            else
            {
                shortLinear.transform.localScale = new Vector3(0.05f, 0.05f, 0.3f);
            }

            if (shortLinear2.transform.localScale.z > 0.3f)
            {
                shortLinear2.transform.localScale -= scale;
            }

            else
            {
                shortLinear2.transform.localScale = new Vector3(0.05f, 0.05f, 0.3f);
            }
        }

        if(arrowColor)
        {
            RandomValue();

            longLinear.GetComponent<MeshRenderer>().material = materialList[matNum];
            shortLinear.GetComponent<MeshRenderer>().material = materialList[matNum];
            shortLinear2.GetComponent<MeshRenderer>().material = materialList[matNum];

            arrowColor = false;
        }

        if(MakeArrowFinish && arrowMove && !arrowRotFinish)
        {
            if(!iTweenFunc)
            {
                ArrowITween();
                iTweenFunc = true;
            }

            arrows.transform.Rotate(Vector3.up * 24f * Time.deltaTime);
        }

        if(arrowRotFinish && !arrowUp)
        {
            arrows.transform.position = Vector3.MoveTowards(arrows.transform.position,
                new Vector3(0, 3, 1), 1.0f * Time.deltaTime);
            arrows.transform.rotation = Quaternion.Slerp(arrows.transform.rotation,
                Quaternion.Euler(0, 0, 90), 3.0f * Time.deltaTime);

            if(arrows.transform.position == new Vector3(0,3,1))
            {
                arrowUp = true;
            }
        }

        if(arrowUp && !arrowMove2)
        {
            if(!iTweenFunc2)
            {
                ArrowITween2();
                iTweenFunc2 = true;
            }

            arrows.transform.Rotate(Vector3.up * 40f * Time.deltaTime);
        }

        if(arrowMove2 && !arrowDown)
        {
            arrows.transform.position = Vector3.MoveTowards(arrows.transform.position,
                new Vector3(0, 1.5f, 0), 1.0f * Time.deltaTime);

            if(arrows.transform.position == new Vector3(0, 1.5f, 0))
            {
                Invoke("ArrowDown", 2.0f);
            }
        }
    }

    void MakeArrowFin()
    {
        MakeArrowFinish = true;
    }

    void RandomValue()
    {
        float num = Random.value * 1000;

        matNum = System.Convert.ToInt32(num) % 11;
    }

    void ArrowITween()
    {
        iTween.MoveTo(arrows, iTween.Hash("path", iTweenPath.GetPath("ArrowPath"),
            "easeType", iTween.EaseType.linear, "time", 16, "oncomplete", "ArrowRotateFinish",
            "oncompletetarget", this.gameObject));
    }

    void ArrowITween2()
    {
        iTween.MoveTo(arrows, iTween.Hash("path", iTweenPath.GetPath("ArrowPath2"),
            "easeType", iTween.EaseType.linear, "time", 5, "oncomplete", "ArrowMoveFinish",
            "oncompletetarget", this.gameObject));
    }

    void ArrowRotateFinish()
    {
        arrowRotFinish = true;
        arrows.transform.rotation = Quaternion.Euler(0, 0, 0);
    }

    void ArrowMoveFinish()
    {
        arrowMove2 = true;
        arrows.transform.rotation = Quaternion.Euler(-180, 0, 90);
    }

    void ArrowDown()
    {
        arrowDown = true;
    }
}
