using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ColorCircle : MonoBehaviour
{
    public GameObject blueCircle, blueTorus1, blueTorus2, blueSphere;
    public GameObject yellowCircle, yellowTorus1, yellowTorus2, yellowSphere;
    public GameObject inCircle;
    Circle circle;

    public bool torus, torus2, yellow, ytorus2, changeStart, ytorus;

    public bool Ctorus, move;

    public bool blueStart, yellowSizeStart, yellowStart, blueSizeStart;

    bool f1, f2, f3;
    public bool fin1, fin2;

    void Start()
    {
        circle = GameObject.Find("CircleManager").GetComponent<Circle>();
        torus = torus2 = Ctorus = false;
        yellow = ytorus = ytorus2 = false;
        changeStart = false;
        ActiveFalse();
        blueSizeStart = false;
        fin1 = fin2 = false;
        blueStart = yellowSizeStart = yellowStart = false;

        f1 = f2 = f3 = false;
        move = false;
    }

    
    void Update()
    {
        if(circle.CircleFinish && blueStart && !fin1)
        {
            inCircle.SetActive(false);
            blueCircle.SetActive(true);
            StartCoroutine(blueCircletorusSize());
            StartCoroutine(blueCircletorusSize2());
            fin1 = true;
        }

        if(torus && torus2 && yellowStart && !fin2)
        {
            blueCircle.SetActive(false);
            yellowCircle.SetActive(true);
            StartCoroutine(yellowCircletorusSize());
            StartCoroutine(yellowCircletorusSize2());
            fin2 = true;
        }

        if(ytorus && ytorus2 && !f3 && changeStart)
        {
            StartCoroutine(Change());
            f3 = true;
        }

        if(Ctorus)
        {
            if(!move)
            {
                blueCircle.SetActive(true);
                yellowCircle.SetActive(true);

                blueCircle.transform.position = Vector3.MoveTowards(blueCircle.transform.position,
                    new Vector3(0, 1, 1), 1.0f * Time.deltaTime);
                yellowCircle.transform.position = Vector3.MoveTowards(yellowCircle.transform.position,
                    new Vector3(0, 1, -1), 1.0f * Time.deltaTime);

                if(blueCircle.transform.position == new Vector3(0,1,1) && 
                    yellowCircle.transform.position == new Vector3(0,1,-1))
                {
                    move = true;
                }
            }
        }
    }


    void F3()
    {
        f3 = true;
    }

    IEnumerator blueCircletorusSize()
    {
        Vector3 scale = new Vector3(0.007f, 0.007f, 0.007f);
        while (!torus)
        {
            blueTorus1.transform.localScale += scale;

            if(blueTorus1.transform.localScale.x >= 1.2f)
            {
                torus = true;
            }

            yield return new WaitForSeconds(0.01f);
        }
    }

    IEnumerator blueCircletorusSize2()
    {
        Vector3 scale = new Vector3(0.007f, 0.007f, 0.007f);
        while (!torus2)
        {
            blueTorus2.transform.localScale += scale;

            if (blueTorus2.transform.localScale.x >= 1.5f)
            {
                torus2 = true;
            }

            yield return new WaitForSeconds(0.01f);
        }
    }

    IEnumerator yellowCircletorusSize()
    {
        Vector3 scale = new Vector3(0.007f, 0.007f, 0.007f);
        while (!ytorus)
        {
            yellowTorus1.transform.localScale += scale;

            if (yellowTorus1.transform.localScale.x >= 1.2f)
            {
                ytorus = true;
            }

            yield return new WaitForSeconds(0.01f);
        }
    }

    IEnumerator yellowCircletorusSize2()
    {
        Vector3 scale = new Vector3(0.007f, 0.007f, 0.007f);
        while (!ytorus2)
        {
            yellowTorus2.transform.localScale += scale;

            if (yellowTorus2.transform.localScale.x >= 1.5f)
            {
                ytorus2 = true;
            }

            yield return new WaitForSeconds(0.01f);
        }
    }

    IEnumerator Change()
    {
        int cnt = 0;
        bool isYellow = false;
        while(!Ctorus)
        {
            if(!isYellow)
            {
                yellowCircle.SetActive(false);
                blueCircle.SetActive(true);
                isYellow = true;
            }

            else
            {
                yellowCircle.SetActive(true);
                blueCircle.SetActive(false);
                isYellow = false;
            }

            cnt++;

            if(cnt > 15)
            {
                Ctorus = true;
            }

            yield return new WaitForSeconds(1.0f);
        }
    }

    void ActiveFalse()
    {
        blueCircle.SetActive(false);
        yellowCircle.SetActive(false);
    }
}
