using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FigureColliding : MonoBehaviour
{
    MakeFigure makeFigure;

    void Start()
    {
        makeFigure = GameObject.Find("FigureManager").GetComponent<MakeFigure>();
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if(gameObject.name == "Col1" || gameObject.name == "Col2")
            {
                Debug.Log("Col1");
                makeFigure.collider1 = true;
            }

            else if(gameObject.name == "Col3" || gameObject.name == "Col4")
            {
                Debug.Log("Col2");
                makeFigure.collider2 = true;
            }
        }   
    }

    private void OnTriggerExit(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if(gameObject.name == "Col1" || gameObject.name == "Col2")
            {
                Debug.Log("ColEx1");
                makeFigure.collider1 = false;
            }

            else if(gameObject.name == "Col3" || gameObject.name == "Col4")
            {
                Debug.Log("ColEx2");
                makeFigure.collider2 = false;
            }
        }
    }
}
