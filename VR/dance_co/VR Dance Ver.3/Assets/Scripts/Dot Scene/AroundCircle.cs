using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AroundCircle : MonoBehaviour
{
    public GameObject sphere;
    public Material black, blue, green, gray, yellow, pupple, orange, brown;

    public List<GameObject> sphereList = new List<GameObject>();
    public List<Material> matList = new List<Material>();

    public bool finish;

    Eye eye;

    float x, y, z;

    List<float> xList = new List<float>();
    List<float> yList = new List<float>();
    List<float> zList = new List<float>();

    int arriveCnt;

    void Start()
    {
        eye = GameObject.Find("EyeManager").GetComponent<Eye>();
        for(int i=0;i<10;i++)
        {
            sphereList.Add(Instantiate(sphere));
            sphereList[i].SetActive(false);
        }

        matList.Add(black);
        matList.Add(blue);
        matList.Add(green);
        matList.Add(gray);
        matList.Add(yellow);
        matList.Add(pupple);
        matList.Add(orange);
        matList.Add(brown);

        arriveCnt = 0;

        finish = false;

        for(int i=0;i<10;i++)
        {
            RandomValue();
            xList.Add(x);
            yList.Add(y);
            zList.Add(z);
        }
    }

    void Update()
    {
        if (eye.time10 && !finish)
        {
            for(int i=0;i<10;i++)
            {
                sphereList[i].SetActive(true);
            }

            for(int i=0;i<10;i++)
            {
                moveObject(sphereList[i], new Vector3(xList[i], yList[i], zList[i]));
            }

            arriveCnt = 0;
            for(int i=0;i<10;i++)
            {
                if(sphereList[i].transform.position == new Vector3(xList[i], yList[i], zList[i]))
                {
                    arriveCnt++;
                }
            }

            if(arriveCnt == 10)
            {
                finish = true;
            }
        }
    }

    void RandomValue()
    {
        int ix, iy, iz;

        x = Random.value * 100;
        y = Random.value * 100;
        z = Random.value * 100;

        ix = System.Convert.ToInt32(x) % 20;
        iy = System.Convert.ToInt32(y) % 16;
        iz = System.Convert.ToInt32(z) % 20;

        x = System.Convert.ToSingle(ix) / 10 - 1;
        y = System.Convert.ToSingle(iy) / 10;
        z = System.Convert.ToSingle(iz) / 10 - 1;
    }

    void moveObject(GameObject obj, Vector3 toPos)
    {
        obj.transform.position = Vector3.MoveTowards(obj.transform.position,
            toPos, 1.0f * Time.deltaTime);
    }
}
