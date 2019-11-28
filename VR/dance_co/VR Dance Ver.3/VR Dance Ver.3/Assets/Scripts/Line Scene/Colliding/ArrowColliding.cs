using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ArrowColliding : MonoBehaviour
{
    public GameObject Arrows, nullParent;
    Linear linear;
    MakeFigure makeFigure;
    bool isColliding, isFin;

    void Start()
    {
        linear = GameObject.Find("LinearManager").GetComponent<Linear>();
        makeFigure = GameObject.Find("FigureManager").GetComponent<MakeFigure>();
        isColliding = isFin = false;
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if(!linear.arrowColor && !isColliding && linear.MakeArrowFinish && !makeFigure.makeArrow)
            {
                isColliding = true;
                linear.arrowColor = true;
            }

            if(!linear.arrowMove && linear.MakeArrowFinish)
            {
                linear.arrowMove = true;
            }

            if(linear.arrowDown && !makeFigure.makeArrow && !makeFigure.MakeStart)
            {
                makeFigure.MakeStart = true;
            }

            if(makeFigure.makeArrow && !makeFigure.isColliding && !isFin)
            {
                makeFigure.isColliding = true;
                isFin = true;
            }

            if(makeFigure.arr)
            {
                for (int i = 0; i < other.gameObject.transform.childCount; i++)
                {
                    other.gameObject.transform.GetChild(i).SetParent(nullParent.transform);
                }

                Arrows.transform.SetParent(other.transform);
            }
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if(other.tag == "Tracker")
        {
            isColliding = false;
        }
    }
}
