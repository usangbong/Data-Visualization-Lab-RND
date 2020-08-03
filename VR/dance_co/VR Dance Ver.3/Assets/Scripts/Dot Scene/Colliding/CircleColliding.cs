using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CircleColliding : MonoBehaviour
{
    Circle circle;
    ColorCircle cCircle;

    bool isEnter;

    void Start()
    {
        circle = GameObject.Find("CircleManager").GetComponent<Circle>();
        cCircle = GameObject.Find("ColorCircleManager").GetComponent<ColorCircle>();

        isEnter = false;
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Tracker")
        {
            if (!circle.moveStart && circle.sizeStart && !isEnter)
            {
                circle.moveStart = true;
            }

            if(!circle.sizeStart && !isEnter)
            {
                circle.sizeStart = true;
            }

            if(circle.moveStart && circle.sizeStart && !circle.halfCircleColliding && !circle.back && !isEnter)
            {
                circle.halfCircleColliding = true;
            }

            if(circle.isBlinking && circle.returnColor && !isEnter)
            {
                circle.isBlinking = false;
            }

            if (!cCircle.blueStart && !isEnter && circle.CircleFinish && !cCircle.fin1)
            {
                cCircle.blueStart = true;
            }


            isEnter = true;
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if(other.tag == "Tracker")
        {
            isEnter = false;
        }
    }
}
