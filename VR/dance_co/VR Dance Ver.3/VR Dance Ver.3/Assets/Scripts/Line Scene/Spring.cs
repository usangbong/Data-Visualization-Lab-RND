using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Spring : MonoBehaviour
{
    public GameObject spring, gameManager;
    public GameObject trakerL, trakerR, trakerH, trakerLf, trakerRf;
    CircleMove circle;
    bool func, isSpeed;
    public bool isSize;

    CollidingTracker col;
    MakeFigure makeFigure;

    void Start()
    {
        spring.GetComponent<Animator>().enabled = false;
        circle = GameObject.Find("WaveManager").GetComponent<CircleMove>();
        makeFigure = GameObject.Find("FigureManager").GetComponent<MakeFigure>();
        isSize = isSpeed = true;
        func = false;
        col = GameObject.Find("spring5_t").GetComponent<CollidingTracker>();
    }

    void Update()
    {
        if (makeFigure.FigureFin)
        {
            if (!func)
            {
                StartCoroutine(size());
                func = true;
                iTween.MoveTo(spring, iTween.Hash("path", iTweenPath.GetPath("springPath"),
                    "easeType", "easeOutCirc", "time", 1.5f, "delay", 1.0f));
            }

            spring.GetComponent<Animator>().enabled = true;
        }
    }

    IEnumerator size()
    {
        Vector3 sizes = new Vector3(0.01f, 0.01f, 0.01f);
        while(isSize)
        {
            if(spring.transform.localScale.z <= 0.17f)
            {
                isSize = false;
            }

            spring.transform.localScale -= sizes;
            yield return new WaitForSeconds(0.01f);
        }
    }
}
