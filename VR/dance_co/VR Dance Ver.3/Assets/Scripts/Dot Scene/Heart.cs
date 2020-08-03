using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Heart : MonoBehaviour
{
    public GameObject Hearts, cameras;
    public Vector3 pos;

    Flat flat;

    public bool heartFinish;
    public bool isscale, isMove, moveStart;
    bool func, func2, iTw;
    bool BeatCor, timeBool;
    bool timeS;
    float time;

    void Start()
    {
        heartFinish = false;
        isscale = true;
        isMove = moveStart = false;
        func = func2 = iTw = false;
        BeatCor = timeBool = false;
        time = 0;
        Hearts.SetActive(false);
        timeS = false;

        flat = GameObject.Find("FlatManager").GetComponent<Flat>();
    }

    void Update()
    {
        if(!flat.isTime && !func)
        {
            Hearts.SetActive(true);
            StartCoroutine(scale1());
            func = true;
        }

        if (!flat.isTime && !isMove && !iTw)
        {
            Hearts.transform.position = Vector3.MoveTowards(Hearts.transform.position,
                new Vector3(0f, 1.66f, 3), 6.0f * Time.deltaTime);
            Hearts.transform.rotation = Quaternion.Slerp(Hearts.transform.rotation,
                Quaternion.Euler(0f, -90f, 0), 4.0f * Time.deltaTime);

            if (Hearts.transform.position == new Vector3(0f, 1.66f, 3))
            {
                if (!BeatCor)
                {
                    Invoke("IT", 3.0f);
                    StartCoroutine(HeartBeat());
                    BeatCor = true;
                }
            }
        }

        if(iTw && !heartFinish)
        {
            if(!timeS)
            {
                StartCoroutine(TimeChecker());
                timeS = true;
            }

            Hearts.transform.RotateAround(Vector3.zero, Vector3.down, 15f * Time.deltaTime);
        }
    }

    void IT()
    {
        iTw = true;
    }

    IEnumerator scale1()
    {
        while (isscale)
        {
            Vector3 scale = new Vector3(0.1f, 0.1f, 0.1f);

            Hearts.transform.localScale -= scale;

            if(Hearts.transform.localScale.x <= 0.6f)
            {
                isscale = false;
            }

            yield return new WaitForSeconds(0.01f);
        }
    }

    IEnumerator HeartBeat()
    {
        Vector3 scale = new Vector3(-0.0015f, -0.0015f, -0.0015f);
        while (true)
        {
            Hearts.transform.localScale += scale;

            if(Hearts.transform.localScale.x < 0.6f)
            {
                scale = new Vector3(0.001f, 0.001f, 0.001f);
            }

            if(Hearts.transform.localScale.x > 0.8f)
            {
                scale = new Vector3(-0.001f, -0.001f, -0.001f);
            }

            yield return new WaitForSeconds(0.01f);
        }
    }

    IEnumerator TimeChecker()
    {
        while(!heartFinish)
        {
            time += 0.1f;

            if(time >= 20f)
            {
                heartFinish = true;
            }

            yield return new WaitForSeconds(0.1f);
        }
    }
}
